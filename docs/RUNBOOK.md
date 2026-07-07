# Runbook

## Adding leads

The only manual step in the whole system: add a row to the `Leads` sheet
with `website_url` and `client_email` (`client_name` optional). Leave
`status` and every column after it blank — the pipeline owns those.
`Lead-Gen Orchestrator` polls every 5 minutes and picks up any row where
`status` is blank or `Retry`.

## Checking on a lead

Either open the sheet directly, or use the dashboard (see
[dashboard/README.md](../dashboard/README.md)), which polls the same data
through the `Dashboard API` workflow.

| Status | Meaning |
|---|---|
| *(blank)* | Not picked up yet, waits for next poll |
| `Processing` | Currently running through `Process Single Lead` |
| `Done` | Deployed; `live_url` is populated and the client was emailed |
| `Failed` | See `error_message`; site was not deployed, no email was sent |
| `Retry` | Manually reset (via dashboard or by editing the sheet), waits for next poll |

## Retrying a failed lead

Click "Retry" on the dashboard (calls `POST /leads/retry`), or manually set
that row's `status` cell to `Retry`. Because every step in `Process Single
Lead` is idempotent (repo creation, file upload, Pages enablement all
tolerate "already exists"), retrying is always safe — it will not create
duplicate repos or double-send the client email past the point where it
last failed... except the email step itself: if a lead fails *after*
emailing the client (extremely unlikely, since email is the last real step),
a retry would email them again. If that ever happens, clear `live_url`
manually before retrying, or just don't retry that specific row.

## Diagnosing a `Failed` row

1. Read `error_message` in the sheet — it's the literal error thrown by the
   failing node (site unreachable, malformed AI JSON, GitHub API error,
   etc).
2. If it's not self-explanatory, open n8n → `Process Single Lead` →
   Executions, find the failed run for that row, and inspect the failing
   node's input/output.
3. Common causes:
   - **Site unreachable/empty**: the prospect's site blocks scrapers or is
     down. Verify the URL manually.
   - **Malformed AI JSON**: rare with `response_format: json_object`, but
     can happen if the model refuses (e.g. flagged content). Check the raw
     OpenAI response in the execution log.
   - **GitHub API error**: usually a bad/expired PAT, or the PAT lacks
     `repo` scope.

## Uncaught crashes (not a normal `Failed` row)

If a node fails in a way that isn't caught by that workflow's own error
handling, n8n fires `Error Notifier`, which emails the admin inbox
configured in step 3 of [SETUP.md](SETUP.md) with the workflow name, failing
node, error message, and a link to the execution. This is the safety net
for bugs, not the expected path for a bad lead (which always resolves to a
clean `Failed` row instead).

## Rotating credentials

Rotate the GitHub PAT, OpenAI key, or Google/Gmail OAuth tokens directly in
n8n's Credentials screen — no workflow JSON changes needed, since all 4
workflows reference credentials by name, not by embedded secret.
