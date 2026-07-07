export type LeadStatus = 'Pending' | 'Processing' | 'Done' | 'Failed' | 'Retry';

export interface Lead {
  row_number: number;
  website_url: string;
  client_email: string;
  client_name: string;
  status: LeadStatus | string;
  repo_name: string;
  live_url: string;
  error_message: string;
  processed_at: string;
}

export interface LeadsResponse {
  leads: Lead[];
}
