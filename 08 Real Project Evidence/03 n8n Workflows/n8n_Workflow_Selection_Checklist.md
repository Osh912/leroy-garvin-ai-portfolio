# n8n Workflow Selection Checklist

Score each workflow **1 (low) to 5 (high)** using the definition + available evidence. Do **not** score “Successful execution evidence” as 5 unless screenshots/logs exist.

## Scoring dimensions
| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| Business value | Unclear purpose | Clear internal ops value | Clear employer-relevant outcome |
| Technical complexity | 1–5 simple nodes | Branching/batching | Multi-integration advanced graph |
| AI integration | None | Prompt/Code only | OpenAI/HeyGen (or similar) in graph |
| Number of integrations | 1 | 2–3 | 4+ |
| Testing evidence | None | Notes only | Documented test cases + fixes |
| Successful execution evidence | None | Partial/unclear | Clear success execution screenshots |
| Originality | Template-like | Adapted | Distinct custom logic |
| Recruiter relevance | Weak | Moderate | Strong for target roles |
| Privacy safety | High risk secrets/PII | Needs redaction | Clean/sanitized |
| Ease of explanation | Hard | Moderate | Easy 60-second story |

## Scorecard (fill manually)

| Workflow | Biz | Tech | AI | Ints | Test | Exec | Orig | Recruiter | Privacy | Explain | Total | Include? |
|----------|-----|------|----|------|------|------|------|-----------|---------|---------|-------|---------|
| GHX-01-Idea-Intelligence |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-11-Winning-Idea-Loop |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-12-Content-Idea-Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-Generate-Product-Listing |  |  |  |  |  | 1 |  |  |  |  |  | |
| Design + Reel Prompt Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GH-X OpenAI Image Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-04-Mockup-Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-05-Social-Asset-Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-03B-Product-File-Uploader |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-06-Publish-Queue-Manager |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-03-Etsy-Metricool-Handoff |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-07-Etsy-Draft-Publisher |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-08-Metricool-Scheduler |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-14-Metricool-Content-Scheduler |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-09-Ready-To-Post-Queue |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-13-Video-Script-Builder |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-16-HeyGen-Video-Generator |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-17-HeyGen-Status-Poller |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-15-Content-QA |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-07-Performance-Tracker |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-10-Performance-Tracker |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-00-Error-Alerts |  |  |  |  |  | 1 |  |  |  |  |  | |
| GHX-09-Self-Healing-QA |  |  |  |  |  | 1 |  |  |  |  |  | |

**Note:** Execution column pre-filled as **1** because local execution history was empty at analysis time. Update only when you capture real execution screenshots.
