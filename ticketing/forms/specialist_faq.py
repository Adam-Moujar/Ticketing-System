from django import forms
from ticketing.models.faq import FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['questions','subsection', 'answer']
        widgets = {
            'questions': forms.TextInput(attrs={'class': 'form-control'}),
            'subsection':forms.TextInput(attrs={'class':'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def custom_save(self, specialist, department, questions,subsection, answer):
        FAQ.objects.create(
            specialist=specialist,
            department=department,
            subsection=subsection,
            questions=questions,
            answer=answer,
        )
