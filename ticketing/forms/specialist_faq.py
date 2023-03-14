from django import forms
from ticketing.models.faq import FAQ
from ticketing.models.departments import Subsection

#TODO create a choice fields.
class FAQForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department')
        super(FAQForm, self).__init__(*args, **kwargs)
        subsections = Subsection.objects.filter(department = self.department)
        self.fields['subsection'] = forms.ChoiceField(
            choices=[(s.id, s.name) for s in subsections],
            label="Select the Subsection"
        )
    def custom_save(self, specialist, department, questions,subsection, answer):
        subsection_obj = Subsection.objects.get(id=int(subsection))
        FAQ.objects.create(
            specialist=specialist,
            department=department,
            subsection=subsection_obj,
            questions=questions,
            answer=answer,
        )

    class Meta:
        model = FAQ
        fields = ['questions','subsection', 'answer']
        widgets = {
            'questions': forms.TextInput(),
            'answer': forms.Textarea(),
        }
        
    
