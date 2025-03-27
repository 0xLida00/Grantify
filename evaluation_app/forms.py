from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter score'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter feedback', 'rows': 5}),
        }