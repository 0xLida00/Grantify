from django import forms
from .models import SupportTicket, Feedback, FAQ

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'description', 'priority']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the subject of your issue',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your issue in detail',
                'rows': 4,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your feedback here',
                'rows': 4,
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
            }),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'status']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the answer'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }