# Google Sheet Schema

One sheet, one tab named `Leads`. Row 1 is the header row — column names must
match exactly (n8n's Google Sheets nodes map by header name).

| Column | Type | Set by | Description |
|---|---|---|---|
| `website_url` | text (input) | Team | Prospect's current website. Must include scheme, e.g. `https://example.com`. |
| `client_email` | text (input) | Team | Where the live preview link is sent. |
| `client_name` | text (input) | Team | Optional. Used in the email greeting; falls back to the AI-detected business name. |
| `status` | text (managed) | Workflow A | One of: *(empty)*, `Processing`, `Done`, `Failed`, `Retry`. Only empty/`Retry` rows are picked up. |
| `repo_name` | text (managed) | Workflow B | GitHub repo the site was deployed to. |
| `live_url` | text (managed) | Workflow B | `https://<owner>.github.io/<repo_name>/` once Pages build succeeds. |
| `error_message` | text (managed) | Workflow A | Populated only when `status = Failed`. |
| `processed_at` | datetime (managed) | Workflow A | ISO timestamp of the last processing attempt. |

## Row lifecycle

```
(empty) --Workflow A picks up--> Processing --Workflow B succeeds--> Done
                                          \--Workflow B fails-------> Failed
Failed --dashboard "Retry" click--> Retry --Workflow A picks up--> Processing --> ...
```

## Adding new leads

The team's only manual action in the entire system is adding rows
(`website_url`, `client_email`, `client_name`) to this sheet — everything
from that point on is automated. Paste directly from the source Excel file;
column order doesn't matter as long as headers match.
