from django import forms
from demande.models.type_conges_model import TypeConge


class TypeCongesForm(forms.ModelForm):

    class Meta:

        model = TypeConge

        fields = [
            "libelle",
            "description",
        ]

        labels = {
            "libelle": "Libellé du type de congés",
            "description": "Description",
        }

        widgets = {
            "libelle": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Exemple : Congés annuel",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Décrivez le type de permission...",
                "rows": 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajout de classes Bootstrap supplémentaires
        self.fields["libelle"].widget.attrs.update({
            "autocomplete": "off",
        })

        self.fields["description"].widget.attrs.update({
            "style": "resize: vertical;",
        })