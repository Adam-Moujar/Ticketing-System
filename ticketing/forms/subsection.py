from django import forms
from ticketing.models.departments import Subsection
 
class SubsectionForm(forms.ModelForm): 
    class Meta:
        model = Subsection
        fields = ['name']
        widgets = {
            'subsection':forms.TextInput(attrs={'class':'form-control'})
        }
    def custom_save(self, department, subsection_name): 
        Subsection.objects.create(
            department = department, 
            name = subsection_name
        )
