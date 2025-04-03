from django.db import models
from accounts_app.models import CustomUser

class GrantCall(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    eligibility = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grant_calls")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_grant_calls")
    modified_at = models.DateTimeField(auto_now=True)

    favorited_by = models.ManyToManyField(CustomUser, related_name="favorite_grants", blank=True)

    def __str__(self):
        return self.title


class GrantQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('open', 'Open-Ended'),
        ('multiple_choice', 'Multiple Choice'),
    )
    grant_call = models.ForeignKey(GrantCall, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='open')

    def __str__(self):
        return self.question_text


class GrantChoice(models.Model):
    question = models.ForeignKey(GrantQuestion, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text
    

from django.db import models
from accounts_app.models import CustomUser

class GrantResponse(models.Model):
    question = models.ForeignKey(GrantQuestion, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    grant_call = models.ForeignKey(GrantCall, on_delete=models.CASCADE, related_name="responses")
    response = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="grant_responses/", blank=True, null=True)
    is_final_submission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response by {self.user.username} to {self.question.question_text}"