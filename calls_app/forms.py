from django import forms
from django.forms import inlineformset_factory
from .models import GrantCall, GrantQuestion, GrantResponse

class GrantCallForm(forms.ModelForm):
    class Meta:
        model = GrantCall
        fields = ["title", "description", "deadline", "eligibility", "budget", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter grant title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter grant description"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "eligibility": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter eligibility criteria, one per line"}),
            "budget": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter budget"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class GrantQuestionForm(forms.ModelForm):
    class Meta:
        model = GrantQuestion
        fields = ["id", "question_text", "question_type"]
        widgets = {
            "question_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter question text"}),
            "question_type": forms.Select(attrs={"class": "form-control"}),
        }


GrantQuestionFormSet = inlineformset_factory(
    GrantCall,
    GrantQuestion,
    form=GrantQuestionForm,
    extra=1,
    can_delete=True,
)


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        for question in questions:
            if question.question_type == 'open':
                self.fields[f'question_{question.id}_response'] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    required=False,
                )
            elif question.question_type == 'file_upload':
                self.fields[f'question_{question.id}_file'] = forms.FileField(
                    label=question.question_text,
                    required=False,
                )