from django.core.mail import EmailMessage
from utils.generer_pdf_conge import generer_pdf_conge
from utils.generer_pdf_permission import generer_pdf_permission
from utils.generer_pdf_repos_maladie import generer_pdf_repos_maladie
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





def notifier_rh(conge):

    rhs = Employe.objects.filter(
        utilisateur__role="rh"
    )

    if not rhs.exists():
        return

    destinataires = [
        rh.utilisateur.email
        for rh in rhs
        if rh.utilisateur.email
    ]

    email = EmailMessage(
        subject="Nouvelle demande de congé validée",

        body=f"""
Bonjour,

Une demande de congé vient d'être validée par le manager.

Employé :
{conge.employe.nom} {conge.employe.prenom}

Veuillez vous connecter afin de traiter cette demande.

Système de Gestion RH.
        """,

        to=destinataires
    )

    email.send(fail_silently=False)



def envoyer_mail_refus_manager(demande):

    employe = demande.employe

    type_demande = demande._meta.verbose_name.title()

    email = EmailMessage(

        subject=f"{type_demande} refusé",

        body=f"""
Bonjour {employe.prenom},

Votre demande de {type_demande.lower()} a été refusée par votre responsable.

Veuillez vous rapprocher de votre manager pour plus d'informations.

Cordialement,

Service RH
        """,

        to=[employe.utilisateur.email]

    )

    email.send(fail_silently=False)






def envoyer_mail_permission(permission):

    pdf = generer_pdf_permission(permission)

    email = EmailMessage(

        subject="Permission validée",

        body=f"""
Bonjour {permission.employe.prenom},

Votre demande de permission a été acceptée par votre manager.

Vous trouverez le document officiel en pièce jointe.

Cordialement,

Service RH
        """,

        to=[permission.employe.utilisateur.email]

    )

    email.attach(
        f"Permission_{permission.id}.pdf",
        pdf.getvalue(),
        "application/pdf"
    )

    email.send(fail_silently=False)





def envoyer_mail_repos_maladie(repos):

    pdf = generer_pdf_repos_maladie(repos)

    email = EmailMessage(

        subject="Repos maladie validé",

        body=f"""
Bonjour {repos.employe.prenom},

Votre demande de repos maladie a été acceptée.

Veuillez trouver le document officiel en pièce jointe.

Cordialement,

Service RH
        """,

        to=[repos.employe.utilisateur.email]

    )

    email.attach(
        f"Repos_Maladie_{repos.id}.pdf",
        pdf.getvalue(),
        "application/pdf"
    )

    email.send(fail_silently=False)