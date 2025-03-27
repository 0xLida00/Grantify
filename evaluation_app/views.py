from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from alerts_app.utils import create_in_app_notification
from django.utils.timezone import now
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
        Evaluation.objects.create(proposal=proposal, evaluator=evaluator)
        return redirect('assign_evaluators')
    return render(request, 'evaluation_app/assign_evaluators.html', {'proposals': proposals, 'evaluators': evaluators})

# Admin: Monitor evaluation progress
@staff_member_required
def monitor_evaluations(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'evaluation_app/monitor_evaluations.html', {'evaluations': evaluations})

# Evaluator: View assigned proposals
@login_required
def evaluator_dashboard(request):
    evaluations = Evaluation.objects.filter(evaluator=request.user)
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

            return redirect('evaluator_dashboard')
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'evaluation_app/submit_evaluation.html', {'form': form, 'evaluation': evaluation})