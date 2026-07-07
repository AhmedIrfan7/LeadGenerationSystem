# Lead Generation System

Fully automated pipeline that turns a spreadsheet of prospect websites into
live, deployed preview sites — with zero manual steps.

**Flow:** Google Sheet row → scrape prospect's site → AI generates a
redesigned website → files pushed to a new GitHub repo → GitHub Pages
enabled → live preview emailed to the client.

Status: under active development. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
for the full design once available.

## Repo layout

- `n8n/workflows/` — importable n8n workflow JSON (orchestrator, worker, error handler, dashboard API)
- `dashboard/` — Next.js monitoring dashboard for the pipeline
- `docs/` — architecture, setup, and operational runbook

## Tech stack

n8n (automation) · OpenAI (content/design generation) · GitHub REST API (deploy)
· Gmail (client email) · Google Sheets (source of truth) · Next.js + TypeScript
+ Tailwind (dashboard)
