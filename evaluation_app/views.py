from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from alerts_app.utils import create_in_app_notification
from django.utils.timezone import now
from audit_app.models import LogEntry
from alerts_app.models import Notification
from .models import Evaluation
from .forms import EvaluationForm
from proposals_app.models import Proposal
from accounts_app.models import CustomUser

# Admin: Assign proposals to evaluators
@staff_member_required
def assign_evaluators(request):
    proposals = Proposal.objects.all()
    evaluators = CustomUser.objects.filter(is_staff=False)  # Non-admin users
    if request.method == 'POST':
        proposal_id = request.POST.get('proposal')
        evaluator_id = request.POST.get('evaluator')
        proposal = get_object_or_404(Proposal, id=proposal_id)
        evaluator = get_object_or_404(CustomUser, id=evaluator_id)

        # Create the evaluation
        evaluation = Evaluation.objects.create(proposal=proposal, evaluator=evaluator)

        # Log the action
        LogEntry.objects.create(
            user=request.user,
            action="Evaluator Assigned",
            object_repr=str(proposal),
            change_message=f"Evaluator '{evaluator.username}' was assigned to proposal '{proposal.title}'.",
            log_level="INFO",
            source="Admin",
        )

        Notification.objects.create(
            user=evaluator,
            notification_type="in_app",
            message=f"You have been assigned to evaluate the proposal: '{proposal.title}'.",
            is_read=False,
        )

        return redirect('assign_evaluators')
    return render(request, 'evaluation_app/assign_evaluators.html', {'proposals': proposals, 'evaluators': evaluators})

# Admin: Monitor evaluation progress
@staff_member_required
def monitor_evaluations(request):
    evaluations = Evaluation.objects.all()

    # Log the action
    LogEntry.objects.create(
        user=request.user,
        action="Monitor Evaluations",
        object_repr="Evaluation Monitoring",
        change_message="Admin viewed the evaluation progress.",
        log_level="INFO",
        source="Admin",
    )

    return render(request, 'evaluation_app/monitor_evaluations.html', {'evaluations': evaluations})

# Evaluator: View assigned proposals
@login_required
def evaluator_dashboard(request):
    evaluations = Evaluation.objects.filter(evaluator=request.user)

    # Log the action
    LogEntry.objects.create(
        user=request.user,
        action="View Evaluator Dashboard",
        object_repr="Evaluator Dashboard",
        change_message="Evaluator viewed their assigned proposals.",
        log_level="INFO",
        source="User",
    )

    return render(request, 'evaluation_app/evaluator_dashboard.html', {'evaluations': evaluations})

# Evaluator: Submit evaluation
@login_required
def submit_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk, evaluator=request.user)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.status = 'completed'
            evaluation.evaluated_at = now()
            evaluation.save()

            # Notify the applicant about the evaluation
            message = f"Your proposal '{evaluation.proposal.title}' has been evaluated."
            create_in_app_notification(evaluation.proposal.applicant, message)

            # Log the action
            LogEntry.objects.create(
                user=request.user,
                action="Evaluation Submitted",
                object_repr=str(evaluation.proposal),
                change_message=f"Evaluator '{request.user.username}' submitted an evaluation for proposal '{evaluation.proposal.title}'.",
                log_level="INFO",
                source="User",
            )

            Notification.objects.create(
                user=request.user,
                notification_type="in_app",
                message=f"You have successfully submitted your evaluation for the proposal: '{evaluation.proposal.title}'.",
                is_read=False,
            )

            return redirect('evaluator_dashboard')
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'evaluation_app/submit_evaluation.html', {'form': form, 'evaluation': evaluation})