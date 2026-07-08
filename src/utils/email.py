from django.core.mail import EmailMessage
from utils.generer_pdf_conge import generer_pdf_conge
from employe.models.employe_model import Employe


def notifier_manager(demande):

    employe = demande.employe

    manager = Employe.objects.filter(
        departement=employe.departement,
        utilisateur__role="manager"
    ).first()

    if manager is None:
        return

    type_demande = demande._meta.verbose_name.title()

    sujet = f"Nouvelle demande de {type_demande}"

    message = f"""
Bonjour {manager.prenom},

Une nouvelle demande nécessite votre validation.

Employé :
{employe.nom} {employe.prenom}

Type de demande :
{type_demande}

Merci de vous connecter à la plateforme pour consulation.

Cordialement,

Système de Gestion RH
"""

    email = EmailMessage(
        subject=sujet,
        body=message,
        to=[manager.utilisateur.email]
    )

    email.send()



def envoyer_mail_conge(conge):

    pdf = generer_pdf_conge(conge)

    email = EmailMessage(
        subject="Validation de votre demande de congé",
        body=f"""
Bonjour {conge.employe.prenom},

Votre demande de congé a été traitée par le service des Ressources Humaines.

Vous trouverez en pièce jointe le document officiel de validation.

Cordialement,

Service RH
        """,
        to=[conge.employe.utilisateur.email],
    )

    email.attach(
        f"Conge_{conge.employe.nom}.pdf",
        pdf.getvalue(),
        "application/pdf",
    )

    email.send(fail_silently=False)