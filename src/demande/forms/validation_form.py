from django import forms
from demande.models.validation_model import Validation


class ValidationForm(forms.ModelForm):

    class Meta:

        model = Validation

        fields = [

            'decision',
            'commentaire',

        ]

        widgets = {

            'decision': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'commentaire': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Commentaire'
                }
            )

        }