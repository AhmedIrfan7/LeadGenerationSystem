# n8n Workflows

Import these into n8n in this order (each has hard dependencies on the last):

| File | Name | Role |
|---|---|---|
| `02-process-single-lead.json` | Process Single Lead | Built first since it has no dependency on the others; called by Workflow A. |
| `01-main-orchestrator.json` | Lead-Gen Orchestrator | Polls the Google Sheet, calls Workflow B per row, writes status back. |
| `03-error-notifier.json` | Error Notifier | Set as the **Error Workflow** in Settings for both 01 and 02. |
| `04-dashboard-api.json` | Dashboard API | Webhooks backing the frontend dashboard. |

Files are numbered by dependency order, not build order — `02` is built
first in this repo's commit history because `01` needs to reference its
workflow ID once it exists in your n8n instance.

After importing, open each workflow and re-select credentials (n8n does not
export credential secrets, only credential *names/types* as placeholders).
See [../../docs/SETUP.md](../../docs/SETUP.md).

## Manual links required after import (workflow IDs are instance-specific)

n8n assigns a new workflow ID on every import, so these can't be baked into
the JSON ahead of time — set them once, right after importing all 4 files:

1. **01 → 02**: open `Lead-Gen Orchestrator` → `Call Process Single Lead`
   node → set its workflow reference to your imported `Process Single Lead`.
   Also confirm the run mode is "Run once for each item".
2. **01 & 02 → 03**: open each workflow's Settings (top-right menu) → Error
   Workflow → select `Error Notifier`.
3. Replace every `YOUR_SPREADSHEET_ID` and `admin-placeholder@example.com`
   placeholder (search-and-replace across the 4 files works fine) with your
   real sheet ID and admin inbox.
