export interface ResearchKeyFinding {
  title: string;
  description: string;
}

export interface ResearchReportSchema {
  title: string;
  executive_summary: string;
  key_findings: ResearchKeyFinding[];
  summary_outlook: string;
}

export interface ResearchResponse {
  message: string;
  topic: string;
  status: string;
  result: ResearchReportSchema;
}

export interface ResearchRequest {
  topic: string;
  depth?: 'shallow' | 'medium' | 'deep';
}