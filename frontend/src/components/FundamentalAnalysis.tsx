import { FundamentalMetrics } from "@/types";
import { ChevronDown, BookOpen, TrendingUp, DollarSign, Percent, Users, Landmark, Wallet } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  analysis: FundamentalMetrics;
}

export default function FundamentalAnalysisCard({ analysis }: Props) {
  const [expanded, setExpanded] = useState(true);

  const metrics = [
    { label: "Revenue Growth", value: analysis.revenue_growth || "N/A", icon: TrendingUp, good: analysis.revenue_growth && analysis.revenue_growth.includes("up") },
    { label: "Profit Growth", value: analysis.profit_growth || "N/A", icon: TrendingUp, good: analysis.profit_growth && analysis.profit_growth.includes("up") },
    { label: "EPS", value: analysis.eps ? `₹${analysis.eps.toFixed(2)}` : "N/A", icon: DollarSign, good: analysis.eps && analysis.eps > 0 },
    { label: "ROE", value: analysis.roe ? `${analysis.roe}%` : "N/A", icon: Percent, good: analysis.roe && analysis.roe > 15 },
    { label: "ROCE", value: analysis.roce ? `${analysis.roce}%` : "N/A", icon: Percent, good: analysis.roce && analysis.roce > 15 },
    { label: "Debt/Equity", value: analysis.debt_to_equity ? `${analysis.debt_to_equity}x` : "N/A", icon: Landmark, good: analysis.debt_to_equity && analysis.debt_to_equity < 1 },
    { label: "Free Cash Flow", value: analysis.free_cash_flow || "N/A", icon: Wallet, good: analysis.free_cash_flow && !analysis.free_cash_flow.includes("-") },
    { label: "Promoter Holding", value: analysis.promoter_holding ? `${analysis.promoter_holding}%` : "N/A", icon: Users, good: analysis.promoter_holding && analysis.promoter_holding > 50 },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <BookOpen className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Fundamental Analysis</h3>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {metrics.map((m) => (
              <div key={m.label} className={cn(
                "bg-slate-800/50 rounded-lg p-3 border",
                m.good ? "border-emerald-500/20" : "border-slate-700/30"
              )}>
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <m.icon className="w-3.5 h-3.5" />
                  <span className="text-xs">{m.label}</span>
                </div>
                <p className={cn("text-sm font-medium", m.good ? "text-emerald-300" : "text-slate-300")}>
                  {m.value}
                </p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
              <span className="text-xs text-slate-500">Quarterly Performance</span>
              <p className="text-sm text-slate-300 mt-1">{analysis.quarterly_performance}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
              <span className="text-xs text-slate-500">Annual Performance</span>
              <p className="text-sm text-slate-300 mt-1">{analysis.annual_performance}</p>
            </div>
          </div>

          <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4">
            <h4 className="text-sm font-medium text-indigo-300 mb-1">Valuation Assessment</h4>
            <p className="text-sm text-slate-300">{analysis.valuation_assessment}</p>
          </div>
        </div>
      )}
    </div>
  );
}
