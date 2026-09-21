from django import forms
from demande.models.conges_model import Conges


class CongesForm(forms.ModelForm):

    class Meta:

        model = Conges

        fields = [
            "type_conge",
            "date_debut",
            "nombre_jours",
        ]

        labels = {
            "type_conge": "Type de congé",
            "date_debut": "Date de début",
            "nombre_jours": "Nombre de jours",
        }

        widgets = {

            # Type de congé
            "type_conge": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            # Date de début
            "date_debut": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            # Nombre de jours
            "nombre_jours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Exemple : 5",
                    "min": 1,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Texte affiché dans la liste déroulante
        self.fields["type_conge"].empty_label = (
            "Sélectionnez un type de congé"
        )

        # Attributs supplémentaires
        self.fields["date_debut"].widget.attrs.update({
            "autocomplete": "off",
        })

        self.fields["nombre_jours"].widget.attrs.update({
            "autocomplete": "off",
        })

    def clean_nombre_jours(self):

        nombre_jours = self.cleaned_data.get("nombre_jours")

        if nombre_jours is not None and nombre_jours <= 0:

            raise forms.ValidationError(
                "Le nombre de jours doit être supérieur à zéro."
            )

        return nombre_jours