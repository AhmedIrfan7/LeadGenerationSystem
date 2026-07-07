'use client';

import { useCallback, useEffect, useState } from 'react';
import { getLeads } from '../lib/api';
import type { Lead } from '../lib/types';
import StatCards from '../components/StatCards';
import LeadsTable from '../components/LeadsTable';

const POLL_INTERVAL_MS = 10000;

export default function Page() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const data = await getLeads();
      setLeads(data);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load leads');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [load]);

  return (
    <main className="min-h-screen max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-bold mb-1">Lead-Gen Pipeline</h1>
      <p className="text-slate-500 text-sm mb-8">
        Live status, auto-refreshing every {POLL_INTERVAL_MS / 1000}s.
      </p>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading…</p>
      ) : error ? (
        <p className="text-red-600 text-sm">{error}</p>
      ) : (
        <>
          <StatCards leads={leads} />
          <div className="mt-8 bg-white rounded-xl shadow-sm p-4">
            <LeadsTable leads={leads} onRetried={load} />
          </div>
        </>
      )}
    </main>
  );
}
