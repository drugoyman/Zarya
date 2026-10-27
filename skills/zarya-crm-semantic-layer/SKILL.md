---
name: zarya-crm-semantic-layer
description: Use for the user-owned legal company project ЮК Заря (Zarya), CRM database sitemanager (Озеро; also called sitemanage), Пульс / Zarya Pulse, business-process analysis and CRM reports. Read-only database use, verified field mappings and explicit measurement caveats.
---

# Zarya CRM semantic layer

## Mango: two distinct databases

- Do not conflate `zarya_mango_new` (separate Mango database, including `public.summary`, `calls_state`, `early_statistics`, `full_statistics`) with the user's nightly analytics collection.
- «Наша база Mango, которая собирается ночью» means PostgreSQL `<SERVICE_HOST>`, database `skorozvon`, schema `mango`. Main tables: `calls`, `call_base_stats`, `etl_runs`, `users`, `lines`, `groups`, `trunk_numbers`. This identity was live-verified on 2026-10-13. Verify current database/schema and collection freshness before comparisons.
- Nightly collector: `/opt/mango-monitor`, systemd `mango-etl.timer` / `mango-etl.service`; local source `<LOCAL_WORKSPACE>`. Configured schedule: 03:15 Europe/Moscow with up to five minutes randomized delay; verify runtime schedule rather than assuming it remains unchanged.
- Check `mango.calls.raw_payload` and nested `context_calls` before asserting that a field is missing. A bounded 2026-10-13 sample contained per-part `call_end_reason`, `dial_duration`, `talk_duration`, start/answer/end times, `call_id`, `communication_id`, `external_call_id`, `members`, and transfer flags; top-level `recall_status` was also present. `hold_duration` existed but was null throughout the inspected sample. Key presence does not establish completeness or semantics; null is not zero.
- Compare cabinet HAR fields to this nightly database when requested, not to `zarya_mango_new`. Distinguish missing columns from data already stored in JSON, and call parts from unique calls/leads. Do not assume Mango completion codes are raw SIP codes or that a line number proves the final caller ID displayed to the client.
- Analyses remain read-only. Explicitly requested collector enhancements target the confirmed analytics database only; they do not authorize changes to `zarya_mango_new` or source CRM «Озеро». This skill stores no passwords, session cookies, or API tokens.

## Project identity and mandatory database boundary

- This is the user's project: юридическая компания «Заря», ЮК Заря / Zarya. CRM database `sitemanager`, called «Озеро» by the user (also written `sitemanage`) and «Пульс» / Zarya Pulse belong to this project. Apply this context to business processes, CRM reporting and analytics for these names.
- All use of the source CRM database is strictly READ ONLY: inspect existing data, schema and metadata only. An analytical or business-process request never authorizes database changes.
- The established MySQL endpoint `<SERVICE_HOST>`, account `<CRM_READONLY_USER>`, is strictly read only. Verify the selected database and available schema before querying; do not infer complete production coverage from the replica.
- Never INSERT, UPDATE, DELETE, REPLACE, perform DDL, execute mutating procedures, or change accounts, permissions, configuration or server settings. Do not change CRM records, robots or business processes through an API or UI as a workaround.
- Use bounded parameterized SELECT queries in an explicitly read-only transaction. Do not create temporary tables or invoke functions with side effects. Retrieve credentials only from an existing approved secret source; never print or save them in skill files, memory or reports.
- Business-process formulas and full replication coverage remain unverified. Propose changes in a separate artifact; do not execute them against the CRM. Existing field names and report code do not prove the true business definition.
Read [references/semantic-layer.md](references/semantic-layer.md) before interpreting CRM metrics. The snapshot was verified 2026-09-29; refresh live data for current questions.

- Search [references/lead-fields.md](references/lead-fields.md) for lead field names, types, and bounded fill profiles.
- For non-lead entities or physical schema, inspect `references/local-catalog.md`: `fields`, `columns`, `business_enums`, `statuses`. Metadata coverage is not value verification. Match ENTITY_ID as well as field name; do not combine CRM_LEAD with CRM_LEAD_SPD or dynamic entities.
- Read [references/source-inventory.md](references/source-inventory.md) for evidence sources and limitations.
- Definitions must distinguish current field state, history events, unique leads, and actual meetings/calls. Never silently substitute one for another.
- This layer does not authorize writes to source systems. The CRM connection used for this evidence is read-only. Never print credentials or include raw client contact details in this skill.
- Use parameterized, bounded SELECTs; establish read-only transactions. Recheck available tables and date conventions rather than assuming the replica is the full Bitrix database.
- Keep conflicting or unproven meanings explicit. Russian labels confirm field identity, not formula, units, automation behavior, or historical immutability.
