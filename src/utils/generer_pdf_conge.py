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
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generer_pdf_conge(conge):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=15 * mm,
        title="Attestation de congé",
        author="Service des Ressources Humaines",
    )

    # ==========================================================
    # COULEURS
    # ==========================================================

    BLEU = colors.HexColor("#0B5ED7")
    BLEU_FONCE = colors.HexColor("#084298")
    BLEU_CLAIR = colors.HexColor("#EAF2FF")

    GRIS_FOND = colors.HexColor("#F5F7FA")
    GRIS_BORDURE = colors.HexColor("#D9DEE5")
    GRIS_TEXTE = colors.HexColor("#5F6B7A")

    VERT = colors.HexColor("#198754")
    ROUGE = colors.HexColor("#DC3545")
    ORANGE = colors.HexColor("#FD7E14")

    NOIR = colors.HexColor("#212529")
    BLANC = colors.white

    # ==========================================================
    # STYLES
    # ==========================================================

    styles = getSampleStyleSheet()

    titre_style = ParagraphStyle(
        "Titre",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        textColor=BLANC,
        alignment=TA_CENTER,
        spaceAfter=0,
    )

    sous_titre_style = ParagraphStyle(
        "SousTitre",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=BLANC,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=BLEU_FONCE,
        spaceAfter=0,
    )

    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=GRIS_TEXTE,
    )

    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=NOIR,
    )

    value_bold_style = ParagraphStyle(
        "ValueBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=NOIR,
    )

    texte_style = ParagraphStyle(
        "Texte",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=NOIR,
        alignment=TA_LEFT,
    )

    decision_style = ParagraphStyle(
        "Decision",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
    )

    # ==========================================================
    # FONCTIONS UTILITAIRES
    # ==========================================================

    def section_header(titre):

        table = Table(
            [
                [
                    Paragraph(
                        f"<b>{titre}</b>",
                        section_style
                    )
                ]
            ],
            colWidths=[178 * mm],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        BLEU_CLAIR,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.7,
                        BLEU,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        return table

    def info_table(rows, widths=(43 * mm, 46 * mm, 43 * mm, 46 * mm)):

        data = []

        for label1, value1, label2, value2 in rows:

            data.append(
                [
                    Paragraph(label1, label_style),
                    Paragraph(value1, value_style),
                    Paragraph(label2, label_style),
                    Paragraph(value2, value_style),
                ]
            )

        table = Table(
            data,
            colWidths=widths,
            rowHeights=10 * mm,
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        GRIS_FOND,
                    ),
                    (
                        "BACKGROUND",
                        (2, 0),
                        (2, -1),
                        GRIS_FOND,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        GRIS_BORDURE,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        return table

    # ==========================================================
    # ELEMENTS
    # ==========================================================

    elements = []

    # ==========================================================
    # EN-TÊTE
    # ==========================================================

    logo = Paragraph(
        "<b>LOGO</b>",
        ParagraphStyle(
            "Logo",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=BLEU_FONCE,
            alignment=TA_CENTER,
        )
    )

    entreprise = Paragraph(
        "<b>NOM DE L'ENTREPRISE</b><br/>"
        "<font size='8'>Direction des Ressources Humaines</font><br/>"
        "<font size='7'>Service Administration du Personnel</font>",
        ParagraphStyle(
            "Entreprise",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=NOIR,
            alignment=TA_LEFT,
        )
    )

    reference = Paragraph(
        "<b>DOCUMENT OFFICIEL</b><br/>"
        "<font size='7'>Référence : CONGE-"
        f"{conge.id:05d}"
        "</font>",
        ParagraphStyle(
            "Reference",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=BLEU_FONCE,
            alignment=TA_CENTER,
        )
    )

    header = Table(
        [
            [logo, entreprise, reference]
        ],
        colWidths=[
            30 * mm,
            105 * mm,
            43 * mm,
        ],
        rowHeights=[25 * mm],
    )

    header.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    GRIS_BORDURE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    elements.append(header)
    elements.append(Spacer(1, 5 * mm))

    # ==========================================================
    # TITRE
    # ==========================================================

    titre = Table(
        [
            [
                Paragraph(
                    "ATTESTATION DE CONGÉ",
                    titre_style
                )
            ],
            [
                Paragraph(
                    "DOCUMENT OFFICIEL DE VALIDATION",
                    sous_titre_style
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[12 * mm, 7 * mm],
    )

    titre.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    BLEU_FONCE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    elements.append(titre)
    elements.append(Spacer(1, 5 * mm))

    # ==========================================================
    # INFORMATIONS DU SALARIÉ
    # ==========================================================

    elements.append(section_header("1. IDENTIFICATION DU SALARIÉ"))
    elements.append(Spacer(1, 2 * mm))

    superieur = (
        f"{conge.employe.superieur.prenom} "
        f"{conge.employe.superieur.nom}"
        if conge.employe.superieur
        else "Non renseigné"
    )

    email = (
        conge.employe.utilisateur.email
        if conge.employe.utilisateur
        else "Non renseigné"
    )

    fonction = (
        str(conge.employe.fonction)
        if conge.employe.fonction
        else "Non renseignée"
    )

    departement = (
        str(conge.employe.departement)
        if conge.employe.departement
        else "Non renseigné"
    )

    employe_table = info_table(
        [
            (
                "Nom",
                conge.employe.nom,
                "Prénom",
                conge.employe.prenom,
            ),
            (
                "Email",
                email,
                "Fonction",
                fonction,
            ),
            (
                "Département",
                departement,
                "Supérieur hiérarchique",
                superieur,
            ),
        ]
    )

    elements.append(employe_table)
    elements.append(Spacer(1, 5 * mm))

    # ==========================================================
    # INFORMATIONS DU CONGÉ
    # ==========================================================

    elements.append(section_header("2. INFORMATIONS DU CONGÉ"))
    elements.append(Spacer(1, 2 * mm))

    date_debut = (
        conge.date_debut.strftime("%d/%m/%Y")
        if conge.date_debut
        else "Non renseignée"
    )

    date_fin = (
        conge.date_fin.strftime("%d/%m/%Y")
        if conge.date_fin
        else "Non renseignée"
    )

    date_reprise = (
        conge.date_fin.strftime("%d/%m/%Y")
        if conge.date_fin
        else "Non renseignée"
    )

    type_conge = (
        str(conge.type_conge)
        if conge.type_conge
        else "Non renseigné"
    )

    statut = conge.statut.replace("_", " ").upper()

    conge_table = info_table(
        [
            (
                "Type de congé",
                type_conge,
                "Durée",
                f"{conge.nombre_jours} jour(s)",
            ),
            (
                "Date de début",
                date_debut,
                "Date de fin",
                date_fin,
            ),
            (
                "Date de reprise",
                date_reprise,
                "Statut",
                statut,
            ),
            (
                "Date de demande",
                conge.date_creation.strftime("%d/%m/%Y %H:%M"),
                "Référence",
                f"CONGE-{conge.id:05d}",
            ),
        ]
    )

    elements.append(conge_table)
    elements.append(Spacer(1, 5 * mm))

    # ==========================================================
    # DÉCISION
    # ==========================================================

    if conge.statut == "accepte":

        decision = "CONGÉ DÉFINITIVEMENT ACCORDÉ"
        decision_color = VERT
        decision_text = (
            "La demande de congé a reçu les validations requises "
            "et est officiellement accordée."
        )

    elif conge.statut == "refuse":

        decision = "DEMANDE DE CONGÉ REFUSÉE"
        decision_color = ROUGE
        decision_text = (
            "La demande de congé n'a pas été approuvée."
        )

    else:

        decision = "DÉCISION EN ATTENTE"
        decision_color = ORANGE
        decision_text = (
            "La demande est actuellement en attente de validation."
        )

    decision_box = Table(
        [
            [
                Paragraph(
                    decision,
                    ParagraphStyle(
                        "DecisionColor",
                        parent=decision_style,
                        textColor=decision_color,
                    )
                )
            ],
            [
                Paragraph(
                    decision_text,
                    ParagraphStyle(
                        "DecisionText",
                        parent=styles["Normal"],
                        fontName="Helvetica",
                        fontSize=8.5,
                        leading=12,
                        textColor=GRIS_TEXTE,
                        alignment=TA_CENTER,
                    )
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[11 * mm, 10 * mm],
    )

    decision_box.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    decision_color,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.Color(
                        decision_color.red,
                        decision_color.green,
                        decision_color.blue,
                        alpha=0.06
                    ),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    elements.append(decision_box)
    elements.append(Spacer(1, 5 * mm))

    # ==========================================================
    # TEXTE OFFICIEL
    # ==========================================================

    texte = (
        "Le présent document atteste que <b>"
        f"{conge.employe.prenom} {conge.employe.nom}"
        "</b>, appartenant au département "
        f"<b>{departement}</b>, est autorisé(e) à bénéficier "
        "du congé indiqué dans le présent document, conformément "
        "aux procédures internes de gestion des congés de l'entreprise."
    )

    texte_box = Table(
        [
            [
                Paragraph(texte, texte_style)
            ]
        ],
        colWidths=[178 * mm],
        rowHeights=[18 * mm],
    )

    texte_box.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    GRIS_BORDURE,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    GRIS_FOND,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elements.append(texte_box)
    elements.append(Spacer(1, 7 * mm))

    # ==========================================================
    # SIGNATURES
    # ==========================================================

    elements.append(section_header("3. VALIDATION ET SIGNATURES"))
    elements.append(Spacer(1, 3 * mm))

    signature_style = ParagraphStyle(
        "Signature",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
        alignment=TA_CENTER,
    )

    signature_bold = ParagraphStyle(
        "SignatureBold",
        parent=signature_style,
        fontName="Helvetica-Bold",
        fontSize=9,
    )

    signatures = Table(
        [
            [
                Paragraph(
                    "<b>SUPÉRIEUR HIÉRARCHIQUE</b>",
                    signature_bold
                ),
                Paragraph(
                    "<b>RESPONSABLE RH</b>",
                    signature_bold
                ),
                Paragraph(
                    "<b>CACHET DE L'ENTREPRISE</b>",
                    signature_bold
                ),
            ],
            [
                Paragraph(
                    f"{superieur}<br/>"
                    "<br/><br/>"
                    "Signature : __________________",
                    signature_style
                ),
                Paragraph(
                    "Responsable des Ressources Humaines"
                    "<br/><br/><br/>"
                    "Signature : __________________",
                    signature_style
                ),
                Paragraph(
                    "<br/><br/><br/>"
                    "Cachet",
                    signature_style
                ),
            ],
        ],
        colWidths=[
            59 * mm,
            59 * mm,
            60 * mm,
        ],
        rowHeights=[
            10 * mm,
            31 * mm,
        ],
    )

    signatures.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    GRIS_BORDURE,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GRIS_BORDURE,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    GRIS_FOND,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elements.append(signatures)

    # ==========================================================
    # PIED DE PAGE
    # ==========================================================

    def footer(canvas, doc):

        canvas.saveState()

        width, height = A4

        canvas.setStrokeColor(GRIS_BORDURE)
        canvas.setLineWidth(0.5)

        canvas.line(
            15 * mm,
            9 * mm,
            width - 15 * mm,
            9 * mm,
        )

        canvas.setFont(
            "Helvetica",
            7
        )

        canvas.setFillColor(GRIS_TEXTE)

        canvas.drawString(
            15 * mm,
            5 * mm,
            "Service des Ressources Humaines"
        )

        canvas.drawCentredString(
            width / 2,
            5 * mm,
            f"Référence CONGE-{conge.id:05d}"
        )

        canvas.drawRightString(
            width - 15 * mm,
            5 * mm,
            "Page 1 / 1"
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