# Setup

> Skeleton — filled in fully once all workflows and credentials are finalized
> (tracked in this repo's commit history). This file always reflects the
> current state of the build.

## Prerequisites

- n8n Cloud account
- Google account with a Sheet using the schema in
  [GOOGLE_SHEET_SCHEMA.md](GOOGLE_SHEET_SCHEMA.md)
- OpenAI API key
- GitHub account + Personal Access Token
- Gmail account (OAuth2) for sending client emails

## Steps

1. Import the 4 workflow JSON files from `n8n/workflows/` into n8n.
2. Configure credentials (Google Sheets OAuth2, OpenAI, GitHub PAT, Gmail
   OAuth2) — full instructions below once workflows are complete.
3. Point Workflow A's Google Sheets Trigger at your sheet.
4. Set Workflow A and B's error workflow to Workflow C.
5. Activate all 4 workflows.
6. Deploy the dashboard (see `dashboard/README.md`).

*(Detailed credential-by-credential walkthrough added in a later commit.)*
