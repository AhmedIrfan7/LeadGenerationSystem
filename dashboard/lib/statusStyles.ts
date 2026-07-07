export const STATUS_STYLES: Record<string, string> = {
  Pending: 'bg-slate-100 text-slate-700',
  Processing: 'bg-blue-100 text-blue-700',
  Done: 'bg-green-100 text-green-700',
  Failed: 'bg-red-100 text-red-700',
  Retry: 'bg-amber-100 text-amber-700'
};

export function statusStyle(status: string): string {
  return STATUS_STYLES[status] || 'bg-slate-100 text-slate-700';
}
