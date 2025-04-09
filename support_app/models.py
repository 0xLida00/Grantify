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
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket: {self.subject} ({self.status})"
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="feedbacks")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

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
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

class ToDo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"To-Do: {self.title} ({'Completed' if self.completed else 'Pending'})"

    class Meta:
        ordering = ['-created_at']