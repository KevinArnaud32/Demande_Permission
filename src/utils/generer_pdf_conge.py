from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO


def generer_pdf_conge(conge):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # ================= HEADER =================
    title = Paragraph(
        "<b>CONGÉ OFFICIEL - VALIDATION RH</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # ================= EMPLOYÉ =================
    employe_data = [
        ["Nom", conge.employe.nom],
        ["Prénom", conge.employe.prenom],
        ["Email", conge.employe.utilisateur.email],
        ["Fonction", conge.employe.fonction],
        ["Département", conge.employe.departement.nom_departement],
    ]

    table1 = Table(employe_data)
    table1.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),

    ]))

    elements.append(Paragraph("<b>Informations Employé</b>", styles["Heading2"]))
    elements.append(table1)
    elements.append(Spacer(1, 20))

    # ================= CONGÉ =================
    conge_data = [
        ["Date demande", str(conge.date_creation)],
        ["Date début", str(conge.date_debut)],
        ["Nombre de jours", str(conge.nombre_jours)],
        ["Date fin", str(conge.date_fin)],
        ["Statut", conge.statut],
    ]

    table2 = Table(conge_data)
    table2.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),

    ]))

    elements.append(Paragraph("<b>Détails du Congé</b>", styles["Heading2"]))
    elements.append(table2)
    elements.append(Spacer(1, 20))

    # ================= VALIDATION =================
    validation_data = [
        ["Statut final", "CONFIRMÉ PAR RH"],
        ["Service", "Ressources Humaines"],
    ]

    table3 = Table(validation_data)
    table3.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgreen),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),

    ]))

    elements.append(Paragraph("<b>Validation</b>", styles["Heading2"]))
    elements.append(table3)

    # ================= FOOTER =================
    elements.append(Spacer(1, 30))
    elements.append(
        Paragraph(
            "Document généré automatiquement par le système RH",
            styles["Italic"]
        )
    )

    pdf.build(elements)

    buffer.seek(0)
    return buffer