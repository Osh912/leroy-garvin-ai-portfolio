from __future__ import annotations

"""
ATS-ready resume/cover exporters: Markdown source → PDF + DOCX.
PDFs preserve heading/list/emphasis structure from the markdown.
DOCX uses plain sequential styles (ATS-friendly: no tables/textboxes).
"""

import re
import zipfile
from pathlib import Path
from typing import Any

# Standard packet filenames (always written alongside markdown source)
RESUME_MD = "resume.md"
RESUME_PDF = "resume.pdf"
RESUME_DOCX = "resume.docx"
COVER_MD = "cover_letter.md"
COVER_PDF = "cover_letter.pdf"
COVER_DOCX = "cover_letter.docx"

STANDARD_PACKET_FILES = (
    RESUME_MD,
    RESUME_PDF,
    RESUME_DOCX,
    COVER_MD,
    COVER_PDF,
    COVER_DOCX,
)

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_HEADER_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_BULLET_RE = re.compile(r"^(\s*)([-*•]|\d+\.)\s+(.*)$")
_HR_RE = re.compile(r"^---+$")


def _strip_md_inline(text: str) -> str:
    t = _LINK_RE.sub(r"\1 (\2)", text)
    t = _BOLD_RE.sub(r"\1", t)
    t = _ITALIC_RE.sub(r"\1", t)
    return t.strip()


def _parse_blocks(markdown: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for raw in (markdown or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            blocks.append({"type": "blank"})
            continue
        if _HR_RE.match(line.strip()):
            blocks.append({"type": "hr"})
            continue
        hm = _HEADER_RE.match(line)
        if hm:
            level = len(hm.group(1))
            blocks.append({"type": "heading", "level": level, "text": _strip_md_inline(hm.group(2))})
            continue
        bm = _BULLET_RE.match(line)
        if bm:
            blocks.append(
                {
                    "type": "bullet",
                    "indent": len(bm.group(1) or ""),
                    "text": _strip_md_inline(bm.group(3)),
                }
            )
            continue
        blocks.append({"type": "para", "text": _strip_md_inline(line)})
    return blocks


def write_markdown_pdf(path: Path, markdown: str, *, doc_title: str = "") -> bool:
    """Render markdown to PDF with heading hierarchy, bullets, and spacing preserved."""
    if not (markdown or "").strip():
        return False
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = letter
    left, right = 54, width - 54
    max_width = right - left
    c = canvas.Canvas(str(path), pagesize=letter)
    if doc_title:
        c.setTitle(doc_title[:120])

    y = height - 54
    blocks = _parse_blocks(markdown)

    def new_page() -> None:
        nonlocal y
        c.showPage()
        y = height - 54

    def draw_wrapped(text: str, font: str, size: float, leading: float, indent: float = 0) -> None:
        nonlocal y
        c.setFont(font, size)
        words = (text or "").split()
        if not words:
            y -= leading
            return
        line = ""
        x = left + indent
        usable = max_width - indent
        for word in words:
            trial = f"{line} {word}".strip()
            if c.stringWidth(trial, font, size) <= usable:
                line = trial
            else:
                if y < 54:
                    new_page()
                    c.setFont(font, size)
                c.drawString(x, y, line)
                y -= leading
                line = word
        if line:
            if y < 54:
                new_page()
                c.setFont(font, size)
            c.drawString(x, y, line)
            y -= leading

    for block in blocks:
        kind = block["type"]
        if kind == "blank":
            y -= 8
            continue
        if kind == "hr":
            if y < 60:
                new_page()
            c.setStrokeColorRGB(0.55, 0.55, 0.55)
            c.setLineWidth(0.6)
            c.line(left, y + 4, right, y + 4)
            y -= 12
            continue
        if kind == "heading":
            level = int(block["level"])
            sizes = {1: 16, 2: 13, 3: 11}
            size = sizes.get(level, 11)
            y -= 6 if level == 1 else 4
            if y < 60:
                new_page()
            draw_wrapped(block["text"], "Helvetica-Bold", size, size + 4)
            y -= 2
            continue
        if kind == "bullet":
            indent = 14 + min(block.get("indent", 0), 24)
            bullet = "• "
            text = f"{bullet}{block['text']}"
            draw_wrapped(text, "Helvetica", 10, 13, indent=indent - 14)
            continue
        # paragraph — detect contact/header lines (no wrap preference for short lines)
        draw_wrapped(block["text"], "Helvetica", 10, 13)

    c.save()
    return path.exists() and path.stat().st_size > 0


def write_markdown_docx(path: Path, markdown: str, *, doc_title: str = "") -> bool:
    """ATS-friendly DOCX: sequential headings/paragraphs/bullets, no tables or text boxes."""
    if not (markdown or "").strip():
        return False
    try:
        from docx import Document
        from docx.enum.text import WD_LINE_SPACING
        from docx.shared import Pt
    except ImportError:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    if doc_title:
        core = doc.core_properties
        core.title = doc_title[:200]

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    pf = style.paragraph_format
    pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    for block in _parse_blocks(markdown):
        kind = block["type"]
        if kind == "blank":
            doc.add_paragraph("")
            continue
        if kind == "hr":
            doc.add_paragraph("—" * 24)
            continue
        if kind == "heading":
            level = min(int(block["level"]), 3)
            p = doc.add_heading(block["text"], level=level)
            for run in p.runs:
                run.font.name = "Calibri"
            continue
        if kind == "bullet":
            p = doc.add_paragraph(block["text"], style="List Bullet")
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(11)
            continue
        p = doc.add_paragraph(block["text"])
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)

    doc.save(str(path))
    return path.exists() and path.stat().st_size > 0


def write_ats_packet_documents(
    folder: Path,
    *,
    resume_markdown: str,
    cover_markdown: str,
    company: str = "",
    title: str = "",
) -> dict[str, Any]:
    """
    Write resume.md / cover_letter.md plus PDF and DOCX variants into folder.
    Prefer PDF for ATS upload; if PDF fails, DOCX is still produced and marked preferred.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    resume_md_path = folder / RESUME_MD
    cover_md_path = folder / COVER_MD
    resume_md_path.write_text(resume_markdown or "", encoding="utf-8")
    cover_md_path.write_text(cover_markdown or "", encoding="utf-8")

    resume_label = f"Resume — {title} @ {company}".strip(" —@")
    cover_label = f"Cover Letter — {title} @ {company}".strip(" —@")

    resume_pdf = folder / RESUME_PDF
    cover_pdf = folder / COVER_PDF
    resume_docx = folder / RESUME_DOCX
    cover_docx = folder / COVER_DOCX

    resume_pdf_ok = False
    cover_pdf_ok = False
    resume_docx_ok = False
    cover_docx_ok = False
    errors: list[str] = []

    try:
        resume_pdf_ok = write_markdown_pdf(resume_pdf, resume_markdown, doc_title=resume_label)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"resume_pdf: {exc}")
        resume_pdf_ok = False
    try:
        cover_pdf_ok = write_markdown_pdf(cover_pdf, cover_markdown, doc_title=cover_label)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"cover_pdf: {exc}")
        cover_pdf_ok = False

    try:
        resume_docx_ok = write_markdown_docx(resume_docx, resume_markdown, doc_title=resume_label)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"resume_docx: {exc}")
        resume_docx_ok = False
    try:
        cover_docx_ok = write_markdown_docx(cover_docx, cover_markdown, doc_title=cover_label)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"cover_docx: {exc}")
        cover_docx_ok = False

    # Prefer PDF; fall back to DOCX when PDF generation fails
    preferred_resume = RESUME_PDF if resume_pdf_ok else (RESUME_DOCX if resume_docx_ok else RESUME_MD)
    preferred_cover = COVER_PDF if cover_pdf_ok else (COVER_DOCX if cover_docx_ok else COVER_MD)

    paths = {
        "resume_md": str(resume_md_path),
        "cover_md": str(cover_md_path),
        "resume_pdf": str(resume_pdf) if resume_pdf_ok else None,
        "cover_pdf": str(cover_pdf) if cover_pdf_ok else None,
        "resume_docx": str(resume_docx) if resume_docx_ok else None,
        "cover_docx": str(cover_docx) if cover_docx_ok else None,
    }

    return {
        "folder": str(folder),
        "paths": paths,
        "files_written": [n for n in STANDARD_PACKET_FILES if (folder / n).exists()],
        "preferred_resume": preferred_resume,
        "preferred_cover": preferred_cover,
        "preferred_resume_path": str(folder / preferred_resume),
        "preferred_cover_path": str(folder / preferred_cover),
        "pdf_ok": resume_pdf_ok and cover_pdf_ok,
        "docx_ok": resume_docx_ok and cover_docx_ok,
        "fallback_used": (not resume_pdf_ok and resume_docx_ok) or (not cover_pdf_ok and cover_docx_ok),
        "errors": errors,
    }


def build_packet_zip(folder: Path, zip_path: Path | None = None) -> Path:
    """Zip ATS packet files for one-click download."""
    folder = Path(folder)
    zip_path = zip_path or (folder / "export_packet.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in STANDARD_PACKET_FILES:
            p = folder / name
            if p.exists():
                zf.write(p, arcname=name)
        meta = folder / "meta.json"
        if meta.exists():
            zf.write(meta, arcname="meta.json")
    return zip_path


def is_standard_packet_filename(name: str) -> bool:
    n = (name or "").lower().strip()
    return n in {x.lower() for x in STANDARD_PACKET_FILES} or n in {
        "export_packet.zip",
        "cover.md",
        "cover.pdf",
        "cover.docx",
    }
