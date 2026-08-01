# Schema Improvement Suggestions

1. **Normalize field naming** — choose Title Case or snake_case consistently (`Error Log` vs `heygen_error`).
2. **Explicit linked records** — ensure Content Engine ↔ Products uses a Linked record (not only URL), with reciprocal field.
3. **Single Status enum per table** — document allowed values; avoid parallel overlapping fields (`Status`, `Publish Status`, `qa_status`, `social_status`, `mockup_status`) without a state machine map.
4. **Split Products** if too wide — consider Assets table and Listings table to reduce mega-row complexity.
5. **Error taxonomy** — structured Error Code + Error Log instead of free text only.
6. **ContentQueue vs Content Engine overlap** — clarify ownership (social scheduling vs video engine) to prevent duplicate packs.
7. **Dashboard rollups** — replace manual KPI zeros with count formulas / synced rollups from views (if Airtable plan supports).
8. **Settings typing** — separate number vs text settings or use typed fields to avoid parsing errors in n8n.
9. **Assignee on Content Engine** — define if human QA ownership is required; add views by assignee.
10. **Attachments vs URLs** — standardize on URL fields for automation-friendliness, or document when Attachments are source of truth.
