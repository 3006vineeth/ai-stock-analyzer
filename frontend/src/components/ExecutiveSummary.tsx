import { ExecutiveSummary } from "@/types";
import { ChevronDown, AlertTriangle, ThumbsUp, ThumbsDown, Eye, Calendar } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  summary: ExecutiveSummary;
}

export default function ExecutiveSummaryCard({ summary }: Props) {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Eye className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">AI Executive Summary</h3>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-5">
          <p className="text-slate-300 leading-relaxed">{summary.overall_trend}</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <ThumbsUp className="w-4 h-4 text-emerald-400" />
                <h4 className="font-medium text-emerald-300">Strengths</h4>
              </div>
              <ul className="space-y-2">
                {summary.strengths.map((s, i) => (
                  <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-emerald-400 mt-1">•</span>{s}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <ThumbsDown className="w-4 h-4 text-rose-400" />
                <h4 className="font-medium text-rose-300">Weaknesses</h4>
              </div>
              <ul className="space-y-2">
                {summary.weaknesses.map((w, i) => (
                  <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-rose-400 mt-1">•</span>{w}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-slate-500 mb-1">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span className="text-xs">Market Sentiment</span>
              </div>
              <p className="text-sm font-medium text-slate-200">{summary.market_sentiment}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-slate-500 mb-1">
                <Calendar className="w-3.5 h-3.5" />
                <span className="text-xs">Short-term</span>
              </div>
              <p className="text-sm font-medium text-slate-200">{summary.short_term_outlook}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-slate-500 mb-1">
                <Calendar className="w-3.5 h-3.5" />
                <span className="text-xs">Long-term</span>
              </div>
              <p className="text-sm font-medium text-slate-200">{summary.long_term_outlook}</p>
            </div>
          </div>

          <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4">
            <h4 className="text-sm font-medium text-amber-300 mb-2">Key Risks</h4>
            <div className="flex flex-wrap gap-2">
              {summary.key_risks.map((r, i) => (
                <span key={i} className="px-3 py-1 bg-amber-500/10 text-amber-300 text-xs rounded-full border border-amber-500/20">
                  {r}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
