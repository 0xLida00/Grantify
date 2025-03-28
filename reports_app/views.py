from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from proposals_app.models import Proposal
from evaluation_app.models import Evaluation
from django.db import models

# Dashboard view for Admin and Staff
@staff_member_required
def dashboard(request):
    # Aggregated metrics
    total_proposals = Proposal.objects.count()
    total_evaluations = Evaluation.objects.count()
    average_score = Evaluation.objects.aggregate(models.Avg('score'))['score__avg']
    accepted_proposals = Proposal.objects.filter(status='accepted').count()
    rejected_proposals = Proposal.objects.filter(status='rejected').count()

    context = {
        'total_proposals': total_proposals,
        'total_evaluations': total_evaluations,
        'average_score': average_score,
        'accepted_proposals': accepted_proposals,
        'rejected_proposals': rejected_proposals,
    }
    return render(request, 'reports_app/dashboard.html', context)

# View to display a list of reports
@staff_member_required
def report_list(request):
    reports = Report.objects.all().order_by('-generated_at')
    return render(request, 'reports_app/report_list.html', {'reports': reports})

# View to display a detailed report
@staff_member_required
def report_detail(request, pk):
    report = Report.objects.get(pk=pk)
    return render(request, 'reports_app/report_detail.html', {'report': report})