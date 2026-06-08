from django import forms
from employe.models.departement_model import Departement


class DepartementForm(forms.ModelForm):

    class Meta:
        model = Departement
        fields = [
            'nom_departement'
        ]

        labels = {
            'nom_departement': 'Nom du département'
        }

        widgets = {
            'nom_departement': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex : Ressources Humaines'
                }
            )
        }