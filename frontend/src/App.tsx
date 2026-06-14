import { useEffect, useState } from "react";
import { Dashboard } from "./pages/Dashboard";
import { JobAnalyzer } from "./pages/JobAnalyzer";
import { Login } from "./pages/Login";

export default function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(localStorage.getItem("talentiq_token")));
  const [view, setView] = useState<"dashboard" | "jobs">("dashboard");

  useEffect(() => {
    function logout() {
      setAuthenticated(false);
    }
    window.addEventListener("talentiq:logout", logout);
    return () => window.removeEventListener("talentiq:logout", logout);
  }, []);

  if (!authenticated) {
    return <Login onLogin={() => setAuthenticated(true)} />;
  }

  function logout() {
    localStorage.removeItem("talentiq_token");
    setAuthenticated(false);
    setView("dashboard");
  }

  return (
    <>
      <nav className="border-b border-slate-200 bg-white px-6">
        <div className="mx-auto flex max-w-7xl items-center justify-between py-2">
          <div className="flex gap-2">
            <button className={`rounded-md px-3 py-2 text-sm ${view === "dashboard" ? "bg-ink text-white" : "text-steel"}`} onClick={() => setView("dashboard")}>Dashboard</button>
            <button className={`rounded-md px-3 py-2 text-sm ${view === "jobs" ? "bg-ink text-white" : "text-steel"}`} onClick={() => setView("jobs")}>JD Analyzer</button>
          </div>
          <button className="rounded-md border border-slate-200 px-3 py-2 text-sm text-steel" onClick={logout}>Logout</button>
        </div>
      </nav>
      {view === "dashboard" ? <Dashboard /> : <div className="mx-auto max-w-5xl px-6 py-6"><JobAnalyzer /></div>}
    </>
  );
}
