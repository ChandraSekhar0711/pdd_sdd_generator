"""Document extraction and professional SDD export services."""

import io
from xml.sax.saxutils import escape

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


ACCENT = "#4F46E5"
ACCENT_DARK = "#3730A3"
PALE = "#EEF2FF"
BORDER = "#D9E0EF"
TEXT = "#1F2937"
MUTED = "#64748B"


def extract_text(file_bytes: bytes, filename: str) -> str:
    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "txt":
        text = file_bytes.decode("utf-8-sig")
    elif extension == "pdf":
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif extension == "docx":
        document = Document(io.BytesIO(file_bytes))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        for table in document.tables:
            for row in table.rows:
                text += "\n" + " | ".join(cell.text for cell in row.cells)
    else:
        raise ValueError("Unsupported file format. Upload PDF, DOCX, or TXT.")

    if not text.strip():
        raise ValueError("The uploaded document contains no extractable text.")

    return text.strip()


def _display_name(key: str) -> str:
    return str(key).replace("_", " ").replace("-", " ").title()


def _flatten(value):
    """Turn nested values into readable text for table cells."""
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(_flatten(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(f"{_display_name(k)}: {_flatten(v)}" for k, v in value.items())
    return str(value)


def _set_cell_shading(cell, fill: str):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shading)


def _set_cell_text(cell, text: str, bold=False, color=None, size=9):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(str(text))
    run.bold = bold
    run.font.name = "Arial"
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)


def _add_docx_table(document, items):
    keys = list(dict.fromkeys(k for item in items for k in item.keys()))
    if not keys:
        return
    table = document.add_table(rows=1, cols=len(keys))
    table.style = "Table Grid"
    table.autofit = True

    header = table.rows[0].cells
    for idx, key in enumerate(keys):
        _set_cell_text(header[idx], _display_name(key), bold=True, color=(55, 48, 163))
        _set_cell_shading(header[idx], "EEF2FF")

    for item in items:
        cells = table.add_row().cells
        for idx, key in enumerate(keys):
            _set_cell_text(cells[idx], _flatten(item.get(key, "")))

    document.add_paragraph()


def generate_docx(sdd: dict, project_name: str) -> io.BytesIO:
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.68)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # Default typography
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor(31, 41, 55)
    normal.paragraph_format.space_after = Pt(5)

    for style_name in ("Heading 1", "Heading 2", "Heading 3"):
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.color.rgb = RGBColor(79, 70, 229)
    document.styles["Heading 1"].font.size = Pt(16)
    document.styles["Heading 2"].font.size = Pt(12)
    document.styles["Heading 3"].font.size = Pt(10)

    # Cover-style heading (compact, avoids wasting a full page)
    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(16)
    title.paragraph_format.space_after = Pt(5)
    run = title.add_run(project_name)
    run.bold = True
    run.font.name = "Arial"
    run.font.size = Pt(23)
    run.font.color.rgb = RGBColor(79, 70, 229)

    subtitle = document.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(18)
    subrun = subtitle.add_run("Solution Design Document")
    subrun.font.name = "Arial"
    subrun.font.size = Pt(13)
    subrun.font.color.rgb = RGBColor(100, 116, 139)

    # Header and footer
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header_run = header.add_run("SOLUTION DESIGN DOCUMENT")
    header_run.font.name = "Arial"
    header_run.font.size = Pt(8)
    header_run.font.color.rgb = RGBColor(100, 116, 139)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run(f"{project_name}  |  ")
    footer_run.font.size = Pt(8)
    footer_run.font.color.rgb = RGBColor(100, 116, 139)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer._p.append(fld)

    def add_content(key, value, level=1):
        if value is None or value == "":
            return
        heading = _display_name(key)

        if isinstance(value, dict):
            document.add_heading(heading, level=min(level, 3))
            for child_key, child_value in value.items():
                add_content(child_key, child_value, level + 1)
        elif isinstance(value, list):
            document.add_heading(heading, level=min(level, 3))
            if value and all(isinstance(item, dict) for item in value):
                _add_docx_table(document, value)
            else:
                for item in value:
                    if isinstance(item, dict):
                        document.add_heading(_display_name(item.get("name", "Item")), level=min(level + 1, 3))
                        for child_key, child_value in item.items():
                            if child_key != "name":
                                document.add_paragraph(
                                    f"{_display_name(child_key)}: {_flatten(child_value)}",
                                    style="List Bullet",
                                )
                    else:
                        document.add_paragraph(_flatten(item), style="List Bullet")
        else:
            document.add_heading(heading, level=min(level, 3))
            document.add_paragraph(_flatten(value))

    for key, value in sdd.items():
        if key != "project_name":
            add_content(key, value)

    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer


def generate_pdf(sdd: dict, project_name: str) -> io.BytesIO:
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=19 * mm,
        bottomMargin=17 * mm,
        title=f"{project_name} - Solution Design Document",
        author="PDD to SDD Generator",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SDDTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=21, leading=27, textColor=colors.HexColor(ACCENT),
        alignment=TA_CENTER, spaceAfter=7,
    )
    subtitle_style = ParagraphStyle(
        "SDDSubtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=12, leading=17, textColor=colors.HexColor(MUTED),
        alignment=TA_CENTER, spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        "SDDHeading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=colors.HexColor(ACCENT_DARK),
        spaceBefore=12, spaceAfter=6, keepWithNext=True,
    )
    subheading_style = ParagraphStyle(
        "SDDSubheading", parent=styles["Heading3"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=colors.HexColor(TEXT),
        spaceBefore=6, spaceAfter=4, keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "SDDBody", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=8.8, leading=12.5, textColor=colors.HexColor(TEXT),
        spaceAfter=5, wordWrap="CJK",
    )
    bullet_style = ParagraphStyle(
        "SDDBullet", parent=body_style, leftIndent=12, firstLineIndent=-8,
        spaceAfter=3,
    )
    table_cell_style = ParagraphStyle(
        "SDDTableCell", parent=body_style, fontSize=7.5, leading=10,
        spaceAfter=0,
    )
    table_header_style = ParagraphStyle(
        "SDDTableHeader", parent=table_cell_style, fontName="Helvetica-Bold",
        textColor=colors.HexColor(ACCENT_DARK),
    )

    story = [
        Spacer(1, 7 * mm),
        Paragraph(escape(project_name), title_style),
        Paragraph("Solution Design Document", subtitle_style),
    ]

    def add_dict_table(items):
        keys = list(dict.fromkeys(k for item in items for k in item.keys()))
        if not keys:
            return
        data = [[Paragraph(escape(_display_name(key)), table_header_style) for key in keys]]
        for item in items:
            data.append([
                Paragraph(escape(_flatten(item.get(key, ""))), table_cell_style)
                for key in keys
            ])
        available_width = A4[0] - 32 * mm
        # Equal column widths are a reliable general layout for variable schemas.
        widths = [available_width / len(keys)] * len(keys)
        table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(PALE)),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor(BORDER)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.extend([table, Spacer(1, 7)])

    def add_content(key, value, level=1):
        if value is None or value == "":
            return
        heading = escape(_display_name(key))

        if isinstance(value, dict):
            story.append(Paragraph(heading, heading_style if level <= 1 else subheading_style))
            for child_key, child_value in value.items():
                add_content(child_key, child_value, level + 1)
        elif isinstance(value, list):
            story.append(Paragraph(heading, heading_style if level <= 1 else subheading_style))
            if value and all(isinstance(item, dict) for item in value):
                add_dict_table(value)
            else:
                for item in value:
                    if isinstance(item, dict):
                        item_title = item.get("name") or item.get("title") or "Item"
                        story.append(Paragraph(escape(_flatten(item_title)), subheading_style))
                        for child_key, child_value in item.items():
                            if child_key not in ("name", "title"):
                                story.append(Paragraph(
                                    f"<b>{escape(_display_name(child_key))}:</b> "
                                    f"{escape(_flatten(child_value))}", body_style
                                ))
                    else:
                        story.append(Paragraph("• " + escape(_flatten(item)), bullet_style))
        else:
            story.append(Paragraph(heading, heading_style if level <= 1 else subheading_style))
            story.append(Paragraph(escape(_flatten(value)), body_style))

    for key, value in sdd.items():
        if key != "project_name":
            add_content(key, value)

    def draw_page(canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(colors.HexColor(BORDER))
        canvas.setLineWidth(0.5)
        canvas.line(16 * mm, height - 12 * mm, width - 16 * mm, height - 12 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(16 * mm, 9 * mm, project_name)
        canvas.drawRightString(width - 16 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()

    pdf.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    buffer.seek(0)
    return buffer
