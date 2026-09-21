from io import BytesIO
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def generer_pdf_permission(permission):

    buffer = BytesIO()

    # ==========================================================
    # CONFIGURATION DU DOCUMENT
    # ==========================================================

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="Validation de permission",
        author="Service des Ressources Humaines",
    )

    # ==========================================================
    # COULEURS
    # ==========================================================

    BLEU = colors.HexColor("#174A7E")
    BLEU_CLAIR = colors.HexColor("#EAF2F8")

    VERT = colors.HexColor("#198754")
    VERT_CLAIR = colors.HexColor("#D1E7DD")

    ROUGE = colors.HexColor("#DC3545")
    ROUGE_CLAIR = colors.HexColor("#F8D7DA")

    ORANGE = colors.HexColor("#FD7E14")
    ORANGE_CLAIR = colors.HexColor("#FFE5D0")

    GRIS = colors.HexColor("#6C757D")
    GRIS_CLAIR = colors.HexColor("#DEE2E6")
    GRIS_FOND = colors.HexColor("#F8F9FA")

    NOIR = colors.HexColor("#212529")

    # ==========================================================
    # STYLES
    # ==========================================================

    styles = getSampleStyleSheet()

    style_entreprise = ParagraphStyle(
        "EntreprisePermission",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=BLEU,
    )

    style_coordonnees = ParagraphStyle(
        "CoordonneesPermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=GRIS,
    )

    style_titre = ParagraphStyle(
        "TitrePermission",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=BLEU,
        spaceAfter=4,
    )

    style_sous_titre = ParagraphStyle(
        "SousTitrePermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    style_section = ParagraphStyle(
        "SectionPermission",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=BLEU,
        spaceBefore=4,
        spaceAfter=7,
    )

    style_label = ParagraphStyle(
        "LabelPermission",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
    )

    style_valeur = ParagraphStyle(
        "ValeurPermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
    )

    style_decision = ParagraphStyle(
        "DecisionPermission",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
    )

    style_footer = ParagraphStyle(
        "FooterPermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    # ==========================================================
    # CONTENU
    # ==========================================================

    elements = []

    # ==========================================================
    # EN-TÊTE ENTREPRISE
    # ==========================================================

    # Emplacement prévu pour le logo
    logo = Table(
        [
            [
                Paragraph(
                    "<b>LOGO</b>",
                    ParagraphStyle(
                        "LogoPermission",
                        parent=styles["Normal"],
                        fontName="Helvetica-Bold",
                        fontSize=10,
                        alignment=TA_CENTER,
                        textColor=BLEU,
                    ),
                )
            ]
        ],
        colWidths=[30 * mm],
        rowHeights=[20 * mm],
    )

    logo.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, BLEU),
                ("BACKGROUND", (0, 0), (-1, -1), BLEU_CLAIR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    entreprise = [
        Paragraph(
            "NOM DE L'ENTREPRISE",
            style_entreprise
        ),
        Paragraph(
            "Direction des Ressources Humaines",
            style_coordonnees
        ),
        Paragraph(
            "Adresse de l'entreprise<br/>"
            "Téléphone : +225 XX XX XX XX XX<br/>"
            "Email : contact@entreprise.com",
            style_coordonnees
        ),
    ]

    header = Table(
        [
            [
                logo,
                entreprise,
            ]
        ],
        colWidths=[38 * mm, 135 * mm],
    )

    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    elements.append(header)

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=BLEU,
            spaceBefore=6,
            spaceAfter=16,
        )
    )

    # ==========================================================
    # TITRE
    # ==========================================================

    elements.append(
        Paragraph(
            "VALIDATION DE PERMISSION",
            style_titre
        )
    )

    elements.append(
        Paragraph(
            "DÉCISION DU SERVICE DES RESSOURCES HUMAINES",
            style_sous_titre
        )
    )

    elements.append(Spacer(1, 12))

    # ==========================================================
    # RÉFÉRENCE DU DOCUMENT
    # ==========================================================

    reference = f"VAL-PERM-{permission.pk:05d}"

    date_validation = (
        permission.date_modification.strftime("%d/%m/%Y")
        if permission.date_modification
        else timezone.now().strftime("%d/%m/%Y")
    )

    reference_data = [
        [
            Paragraph("<b>Référence</b>", style_label),
            Paragraph(reference, style_valeur),
            Paragraph("<b>Date de validation</b>", style_label),
            Paragraph(date_validation, style_valeur),
        ]
    ]

    reference_table = Table(
        reference_data,
        colWidths=[32 * mm, 50 * mm, 38 * mm, 53 * mm],
    )

    reference_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GRIS_FOND),
                ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.append(reference_table)
    elements.append(Spacer(1, 17))

    # ==========================================================
    # IDENTIFICATION DE L'EMPLOYÉ
    # ==========================================================

    elements.append(
        Paragraph(
            "1. IDENTIFICATION DE L'EMPLOYÉ",
            style_section
        )
    )

    employe = permission.employe

    nom = employe.nom or "-"
    prenom = employe.prenom or "-"

    email = (
        employe.utilisateur.email
        if employe.utilisateur
        else "-"
    )

    fonction = (
        str(employe.fonction)
        if employe.fonction
        else "-"
    )

    departement = (
        employe.departement.nom_departement
        if employe.departement
        else "-"
    )

    employe_data = [
        [
            Paragraph("<b>Nom</b>", style_label),
            Paragraph(nom, style_valeur),
            Paragraph("<b>Prénom</b>", style_label),
            Paragraph(prenom, style_valeur),
        ],
        [
            Paragraph("<b>Email</b>", style_label),
            Paragraph(email, style_valeur),
            Paragraph("<b>Fonction</b>", style_label),
            Paragraph(fonction, style_valeur),
        ],
        [
            Paragraph("<b>Département</b>", style_label),
            Paragraph(departement, style_valeur),
        ],
    ]

    employe_table = Table(
        employe_data,
        colWidths=[30 * mm, 55 * mm, 30 * mm, 58 * mm],
    )

    employe_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BLEU_CLAIR),
                ("BACKGROUND", (2, 0), (2, -1), BLEU_CLAIR),
                ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.append(employe_table)
    elements.append(Spacer(1, 17))

    # ==========================================================
    # INFORMATIONS SUR LA PERMISSION
    # ==========================================================

    elements.append(
        Paragraph(
            "2. INFORMATIONS RELATIVES À LA PERMISSION",
            style_section
        )
    )

    type_permission = (
        str(permission.type_permission)
        if permission.type_permission
        else "-"
    )

    date_permission = (
        permission.date_permission.strftime("%d/%m/%Y")
        if permission.date_permission
        else "-"
    )

    date_retour = (
        permission.date_retour.strftime("%d/%m/%Y")
        if permission.date_retour
        else "-"
    )

    motif = (
        permission.motif
        if permission.motif
        else "Aucun motif renseigné."
    )

    permission_data = [
        [
            Paragraph("<b>Type de permission</b>", style_label),
            Paragraph(type_permission, style_valeur),
        ],
        [
            Paragraph("<b>Date de permission</b>", style_label),
            Paragraph(date_permission, style_valeur),
        ],
        [
            Paragraph("<b>Date de retour</b>", style_label),
            Paragraph(date_retour, style_valeur),
        ],
        [
            Paragraph("<b>Motif</b>", style_label),
            Paragraph(motif, style_valeur),
        ],
    ]

    permission_table = Table(
        permission_data,
        colWidths=[55 * mm, 118 * mm],
    )

    permission_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BLEU_CLAIR),
                ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(permission_table)
    elements.append(Spacer(1, 18))

    # ==========================================================
    # DÉCISION
    # ==========================================================

    elements.append(
        Paragraph(
            "3. DÉCISION",
            style_section
        )
    )

    statut = (
        str(permission.statut).lower()
        if permission.statut
        else ""
    )

    if "accepte" in statut:
        decision_text = "PERMISSION ACCORDÉE"
        decision_color = VERT
        decision_background = VERT_CLAIR

    elif "refuse" in statut:
        decision_text = "PERMISSION REFUSÉE"
        decision_color = ROUGE
        decision_background = ROUGE_CLAIR

    else:
        decision_text = "PERMISSION EN ATTENTE DE VALIDATION"
        decision_color = ORANGE
        decision_background = ORANGE_CLAIR

    decision_style = ParagraphStyle(
        "DecisionFinalePermission",
        parent=style_decision,
        textColor=decision_color,
    )

    decision_table = Table(
        [
            [
                Paragraph(
                    decision_text,
                    decision_style
                )
            ]
        ],
        colWidths=[173 * mm],
        rowHeights=[22 * mm],
    )

    decision_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    decision_background
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1.2,
                    decision_color
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(decision_table)
    elements.append(Spacer(1, 15))

    # ==========================================================
    # TEXTE OFFICIEL
    # ==========================================================

    if "accepte" in statut:

        texte = (
            f"Après examen de la demande de permission présentée par "
            f"<b>{prenom} {nom}</b>, le Service des Ressources Humaines "
            f"confirme l'autorisation de la permission pour la date du "
            f"<b>{date_permission}</b>, avec une date de retour prévue "
            f"le <b>{date_retour}</b>."
        )

    elif "refuse" in statut:

        texte = (
            f"Après examen de la demande de permission présentée par "
            f"<b>{prenom} {nom}</b>, le Service des Ressources Humaines "
            f"confirme le refus de la permission demandée pour la date "
            f"du <b>{date_permission}</b>."
        )

    else:

        texte = (
            f"La demande de permission présentée par "
            f"<b>{prenom} {nom}</b> est actuellement en attente "
            f"de validation."
        )

    texte_table = Table(
        [
            [
                Paragraph(
                    texte,
                    style_valeur
                )
            ]
        ],
        colWidths=[173 * mm],
    )

    texte_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GRIS_FOND),
                ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(texte_table)
    elements.append(Spacer(1, 22))

    # ==========================================================
    # SIGNATURES
    # ==========================================================

    signature_data = [
        [
            Paragraph(
                "<b>RESPONSABLE HIÉRARCHIQUE</b>",
                style_label
            ),
            Paragraph(
                "<b>RESSOURCES HUMAINES</b>",
                style_label
            ),
        ],
        [
            Paragraph(
                "<br/><br/><br/>"
                "Nom et signature :<br/>"
                "____________________________",
                style_valeur
            ),
            Paragraph(
                "<br/><br/><br/>"
                "Nom et signature :<br/>"
                "____________________________",
                style_valeur
            ),
        ],
    ]

    signature_table = Table(
        signature_data,
        colWidths=[86.5 * mm, 86.5 * mm],
        rowHeights=[10 * mm, 35 * mm],
    )

    signature_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), GRIS_FOND),
                ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(signature_table)
    elements.append(Spacer(1, 18))

    # ==========================================================
    # MENTION
    # ==========================================================

    elements.append(
        Paragraph(
            "Document généré automatiquement par le système "
            "de gestion des ressources humaines. "
            "Ce document constitue une pièce administrative "
            "relative à la demande de permission enregistrée.",
            style_footer
        )
    )

    # ==========================================================
    # PIED DE PAGE
    # ==========================================================

    def footer(canvas, doc):

        canvas.saveState()

        width, height = A4

        canvas.setStrokeColor(BLEU)
        canvas.setLineWidth(0.7)

        canvas.line(
            18 * mm,
            14 * mm,
            width - 18 * mm,
            14 * mm
        )

        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GRIS)

        canvas.drawString(
            18 * mm,
            9 * mm,
            "Service des Ressources Humaines"
        )

        canvas.drawCentredString(
            width / 2,
            9 * mm,
            f"Référence : {reference}"
        )

        canvas.drawRightString(
            width - 18 * mm,
            9 * mm,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    # ==========================================================
    # GÉNÉRATION
    # ==========================================================

    pdf.build(
        elements,
        onFirstPage=footer,
        onLaterPages=footer
    )

    buffer.seek(0)

    return buffer
