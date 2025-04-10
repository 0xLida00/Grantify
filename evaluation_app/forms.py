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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].required = True
        self.fields['feedback'].required = True

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is None:
            raise forms.ValidationError("Score is required.")
        if score < 0 or score > 10:
            raise forms.ValidationError("Score must be between 0 and 10.")
        return score