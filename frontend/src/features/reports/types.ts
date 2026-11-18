export type Summary = {
  generated: string;
  verified_compost: string;
  pending: string;
  delivered: string;
  available: string;
  in_process: string;
  rate: string | null;
  provenance: string;
  formula: string;
  cutoff: string;
  limitations: string;
  provisional: boolean;
  distribution: { material: string; kg: string }[];
};
export type Observatory = {
  summary: Summary;
  comparison: {
    available: boolean;
    reason: string;
    current_from: string | null;
    current_to: string | null;
    previous_from: string | null;
    previous_to: string | null;
    previous_generated: string | null;
    absolute: string | null;
    percent: string | null;
  };
  series: { date: string; kg: string; count: number }[];
  areas: { id: number; name: string; generated: string; pending: string }[];
  provenance_totals: { provenance: string; generated: string }[];
  insights: {
    code: string;
    title: string;
    detail: string;
    interpretation?: string;
    suggestion?: string;
    area?: number;
  }[];
  context: { cutoff: string; coverage: string; series_reason: string };
};
