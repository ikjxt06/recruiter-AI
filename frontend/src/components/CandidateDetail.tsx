import { X } from "lucide-react";
import type { Candidate } from "../types";

type Props = {
  candidate: Candidate;
  onClose: () => void;
};

function DetailList({ title, items }: { title: string; items: unknown[] }) {
  return (
    <section>
      <h3 className="text-sm font-semibold text-ink">{title}</h3>
      {items.length ? (
        <div className="mt-2 space-y-2">
          {items.map((item, index) => (
            <div key={index} className="rounded-md bg-slate-50 p-3 text-sm text-steel">
              {typeof item === "string" ? item : JSON.stringify(item)}
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-2 text-sm text-slate-500">No data found</p>
      )}
    </section>
  );
}

export function CandidateDetail({ candidate, onClose }: Props) {
  return (
    <div className="fixed inset-0 z-50 bg-ink/30 px-4 py-6">
      <aside className="ml-auto flex h-full max-w-2xl flex-col rounded-lg bg-white shadow-xl">
        <header className="flex items-start justify-between border-b border-slate-200 p-5">
          <div>
            <h2 className="text-xl font-semibold">{candidate.name ?? "Unnamed Candidate"}</h2>
            <p className="text-sm text-steel">{candidate.email ?? "No email"} · {candidate.phone ?? "No phone"}</p>
          </div>
          <button className="rounded-md border border-slate-200 p-2" onClick={onClose} aria-label="Close candidate detail">
            <X size={16} />
          </button>
        </header>
        <div className="flex-1 space-y-6 overflow-auto p-5">
          <section>
            <h3 className="text-sm font-semibold text-ink">Skills</h3>
            <div className="mt-2 flex flex-wrap gap-2">
              {candidate.skills.length ? candidate.skills.map((skill) => (
                <span key={skill} className="rounded bg-mint/10 px-2 py-1 text-xs text-mint">{skill}</span>
              )) : <p className="text-sm text-slate-500">No skills found</p>}
            </div>
          </section>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-md border border-slate-200 p-3">
              <p className="text-xs uppercase text-slate-500">Experience</p>
              <p className="mt-1 font-semibold">{candidate.experience_years > 0 ? `${candidate.experience_years} years` : "Fresher"}</p>
            </div>
            <div className="rounded-md border border-slate-200 p-3">
              <p className="text-xs uppercase text-slate-500">Status</p>
              <p className="mt-1 font-semibold capitalize">{candidate.status}</p>
            </div>
          </div>
          <DetailList title="Education" items={candidate.education} />
          <DetailList title="Projects" items={candidate.projects} />
          <DetailList title="Internships" items={candidate.internships} />
          <DetailList title="Experience Evidence" items={candidate.experience} />
          <DetailList title="Certifications" items={candidate.certifications} />
        </div>
      </aside>
    </div>
  );
}
