import { Download, Search, Upload } from "lucide-react";
import { ChangeEvent, useEffect, useState } from "react";
import { api } from "../api/client";
import { CandidateDetail } from "../components/CandidateDetail";
import { CandidateTable } from "../components/CandidateTable";
import { StatCard } from "../components/StatCard";
import type { Candidate, CandidateStatus, DashboardStats } from "../types";

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<"all" | CandidateStatus>("all");
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  async function load() {
    const [statsResponse, candidateResponse] = await Promise.all([
      api.get("/analytics/dashboard"),
      api.get("/candidates", { params: { search: query || undefined, status: status === "all" ? undefined : status } })
    ]);
    setStats(statsResponse.data);
    setCandidates(candidateResponse.data);
  }

  async function upload(event: ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files ?? []);
    if (!files.length) return;
    setMessage("");
    setUploading(true);
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    try {
      const { data } = await api.post("/candidates/upload", formData);
      setMessage(`Uploaded ${data.processed} resume${data.processed === 1 ? "" : "s"}.`);
      await load();
    } catch (error: any) {
      setMessage(error.response?.data?.detail ?? error.message ?? "Upload failed");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  async function downloadReport() {
    const { data } = await api.get("/reports/candidates.csv", { responseType: "blob" });
    const url = URL.createObjectURL(data);
    const link = document.createElement("a");
    link.href = url;
    link.download = "talentiq-candidates.csv";
    link.click();
    URL.revokeObjectURL(url);
  }

  async function updateStatus(candidateId: number, nextStatus: CandidateStatus) {
    await api.patch(`/candidates/${candidateId}/status`, { status: nextStatus });
    await load();
  }

  async function deleteCandidate(candidateId: number) {
    if (!window.confirm("Delete this candidate?")) return;
    await api.delete(`/candidates/${candidateId}`);
    if (selectedCandidate?.id === candidateId) {
      setSelectedCandidate(null);
    }
    await load();
  }

  useEffect(() => {
    void load();
  }, [status]);

  return (
    <main className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-semibold">TalentIQ AI</h1>
            <p className="text-sm text-steel">Recruiter dashboard</p>
          </div>
          <div className="flex items-center gap-2">
            <label className="inline-flex h-10 cursor-pointer items-center gap-2 rounded-md bg-ink px-4 text-sm font-medium text-white">
              <Upload size={16} /> {uploading ? "Uploading..." : "Upload Resumes"}
              <input className="hidden" type="file" multiple accept=".pdf,.docx" onChange={upload} />
            </label>
            <button className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-200 px-4 text-sm" onClick={downloadReport}>
              <Download size={16} /> CSV
            </button>
          </div>
        </div>
      </header>
      <section className="mx-auto max-w-7xl px-6 py-6">
        {message ? (
          <div className="mb-4 rounded-md border border-slate-200 bg-white px-4 py-3 text-sm text-steel shadow-sm">
            {message}
          </div>
        ) : null}
        <div className="grid gap-4 md:grid-cols-4">
          <StatCard label="Total Candidates" value={stats?.total_candidates ?? 0} />
          <StatCard label="Average Match" value={`${stats?.average_match_score ?? 0}%`} />
          <StatCard label="Shortlisted" value={stats?.shortlisted_candidates ?? 0} />
          <StatCard label="Rejected" value={stats?.rejected_candidates ?? 0} />
        </div>
        <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_320px]">
          <div>
            <div className="mb-3 flex flex-col gap-3 md:flex-row">
              <div className="flex h-10 flex-1 items-center gap-2 rounded-md border border-slate-200 bg-white px-3">
                <Search size={16} className="text-slate-400" />
                <input className="w-full outline-none" placeholder="Search candidates" value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => event.key === "Enter" && load()} />
              </div>
              <div className="flex rounded-md border border-slate-200 bg-white p-1">
                {(["all", "new", "shortlisted", "rejected"] as const).map((item) => (
                  <button
                    key={item}
                    className={`rounded px-3 py-1 text-sm capitalize ${status === item ? "bg-ink text-white" : "text-steel"}`}
                    onClick={() => setStatus(item)}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
            <CandidateTable candidates={candidates} onStatusChange={updateStatus} onSelect={setSelectedCandidate} onDelete={deleteCandidate} />
          </div>
          <aside className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-semibold">Top Skills</h2>
            <div className="mt-4 space-y-3">
              {(stats?.top_skills ?? []).map(([skill, count]) => (
                <div key={skill}>
                  <div className="flex justify-between text-sm">
                    <span className="capitalize">{skill}</span>
                    <span>{count}</span>
                  </div>
                  <div className="mt-1 h-2 rounded bg-slate-100">
                    <div className="h-2 rounded bg-mint" style={{ width: `${Math.min(count * 10, 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </aside>
        </div>
      </section>
      {selectedCandidate ? <CandidateDetail candidate={selectedCandidate} onClose={() => setSelectedCandidate(null)} /> : null}
    </main>
  );
}
