# Airtable ↔ n8n Workflow Diagram

```mermaid
flowchart LR
  subgraph AT[Airtable GH-X MEO]
    P[Products queue and status fields]
    CQ[ContentQueue]
    CE[Content Engine video queue]
    S[Settings defaults]
    D[GHX Dashboard KPIs]
  end

  subgraph N8[n8n scheduled workflows]
    T[Schedule or Error Trigger]
    R[Search Airtable by status or view logic]
    C[Code build payload]
    AI[HTTP OpenAI / HeyGen / Etsy / Metricool / Drive]
    W[Update Airtable success or Error Log]
  end

  S -.->|defaults brand price limits| C
  T --> R
  P --> R
  CQ --> R
  CE --> R
  R --> C --> AI --> W
  W --> P
  W --> CQ
  W --> CE
  D -.->|manual or future rollups Needs Review| AT
```

## How it connects (definition-aligned)
1. **Products** holds the main product lifecycle states n8n searches/updates (Ready to Design, upload/publish fields, Error Log, asset URLs, Etsy IDs, social fields).
2. **ContentQueue** supports social scheduling packs (Ready for Metricool / Scheduled / Posted views).
3. **Content Engine** supports script → video_ready → Metricool views with HeyGen-oriented fields (`video_id`, `video_status`, `heygen_error`).
4. **Settings** supplies defaults (price, platforms, daily limits, brand voice) for generation workflows.
5. Native Airtable Automations were **not** used at inspection time — orchestration is external via n8n.

## Non-claims
This diagram reflects schema + known n8n definition patterns. It does **not** claim current successful execution volume.
