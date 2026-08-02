#!/usr/bin/env python3
"""Generate recruiter-ready one/two-page resume PDF for Leroy Garvin Jr."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "resume" / "Leroy_Garvin_Jr_AI_Operations_Resume.pdf"
OUT_COPY = ROOT / "00 PUBLIC RECRUITER PORTFOLIO" / "01 Resume" / "Leroy_Garvin_Jr_AI_Operations_Resume.pdf"

INK = HexColor("#1c2420")
MUTED = HexColor("#4a524c")
ACCENT = HexColor("#3f5c48")
RULE = HexColor("#c9b896")


def styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "tagline": ParagraphStyle(
            "Tagline",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=11,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "job": ParagraphStyle(
            "Job",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.6,
            leading=11,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=0,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=7.8,
            leading=10,
            textColor=MUTED,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.5,
            textColor=INK,
        ),
        "proj": ParagraphStyle(
            "Proj",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.4,
            leading=10.5,
            textColor=INK,
            spaceBefore=3,
            spaceAfter=1,
        ),
    }


def bullets(items, s):
    return ListFlowable(
        [ListItem(Paragraph(i, s["bullet"]), leftIndent=8, bulletColor=ACCENT) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        bulletFontSize=7,
        spaceBefore=0,
        spaceAfter=2,
    )


def build():
    s = styles()
    story = []

    story.append(Paragraph("Leroy Garvin Jr.", s["name"]))
    story.append(Paragraph("AI Automation | AI Operations | Workflow Automation", s["tagline"]))
    story.append(
        Paragraph(
            "Savannah, Georgia, USA · Open to Remote<br/>"
            "(912) 901-6378 · AlignedVibesCo@gmail.com<br/>"
            "Portfolio: https://leroy-garvin-ai-portfolio.vercel.app · "
            "LinkedIn: linkedin.com/in/leroy-garvin-49443b423 · "
            "Etsy: alignedvibesco.etsy.com",
            s["contact"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=2, spaceAfter=4))

    story.append(Paragraph("PROFESSIONAL SUMMARY", s["h2"]))
    story.append(
        Paragraph(
            "Owner and AI Operations Specialist at Right Outside Auto Detailing LLC. Design, test, "
            "and document AI-assisted customer workflows and no-code automation with n8n and Airtable. "
            "Hands-on implementation across GH-X digital product automation (23 workflows / 8 stages), "
            "a 10-stage AI voice booking assistant, Harbor &amp; Home product packaging, and LawOne AI "
            "platform foundations (in development). Strong fit for AI Operations Specialist, Workflow "
            "Automation Specialist, AI Implementation Specialist, AI Support Specialist, Technical "
            "Support Specialist, Conversational AI QA, No-Code / Low-Code Automation Specialist, and "
            "Remote Operations Specialist roles.",
            s["body"],
        )
    )

    story.append(Paragraph("CORE SKILLS", s["h2"]))
    story.append(
        Paragraph(
            "AI Workflow Design · Prompt Engineering · Conversational AI Testing · AI Quality Assurance · "
            "Root Cause Analysis · Process Documentation · Workflow Automation · No-Code Automation "
            "(n8n, Airtable) · Business Rules Design · Troubleshooting · Continuous Improvement · "
            "Technical Documentation · Customer Operations · Independent Project Ownership",
            s["body"],
        )
    )

    story.append(Paragraph("PROFESSIONAL EXPERIENCE", s["h2"]))
    story.append(Paragraph("Owner &amp; AI Operations Specialist", s["job"]))
    story.append(
        Paragraph(
            "Right Outside Auto Detailing LLC — Savannah, Georgia, USA · Present · "
            "On-site/field operations with remote AI workflow design and testing",
            s["meta"],
        )
    )
    story.append(
        bullets(
            [
                "Own and operate the business: customer service, service coordination, and day-to-day operations.",
                "Design, test, and improve AI-assisted booking workflows for qualification, pricing confirmation, and appointment handling.",
                "Build and document no-code automation with n8n and Airtable to support operational consistency.",
                "Use ChatGPT and Claude to prototype workflows, refine prompts, and document processes.",
                "Run structured conversational testing: classify failures, perform root-cause analysis, fix, retest, and document.",
                "Troubleshoot process gaps and implement improvements that keep AI-assisted systems clearer and more reliable.",
            ],
            s,
        )
    )

    story.append(Paragraph("SELECTED PROJECTS", s["h2"]))

    blocks = [
        (
            "GH-X Automation System — Workflow Automation · AI Operations",
            [
                "Designed an 8-stage digital-product pipeline orchestrated in n8n with Airtable queues and status writebacks.",
                "Built 23 unique n8n workflow definitions spanning idea intake through draft publish, assets, and reliability stages.",
                "Supported Etsy draft listing creation and asset packaging; public storefront at alignedvibesco.etsy.com (sales volume not claimed).",
            ],
        ),
        (
            "AI Voice Booking Assistant — Conversational AI · Prompt Engineering · QA",
            [
                "Built a 10-stage booking flow: greeting, qualification, vehicle details, pricing, confirmations, address, appointment, and close.",
                "Enforced one-question-at-a-time behavior, stage control, and confirmation checkpoints through iterative prompt refinement.",
                "Applied structured QA (define expected behavior → test → classify → root cause → fix → retest → document).",
            ],
        ),
        (
            "Harbor &amp; Home Moving Binder — Product Ops · Marketplace Packaging",
            [
                "Packaged a 66-page relocation planner with mockups, Etsy listing creatives, and 8 marketing videos.",
                "Verified READY_TO_SELL checklist coverage for PDF, visuals, videos, and listing metadata ($14.99 listing package price).",
            ],
        ),
        (
            "LawOne AI — Platform Foundations (In Development)",
            [
                "Documented and built Next.js / TypeScript legal-information research UI foundations across phases A–H.",
                "Published labeled demonstration data and architecture evidence; not legal advice; not a finished commercial product; no live LLM/Auth claims.",
            ],
        ),
        (
            "n8n · Airtable · Technical Documentation &amp; QA",
            [
                "Inventoried orchestration patterns for queues, API calls, branching, and error handling across GH-X stages.",
                "Documented five Airtable operational tables for product queues, stage status, and QA visibility.",
                "Maintain acceptance criteria, failure classification, and retest loops for AI workflow reliability.",
            ],
        ),
    ]

    for title, items in blocks:
        story.append(KeepTogether([Paragraph(title, s["proj"]), bullets(items, s)]))

    story.append(Paragraph("TOOLS &amp; PLATFORMS", s["h2"]))
    story.append(
        Paragraph(
            "ChatGPT · Claude · n8n · Airtable · OpenAI · Etsy API · Twilio (documented scope) · Cursor · "
            "Prompt Engineering · Process Documentation · Next.js / TypeScript (LawOne)",
            s["body"],
        )
    )

    story.append(Paragraph("ADDITIONAL", s["h2"]))
    story.append(
        Paragraph(
            "Open to remote roles listed above. Strong documentation discipline and assessment-ready work samples. "
            "References available upon request. Education and certifications added only when verified.",
            s["body"],
        )
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title="Leroy Garvin Jr — AI Operations Resume",
        author="Leroy Garvin Jr",
    )
    doc.build(story)

    if OUT_COPY.parent.exists():
        OUT_COPY.write_bytes(OUT.read_bytes())

    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
