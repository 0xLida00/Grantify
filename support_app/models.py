from django.db import models
from accounts_app.models import CustomUser

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="support_tickets")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    response = models.TextField(blank=True, null=True)  # Admin's response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket: {self.subject} ({self.status})"

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="feedbacks")
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} (Rating: {self.rating})"

class FAQ(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    thumbs_up = models.PositiveIntegerField(default=0)
    thumbs_down = models.PositiveIntegerField(default=0)
    voted_up = models.ManyToManyField(CustomUser, related_name='voted_up_faqs', blank=True)
    voted_down = models.ManyToManyField(CustomUser, related_name='voted_down_faqs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question