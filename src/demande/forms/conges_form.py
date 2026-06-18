from django import forms
from demande.models.conges_model import Conges


class CongesForm(forms.ModelForm):

    class Meta:

        model = Conges

        fields = [
            "date_debut",
            "nombre_jours",
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
                    "placeholder": "Ex : 20",
                    "min": "1",
                }
            ),
        }