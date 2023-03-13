from django import forms
from ticketing.models.departments import Subsection
 
class SubsectionForm(forms.ModelForm): #
    class Meta:
        model = Subsection
        fields = ['name']
        widgets = {
            'subsection':forms.TextInput(attrs={'class':'form-control'})
        }
    def custom_save(self, department, subsection): 
        Subsection.objects.create(
            department = department, 
            subsection = subsection
        )
