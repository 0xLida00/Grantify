from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Proposal
from .forms import ProposalForm
from calls_app.forms import ApplicationForm
from calls_app.models import GrantCall, GrantResponse
from audit_app.models import LogEntry
from alerts_app.models import Notification
from evaluation_app.models import Evaluation
from accounts_app.models import CustomUser
from django.core.paginator import Paginator

# Admin: List all proposals for a specific grant call
@staff_member_required
def admin_proposal_list(request):
    grant_call_id = request.GET.get('grant_call')
    status = request.GET.get('status')

    # Fetch all proposals by default
    proposals = Proposal.objects.all().order_by('-submitted_at')

    # Filter by grant call if provided
    if grant_call_id:
        proposals = proposals.filter(grant_call_id=grant_call_id)

    # Filter by status if provided
    if status:
        proposals = proposals.filter(status=status)

    grant_calls = GrantCall.objects.all()
    evaluators = CustomUser.objects.filter(role='evaluator')

    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        proposal_id = request.POST.get("proposal_id")
        evaluator_id = request.POST.get("evaluator_id")
        if proposal_id and evaluator_id:
            proposal = get_object_or_404(Proposal, id=proposal_id)
            evaluator = get_object_or_404(CustomUser, id=evaluator_id)

            # Assign or reassign the evaluator to the proposal
            proposal.evaluator = evaluator
            proposal.status = "under_review"  # Update status to "under_review"
            proposal.save()

            # Create or update the Evaluation object
            evaluation, created = Evaluation.objects.get_or_create(
                proposal=proposal,
                defaults={'evaluator': evaluator, 'status': 'pending'}
            )
            if not created:
                # If the evaluation already exists, update the evaluator and status
                evaluation.evaluator = evaluator
                evaluation.status = 'pending'
                evaluation.save()

            # Log the action
            LogEntry.objects.create(
                user=request.user,
                action="Evaluator Assigned/Reassigned",
                object_repr=str(proposal),
                change_message=f"Evaluator '{evaluator.username}' was assigned/reassigned to proposal '{proposal.title}'.",
                log_level="INFO",
                source="Admin",
            )

            # Notify the evaluator
            Notification.objects.create(
                user=evaluator,
                notification_type="in_app",
                message=f"You have been assigned to evaluate the proposal: '{proposal.title}'.",
                is_read=False,
            )

            messages.success(request, f"Evaluator '{evaluator.username}' assigned/reassigned to proposal '{proposal.title}'.")
            return redirect("proposals_app:admin_proposal_list")

    return render(request, 'proposals_app/admin_proposal_list.html', {
        'page_obj': page_obj,
        'grant_calls': grant_calls,
        'selected_grant_call': grant_call_id,
        'selected_status': status,
        'evaluators': evaluators,
    })


# Admin: View proposal details
@staff_member_required
def admin_proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    responses = GrantResponse.objects.filter(grant_call=proposal.grant_call, user=proposal.applicant)
    return render(request, 'proposals_app/admin_proposal_detail.html', {
        'proposal': proposal,
        'responses': responses,
    })


# Applicant: List saved and submitted proposals
@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(applicant=request.user).order_by('-submitted_at')
    
    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'proposals_app/proposal_list.html', {'page_obj': page_obj})


# Applicant: Update a proposal
@login_required
def proposal_update(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)

    if proposal.status != "draft":
        messages.error(request, "You can only edit proposals that are in draft status.")
        return redirect("proposals_app:proposal_list")

    grant_call = proposal.grant_call
    questions = grant_call.questions.all()

    initial_data = {}
    for question in questions:
        try:
            response = GrantResponse.objects.get(
                question=question, user=request.user, grant_call=grant_call
            )
            initial_data[f'question_{question.id}_response'] = response.response
            initial_data[f'question_{question.id}_file'] = response.file
        except GrantResponse.DoesNotExist:
            pass

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, questions=questions, initial=initial_data)
        if form.is_valid():
            for question in questions:
                response_text = form.cleaned_data.get(f'question_{question.id}_response')
                response_file = form.cleaned_data.get(f'question_{question.id}_file')
                response, created = GrantResponse.objects.get_or_create(
                    question=question,
                    user=request.user,
                    grant_call=grant_call,
                )
                response.response = response_text
                if response_file:
                    response.file = response_file
                response.save()

            messages.success(request, "Your proposal has been updated successfully!")
            return redirect("proposals_app:proposal_list")
        else:
            messages.error(request, "There was an error updating your proposal. Please check the form.")
    else:
        form = ApplicationForm(questions=questions, initial=initial_data)

    return render(request, "proposals_app/proposal_form.html", {
        "form": form,
        "proposal": proposal,
        "grant_call": grant_call,
    })


# Applicant: Delete a proposal
@login_required
def proposal_delete(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)

    if proposal.status != "draft":
        messages.error(request, "You can only delete proposals that are in draft status.")
        return redirect("proposals_app:proposal_list")

    if request.method == "POST":
        proposal.delete()
        messages.success(request, "Your proposal has been deleted successfully!")
        return redirect("proposals_app:proposal_list")

    return render(request, "proposals_app/proposal_confirm_delete.html", {
        "proposal": proposal,
    })


# Applicant: View proposal details
@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    if proposal.applicant != request.user:
        return HttpResponseForbidden("You are not allowed to view this proposal.")

    grant_call = proposal.grant_call
    questions = grant_call.questions.all()

    initial_data = {}
    for question in questions:
        try:
            response = GrantResponse.objects.get(
                question=question, user=request.user, grant_call=grant_call
            )
            initial_data[f'question_{question.id}_response'] = response.response
            initial_data[f'question_{question.id}_file'] = response.file
        except GrantResponse.DoesNotExist:
            pass

    form = ApplicationForm(questions=questions, initial=initial_data)

    return render(request, 'proposals_app/proposal_detail.html', {
        'proposal': proposal,
        'grant_call': grant_call,
        'form': form,
    })