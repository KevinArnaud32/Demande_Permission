from django import forms
from demande.models.type_permission_model import TypePermission


class TypePermissionForm(forms.ModelForm):

    class Meta:

        model = TypePermission

        fields = [
            "libelle",
            "description",
        ]

        labels = {
            "libelle": "Libellé du type de permission",
            "description": "Description",
        }

        widgets = {
            "libelle": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Exemple : Permission de sortie",
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