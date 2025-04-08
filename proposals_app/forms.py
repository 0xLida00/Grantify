from django import forms
from .models import Proposal
from calls_app.models import GrantCall

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['grant_call', 'title', 'description', 'document']
        widgets = {
            'grant_call': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter proposal title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter proposal description', 'rows': 5}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grant_call'].queryset = GrantCall.objects.filter(status='open')