import { FormEvent, useState } from "react";
import { api } from "../api/client";

export function Login({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("hr@example.com");
  const [password, setPassword] = useState("password");
  const [fullName, setFullName] = useState("HR Manager");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const path = mode === "login" ? "/auth/login" : "/auth/register";
      const payload = mode === "login" ? { email, password } : { email, password, full_name: fullName, role: "hr" };
      const { data } = await api.post(path, payload);
      localStorage.setItem("talentiq_token", data.access_token);
      onLogin();
    } catch (requestError: any) {
      setError(requestError.response?.data?.detail ?? requestError.message ?? "Request failed");
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-100 px-4">
      <form onSubmit={submit} className="w-full max-w-sm rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-semibold text-ink">TalentIQ AI</h1>
        <p className="mt-1 text-sm text-steel">{mode === "login" ? "Recruiter login" : "Create HR account"}</p>
        {mode === "register" ? (
          <>
            <label className="mt-6 block text-sm font-medium">Full name</label>
            <input className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </>
        ) : null}
        <label className={`${mode === "register" ? "mt-4" : "mt-6"} block text-sm font-medium`}>Email</label>
        <input className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3" value={email} onChange={(e) => setEmail(e.target.value)} />
        <label className="mt-4 block text-sm font-medium">Password</label>
        <input className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error ? <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
        <button className="mt-6 h-10 w-full rounded-md bg-ink px-4 font-medium text-white">{mode === "login" ? "Sign in" : "Create account"}</button>
        <button type="button" className="mt-3 h-10 w-full rounded-md border border-slate-200 px-4 text-sm text-steel" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Create first HR account" : "Back to sign in"}
        </button>
      </form>
    </main>
  );
}
