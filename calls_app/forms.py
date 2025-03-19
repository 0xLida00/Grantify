from django import forms
from django.forms import inlineformset_factory
from .models import GrantCall, GrantQuestion, GrantChoice


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
        fields = ["question_text", "question_type"]
        widgets = {
            "question_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter question text"}),
            "question_type": forms.Select(attrs={"class": "form-control"}),
        }


class GrantChoiceForm(forms.ModelForm):
    class Meta:
        model = GrantChoice
        fields = ["choice_text"]
        widgets = {
            "choice_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter choice text"}),
        }


# Formset for adding multiple questions
GrantQuestionFormSet = inlineformset_factory(
    GrantCall,
    GrantQuestion,
    form=GrantQuestionForm,
    extra=1,  # Start with one empty form
    can_delete=True,  # Allow deleting questions
)