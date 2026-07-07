# Lead Generation System

Fully automated pipeline that turns a spreadsheet of prospect websites into
live, deployed preview sites — with zero manual steps beyond adding a row.

**Flow:** Google Sheet row → scrape prospect's site → OpenAI generates a
redesigned site spec → static HTML/CSS/README rendered → files pushed to a
new GitHub repo → GitHub Pages enabled → live preview emailed to the client
→ sheet updated with status and the live URL, visible on a live dashboard.

## Status: v1.0.0 — complete

All 4 n8n workflows and the monitoring dashboard are built and validated.
See [CHANGELOG.md](CHANGELOG.md).

## Repo layout

```
n8n/workflows/   importable n8n workflow JSON
  01-main-orchestrator.json   polls the sheet, dispatches each row, writes status back
  02-process-single-lead.json scrape -> AI spec -> build files -> deploy -> email (one lead)
  03-error-notifier.json      catches uncaught crashes, alerts admin
  04-dashboard-api.json       webhooks backing the dashboard (GET /leads, POST /leads/retry)
scripts/
  validate-workflows.js       structural + wiring validation for the 4 workflow files
dashboard/       Next.js + TypeScript + Tailwind monitoring UI
docs/
  ARCHITECTURE.md            full system design and reliability choices
  GOOGLE_SHEET_SCHEMA.md     sheet columns and row lifecycle
  SETUP.md                   step-by-step credential + import guide
  RUNBOOK.md                 day-2 operations: statuses, retries, diagnosing failures
```

## Quick start

1. Read [docs/SETUP.md](docs/SETUP.md) and follow it end to end (Google Sheet,
   n8n credentials, workflow import, cross-workflow wiring).
2. Read [docs/RUNBOOK.md](docs/RUNBOOK.md) for day-to-day operation once it's live.
3. Deploy the dashboard — see [dashboard/README.md](dashboard/README.md).
4. Run `npm run validate` any time you edit a workflow JSON by hand, to catch
   structural mistakes before importing into n8n.

## Design highlights

- **Idempotent by construction**: repo creation, file uploads, and Pages
  enablement all treat "already exists" as success, so retrying a failed
  lead is always safe — never produces duplicates.
- **Per-lead isolation**: each row is processed by its own sub-workflow
  execution, so one bad website never blocks the batch.
- **Two-tier error handling**: expected failures (unreachable site,
  malformed AI output, GitHub API error) resolve to a clean `Failed` row
  with a human-readable message; genuinely uncaught crashes trip a separate
  admin-alert workflow.
- **No database**: the Google Sheet is the single source of truth; the
  dashboard reads it through n8n webhooks, keeping the frontend static and
  cheap to host.

## Tech stack

n8n (automation) · OpenAI Chat Completions API (content/design generation) ·
GitHub REST API (repo creation, file upload, Pages) · Gmail (client + admin
email) · Google Sheets API (source of truth) · Next.js + TypeScript +
Tailwind (dashboard, deployed on Vercel)
