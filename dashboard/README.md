# Lead-Gen Dashboard

Next.js + TypeScript + Tailwind frontend that shows live pipeline status by
polling the `Dashboard API` n8n workflow — no database, no backend of its
own.

## Local development

```bash
npm install
cp .env.example .env.local   # then fill in your real webhook base URL
npm run dev
```

Open http://localhost:3000.

## Configuration

One environment variable, set in `.env.local` (dev) or your host's env
settings (production):

```
NEXT_PUBLIC_N8N_WEBHOOK_BASE_URL=https://your-n8n-instance.app.n8n.cloud/webhook
```

This must be the base webhook URL for your n8n instance — the app calls
`${NEXT_PUBLIC_N8N_WEBHOOK_BASE_URL}/leads` and `/leads/retry`, which must
match the `Dashboard API` workflow's webhook paths (see
[../docs/SETUP.md](../docs/SETUP.md)).

## Deploying to Vercel

1. Push this repo to GitHub (already done if you're reading this from the repo).
2. In Vercel: **New Project** → import `LeadGenerationSystem` → set
   **Root Directory** to `dashboard`.
3. Add the `NEXT_PUBLIC_N8N_WEBHOOK_BASE_URL` environment variable in the
   Vercel project settings (Production + Preview).
4. Deploy. Vercel auto-detects Next.js — no build command changes needed.

## What it does

- Polls `GET /leads` every 10 seconds, shows per-status counts and a table
  of every row in the sheet.
- "Retry" button on any `Failed` row calls `POST /leads/retry`, which flips
  that row's status back to `Retry` so the next orchestrator poll picks it
  up again.
- No auth of its own — access control is whatever you put in front of the
  n8n webhooks (e.g. n8n's built-in webhook auth) or the Vercel deployment
  itself (e.g. Vercel password protection) if this needs to be private.
