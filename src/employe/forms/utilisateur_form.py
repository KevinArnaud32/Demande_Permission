from django import forms

from employe.models.utilisateur_model import Utilisateur


class UtilisateurForm(forms.ModelForm):

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le mot de passe'
            }
        )
    )

    class Meta:
        model = Utilisateur

        fields = [
            'username',
            'password',
            'email',
            'role',
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Nom d'utilisateur"
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Adresse email'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

        labels = {
            'username': "Nom d'utilisateur",
            'email': 'Adresse email',
            'role': 'Rôle',
        }