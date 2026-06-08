from django import forms
from employe.models.fonction_model import Fonction


class FonctionForm(forms.ModelForm):

    class Meta:

        model = Fonction
        fields = [
            'nom_fonction'
        ]

        labels = {
            'nom_fonction': 'Fonction de l\'employe'
        }

        widgets = {
            'nom_fonction': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex : Assistant RH'
                }
            )
        }