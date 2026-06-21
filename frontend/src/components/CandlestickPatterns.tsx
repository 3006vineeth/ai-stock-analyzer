import { CandlestickPattern } from "@/types";
import { ChevronDown, CandlestickChart } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  patterns: CandlestickPattern[];
}

export default function CandlestickPatterns({ patterns }: Props) {
  const [expanded, setExpanded] = useState(true);
  const detected = patterns.filter((p) => p.detected);

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <CandlestickChart className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Candlestick Patterns</h3>
          <span className={cn("px-2 py-0.5 text-xs rounded-full",
            detected.length > 0 ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20" : "bg-slate-700/50 text-slate-500"
          )}>
            {detected.length} detected
          </span>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6">
          {detected.length > 0 ? (
            <div className="space-y-3">
              {detected.map((p, i) => (
                <div key={i} className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-indigo-300">{p.name}</h4>
                    <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-400 text-xs rounded-full border border-indigo-500/20">
                      Detected
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 mb-1">{p.significance}</p>
                  <p className="text-xs text-slate-500">{p.confirmation_needed}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500 py-2">No significant candlestick patterns detected on the latest candles.</p>
          )}

          {/* All patterns grid */}
          <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-2">
            {patterns.map((p, i) => (
              <div key={i} className={cn(
                "px-3 py-2 rounded-lg text-xs text-center border",
                p.detected 
                  ? "bg-indigo-500/10 text-indigo-300 border-indigo-500/20" 
                  : "bg-slate-800/30 text-slate-600 border-slate-700/20"
              )}>
                {p.name}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
