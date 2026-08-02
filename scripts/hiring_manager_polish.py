#!/usr/bin/env python3
"""Hiring Manager Mode: apply recruiter-focused copy updates across the site."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

AVAILABILITY = """
    <section class="section availability-band" id="availability" aria-labelledby="availability-heading">
      <div class="wrap">
        <p class="section-label">Availability</p>
        <h2 id="availability-heading">Available for Remote AI Operations, Automation, Technical Support, and AI Implementation roles</h2>
        <p class="lede avail-lede">Ready to help your team design, test, document, and improve AI-assisted workflows — without exaggerated engineering claims.</p>
        <div class="hero-ctas static-ctas">
          <a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>
          <a class="btn btn-secondary" href="tel:+19129016378">Call (912) 901-6378</a>
          <a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download>Download Resume</a>
        </div>
      </div>
    </section>
"""

HIRE_CTA = """
      <div class="hire-cta" role="complementary" aria-label="Contact to interview">
        <p><strong>Ready to interview?</strong> I am available for remote AI Operations, Automation, Technical Support, and AI Implementation roles.</p>
        <p class="hire-cta-actions">
          <a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>
          <a class="btn btn-secondary" href="/contact.html">Contact details</a>
          <a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download>Download Resume</a>
        </p>
      </div>
"""

NAV_BTN_OLD = '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
NAV_BTN_NEW = '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">Menu</button>'

# Project page case-block replacements: (filename, lede, case_html_inner)
PROJECTS = {
    "ghx.html": {
        "lede": "I automated the handoff from product idea to listing-ready package so digital products can move through production with clearer stages and fewer skipped steps.",
        "case": """
        <h2>Problem solved</h2>
        <p>Manual digital-product handoffs (idea → listing → images → publish → social → measurement) were inconsistent and easy to skip.</p>
        <h2>What I built</h2>
        <p>An 8-stage operations pipeline in n8n + Airtable that moves work through queues, creates draft Etsy listing packages, and tracks status for the next stage.</p>
        <h2>Technologies used</h2>
        <p>n8n, Airtable, OpenAI, Etsy API, Google Drive, HeyGen, Metricool.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get someone who can turn messy multi-tool product ops into a documented, testable automation system — and ship real sell packages, not just diagrams.</p>
        <h2>Verified outcome</h2>
        <p>23 workflow definitions across 8 stages. Produced Harbor &amp; Home READY_TO_SELL packages (66-page PDF, creatives, 8 videos). Live storefront: <a href="https://alignedvibesco.etsy.com" rel="noopener noreferrer" target="_blank">alignedvibesco.etsy.com</a>. Sales volume is not claimed.</p>
        <h2>Pipeline overview</h2>
        <p class="diagram-note">Architecture diagram — not a live n8n canvas screenshot.</p>
""",
        "evidence_intro": '<div class="prose"><h2>Customer-ready product evidence</h2><p>Harbor &amp; Home outputs from the pipeline. <a href="https://alignedvibesco.etsy.com" rel="noopener noreferrer" target="_blank">View Live Etsy Shop</a>.</p></div>',
    },
    "voice.html": {
        "lede": "I designed a controlled AI booking conversation so a real service business can collect the right details, confirm pricing, and book appointments more reliably.",
        "case": """
        <h2>Problem solved</h2>
        <p>Missed or unstructured calls left incomplete customer data, unclear service requests, pricing confusion, and unreliable appointment confirmation.</p>
        <h2>What I built</h2>
        <p>A 10-stage booking flow with one-question-at-a-time control, pricing confirmation checkpoints, address collection, appointment options, and a professional close.</p>
        <h2>Technologies used</h2>
        <p>Prompt engineering, conversational QA, business rules, ChatGPT; n8n / Airtable / Twilio in documented project scope.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get hands-on conversational AI operations: define expected behavior, catch failure patterns, fix prompts/rules, retest, and document — the same loop production AI teams need.</p>
        <h2>Verified outcome</h2>
        <p>Documented 10-stage Functional Build with published sanitized docs. Addressed 5+ failure classes in testing (loops, repeated questions, order errors, pricing gaps, address handling). No call-volume metrics claimed.</p>
        <h2>Workflow diagram</h2>
        <p class="diagram-note">Architecture diagram of booking stages — not a live telephony UI screenshot.</p>
""",
    },
    "harbor.html": {
        "lede": "I packaged a complete marketplace-ready moving planner so a digital product could go from build to READY_TO_SELL with listing assets and campaign videos included.",
        "case": """
        <h2>Problem solved</h2>
        <p>A PDF alone is not enough to list. Marketplace work needs a complete sell package: product file, visuals, copy readiness, and campaign assets.</p>
        <h2>What I built</h2>
        <p>Harbor &amp; Home Moving Binder: 66-page PDF, mockups, Etsy listing creatives, listing metadata, and 8 short marketing videos — verified READY_TO_SELL.</p>
        <h2>Technologies used</h2>
        <p>GH-X product pipeline, listing creative production, READY_TO_SELL ops checklist.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get an operator who finishes the last mile: packaging, verification, and publish readiness — not just unfinished drafts.</p>
        <h2>Verified outcome</h2>
        <p>66 verified PDF pages · $14.99 listing package price · 8 videos · 13 Etsy tags prepared · live shop at <a href="https://alignedvibesco.etsy.com" rel="noopener noreferrer" target="_blank">alignedvibesco.etsy.com</a>. Sales volume is not claimed.</p>
""",
    },
    "lawone.html": {
        "lede": "I built the foundation of a legal-information research platform so users can organize jurisdictions and search with clear source labeling — not legal advice, and not a finished commercial product yet.",
        "case": """
        <h2>Problem solved</h2>
        <p>Legal research materials are fragmented across jurisdictions. Teams need organized search with honest source labeling.</p>
        <h2>What I built</h2>
        <p>A Next.js platform foundation with research UI, search filters, change-monitoring UI, assistant scaffolding, and a national catalog framework — with demonstration data labeled in-product.</p>
        <h2>Technologies used</h2>
        <p>Next.js, TypeScript, Tailwind, Vitest, Supabase schema foundations.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get someone who can document and ship product foundations carefully — with clear disclaimers, labeled demo data, and no over-claims about live LLM or Auth.</p>
        <h2>Verified outcome</h2>
        <p>Phases A–H documented. 6 UI screenshots published. Explicit constraints: no live LLM, no live Auth/Stripe in public claims; catalog ≠ ingested law. Status: in development — not a finished commercial product.</p>
""",
    },
    "n8n.html": {
        "lede": "I designed n8n orchestration so multi-step product work can run through validation, API calls, branching, and status updates with clearer failure handling.",
        "case": """
        <h2>Problem solved</h2>
        <p>Multi-step product operations break when queues, APIs, and failure paths are not orchestrated consistently.</p>
        <h2>What I built</h2>
        <p>Stage workflows that validate queue items, call APIs or AI steps when needed, branch on quality/status, write results to Airtable, and support reliability/requeue patterns.</p>
        <h2>Technologies used</h2>
        <p>n8n (Schedule, Error, Code, IF/Switch, Split In Batches, HTTP), Airtable, OpenAI / Etsy / HeyGen / Metricool / Drive where defined.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get a no-code automation specialist who thinks in queues, edge cases, and recovery — not only happy-path demos.</p>
        <h2>Verified outcome</h2>
        <p>23 unique workflow definitions inventoried across 8 stages. Public visuals are architecture diagrams — not live canvas captures with credentials.</p>
""",
    },
    "airtable.html": {
        "lede": "I designed the Airtable backbone so automation stages share one source of truth for queues, status, and QA notes.",
        "case": """
        <h2>Problem solved</h2>
        <p>Automation stages need a shared view of what is queued, in progress, blocked, or ready to publish.</p>
        <h2>What I built</h2>
        <p>Airtable structures for Products, ContentQueue, Settings, Content Engine, and GHX Dashboard so n8n can read/write status and capture QA notes.</p>
        <h2>Technologies used</h2>
        <p>Airtable + n8n Airtable nodes across GH-X definitions.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get operational data design that makes automation visible and reviewable — critical for AI Ops and support teams.</p>
        <h2>Verified outcome</h2>
        <p>5 tables documented publicly via architecture diagrams. Private base IDs and identifiable live records are withheld.</p>
""",
    },
    "qa.html": {
        "lede": "I built a repeatable QA loop so AI workflows get tested, failures get classified, and fixes stick through retest and documentation.",
        "case": """
        <h2>Problem solved</h2>
        <p>AI workflows fail quietly unless expected behavior is defined and failures are classified.</p>
        <h2>What I built</h2>
        <p>A 7-step loop: define expected behavior → test → classify → root cause → fix → retest → document. Applied to voice booking and GH-X reliability work.</p>
        <h2>Technologies used</h2>
        <p>Structured test notes, case-study documentation, prompt and process revision.</p>
        <h2>Why this matters to an employer</h2>
        <p>You get AI support / QA discipline that protects customer experience and reduces repeat defects — without inventing production volume metrics.</p>
        <h2>Verified outcome</h2>
        <p>Published sanitized testing docs. Methodology used across voice (5+ failure classes), GH-X reliability thinking, and Airtable QA notes.</p>
""",
    },
}


def replace_between(text: str, start: str, end: str, new_middle: str) -> str:
    i = text.find(start)
    j = text.find(end, i + len(start) if i != -1 else 0)
    if i == -1 or j == -1:
        raise ValueError(f"markers not found: {start!r} ... {end!r}")
    return text[: i + len(start)] + new_middle + text[j:]


def add_hire_cta(html: str) -> str:
    if 'class="hire-cta"' in html:
        return html
    # insert before closing of main's last section or before </main>
    marker = "    </section>\n  </main>"
    if marker in html:
        return html.replace(marker, "      " + HIRE_CTA.strip() + "\n    </section>\n  </main>", 1)
    # projects pages often end section then main
    marker2 = "    </div></section>\n  </main>"
    if marker2 in html:
        return html.replace(
            marker2,
            "      " + HIRE_CTA.strip() + "\n    </div></section>\n  </main>",
            1,
        )
    return html


def patch_project(name: str, meta: dict) -> None:
    path = SITE / "projects" / name
    text = path.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)

    # lede
    import re

    text = re.sub(
        r'(<h1>[^<]+</h1>\n\s*<p class="lede">)(.*?)(</p>)',
        r"\1" + meta["lede"] + r"\3",
        text,
        count=1,
        flags=re.S,
    )

    # case block content between <div class="prose case-block"> and closing before diagram or gallery
    start = '<div class="prose case-block">'
    # end at first diagram-frame or gallery after case-block
    i = text.find(start)
    if i == -1:
        raise SystemExit(f"no case-block in {name}")
    # find end of case-block div - it's closed before diagram-frame or gallery
    rest = text[i:]
    # Match until </div> that closes case-block - look for pattern after verified/diagram note
    end_markers = [
        "\n      </div>\n      <div class=\"diagram-frame\">",
        "\n      </div>\n      <div class=\"gallery",
        "\n      </div>\n      <div class=\"prose\">",
    ]
    end_rel = None
    for em in end_markers:
        pos = rest.find(em)
        if pos != -1 and (end_rel is None or pos < end_rel):
            end_rel = pos
    if end_rel is None:
        raise SystemExit(f"no case end in {name}")
    new_block = start + "\n" + meta["case"].rstrip() + "\n      "
    text = text[:i] + new_block + rest[end_rel + len("\n      ") :]

    if "evidence_intro" in meta and "Customer-ready product evidence" in text:
        text = re.sub(
            r'<div class="prose"><h2>Customer-ready product evidence</h2>.*?</div>',
            meta["evidence_intro"],
            text,
            count=1,
            flags=re.S,
        )

    # Update bottom nav links area to include hire CTA before it
    text = add_hire_cta(text)

    # Prefer contact CTAs on bottom project links line
    text = re.sub(
        r'(<div class="prose"><p><a href="/projects/">← All projects</a>.*?</p></div>)',
        r"\1",
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8")
    print("updated", name)


def write_index():
    path = SITE / "index.html"
    # Full rewrite of main content while keeping head/nav/footer structure
    text = path.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)
    text = text.replace(
        'content="AI Operations specialist portfolio: GH-X automation, voice booking QA, n8n, Airtable, Harbor product ops, and LawOne AI. Remote-ready implementation evidence."',
        'content="Hire Leroy Garvin Jr for remote AI Operations, workflow automation, technical support, and AI implementation. Evidence-backed projects with n8n, Airtable, and conversational AI QA."',
    )

    main = '''  <main id="main">
    <section class="home-hero" aria-label="Introduction">
      <div class="wrap">
        <h1 class="hero-brand">
          Leroy Garvin Jr
          <span class="role-line">AI Automation | AI Operations | Workflow Automation</span>
        </h1>
        <p class="hero-headline">I help companies design, test, and run AI-assisted business workflows.</p>
        <p class="hero-support">I turn messy operational processes into clear stages, prompts, automations, and QA loops — so booking, product ops, and support work become more reliable. Built and documented on real business systems, not theory.</p>
        <div class="role-fit" aria-label="Target roles">
          <span>AI Operations Specialist</span>
          <span>Workflow Automation</span>
          <span>AI Implementation</span>
          <span>AI Support</span>
          <span>Technical Support</span>
          <span>Conversational AI QA</span>
          <span>No-Code / Low-Code Automation</span>
          <span>Remote Operations</span>
        </div>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>
          <a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download>Download Resume</a>
          <a class="btn btn-secondary" href="/projects/">View Projects</a>
          <a class="btn btn-secondary" href="/contact.html">Contact Details</a>
        </div>
        <div class="contact-bar">
          <span>Savannah, Georgia · Open to Remote</span>
          <a href="mailto:AlignedVibesCo@gmail.com">AlignedVibesCo@gmail.com</a>
          <a href="tel:+19129016378">(912) 901-6378</a>
          <a href="https://www.linkedin.com/in/leroy-garvin-49443b423/" rel="noopener noreferrer" target="_blank">LinkedIn</a>
        </div>
      </div>
    </section>
''' + AVAILABILITY + '''
    <section class="section" aria-labelledby="results-heading">
      <div class="wrap">
        <p class="section-label">Selected results</p>
        <h2 id="results-heading">What you can verify in this portfolio</h2>
        <p class="lede" style="max-width:40rem">Truthful metrics only — no invented revenue, headcount, or unverified scale.</p>
        <div class="results-grid">
          <div class="metric"><div class="metric-value">23</div><div class="metric-label">Automation workflows designed</div></div>
          <div class="metric"><div class="metric-value">10</div><div class="metric-label">Stage AI booking flow</div></div>
          <div class="metric"><div class="metric-value">66</div><div class="metric-label">Page marketplace product package</div></div>
          <div class="metric"><div class="metric-value">8</div><div class="metric-label">Marketing videos packaged</div></div>
          <div class="metric"><div class="metric-value">5</div><div class="metric-label">Airtable ops tables documented</div></div>
          <div class="metric"><div class="metric-value">5+</div><div class="metric-label">Voice failure classes addressed</div></div>
          <div class="metric"><div class="metric-value">Live</div><div class="metric-label">Etsy shop + portfolio online</div></div>
        </div>
      </div>
    </section>

    <section class="section" id="live-work" aria-labelledby="live-work-heading">
      <div class="wrap">
        <p class="section-label">Live work</p>
        <h2 id="live-work-heading">Live Work</h2>
        <p class="lede" style="max-width:40rem">Open these now to see shipping evidence — not slideware.</p>
        <div class="live-work-grid">
          <a class="live-work-card" href="/projects/ghx.html">
            <h3>GH-X Automation System</h3>
            <p>Cut manual product handoffs with a 23-workflow, 8-stage pipeline.</p>
            <span class="card-link">See business impact →</span>
          </a>
          <a class="live-work-card" href="/projects/harbor.html">
            <h3>Harbor &amp; Home Moving Binder</h3>
            <p>66-page READY_TO_SELL package with creatives and 8 videos.</p>
            <span class="card-link">See product package →</span>
          </a>
          <a class="live-work-card" href="https://alignedvibesco.etsy.com" rel="noopener noreferrer" target="_blank">
            <h3>Aligned Vibes Co Etsy Shop</h3>
            <p>Public storefront for published digital products.</p>
            <span class="card-link">See Live Store ↗</span>
          </a>
          <a class="live-work-card" href="/projects/lawone.html">
            <h3>LawOne AI</h3>
            <p>In development — documented platform foundation, not a finished commercial product.</p>
            <span class="card-link">See build status →</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section featured-strip" id="featured" aria-labelledby="featured-heading">
      <div class="wrap">
        <p class="section-label">Featured work</p>
        <h2 id="featured-heading">Projects that show how I help a team</h2>
        <div class="project-grid">
          <a class="project-card" href="/projects/ghx.html">
            <div class="badge-row"><span class="badge">Functional Build</span></div>
            <h3>GH-X Automation System</h3>
            <p>Reduced skipped product-ops steps by automating idea → listing packages across 8 stages.</p>
            <p class="card-metric">23 workflows · marketplace-ready outputs</p>
            <ul class="tech-tags"><li>n8n</li><li>Airtable</li><li>OpenAI</li><li>Etsy API</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/voice.html">
            <div class="badge-row"><span class="badge">Functional Build</span></div>
            <h3>AI Voice Booking Assistant</h3>
            <p>Made booking conversations collect complete details and confirm pricing before appointments.</p>
            <p class="card-metric">10 stages · 5+ failure classes fixed in QA</p>
            <ul class="tech-tags"><li>Prompt engineering</li><li>Conversational QA</li><li>Business rules</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/harbor.html">
            <div class="badge-row"><span class="badge">Featured product</span></div>
            <h3>Harbor &amp; Home Moving Binder</h3>
            <p>Delivered a complete sell package so a digital product was listing-ready, not half-finished.</p>
            <p class="card-metric">66 pages · 8 videos · live Etsy shop</p>
            <ul class="tech-tags"><li>Product packaging</li><li>Listing creatives</li><li>Ops checklist</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/lawone.html">
            <div class="badge-row"><span class="badge">In development</span></div>
            <h3>LawOne AI</h3>
            <p>Organized legal-information research into a documented platform foundation with labeled demo data.</p>
            <p class="card-metric">Phases A–H · honest build status</p>
            <ul class="tech-tags"><li>Next.js</li><li>TypeScript</li><li>Research UI</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/n8n.html">
            <div class="badge-row"><span class="badge">Functional Build</span></div>
            <h3>n8n Workflow Automation</h3>
            <p>Connected queues, APIs, and error paths so multi-step work recovers instead of silently failing.</p>
            <p class="card-metric">23 workflows inventoried</p>
            <ul class="tech-tags"><li>n8n</li><li>HTTP APIs</li><li>Error branches</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/airtable.html">
            <div class="badge-row"><span class="badge">Functional Build</span></div>
            <h3>Airtable Systems</h3>
            <p>Gave automation a shared status board so teams can see queued, blocked, and ready work.</p>
            <p class="card-metric">5 documented tables</p>
            <ul class="tech-tags"><li>Airtable</li><li>Queues</li><li>Status fields</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
          <a class="project-card" href="/projects/qa.html">
            <div class="badge-row"><span class="badge">Methodology</span></div>
            <h3>Technical Documentation &amp; QA</h3>
            <p>Installed a retest loop so AI workflow defects get classified, fixed, and documented.</p>
            <p class="card-metric">7-step QA loop · published evidence</p>
            <ul class="tech-tags"><li>QA</li><li>Documentation</li><li>Root cause</li></ul>
            <span class="card-link">See how it helps employers →</span>
          </a>
        </div>
        <p class="meta-line" style="margin-top:1.75rem">Red Flag Diaries and ServiceFlowAI are excluded from this public site. See <a href="/legal.html">usage notice</a>.</p>
        ''' + HIRE_CTA + '''
      </div>
    </section>
  </main>
'''
    import re
    text = re.sub(r"  <main id=\"main\">.*?</main>", main.rstrip(), text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")
    print("updated index.html")


def write_projects_index():
    path = SITE / "projects" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)
    text = text.replace(
        "<h1>Case studies with published evidence</h1>\n      <p class=\"lede\">Concise recruiter views: problem, solution, role, tools, challenges, improvements, and verified outcomes. Diagrams are labeled as architecture — not production screenshots.</p>",
        "<h1>Work that shows business impact</h1>\n      <p class=\"lede\">Each case study answers: what problem was solved, what tools were used, and why it matters to an employer. Diagrams are architecture views — not production screenshots with secrets.</p>",
    )
    cards = """      <div class="project-grid">
        <a class="project-card" href="/projects/ghx.html"><div class="badge-row"><span class="badge">Functional Build</span></div><h3>GH-X Automation System</h3><p>Reduced skipped product-ops steps by automating idea → listing packages across 8 stages.</p><p class="card-metric">23 workflows · marketplace-ready outputs</p><ul class="tech-tags"><li>n8n</li><li>Airtable</li><li>OpenAI</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/voice.html"><div class="badge-row"><span class="badge">Functional Build</span></div><h3>AI Voice Booking Assistant</h3><p>Made booking conversations collect complete details and confirm pricing before appointments.</p><p class="card-metric">10 stages · 5+ failure classes fixed in QA</p><ul class="tech-tags"><li>Prompts</li><li>QA</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/harbor.html"><div class="badge-row"><span class="badge">Featured product</span></div><h3>Harbor &amp; Home Moving Binder</h3><p>Delivered a complete sell package so a digital product was listing-ready, not half-finished.</p><p class="card-metric">66 pages · 8 videos · live Etsy shop</p><ul class="tech-tags"><li>Product package</li><li>Listing creatives</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/lawone.html"><div class="badge-row"><span class="badge">In development</span></div><h3>LawOne AI</h3><p>Organized legal-information research into a documented platform foundation with labeled demo data.</p><p class="card-metric">Phases A–H · honest build status</p><ul class="tech-tags"><li>Next.js</li><li>Search UI</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/n8n.html"><div class="badge-row"><span class="badge">Functional Build</span></div><h3>n8n Workflow Automation</h3><p>Connected queues, APIs, and error paths so multi-step work recovers instead of silently failing.</p><p class="card-metric">23 workflows inventoried</p><ul class="tech-tags"><li>n8n</li><li>APIs</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/airtable.html"><div class="badge-row"><span class="badge">Functional Build</span></div><h3>Airtable Systems</h3><p>Gave automation a shared status board so teams can see queued, blocked, and ready work.</p><p class="card-metric">5 documented tables</p><ul class="tech-tags"><li>Airtable</li></ul><span class="card-link">See how it helps employers →</span></a>
        <a class="project-card" href="/projects/qa.html"><div class="badge-row"><span class="badge">Methodology</span></div><h3>Technical Documentation &amp; QA</h3><p>Installed a retest loop so AI workflow defects get classified, fixed, and documented.</p><p class="card-metric">7-step QA loop · published evidence</p><ul class="tech-tags"><li>QA docs</li></ul><span class="card-link">See how it helps employers →</span></a>
      </div>
"""
    import re
    text = re.sub(r'<div class="project-grid">.*?</div>\n      <div class="notice-box"', cards.rstrip() + '\n      <div class="notice-box"', text, count=1, flags=re.S)
    text = add_hire_cta(text)
    path.write_text(text, encoding="utf-8")
    print("updated projects/index.html")


def write_resume():
    path = SITE / "resume.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)
    main = '''  <main id="main">
    <div class="wrap page-hero">
      <p class="section-label">Resume</p>
      <h1>Leroy Garvin Jr</h1>
      <p class="lede">AI Automation | AI Operations | Workflow Automation</p>
      <p class="lede" style="margin-top:0.5rem">I help companies design, test, and run AI-assisted business workflows.</p>
    </div>
''' + AVAILABILITY + '''
    <section class="section" style="padding-top:0"><div class="wrap">
      <div class="resume-actions">
        <a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>
        <a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download>Download PDF resume</a>
        <a class="btn btn-secondary" href="/contact.html">Contact details</a>
        <a class="btn btn-secondary" href="https://www.linkedin.com/in/leroy-garvin-49443b423/" rel="noopener noreferrer" target="_blank">LinkedIn</a>
      </div>
      <article class="resume-block">
        <p class="resume-name">Leroy Garvin Jr</p>
        <p class="job-meta">AI Automation | AI Operations | Workflow Automation<br>
          Savannah, Georgia, USA · Open to Remote<br>
          <a href="tel:+19129016378">(912) 901-6378</a> ·
          <a href="mailto:AlignedVibesCo@gmail.com">AlignedVibesCo@gmail.com</a> ·
          <a href="https://www.linkedin.com/in/leroy-garvin-49443b423/" rel="noopener noreferrer" target="_blank">LinkedIn</a> ·
          <a href="https://leroy-garvin-ai-portfolio.vercel.app/">Portfolio</a> ·
          <a href="https://alignedvibesco.etsy.com" rel="noopener noreferrer" target="_blank">Etsy Shop</a>
        </p>
        <h2>Professional summary</h2>
        <p>Owner and AI Operations Specialist at Right Outside Auto Detailing LLC. I design, test, and document AI-assisted workflows and no-code automation with n8n and Airtable. Proven delivery across GH-X (23 workflows / 8 stages), a 10-stage voice booking assistant, Harbor &amp; Home product packaging (66 pages, 8 videos), and LawOne AI foundations (in development). Available for remote AI Operations, Automation, Technical Support, and AI Implementation roles.</p>
        <h2>Core skills</h2>
        <ul class="skills-list">
          <li>AI Workflow Design</li><li>Prompt Engineering</li><li>Conversational AI Testing</li><li>AI Quality Assurance</li>
          <li>Root Cause Analysis</li><li>Process Documentation</li><li>Workflow Automation</li><li>No-Code (n8n, Airtable)</li>
          <li>Business Rules Design</li><li>Continuous Improvement</li><li>Technical Support</li><li>Remote Operations</li>
          <li>AI Evaluation</li><li>Implementation</li><li>Troubleshooting</li>
        </ul>
        <h2>Professional experience</h2>
        <h3>Owner &amp; AI Operations Specialist</h3>
        <p class="job-meta">Right Outside Auto Detailing LLC — Savannah, Georgia, USA<br>Present · On-site/field operations with remote AI workflow design and testing</p>
        <ul>
          <li>Own and operate the business: customer service, service coordination, and day-to-day operations.</li>
          <li>Design, test, and improve AI-assisted booking workflows for qualification, pricing confirmation, and appointment handling.</li>
          <li>Build and document no-code automation with n8n and Airtable for operational consistency.</li>
          <li>Use ChatGPT and Claude to prototype workflows, refine prompts, and document processes.</li>
          <li>Run structured conversational testing: classify failures, root-cause, fix, retest, and document.</li>
        </ul>
        <h2>Selected projects</h2>
        <h3>GH-X Automation System</h3>
        <ul>
          <li>Designed 23 n8n workflows across 8 stages to reduce skipped product-ops handoffs.</li>
          <li>Produced marketplace-ready packages such as Harbor &amp; Home (66-page READY_TO_SELL pack).</li>
        </ul>
        <h3>AI Voice Booking Assistant</h3>
        <ul>
          <li>Built a 10-stage booking flow that collects complete details and confirms pricing before booking.</li>
          <li>Addressed 5+ failure classes in iterative QA (qualitative; no call-volume metrics claimed).</li>
        </ul>
        <h3>Harbor &amp; Home Moving Binder</h3>
        <ul>
          <li>Packaged a 66-page relocation planner with listing creatives and 8 marketing videos.</li>
          <li>Live storefront: alignedvibesco.etsy.com (sales volume not claimed).</li>
        </ul>
        <h3>LawOne AI</h3>
        <ul>
          <li>Next.js legal-information platform foundations; phases A–H documented; not legal advice; not a finished commercial product.</li>
        </ul>
        <h3>n8n · Airtable · QA</h3>
        <ul>
          <li>Inventoried orchestration and error-handling patterns; documented 5 Airtable ops tables; published a 7-step QA loop.</li>
        </ul>
        <h2>Tools</h2>
        <p>ChatGPT · Claude · n8n · Airtable · OpenAI · Etsy API · Twilio (documented scope) · Cursor · Prompt engineering · Process documentation · Next.js/TypeScript (LawOne)</p>
      </article>
      ''' + HIRE_CTA + '''
    </div></section>
  </main>
'''
    import re
    text = re.sub(r"  <main id=\"main\">.*?</main>", main.rstrip(), text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")
    print("updated resume.html")


def write_about_contact():
    about = SITE / "about.html"
    text = about.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)
    text = text.replace(
        "<h1>AI Operations with business implementation experience</h1>\n      <p class=\"lede\">Owner &amp; AI Operations Specialist at Right Outside Auto Detailing LLC. I design, test, and document AI-assisted workflows for booking, product ops, and platform foundations.</p>",
        "<h1>I help teams make AI workflows reliable in real operations</h1>\n      <p class=\"lede\">Owner &amp; AI Operations Specialist at Right Outside Auto Detailing LLC. I design, test, and document AI-assisted workflows for booking, product ops, and platform foundations — then prove the work with evidence.</p>",
    )
    # insert availability after page-hero
    if 'id="availability"' not in text:
        text = text.replace(
            "    </div>\n    <section class=\"section\"><div class=\"wrap prose case-block\">",
            "    </div>\n" + AVAILABILITY + "\n    <section class=\"section\" style=\"padding-top:0\"><div class=\"wrap prose case-block\">",
            1,
        )
    text = text.replace(
        '<a class="btn btn-primary" href="/contact.html">Contact</a>',
        '<a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>',
    )
    text = text.replace(
        '<a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download style="margin-left:0.5rem">Download resume</a>',
        '<a class="btn btn-secondary" href="/contact.html" style="margin-left:0.5rem">Contact details</a>\n        <a class="btn btn-secondary" href="/assets/resume/Leroy_Garvin_Jr_AI_Operations_Resume.pdf" download style="margin-left:0.5rem">Download resume</a>',
    )
    about.write_text(text, encoding="utf-8")
    print("updated about.html")

    contact = SITE / "contact.html"
    text = contact.read_text(encoding="utf-8")
    text = text.replace(NAV_BTN_OLD, NAV_BTN_NEW)
    text = text.replace(
        "<h1>Let’s talk about AI Operations roles</h1>\n      <p class=\"lede\">Open to remote AI Operations Specialist, Workflow Automation, AI Implementation, AI Support, Technical Support, Prompt &amp; Conversational QA, No-Code Automation, and Remote Operations roles.</p>",
        "<h1>Contact Leroy to schedule an interview</h1>\n      <p class=\"lede\">Available for Remote AI Operations, Automation, Technical Support, and AI Implementation roles. Email is the fastest way to start the conversation.</p>",
    )
    if 'id="availability"' not in text:
        text = text.replace(
            "    </div>\n    <section class=\"section\" style=\"padding-top:0\"><div class=\"wrap prose\">",
            "    </div>\n" + AVAILABILITY + "\n    <section class=\"section\" style=\"padding-top:0\"><div class=\"wrap prose\">",
            1,
        )
    text = text.replace(
        '<a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email me</a>',
        '<a class="btn btn-primary" href="mailto:AlignedVibesCo@gmail.com">Email Leroy to Interview</a>',
    )
    contact.write_text(text, encoding="utf-8")
    print("updated contact.html")


def patch_remaining_nav():
    for path in SITE.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if NAV_BTN_OLD in text:
            path.write_text(text.replace(NAV_BTN_OLD, NAV_BTN_NEW), encoding="utf-8")
            print("aria-label menu:", path.name)


def main():
    write_index()
    write_projects_index()
    write_resume()
    write_about_contact()
    for name, meta in PROJECTS.items():
        patch_project(name, meta)
    patch_remaining_nav()
    print("done")


if __name__ == "__main__":
    main()
