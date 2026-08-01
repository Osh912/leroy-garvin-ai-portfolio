# Missing Automation Opportunities

Observed: **no native Airtable Automations** configured. Opportunities (design suggestions only — not claims of existing builds):

1. **When Products enter “Ready to Design”** → notify or stamp Updated At / create checklist record.
2. **When Error Log is not empty** → create Needs Review view alert / Slack/email (if desired).
3. **When Content Engine Status = needs_fix** → assign Assignee + due date.
4. **Daily digest** from GHX Dashboard goals vs actual counts.
5. **When etsy_listing_id set** → set Publish Status=Live and clear publish queue flags.
6. **When video_status=completed** → move to Ready for Metricool view automatically.
7. **Settings-driven guards** — stop creation when daily_product_limit reached (n8n or Airtable).
8. **Form intake** — public/internal form for new product ideas into Products Ideas view (Forms currently empty).
9. **Interface for non-technical ops** — Interfaces hub empty; a simple ops dashboard interface could replace raw grid for QA.
10. **Record templates** for new Content Engine rows (hook/script/CTA structure).

Prefer implementing critical paths in **n8n** (already used for GH-X) and keep Airtable automations for lightweight notifications unless duplication is desired.
