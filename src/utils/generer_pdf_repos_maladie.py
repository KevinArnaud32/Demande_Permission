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


def generer_pdf_repos_maladie(repos):

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
            "<b>AUTORISATION DE REPOS MALADIE</b>",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 20))

    # ==================== EMPLOYE ====================

    data = [

        ["Nom", repos.employe.nom],

        ["Prénom", repos.employe.prenom],

        ["Email", repos.employe.utilisateur.email],

        ["Département", repos.employe.departement.nom_departement],

        ["Fonction", repos.employe.fonction.nom_fonction],

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

    ]))

    elements.append(Paragraph("<b>Informations du demandeur</b>", styles["Heading2"]))
    elements.append(table)

    elements.append(Spacer(1, 20))

    # ==================== REPOS ====================

    data = [

        ["Date de demande", str(repos.date_creation.date())],

        ["Date début", str(repos.date_debut)],

        ["Nombre de jours", str(repos.nombre_jours)],

        ["Date fin", str(repos.date_fin)],

        ["Statut", repos.statut],

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgreen),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

    ]))

    elements.append(Paragraph("<b>Détails du repos maladie</b>", styles["Heading2"]))
    elements.append(table)

    elements.append(Spacer(1, 30))

    if hasattr(repos, "justificatif") and repos.justificatif:
        elements.append(
            Paragraph(
                "<b>Justificatif médical fourni.</b>",
                styles["Normal"],
            )
        )

    elements.append(
        Paragraph(
            "Ce repos maladie a été validé par le responsable hiérarchique.",
            styles["Italic"],
        )
    )

    pdf.build(elements)

    buffer.seek(0)

    return buffer