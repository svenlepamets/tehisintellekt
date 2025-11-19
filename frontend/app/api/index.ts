import { Settings, Answer, Health } from "@/app/types"

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function postQuestion(question: string, domain: string, service: string): Promise<Answer> {
    const res = await fetch(`${API_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, domain: domain, service: service }),
    });

    if (!res.ok) throw new Error(`Backend error: ${res.status}`);
    const data = await res.json();
    return data
}

export async function fetchSettings(): Promise<Settings> {
    const res = await fetch(`${API_URL}/api/settings`)
    if (!res.ok) throw new Error(`Backend error: ${res.status}`);
    const data = await res.json()
    return data
}

export async function checkHealth(): Promise<Health> {
    const res = await fetch(`${API_URL}/api/health`)
    if (!res.ok) throw new Error(`Backend error: ${res.status}`);
    const data = await res.json()
    return data
}