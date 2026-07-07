# Architecture

## Goal

Given a spreadsheet of `website_url` + `client_email` rows, produce a
redesigned, deployed preview website for each prospect and email the client
the live link — with no manual steps anywhere in the pipeline.

## Components

| Component | Role |
|---|---|
| Google Sheet | Source of truth / queue. Columns in [GOOGLE_SHEET_SCHEMA.md](GOOGLE_SHEET_SCHEMA.md). |
| **Workflow A** — Orchestrator | Polls the sheet for new rows, dispatches each to Workflow B, writes back status. |
| **Workflow B** — Process Single Lead | Does the actual work for one row: scrape → generate → deploy → email. Callable as a sub-workflow so failures are isolated per-lead. |
| **Workflow C** — Error Notifier | Registered as the n8n Error Workflow for A and B. Any uncaught node failure sends an admin alert with the execution link. |
| **Workflow D** — Dashboard API | Webhooks that expose sheet data as JSON (`GET /leads`) and allow retrying a failed row (`POST /leads/retry`), so the frontend never needs direct Google credentials. |
| Dashboard | Next.js app that polls Workflow D and shows pipeline status. |

## Why a sub-workflow (B) instead of one giant workflow

- **Isolation**: one bad website (timeout, garbage HTML, AI hallucination) fails
  only that row, not the whole batch.
- **Idempotency**: B can be re-run safely for the same row — GitHub repo
  creation and file uploads check for existing state first (create-repo
  handles `422 already exists`, file upload fetches `sha` before overwrite,
  Pages-enable handles `409 already enabled`). This means "retry" from the
  dashboard is just calling B again.
- **Reuse**: the dashboard's manual retry button calls the same Workflow B via
  the Dashboard API, no duplicate logic.

## Workflow B — step by step

1. Receive `{ website_url, client_email, client_name, row_number }`.
2. Scrape the homepage (HTTP Request, retry x3, timeout 15s). Fail fast via
   `Stop And Error` if the site is unreachable or empty.
3. Extract title, meta description, visible text (HTML Extract).
4. Find likely About/Services/Contact links and scrape up to 2 more pages for
   richer context, then aggregate all scraped text (capped ~6000 chars to
   control token cost).
5. Send the aggregated content to OpenAI with a strict JSON response format:
   business name, tagline, color palette, and an array of page sections
   (hero/about/services/testimonials/contact).
6. Parse and validate that JSON; fail loudly if the model returns malformed
   output rather than silently deploying a broken site.
7. Render the site spec into `index.html`, `style.css`, `README.md` via a
   template function (Tailwind CDN + custom CSS, fully static, no build step
   — required for zero-config GitHub Pages hosting).
8. Create (or reuse) a GitHub repo named from a slug of the business name.
9. Upload the three files (idempotent create-or-update).
10. Enable GitHub Pages on `main` / `/`, wait, poll until the Pages build
    reports `built`.
11. Email the client the live `https://<owner>.github.io/<repo>/` URL.
12. Return a structured result so Workflow A can update the sheet.

## Reliability choices

- Every external call (scrape, OpenAI, GitHub, Gmail) has `retryOnFail` and a
  bounded `maxTries`, so transient network blips don't fail a lead outright.
- `continueOnFail` is used precisely where a non-200 / non-2xx response is a
  *meaningful* branch (e.g. GitHub "repo already exists") rather than a real
  error — those are handled with IF nodes instead of being treated as
  failures.
- All genuine failures raise `Stop And Error` with a descriptive message,
  which the Execute-Workflow caller captures and writes to the sheet's
  `ErrorMessage` column, and which triggers Workflow C to alert an admin.
- Processing is per-row, so one row's failure never blocks the rest of the
  batch.
