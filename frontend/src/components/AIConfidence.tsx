import { AIConfidence } from "@/types";
import { ChevronDown, Brain, TrendingUp, Wrench, BookOpen, BarChart3 } from "lucide-react";
import { useState } from "react";
import { cn, getConfidenceBadge } from "@/lib/utils";

interface Props {
  confidence: AIConfidence;
}

export default function AIConfidenceCard({ confidence }: Props) {
  const [expanded, setExpanded] = useState(true);

  const items = [
    { label: "Trend", value: confidence.trend, icon: TrendingUp },
    { label: "Technical Setup", value: confidence.technical_setup, icon: Wrench },
    { label: "Fundamental Quality", value: confidence.fundamental_quality, icon: BookOpen },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Brain className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">AI Confidence</h3>
        </div>
        <div className="flex items-center gap-3">
          <span className={cn("px-2 py-0.5 text-xs rounded-full border", getConfidenceBadge(confidence.overall))}>
            {(confidence.overall * 100).toFixed(0)}% Overall
          </span>
          <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
        </div>
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          <div className="space-y-4">
            {items.map((item) => (
              <div key={item.label} className="space-y-1">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-400">
                    <item.icon className="w-4 h-4" />
                    <span className="text-sm">{item.label}</span>
                  </div>
                  <span className={cn("text-sm font-medium", 
                    item.value >= 0.8 ? "text-emerald-400" : item.value >= 0.6 ? "text-amber-400" : "text-rose-400"
                  )}>
                    {(item.value * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    className={cn("h-full rounded-full transition-all duration-500",
                      item.value >= 0.8 ? "bg-emerald-400" : item.value >= 0.6 ? "bg-amber-400" : "bg-rose-400"
                    )}
                    style={{ width: `${item.value * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Overall Analysis Confidence</span>
              <span className={cn("text-lg font-bold",
                confidence.overall >= 0.8 ? "text-emerald-400" : confidence.overall >= 0.6 ? "text-amber-400" : "text-rose-400"
              )}>
                {(confidence.overall * 100).toFixed(0)}%
              </span>
            </div>
            <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
              <div 
                className={cn("h-full rounded-full transition-all duration-500",
                  confidence.overall >= 0.8 ? "bg-emerald-400" : confidence.overall >= 0.6 ? "bg-amber-400" : "bg-rose-400"
                )}
                style={{ width: `${confidence.overall * 100}%` }}
              />
            </div>
          </div>

          <p className="text-sm text-slate-400 leading-relaxed">{confidence.reasoning}</p>
        </div>
      )}
    </div>
  );
}
