from django import forms
from ticketing.models.faq import FAQ
from ticketing.models.departments import Subsection

#TODO create a choice fields.
class FAQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department')
        super(FAQForm, self).__init__(*args, **kwargs)
        subsections = Subsection.objects.filter(department = self.department)
        self.fields['subsection'] = forms.ChoiceField(choices = subsections, 
                                                    label = "Select the Subsection ",)  
    
    class Meta:
        model = FAQ
        fields = ['questions','subsection', 'answer']
        widgets = {
            'questions': forms.TextInput(),
            'answer': forms.Textarea(),
        }


    def custom_save(self, specialist, department, questions,subsection, answer):
        FAQ.objects.create(
            specialist=specialist,
            department=department,
            subsection=subsection,
            questions=questions,
            answer=answer,
        )
