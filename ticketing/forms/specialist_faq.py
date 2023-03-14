from django import forms
from ticketing.models.faq import FAQ
from ticketing.models.departments import Subsection

# TODO create a choice fields.
class FAQForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        department = kwargs.pop('department', None)
        super(FAQForm, self).__init__(*args, **kwargs)
        if department:
            self.department = department
            subsections = Subsection.objects.filter(department=self.department)
            self.fields['subsection'] = forms.ChoiceField(
                choices=[(s.id, s.name) for s in subsections],
                label='Select the Subsection',
            )
        print(data)

    def custom_save(
        self, specialist, department, questions, subsection, answer
    ):
        FAQ.objects.create(
            specialist=specialist,
            department=department,
            subsection=subsection,
            questions=questions,
            answer=answer,
        )

    def clean(self):
        cleaned_data = super().clean()
        subsection_id = cleaned_data.get('subsection')
        if subsection_id:
            try:
                subsection_obj = Subsection.objects.get(id=int(subsection_id))
                cleaned_data['subsection'] = subsection_obj
            except Subsection.DoesNotExist:
                self.add_error('subsection', 'Invalid subsection selected')
        return cleaned_data

    class Meta:
        model = FAQ
        fields = ['questions', 'subsection', 'answer']
        widgets = {
            'questions': forms.TextInput(),
            'answer': forms.Textarea(),
        }
