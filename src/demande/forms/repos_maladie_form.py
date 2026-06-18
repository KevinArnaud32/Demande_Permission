from django import forms
from demande.models.repos_maladie_model import ReposMaladie


class ReposMaladieForm(forms.ModelForm):

    class Meta:
        model = ReposMaladie

        fields = [
            "date_debut",
            "nombre_jours",
            "justificatif",
        ]

        widgets = {

            "date_debut": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "nombre_jours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Nombre de jours",
                }
            ),
            "justificatif": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf",
                }
            ),
        }