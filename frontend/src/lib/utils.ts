import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatPercent(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

export function getTrendColor(trend: string): string {
  if (trend.includes("Bullish") || trend.includes("Uptrend")) return "text-emerald-400";
  if (trend.includes("Bearish") || trend.includes("Downtrend")) return "text-rose-400";
  return "text-amber-400";
}

export function getRiskColor(score: number): string {
  if (score <= 3) return "text-emerald-400";
  if (score <= 6) return "text-amber-400";
  return "text-rose-400";
}

export function getConfidenceBadge(confidence: number): string {
  if (confidence >= 0.8) return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
  if (confidence >= 0.6) return "bg-amber-500/20 text-amber-400 border-amber-500/30";
  return "bg-rose-500/20 text-rose-400 border-rose-500/30";
}
