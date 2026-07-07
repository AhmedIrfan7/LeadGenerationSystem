import type { Lead } from '../lib/types';
import { statusStyle } from '../lib/statusStyles';

const STATUSES = ['Pending', 'Processing', 'Done', 'Failed'] as const;

export default function StatCards({ leads }: { leads: Lead[] }) {
  const counts: Record<string, number> = {};
  for (const lead of leads) {
    counts[lead.status] = (counts[lead.status] || 0) + 1;
  }

  const cards = [
    { label: 'Total', value: leads.length, style: 'bg-slate-900 text-white' },
    ...STATUSES.map((s) => ({ label: s, value: counts[s] || 0, style: statusStyle(s) }))
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
      {cards.map((c) => (
        <div key={c.label} className={`rounded-xl p-4 ${c.style}`}>
          <div className="text-2xl font-bold">{c.value}</div>
          <div className="text-sm opacity-80">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
