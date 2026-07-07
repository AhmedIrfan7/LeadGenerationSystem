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
