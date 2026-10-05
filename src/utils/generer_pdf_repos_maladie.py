from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from demande.models.repos_maladie_model import ReposMaladie


# ============================================================
# COULEURS
# ============================================================

BLEU = HexColor("#0B5ED7")
BLEU_FONCE = HexColor("#084298")
BLEU_CLAIR = HexColor("#EAF2FF")

GRIS_FOND = HexColor("#F5F7FA")
GRIS_BORDURE = HexColor("#D9DEE5")
GRIS_TEXTE = HexColor("#5F6B7A")

VERT = HexColor("#198754")
ROUGE = HexColor("#DC3545")
ORANGE = HexColor("#FD7E14")

NOIR = HexColor("#212529")
BLANC = colors.white


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generer_pdf_repos_maladie(repos):

    buffer = BytesIO()

    # ========================================================
    # DOCUMENT A4
    # ========================================================

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=12 * mm,
        bottomMargin=15 * mm,
        title="Demande de repos maladie",
        author="Application de gestion des congés et permissions",
    )

    elements = []

    # ========================================================
    # STYLES
    # ========================================================

    title_style = ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        textColor=BLEU_FONCE,
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=GRIS_TEXTE,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "Section",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=BLANC,
        alignment=TA_LEFT,
    )

    label_style = ParagraphStyle(
        "Label",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=GRIS_TEXTE,
    )

    value_style = ParagraphStyle(
        "Value",
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=NOIR,
    )

    text_style = ParagraphStyle(
        "Text",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=NOIR,
    )

    decision_style = ParagraphStyle(
        "Decision",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=NOIR,
        alignment=TA_CENTER,
    )

    # ========================================================
    # DONNÉES EMPLOYÉ
    # ========================================================

    employe = repos.employe

    nom_complet = f"{employe.prenom} {employe.nom}"

    email = (
        getattr(employe.utilisateur, "email", None)
        or "-"
    )

    fonction = (
        str(employe.fonction)
        if employe.fonction
        else "-"
    )

    departement = (
        str(employe.departement)
        if employe.departement
        else "-"
    )

    superieur = "-"

    if employe.superieur:
        superieur = (
            f"{employe.superieur.prenom} "
            f"{employe.superieur.nom}"
        )

    # ========================================================
    # EN-TÊTE
    # ========================================================

    header_data = [
        [
            Paragraph(
                "<b>GESTION DU PERSONNEL</b>",
                value_style
            ),
            Paragraph(
                "<b>DEMANDE DE REPOS MALADIE</b>",
                title_style
            ),
            Paragraph(
                "DOCUMENT OFFICIEL",
                value_style
            ),
        ]
    ]

    header_table = Table(
        header_data,
        colWidths=[
            30 * mm,
            105 * mm,
            43 * mm,
        ],
        rowHeights=[25 * mm],
    )

    header_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            BLANC
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.8,
            BLEU
        ),
        (
            "LINEAFTER",
            (0, 0),
            (1, 0),
            0.5,
            GRIS_BORDURE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "ALIGN",
            (0, 0),
            (0, 0),
            "CENTER"
        ),
        (
            "ALIGN",
            (2, 0),
            (2, 0),
            "CENTER"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ]))

    elements.append(header_table)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # TITRE
    # ========================================================

    title_table = Table(
        [
            [
                Paragraph(
                    "DEMANDE DE REPOS MALADIE",
                    title_style
                )
            ],
            [
                Paragraph(
                    "Document de suivi administratif de l'absence pour raison médicale",
                    subtitle_style
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[
            12 * mm,
            7 * mm,
        ],
    )

    title_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            BLEU_CLAIR
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            GRIS_BORDURE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
    ]))

    elements.append(title_table)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # SECTION INFORMATIONS EMPLOYÉ
    # ========================================================

    section_employe = Table(
        [
            [
                Paragraph(
                    "INFORMATIONS DE L'EMPLOYÉ",
                    section_style
                )
            ]
        ],
        colWidths=[178 * mm],
        rowHeights=[10 * mm],
    )

    section_employe.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            BLEU
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            BLEU
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
    ]))

    elements.append(section_employe)

    elements.append(Spacer(1, 2 * mm))

    # ========================================================
    # TABLEAU EMPLOYÉ
    # ========================================================

    employe_data = [
        [
            Paragraph("Nom et prénom", label_style),
            Paragraph(nom_complet, value_style),
            Paragraph("Email", label_style),
            Paragraph(email, value_style),
        ],
        [
            Paragraph("Fonction", label_style),
            Paragraph(fonction, value_style),
            Paragraph("Département", label_style),
            Paragraph(departement, value_style),
        ],
        [
            Paragraph("Supérieur hiérarchique", label_style),
            Paragraph(superieur, value_style),
            Paragraph("Référence", label_style),
            Paragraph(
                f"MAL-{repos.id:05d}",
                value_style
            ),
        ],
    ]

    employe_table = Table(
        employe_data,
        colWidths=[
            43 * mm,
            46 * mm,
            43 * mm,
            46 * mm,
        ],
        rowHeights=[
            10 * mm,
            10 * mm,
            10 * mm,
        ],
    )

    employe_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            GRIS_FOND
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            GRIS_BORDURE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ]))

    elements.append(employe_table)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # SECTION INFORMATIONS REPOS MALADIE
    # ========================================================

    section_repos = Table(
        [
            [
                Paragraph(
                    "INFORMATIONS DU REPOS MALADIE",
                    section_style
                )
            ]
        ],
        colWidths=[178 * mm],
        rowHeights=[10 * mm],
    )

    section_repos.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            BLEU
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            BLEU
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
    ]))

    elements.append(section_repos)

    elements.append(Spacer(1, 2 * mm))

    # ========================================================
    # JUSTIFICATIF
    # ========================================================

    justificatif = "-"

    if repos.justificatif:
        justificatif = str(repos.justificatif)

    # ========================================================
    # INFORMATIONS REPOS
    # ========================================================

    repos_data = [
        [
            Paragraph("Date de début", label_style),
            Paragraph(
                str(repos.date_debut),
                value_style
            ),
            Paragraph("Date de fin", label_style),
            Paragraph(
                str(repos.date_fin)
                if repos.date_fin
                else "-",
                value_style
            ),
        ],
        [
            Paragraph("Durée", label_style),
            Paragraph(
                f"{repos.nombre_jours} jour(s)",
                value_style
            ),
            Paragraph("Date de reprise", label_style),
            Paragraph(
                str(repos.date_fin)
                if repos.date_fin
                else "-",
                value_style
            ),
        ],
        [
            Paragraph("Statut", label_style),
            Paragraph(
                str(repos.statut),
                value_style
            ),
            Paragraph("Date de demande", label_style),
            Paragraph(
                str(repos.date_creation),
                value_style
            ),
        ],
        [
            Paragraph("Référence", label_style),
            Paragraph(
                f"MAL-{repos.id:05d}",
                value_style
            ),
            Paragraph("Justificatif", label_style),
            Paragraph(
                justificatif,
                value_style
            ),
        ],
    ]

    repos_table = Table(
        repos_data,
        colWidths=[
            43 * mm,
            46 * mm,
            43 * mm,
            46 * mm,
        ],
        rowHeights=[
            10 * mm,
            10 * mm,
            10 * mm,
            10 * mm,
        ],
    )

    repos_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            GRIS_FOND
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            GRIS_BORDURE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ]))

    elements.append(repos_table)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # DÉCISION
    # ========================================================

    statut = repos.statut

    if statut == "accepte":
        decision_text = "DEMANDE ACCEPTÉE"
        decision_color = VERT

    elif statut == "refuse":
        decision_text = "DEMANDE REFUSÉE"
        decision_color = ROUGE

    else:
        decision_text = "DEMANDE EN ATTENTE"
        decision_color = ORANGE

    decision_table = Table(
        [
            [
                Paragraph(
                    decision_text,
                    decision_style
                )
            ],
            [
                Paragraph(
                    f"Statut actuel : {statut}",
                    subtitle_style
                )
            ],
        ],
        colWidths=[178 * mm],
        rowHeights=[
            11 * mm,
            10 * mm,
        ],
    )

    decision_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            decision_color
        ),
        (
            "BACKGROUND",
            (0, 1),
            (-1, 1),
            GRIS_FOND
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            decision_color
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            BLANC
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
    ]))

    elements.append(decision_table)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # TEXTE OFFICIEL
    # ========================================================

    official_text = Table(
        [
            [
                Paragraph(
                    "Le présent document est établi dans le cadre "
                    "du suivi administratif des absences pour raison "
                    "médicale du personnel.",
                    text_style
                )
            ]
        ],
        colWidths=[178 * mm],
        rowHeights=[18 * mm],
    )

    official_text.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            GRIS_FOND
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            GRIS_BORDURE
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ]))

    elements.append(official_text)

    elements.append(Spacer(1, 5 * mm))

    # ========================================================
    # SIGNATURES
    # ========================================================

    signatures_data = [
        [
            Paragraph(
                "EMPLOYÉ",
                label_style
            ),
            Paragraph(
                "SUPÉRIEUR HIÉRARCHIQUE",
                label_style
            ),
            Paragraph(
                "RESSOURCES HUMAINES",
                label_style
            ),
        ],
        [
            "",
            "",
            "",
        ],
    ]

    signatures_table = Table(
        signatures_data,
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

    signatures_table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            BLEU_CLAIR
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            GRIS_BORDURE
        ),
        (
            "ALIGN",
            (0, 0),
            (-1, -1),
            "CENTER"
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            5
        ),
    ]))

    elements.append(signatures_table)

    # ========================================================
    # PIED DE PAGE
    # ========================================================

    def footer(canvas, doc):

        canvas.saveState()

        width, height = A4

        canvas.setStrokeColor(GRIS_BORDURE)
        canvas.setLineWidth(0.5)

        canvas.line(
            15 * mm,
            9 * mm,
            width - 15 * mm,
            9 * mm
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(GRIS_TEXTE)

        canvas.drawString(
            15 * mm,
            5 * mm,
            f"Référence : MAL-{repos.id:05d}"
        )

        canvas.drawRightString(
            width - 15 * mm,
            5 * mm,
            f"Page {doc.page} / 1"
        )

        canvas.restoreState()

    # ========================================================
    # GÉNÉRATION
    # ========================================================

    doc.build(
        elements,
        onFirstPage=footer,
        onLaterPages=footer
    )

    buffer.seek(0)

    return buffer.getvalue()