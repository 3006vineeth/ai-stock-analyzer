import { TechnicalAnalysis } from "@/types";
import { ChevronDown, Activity, ArrowUp, ArrowDown, Minus } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  analysis: TechnicalAnalysis;
}

export default function TechnicalAnalysisCard({ analysis }: Props) {
  const [expanded, setExpanded] = useState(true);

  const getSignalIcon = (signal: string) => {
    if (signal.includes("Bullish") || signal.includes("Above") || signal.includes("Buy") || signal.includes("Positive")) {
      return <ArrowUp className="w-3.5 h-3.5 text-emerald-400" />;
    }
    if (signal.includes("Bearish") || signal.includes("Below") || signal.includes("Sell") || signal.includes("Negative")) {
      return <ArrowDown className="w-3.5 h-3.5 text-rose-400" />;
    }
    return <Minus className="w-3.5 h-3.5 text-amber-400" />;
  };

  const getSignalColor = (signal: string) => {
    if (signal.includes("Bullish") || signal.includes("Above") || signal.includes("Buy") || signal.includes("Positive") || signal.includes("Overbought")) {
      return "text-emerald-400";
    }
    if (signal.includes("Bearish") || signal.includes("Below") || signal.includes("Sell") || signal.includes("Negative") || signal.includes("Oversold")) {
      return "text-rose-400";
    }
    return "text-amber-400";
  };

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Activity className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Technical Analysis</h3>
          <span className={cn("px-2 py-0.5 text-xs rounded-full border", 
            analysis.trend.includes("Uptrend") ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
            analysis.trend.includes("Downtrend") ? "bg-rose-500/10 text-rose-400 border-rose-500/20" :
            "bg-amber-500/10 text-amber-400 border-amber-500/20"
          )}>
            {analysis.trend}
          </span>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-5">
          {/* Support / Resistance */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-4">
              <h4 className="text-sm font-medium text-emerald-300 mb-2">Support Levels</h4>
              <div className="flex flex-wrap gap-2">
                {analysis.support_levels.map((level, i) => (
                  <span key={i} className="px-3 py-1 bg-emerald-500/10 text-emerald-300 text-sm font-medium rounded-lg">
                    ₹{level.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
                  </span>
                ))}
                {analysis.support_levels.length === 0 && (
                  <span className="text-sm text-slate-500">No clear support levels</span>
                )}
              </div>
            </div>
            <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-4">
              <h4 className="text-sm font-medium text-rose-300 mb-2">Resistance Levels</h4>
              <div className="flex flex-wrap gap-2">
                {analysis.resistance_levels.map((level, i) => (
                  <span key={i} className="px-3 py-1 bg-rose-500/10 text-rose-300 text-sm font-medium rounded-lg">
                    ₹{level.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
                  </span>
                ))}
                {analysis.resistance_levels.length === 0 && (
                  <span className="text-sm text-slate-500">No clear resistance levels</span>
                )}
              </div>
            </div>
          </div>

          {/* Indicators */}
          <div>
            <h4 className="text-sm font-medium text-slate-400 mb-3">Indicators</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {analysis.indicators.map((ind, i) => (
                <div key={i} className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-slate-300">{ind.name}</span>
                    <div className="flex items-center gap-1.5">
                      {getSignalIcon(ind.signal)}
                      <span className={cn("text-xs font-medium", getSignalColor(ind.signal))}>
                        {ind.signal}
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{ind.explanation}</p>
                </div>
              ))}
            </div>
          </div>

          <p className="text-sm text-slate-400 leading-relaxed bg-slate-800/30 rounded-lg p-3">{analysis.summary}</p>
        </div>
      )}
    </div>
  );
}
