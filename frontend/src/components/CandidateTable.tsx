import { ArrowDownWideNarrow } from "lucide-react";
import type { Candidate, CandidateStatus } from "../types";

type Props = {
  candidates: Candidate[];
  onStatusChange: (candidateId: number, status: CandidateStatus) => void;
  onSelect: (candidate: Candidate) => void;
  onDelete: (candidateId: number) => void;
};

const statusClass: Record<string, string> = {
  new: "bg-slate-100 text-slate-700",
  shortlisted: "bg-mint/10 text-mint",
  rejected: "bg-red-50 text-red-700"
};

export function CandidateTable({ candidates, onStatusChange, onSelect, onDelete }: Props) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold">Candidate Pipeline</h2>
        <button className="inline-flex h-9 items-center gap-2 rounded-md border border-slate-200 px-3 text-sm text-steel">
          <ArrowDownWideNarrow size={16} /> Sort
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Skills</th>
              <th className="px-4 py-3">Experience</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {candidates.map((candidate) => (
              <tr key={candidate.id} className="hover:bg-slate-50">
                <td className="px-4 py-3">
                  <p className="font-medium text-ink">{candidate.name ?? "Unnamed Candidate"}</p>
                  <p className="text-xs text-slate-500">{candidate.email}</p>
                </td>
                <td className="px-4 py-3">
                  <div className="flex max-w-xl flex-wrap gap-1">
                    {candidate.skills.slice(0, 6).map((skill) => (
                      <span key={skill} className="rounded bg-mint/10 px-2 py-1 text-xs text-mint">
                        {skill}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="px-4 py-3">{candidate.experience_years > 0 ? `${candidate.experience_years} years` : "Fresher"}</td>
                <td className="px-4 py-3">
                  <span className={`rounded px-2 py-1 text-xs font-medium capitalize ${statusClass[candidate.status] ?? statusClass.new}`}>
                    {candidate.status}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap gap-2">
                    <button
                      className="rounded-md border border-slate-200 px-3 py-1 text-xs text-steel"
                      onClick={() => onSelect(candidate)}
                    >
                      View
                    </button>
                    <button
                      className="rounded-md bg-mint px-3 py-1 text-xs font-medium text-white"
                      onClick={() => onStatusChange(candidate.id, "shortlisted")}
                    >
                      Shortlist
                    </button>
                    <button
                      className="rounded-md border border-slate-200 px-3 py-1 text-xs text-steel"
                      onClick={() => onStatusChange(candidate.id, "rejected")}
                    >
                      Reject
                    </button>
                    <button
                      className="rounded-md border border-red-100 px-3 py-1 text-xs text-red-600"
                      onClick={() => onDelete(candidate.id)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
