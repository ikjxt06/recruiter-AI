import { useState } from "react";
import { api } from "../api/client";
import type { Candidate } from "../types";

type RankResult = {
  candidate: Candidate;
  weighted_score: number;
  match_score: number;
  matching_skills: string[];
  missing_skills: string[];
  suspicion_score: number;
  hiring_recommendation: string;
  confidence_score: number;
  component_scores: Record<string, number>;
  weights: Record<string, number>;
};

export function JobAnalyzer() {
  const [title, setTitle] = useState("AI Engineer");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<{ id: number; required_skills: string[]; preferred_skills: string[]; experience_requirements: Record<string, unknown> } | null>(null);
  const [rankings, setRankings] = useState<RankResult[]>([]);

  async function analyze() {
    const { data } = await api.post("/jobs", { title, description });
    setResult(data);
    setRankings([]);
  }

  async function rankCandidates() {
    if (!result) return;
    const { data } = await api.get(`/candidates/rank/${result.id}`);
    setRankings(data);
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="font-semibold">Job Description Analyzer</h2>
      <input className="mt-4 h-10 w-full rounded-md border border-slate-300 px-3" value={title} onChange={(event) => setTitle(event.target.value)} />
      <textarea className="mt-3 min-h-36 w-full rounded-md border border-slate-300 p-3" value={description} onChange={(event) => setDescription(event.target.value)} />
      <div className="mt-3 flex flex-wrap gap-2">
        <button className="h-10 rounded-md bg-coral px-4 font-medium text-white" onClick={analyze}>Analyze JD</button>
        <button className="h-10 rounded-md bg-ink px-4 font-medium text-white disabled:cursor-not-allowed disabled:opacity-40" disabled={!result} onClick={rankCandidates}>Rank Candidates</button>
      </div>
      {result ? (
        <div className="mt-4 rounded-md bg-slate-50 p-4">
          <h3 className="font-medium">Extracted Requirements</h3>
          <div className="mt-3 grid gap-3 md:grid-cols-3">
            <div>
              <p className="text-xs uppercase text-slate-500">Required Skills</p>
              <p className="mt-1 text-sm capitalize">{result.required_skills.join(", ") || "None found"}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-slate-500">Preferred Skills</p>
              <p className="mt-1 text-sm capitalize">{result.preferred_skills.join(", ") || "None found"}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-slate-500">Experience</p>
              <p className="mt-1 text-sm">{String(result.experience_requirements.minimum_years ?? 0)}+ years</p>
            </div>
          </div>
        </div>
      ) : null}
      {rankings.length ? (
        <div className="mt-4 overflow-hidden rounded-lg border border-slate-200">
          <div className="border-b border-slate-200 px-4 py-3 font-medium">Ranked Candidates</div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                <tr>
                  <th className="px-4 py-3">Candidate</th>
                  <th className="px-4 py-3">Score</th>
                  <th className="px-4 py-3">Matched</th>
                  <th className="px-4 py-3">Missing</th>
                  <th className="px-4 py-3">Recommendation</th>
                  <th className="px-4 py-3">Why</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {rankings.map((row) => (
                  <tr key={row.candidate.id}>
                    <td className="px-4 py-3">
                      <p className="font-medium">{row.candidate.name ?? "Unnamed Candidate"}</p>
                      <p className="text-xs text-slate-500">{row.candidate.email}</p>
                    </td>
                    <td className="px-4 py-3 font-semibold">{row.weighted_score}%</td>
                    <td className="px-4 py-3 capitalize">{row.matching_skills.join(", ") || "-"}</td>
                    <td className="px-4 py-3 capitalize">{row.missing_skills.join(", ") || "-"}</td>
                    <td className="px-4 py-3">
                      <p>{row.hiring_recommendation}</p>
                      <p className="text-xs text-slate-500">Confidence {row.confidence_score}%</p>
                    </td>
                    <td className="px-4 py-3 text-xs text-slate-600">
                      <p>Skills {row.component_scores.skills}% × {row.weights.skills}%</p>
                      <p>Experience {row.component_scores.experience}% × {row.weights.experience}%</p>
                      <p>Projects {row.component_scores.projects}% × {row.weights.projects}%</p>
                      <p>Education {row.component_scores.education}% × {row.weights.education}%</p>
                      <p>Certifications {row.component_scores.certifications}% × {row.weights.certifications}%</p>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}
    </section>
  );
}
