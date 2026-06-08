from django import forms
from employe.models.employe_model import Employe


class EmployeForm(forms.ModelForm):

    class Meta:

        model = Employe

        fields = [
            'nom',
            'prenom',
            'departement',
        ]

        widgets = {

            'nom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nom de l\'employé'
                }
            ),

            'prenom': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Prénom de l\'employé'
                }
            ),

            'departement': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Département'
                }
            ),
        }

        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'departement': 'Département',
        }