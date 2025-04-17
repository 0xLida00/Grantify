from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from proposals_app.models import Proposal
from evaluation_app.models import Evaluation
from django.db import models
from django.core.paginator import Paginator


# Dashboard view for Admin and Staff
@staff_member_required
def dashboard(request):
    total_proposals = Proposal.objects.count()
    total_evaluations = Evaluation.objects.count()
    average_score = Evaluation.objects.aggregate(models.Avg('score'))['score__avg']
    accepted_proposals = Proposal.objects.filter(status='accepted').count()
    rejected_proposals = Proposal.objects.filter(status='rejected').count()
    under_review_proposals = Proposal.objects.filter(status='under_review').count()
    submitted_proposals = Proposal.objects.filter(status='submitted').count()

    recent_reports = Report.objects.all().order_by('-generated_at')[:5]

    context = {
        'total_proposals': total_proposals,
        'total_evaluations': total_evaluations,
        'average_score': average_score,
        'accepted_proposals': accepted_proposals,
        'rejected_proposals': rejected_proposals,
        'under_review_proposals': under_review_proposals,
        'submitted_proposals': submitted_proposals,
        'recent_reports': recent_reports,
    }
    return render(request, 'reports_app/dashboard.html', context)


# View to display a list of reports
@staff_member_required
def report_list(request):
    reports = Report.objects.all().order_by('-generated_at')
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reports_app/report_list.html', {'page_obj': page_obj})


# View to display a detailed report
@staff_member_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'reports_app/report_detail.html', {'report': report})


# View to generate a new report
@staff_member_required
def generate_report(request):
    if request.method == 'POST':
        total_proposals = Proposal.objects.count()
        proposals_by_status = Proposal.objects.values('status').annotate(count=models.Count('id'))
        average_score = Evaluation.objects.aggregate(models.Avg('score'))['score__avg']
        recent_proposals = Proposal.objects.filter(created_at__gte=now() - timedelta(days=7)).count()

        report_data = {
            'total_proposals': total_proposals,
            'proposals_by_status': list(proposals_by_status),
            'average_score': average_score,
            'recent_proposals': recent_proposals,
        }

        report = Report.objects.create(
            generated_by=request.user,
            report_data=report_data,
        )

        return JsonResponse({'message': 'Report generated successfully!', 'report_id': report.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)