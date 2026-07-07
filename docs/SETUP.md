# Setup

## Prerequisites

- n8n Cloud account
- A Google account (for the Sheet + Gmail sending)
- An OpenAI API key
- A GitHub Personal Access Token
- The 4 workflow files in `n8n/workflows/` (this repo)

## 1. Create the Google Sheet

Create a new Google Sheet with one tab named exactly `Leads`, header row matching
[GOOGLE_SHEET_SCHEMA.md](GOOGLE_SHEET_SCHEMA.md) column-for-column:

```
website_url | client_email | client_name | status | repo_name | live_url | error_message | processed_at
```

Copy the spreadsheet ID out of its URL —
`https://docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`.

## 2. Create credentials in n8n

Go to **Credentials → New** for each of the following:

| Credential type | Name (must match exactly) | Used for |
|---|---|---|
| Google Sheets OAuth2 API | `Google Sheets account` | Reading/writing the Leads sheet |
| Gmail OAuth2 | `Gmail account` | Emailing clients + admin alerts |
| Header Auth | `OpenAI API` — header `Authorization` = `Bearer YOUR_OPENAI_KEY` | Calling OpenAI's Chat Completions API |
| Header Auth | `GitHub PAT` — header `Authorization` = `Bearer YOUR_GITHUB_TOKEN` | Creating repos, uploading files, enabling Pages |

Your GitHub PAT needs the **`repo`** scope (classic token) or **Contents +
Administration: Read and write** (fine-grained token scoped to repos you own
or "All repositories").

## 3. Import the workflows

Import all 4 files from `n8n/workflows/` (see that folder's
[README.md](../n8n/workflows/README.md) for order and why). For each
imported workflow:

1. Open every node that references a credential and re-select the credential
   you created in step 2 (n8n exports credential *names*, not the linkage).
2. Find-and-replace `YOUR_SPREADSHEET_ID` with your real sheet ID (appears in
   `01-main-orchestrator.json` and `04-dashboard-api.json`).
3. Find-and-replace `admin-placeholder@example.com` with the inbox that
   should receive failure alerts (`01-main-orchestrator.json` and
   `03-error-notifier.json`).
4. If you're deploying under a GitHub account other than `AhmedIrfan7`,
   find-and-replace that in `02-process-single-lead.json`.

## 4. Wire the cross-workflow links (see n8n/workflows/README.md)

- `Lead-Gen Orchestrator` → `Call Process Single Lead` node → point at your
  imported `Process Single Lead` workflow; confirm "Run once for each item".
- Both `Lead-Gen Orchestrator` and `Process Single Lead` → workflow Settings
  → Error Workflow → `Error Notifier`.

## 5. Activate

Activate `Lead-Gen Orchestrator`, `Process Single Lead`, `Error Notifier`,
and `Dashboard API`. Copy the two production webhook URLs from
`Dashboard API` (`GET /leads`, `POST /leads/retry`) — the dashboard needs
them, see [dashboard/README.md](../dashboard/README.md).

## 6. Test end-to-end

Add one real row to the sheet and watch it move through
`(empty) → Processing → Done` within a few minutes (see
[GOOGLE_SHEET_SCHEMA.md](GOOGLE_SHEET_SCHEMA.md) for the full lifecycle). If
it lands on `Failed`, check `error_message` in the sheet first, then the n8n
execution log for the failing node.
