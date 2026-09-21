from django import forms
from demande.models.permission_model import Permission


class PermissionForm(forms.ModelForm):

    class Meta:

        model = Permission

        fields = [
            "type_permission",
            "motif",
            "date_permission",
            "date_retour",
        ]

        labels = {
            "type_permission": "Type de permission",
            "motif": "Motif",
            "date_permission": "Date de la permission",
            "date_retour": "Date de retour",
        }

        widgets = {

            # Type de permission
            "type_permission": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            # Motif
            "motif": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Indiquez le motif de votre permission...",
                    "rows": 5,
                }
            ),

            # Date de permission
            "date_permission": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            # Date de retour
            "date_retour": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["type_permission"].empty_label = (
            "Sélectionnez un type de permission"
        )

        self.fields["date_permission"].widget.attrs.update({
            "autocomplete": "off",
        })

        self.fields["date_retour"].widget.attrs.update({
            "autocomplete": "off",
        })

    def clean(self):

        cleaned_data = super().clean()

        date_permission = cleaned_data.get("date_permission")
        date_retour = cleaned_data.get("date_retour")

        if date_permission and date_retour:

            if date_retour < date_permission:

                raise forms.ValidationError(
                    "La date de retour ne peut pas être antérieure "
                    "à la date de la permission."
                )

        return cleaned_data
