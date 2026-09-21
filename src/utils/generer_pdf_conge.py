from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def generer_pdf_conge(conge):

    buffer = BytesIO()

    # ==========================================================
    # CONFIGURATION DU PDF
    # ==========================================================

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="Validation de congé",
        author="Service des Ressources Humaines",
    )

    # ==========================================================
    # COULEURS
    # ==========================================================

    BLEU = colors.HexColor("#174A7E")
    BLEU_CLAIR = colors.HexColor("#EAF2F8")

    VERT = colors.HexColor("#198754")
    VERT_CLAIR = colors.HexColor("#D1E7DD")

    GRIS = colors.HexColor("#6C757D")
    GRIS_CLAIR = colors.HexColor("#DEE2E6")
    GRIS_FOND = colors.HexColor("#F8F9FA")

    NOIR = colors.HexColor("#212529")

    # ==========================================================
    # STYLES
    # ==========================================================

    styles = getSampleStyleSheet()

    style_entreprise = ParagraphStyle(
        "Entreprise",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=BLEU,
    )

    style_coordonnees = ParagraphStyle(
        "Coordonnees",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=GRIS,
    )

    style_titre = ParagraphStyle(
        "TitreValidation",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=BLEU,
        spaceAfter=4,
    )

    style_sous_titre = ParagraphStyle(
        "SousTitreValidation",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    style_section = ParagraphStyle(
        "SectionValidation",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=BLEU,
        spaceBefore=4,
        spaceAfter=7,
    )

    style_label = ParagraphStyle(
        "LabelValidation",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
    )

    style_valeur = ParagraphStyle(
        "ValeurValidation",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
    )

    style_decision = ParagraphStyle(
        "Decision",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=VERT,
    )

    style_footer = ParagraphStyle(
        "FooterValidation",
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

    # Emplacement provisoire du logo
    logo = Table(
        [
            [
                Paragraph(
                    "<b>LOGO</b>",
                    ParagraphStyle(
                        "Logo",
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
            "VALIDATION DE CONGÉ",
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
    # RÉFÉRENCE
    # ==========================================================

    reference = f"VAL-CONGE-{conge.pk:05d}"

    date_validation = (
        conge.date_modification.strftime("%d/%m/%Y")
        if conge.date_modification
        else "-"
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

    employe = conge.employe

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
    # INFORMATIONS DU CONGÉ
    # ==========================================================

    elements.append(
        Paragraph(
            "2. INFORMATIONS RELATIVES AU CONGÉ",
            style_section
        )
    )

    type_conge = (
        str(conge.type_conge)
        if getattr(conge, "type_conge", None)
        else "-"
    )

    date_debut = (
        conge.date_debut.strftime("%d/%m/%Y")
        if conge.date_debut
        else "-"
    )

    date_fin = (
        conge.date_fin.strftime("%d/%m/%Y")
        if conge.date_fin
        else "-"
    )

    nombre_jours = (
        str(conge.nombre_jours)
        if conge.nombre_jours is not None
        else "-"
    )

    # Calcul de la date de reprise
    date_reprise = "-"

    if conge.date_fin:
        from datetime import timedelta

        date_reprise = (
            conge.date_fin + timedelta(days=1)
        ).strftime("%d/%m/%Y")

    conge_data = [
        [
            Paragraph("<b>Type de congé</b>", style_label),
            Paragraph(type_conge, style_valeur),
        ],
        [
            Paragraph("<b>Date de début</b>", style_label),
            Paragraph(date_debut, style_valeur),
        ],
        [
            Paragraph("<b>Date de fin</b>", style_label),
            Paragraph(date_fin, style_valeur),
        ],
        [
            Paragraph("<b>Durée du congé</b>", style_label),
            Paragraph(
                f"{nombre_jours} jour(s)",
                style_valeur
            ),
        ],
        [
            Paragraph("<b>Date de reprise du travail</b>", style_label),
            Paragraph(date_reprise, style_valeur),
        ],
    ]

    conge_table = Table(
        conge_data,
        colWidths=[65 * mm, 108 * mm],
    )

    conge_table.setStyle(
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

    elements.append(conge_table)
    elements.append(Spacer(1, 18))

    # ==========================================================
    # DÉCISION DE VALIDATION
    # ==========================================================

    elements.append(
        Paragraph(
            "3. DÉCISION",
            style_section
        )
    )

    decision = str(conge.statut).upper() if conge.statut else "EN ATTENTE"

    if "ACCEPTE" in decision:
        decision_text = "CONGÉ ACCORDÉ"
        decision_color = VERT
        decision_background = VERT_CLAIR
    else:
        decision_text = decision
        decision_color = BLEU
        decision_background = BLEU_CLAIR

    decision_paragraph = Paragraph(
        decision_text,
        ParagraphStyle(
            "DecisionFinale",
            parent=style_decision,
            textColor=decision_color,
        )
    )

    decision_table = Table(
        [
            [
                decision_paragraph
            ]
        ],
        colWidths=[173 * mm],
        rowHeights=[20 * mm],
    )

    decision_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), decision_background),
                ("BOX", (0, 0), (-1, -1), 1.2, decision_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(decision_table)
    elements.append(Spacer(1, 14))

    # ==========================================================
    # TEXTE OFFICIEL
    # ==========================================================

    texte_validation = (
        f"Après examen de la demande de congé de "
        f"<b>{prenom} {nom}</b>, le Service des Ressources Humaines "
        f"confirme la décision indiquée ci-dessus concernant la "
        f"période allant du <b>{date_debut}</b> au "
        f"<b>{date_fin}</b>, pour une durée de "
        f"<b>{nombre_jours} jour(s)</b>."
    )

    texte_table = Table(
        [
            [
                Paragraph(
                    texte_validation,
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
    # SIGNATURE RH
    # ==========================================================

    signature_data = [
        [
            Paragraph(
                "<b>RESPONSABLE DES RESSOURCES HUMAINES</b>",
                style_label
            ),
            Paragraph(
                "<b>CACHET DE L'ENTREPRISE</b>",
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
                "Cachet :<br/>"
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
            "Toute modification non autorisée de ce document "
            "est interdite.",
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
