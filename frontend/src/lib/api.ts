import { StockSnapshot, AnalysisReport, ChatResponse } from "@/types";
import type { StockSearchResult } from "@/types";
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function searchStocks(query: string): Promise<StockSearchResult[]> {
  const res = await fetch(`${API_BASE}/stocks/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error("Search failed");
  const data = await res.json();
  return data.results || [];
}

export async function getStockSnapshot(ticker: string): Promise<StockSnapshot> {
  const res = await fetch(`${API_BASE}/stocks/${encodeURIComponent(ticker)}/snapshot`);
  if (!res.ok) throw new Error("Snapshot failed");
  return res.json();
}

export async function analyzeStock(ticker: string): Promise<AnalysisReport> {
  const res = await fetch(`${API_BASE}/analysis/${encodeURIComponent(ticker)}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Analysis failed");
  return res.json();
}

export async function sendChatMessage(ticker: string, message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker, message }),
  });
  if (!res.ok) throw new Error("Chat failed");
  return res.json();
}
