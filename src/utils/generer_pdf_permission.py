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
)


def generer_pdf_permission(permission):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=10 * mm,
        bottomMargin=14 * mm,
        title="Attestation de permission",
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
        "TitrePermission",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=18,
        textColor=BLANC,
        alignment=TA_CENTER,
    )

    sous_titre_style = ParagraphStyle(
        "SousTitrePermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=9,
        textColor=BLANC,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "SectionPermission",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=11,
        textColor=BLEU_FONCE,
    )

    label_style = ParagraphStyle(
        "LabelPermission",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=9,
        textColor=GRIS_TEXTE,
    )

    value_style = ParagraphStyle(
        "ValuePermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        textColor=NOIR,
    )

    texte_style = ParagraphStyle(
        "TextePermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=NOIR,
        alignment=TA_LEFT,
    )

    decision_style = ParagraphStyle(
        "DecisionPermission",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        alignment=TA_CENTER,
    )

    # ==========================================================
    # FONCTIONS
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
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ]
            )
        )

        return table

    def info_table(rows):

        data = []

        for label1, value1, label2, value2 in rows:

            data.append(
                [
                    Paragraph(label1, label_style),
                    Paragraph(str(value1), value_style),
                    Paragraph(label2, label_style),
                    Paragraph(str(value2), value_style),
                ]
            )

        table = Table(
            data,
            colWidths=[
                43 * mm,
                46 * mm,
                43 * mm,
                46 * mm,
            ],
            rowHeights=[8 * mm] * len(data),
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
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        2,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        2,
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
            "LogoPermission",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=BLEU_FONCE,
            alignment=TA_CENTER,
        )
    )

    entreprise = Paragraph(
        "<b>NOM DE L'ENTREPRISE</b><br/>"
        "<font size='7.5'>Direction des Ressources Humaines</font><br/>"
        "<font size='6.5'>Service Administration du Personnel</font>",
        ParagraphStyle(
            "EntreprisePermission",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            textColor=NOIR,
        )
    )

    reference = Paragraph(
        "<b>DOCUMENT OFFICIEL</b><br/>"
        f"<font size='6.5'>Référence : PERM-{permission.id:05d}</font>",
        ParagraphStyle(
            "ReferencePermission",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
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
        rowHeights=[21 * mm],
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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elements.append(header)
    elements.append(Spacer(1, 3 * mm))

    # ==========================================================
    # TITRE
    # ==========================================================

    titre = Table(
        [
            [
                Paragraph(
                    "ATTESTATION DE PERMISSION",
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
        rowHeights=[10 * mm, 6 * mm],
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
            ]
        )
    )

    elements.append(titre)
    elements.append(Spacer(1, 3 * mm))

    # ==========================================================
    # SALARIÉ
    # ==========================================================

    elements.append(
        section_header("1. IDENTIFICATION DU SALARIÉ")
    )

    elements.append(Spacer(1, 1.5 * mm))

    superieur = (
        f"{permission.employe.superieur.prenom} "
        f"{permission.employe.superieur.nom}"
        if permission.employe.superieur
        else "Non renseigné"
    )

    email = (
        permission.employe.utilisateur.email
        if permission.employe.utilisateur
        else "Non renseigné"
    )

    fonction = (
        str(permission.employe.fonction)
        if permission.employe.fonction
        else "Non renseignée"
    )

    departement = (
        str(permission.employe.departement)
        if permission.employe.departement
        else "Non renseigné"
    )

    elements.append(
        info_table(
            [
                (
                    "Nom",
                    permission.employe.nom,
                    "Prénom",
                    permission.employe.prenom,
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
    )

    elements.append(Spacer(1, 3 * mm))

    # ==========================================================
    # PERMISSION
    # ==========================================================

    elements.append(
        section_header("2. INFORMATIONS DE LA PERMISSION")
    )

    elements.append(Spacer(1, 1.5 * mm))

    type_permission = (
        str(permission.type_permission)
        if permission.type_permission
        else "Non renseigné"
    )

    date_permission = (
        permission.date_permission.strftime("%d/%m/%Y")
        if permission.date_permission
        else "Non renseignée"
    )

    date_retour = (
        permission.date_retour.strftime("%d/%m/%Y")
        if permission.date_retour
        else "Non renseignée"
    )

    motif = (
        permission.motif
        if permission.motif
        else "Aucun motif renseigné"
    )

    statut = permission.statut.replace("_", " ").upper()

    permission_table = info_table(
        [
            (
                "Type de permission",
                type_permission,
                "Date de permission",
                date_permission,
            ),
            (
                "Date de retour",
                date_retour,
                "Statut",
                statut,
            ),
            (
                "Date de demande",
                permission.date_creation.strftime(
                    "%d/%m/%Y %H:%M"
                ),
                "Référence",
                f"PERM-{permission.id:05d}",
            ),
        ]
    )

    elements.append(permission_table)
    elements.append(Spacer(1, 2.5 * mm))

    # ==========================================================
    # MOTIF
    # ==========================================================

    motif_box = Table(
        [
            [
                Paragraph(
                    "<b>MOTIF DE LA PERMISSION</b>",
                    label_style
                )
            ],
            [
                Paragraph(
                    str(motif),
                    texte_style
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[6 * mm, 14 * mm],
    )

    motif_box.setStyle(
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
                    2,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
            ]
        )
    )

    elements.append(motif_box)
    elements.append(Spacer(1, 3 * mm))

    # ==========================================================
    # DÉCISION
    # ==========================================================

    if permission.statut == "accepte":

        decision = "PERMISSION DÉFINITIVEMENT ACCORDÉE"
        decision_color = VERT
        decision_text = (
            "La demande de permission a reçu les validations requises "
            "et est officiellement accordée."
        )

    elif permission.statut == "refuse":

        decision = "DEMANDE DE PERMISSION REFUSÉE"
        decision_color = ROUGE
        decision_text = (
            "La demande de permission n'a pas été approuvée."
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
                        "DecisionPermissionTitre",
                        parent=decision_style,
                        textColor=decision_color,
                    )
                )
            ],
            [
                Paragraph(
                    decision_text,
                    ParagraphStyle(
                        "DecisionPermissionText",
                        parent=styles["Normal"],
                        fontName="Helvetica",
                        fontSize=8,
                        leading=10,
                        textColor=GRIS_TEXTE,
                        alignment=TA_CENTER,
                    )
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[8 * mm, 8 * mm],
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
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(decision_box)
    elements.append(Spacer(1, 3 * mm))

    # ==========================================================
    # TEXTE OFFICIEL
    # ==========================================================

    texte = (
        "Le présent document atteste que <b>"
        f"{permission.employe.prenom} {permission.employe.nom}"
        "</b>, appartenant au département "
        f"<b>{departement}</b>, est autorisé(e) à bénéficier "
        "de la permission indiquée dans le présent document, "
        "conformément aux procédures internes de l'entreprise."
    )

    texte_box = Table(
        [
            [
                Paragraph(texte, texte_style)
            ]
        ],
        colWidths=[178 * mm],
        rowHeights=[15 * mm],
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

    elements.append(texte_box)
    elements.append(Spacer(1, 3.5 * mm))

    # ==========================================================
    # SIGNATURES
    # ==========================================================

    elements.append(
        section_header("3. VALIDATION ET SIGNATURES")
    )

    elements.append(Spacer(1, 2 * mm))

    signature_style = ParagraphStyle(
        "SignaturePermission",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=NOIR,
        alignment=TA_CENTER,
    )

    signatures = Table(
        [
            [
                Paragraph(
                    "<b>SUPÉRIEUR HIÉRARCHIQUE</b>",
                    signature_style
                ),
                Paragraph(
                    "<b>RESPONSABLE RH</b>",
                    signature_style
                ),
                Paragraph(
                    "<b>CACHET DE L'ENTREPRISE</b>",
                    signature_style
                ),
            ],
            [
                Paragraph(
                    f"{superieur}<br/><br/>"
                    "Signature : __________________",
                    signature_style
                ),
                Paragraph(
                    "Responsable des Ressources Humaines"
                    "<br/><br/>"
                    "Signature : __________________",
                    signature_style
                ),
                Paragraph(
                    "<br/><br/>"
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
            7 * mm,
            24 * mm,
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
            8 * mm,
            width - 15 * mm,
            8 * mm,
        )

        canvas.setFont(
            "Helvetica",
            6.5
        )

        canvas.setFillColor(GRIS_TEXTE)

        canvas.drawString(
            15 * mm,
            4 * mm,
            "Service des Ressources Humaines"
        )

        canvas.drawCentredString(
            width / 2,
            4 * mm,
            f"Référence PERM-{permission.id:05d}"
        )

        canvas.drawRightString(
            width - 15 * mm,
            4 * mm,
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