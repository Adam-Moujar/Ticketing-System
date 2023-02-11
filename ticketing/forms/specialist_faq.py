from django import forms
from ticketing.models.faq import FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['specialist', 'department', 'questions', 'answer']
        widgets = {
            'specialist': forms.HiddenInput(),
            'department': forms.HiddenInput(),
            'questions': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class:form-control'}),
        }
