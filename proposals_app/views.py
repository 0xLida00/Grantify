from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Proposal
from .forms import ProposalForm
from calls_app.models import GrantCall


@staff_member_required
def admin_proposal_list(request):
    grant_call_id = request.GET.get('grant_call')
    status = request.GET.get('status')

    proposals = Proposal.objects.all()

    if grant_call_id:
        proposals = proposals.filter(grant_call_id=grant_call_id)

    if status:
        proposals = proposals.filter(status=status)

    grant_calls = GrantCall.objects.all()
    return render(request, 'proposals_app/admin_proposal_list.html', {
        'proposals': proposals,
        'grant_calls': grant_calls,
        'selected_grant_call': grant_call_id,
        'selected_status': status,
    })

@login_required
def proposal_list(request):
    proposals = Proposal.objects.filter(applicant=request.user)
    return render(request, 'proposals_app/proposal_list.html', {'proposals': proposals})

@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)
    return render(request, 'proposals_app/proposal_detail.html', {'proposal': proposal})

@login_required
def proposal_create(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.applicant = request.user
            proposal.save()
            return redirect('proposal_list')
    else:
        form = ProposalForm()
    return render(request, 'proposals_app/proposal_form.html', {'form': form})

@login_required
def proposal_update(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('proposal_list')
    else:
        form = ProposalForm(instance=proposal)
    return render(request, 'proposals_app/proposal_form.html', {'form': form})

@login_required
def proposal_delete(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, applicant=request.user)
    if request.method == 'POST':
        proposal.delete()
        return redirect('proposal_list')
    return render(request, 'proposals_app/proposal_confirm_delete.html', {'proposal': proposal})