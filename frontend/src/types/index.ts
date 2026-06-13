export type Candidate = {
  id: number;
  name?: string;
  email?: string;
  phone?: string;
  skills: string[];
  education: Record<string, unknown>[];
  certifications: string[];
  experience: Record<string, unknown>[];
  projects: Record<string, unknown>[];
  internships: Record<string, unknown>[];
  experience_years: number;
  status: string;
};

export type CandidateStatus = "new" | "shortlisted" | "rejected";

export type DashboardStats = {
  total_candidates: number;
  average_match_score: number;
  top_skills: [string, number][];
  candidates_by_experience_level: Record<string, number>;
  shortlisted_candidates: number;
  rejected_candidates: number;
};
