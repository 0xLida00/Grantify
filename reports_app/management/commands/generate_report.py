from django.core.management.base import BaseCommand
from reports_app.models import Report
from proposals_app.models import Proposal
from evaluation_app.models import Evaluation
from django.db.models import Avg

class Command(BaseCommand):
    help = 'Generate a report'

    def handle(self, *args, **kwargs):
        total_proposals = Proposal.objects.count()
        total_evaluations = Evaluation.objects.count()
        average_score = Evaluation.objects.aggregate(Avg('score'))['score__avg']
        accepted_proposals = Proposal.objects.filter(status='accepted').count()
        rejected_proposals = Proposal.objects.filter(status='rejected').count()

        report_data = {
            'total_proposals': total_proposals,
            'total_evaluations': total_evaluations,
            'average_score': average_score,
            'accepted_proposals': accepted_proposals,
            'rejected_proposals': rejected_proposals,
        }

        Report.objects.create(report_data=report_data)
        self.stdout.write(self.style.SUCCESS('Report generated successfully'))