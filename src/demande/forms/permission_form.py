from django import forms
from demande.models.permission_model import Permission


class PermissionForm(forms.ModelForm):

    class Meta :
        model = Permission
        fields = [
            'motif',
            'heure_sortie',
            'nombre_minute',
        ]

        widgets = {

            'motif': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Motif'
                }
            ),

            'heure_sortie': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),

            'nombre_minute': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Durée'
                }
            ),

        }