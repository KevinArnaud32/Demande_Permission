from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generer_pdf_permission(permission):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==================== TITRE ====================

    elements.append(
        Paragraph(
            "<b>AUTORISATION DE PERMISSION</b>",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 20))

    # ==================== EMPLOYE ====================

    data = [

        ["Nom", permission.employe.nom],

        ["Prénom", permission.employe.prenom],

        ["Email", permission.employe.utilisateur.email],

        ["Département", permission.employe.departement.nom_departement],

        ["Fonction", permission.employe.fonction.nom_fonction],

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

    ]))

    elements.append(Paragraph("<b>Informations du demandeur</b>", styles["Heading2"]))
    elements.append(table)

    elements.append(Spacer(1, 20))

    # ==================== PERMISSION ====================

    data = [

        ["Date de demande", str(permission.date_creation.date())],

        ["Heure de sortie", str(permission.heure_sortie)],

        ["Heure de retour", str(permission.heure_retour)],

        ["Durée", f"{permission.nombre_minute} minute(s)"],

        ["Motif", permission.motif],

        ["Statut", permission.statut],

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

    ]))

    elements.append(Paragraph("<b>Détails de la permission</b>", styles["Heading2"]))
    elements.append(table)

    elements.append(Spacer(1, 30))

    elements.append(
        Paragraph(
            "Cette permission a été validée par le responsable hiérarchique.",
            styles["Italic"],
        )
    )

    pdf.build(elements)

    buffer.seek(0)

    return buffer