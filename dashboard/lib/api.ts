import type { Lead, LeadsResponse } from './types';

const BASE_URL = process.env.NEXT_PUBLIC_N8N_WEBHOOK_BASE_URL || '';

function assertBaseUrl() {
  if (!BASE_URL) {
    throw new Error('NEXT_PUBLIC_N8N_WEBHOOK_BASE_URL is not set. See dashboard/README.md.');
  }
}

export async function getLeads(): Promise<Lead[]> {
  assertBaseUrl();
  const res = await fetch(`${BASE_URL}/leads`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(`Failed to fetch leads (${res.status})`);
  }
  const data: LeadsResponse = await res.json();
  return data.leads;
}

export async function retryLead(rowNumber: number): Promise<void> {
  assertBaseUrl();
  const res = await fetch(`${BASE_URL}/leads/retry`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ row_number: rowNumber })
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}) as { error?: string });
    throw new Error(body.error || `Retry failed (${res.status})`);
  }
}
