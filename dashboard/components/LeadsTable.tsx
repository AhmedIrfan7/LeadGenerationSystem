'use client';

import { useState } from 'react';
import type { Lead } from '../lib/types';
import { statusStyle } from '../lib/statusStyles';
import { retryLead } from '../lib/api';

export default function LeadsTable({ leads, onRetried }: { leads: Lead[]; onRetried: () => void }) {
  const [retrying, setRetrying] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleRetry(rowNumber: number) {
    setRetrying(rowNumber);
    setError(null);
    try {
      await retryLead(rowNumber);
      onRetried();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Retry failed');
    } finally {
      setRetrying(null);
    }
  }

  if (leads.length === 0) {
    return (
      <p className="text-slate-500 text-sm py-8 text-center">
        No leads yet. Add a row to the sheet to get started.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      {error && <p className="text-red-600 text-sm mb-2">{error}</p>}
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="text-left text-slate-500 border-b">
            <th className="py-2 pr-4">Website</th>
            <th className="py-2 pr-4">Client</th>
            <th className="py-2 pr-4">Status</th>
            <th className="py-2 pr-4">Live URL</th>
            <th className="py-2 pr-4">Updated</th>
            <th className="py-2 pr-4"></th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.row_number} className="border-b last:border-0">
              <td className="py-2 pr-4">
                <a
                  href={lead.website_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-slate-700 hover:underline"
                >
                  {lead.website_url}
                </a>
              </td>
              <td className="py-2 pr-4">
                <div>{lead.client_name}</div>
                <div className="text-slate-400 text-xs">{lead.client_email}</div>
              </td>
              <td className="py-2 pr-4">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyle(lead.status)}`}>
                  {lead.status}
                </span>
                {lead.status === 'Failed' && lead.error_message && (
                  <div className="text-red-500 text-xs mt-1 max-w-xs truncate" title={lead.error_message}>
                    {lead.error_message}
                  </div>
                )}
              </td>
              <td className="py-2 pr-4">
                {lead.live_url ? (
                  <a href={lead.live_url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                    View site
                  </a>
                ) : (
                  <span className="text-slate-300">—</span>
                )}
              </td>
              <td className="py-2 pr-4 text-slate-400 text-xs">{lead.processed_at || '—'}</td>
              <td className="py-2 pr-4">
                {lead.status === 'Failed' && (
                  <button
                    onClick={() => handleRetry(lead.row_number)}
                    disabled={retrying === lead.row_number}
                    className="px-3 py-1 rounded-full text-xs font-medium bg-slate-900 text-white disabled:opacity-50"
                  >
                    {retrying === lead.row_number ? 'Retrying…' : 'Retry'}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
