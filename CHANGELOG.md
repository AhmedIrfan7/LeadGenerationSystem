# Changelog

## v1.0.0

Initial complete build of the automated lead-generation pipeline.

**n8n workflows**
- `Process Single Lead`: scrapes homepage + up to 2 relevant internal pages,
  generates a structured site spec via OpenAI, renders it into a static
  `index.html` / `style.css` / `README.md`, deploys to a new-or-existing
  GitHub repo, enables GitHub Pages, polls build status, and emails the
  client the live link. Every external call has bounded retries; every
  GitHub operation is idempotent.
- `Lead-Gen Orchestrator`: polls the Google Sheet every 5 minutes for
  blank/`Retry` rows, marks them `Processing`, dispatches each to `Process
  Single Lead` in isolation, and writes back `Done`/`Failed` with the
  live URL or error message.
- `Error Notifier`: registered as the error workflow for the two above,
  emails an admin on any uncaught crash.
- `Dashboard API`: `GET /leads` and `POST /leads/retry` webhooks backing the
  frontend, with input validation on the retry endpoint.

**Tooling**
- `scripts/validate-workflows.js`: checks every workflow JSON for structural
  correctness and full wiring (no orphaned or unreachable nodes). Wired to
  `npm run validate`.

**Dashboard**
- Next.js + TypeScript + Tailwind app: live per-status counts, a
  sortable-by-status leads table, one-click retry on failed rows, 10s
  polling, loading/error states. Ready to deploy on Vercel.

**Docs**
- `docs/ARCHITECTURE.md`, `docs/GOOGLE_SHEET_SCHEMA.md`, `docs/SETUP.md`,
  `docs/RUNBOOK.md`, plus per-package READMEs.
