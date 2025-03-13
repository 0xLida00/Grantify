# evaluation_app/models.py
from django.db import models
from accounts_app.models import CustomUser
from proposals_app.models import Proposal

class Evaluation(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="evaluations")
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluations")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation for {self.proposal.title} by {self.evaluator.username}"