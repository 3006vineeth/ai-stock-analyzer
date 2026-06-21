import { ChartPattern } from "@/types";
import { ChevronDown, Shapes } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  patterns: ChartPattern[];
}

export default function ChartPatterns({ patterns }: Props) {
  const [expanded, setExpanded] = useState(true);
  const detected = patterns.filter((p) => p.detected);

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Shapes className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Chart Patterns</h3>
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
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-indigo-400 rounded-full"
                          style={{ width: `${p.confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-xs text-indigo-400">{(p.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                  <p className="text-sm text-slate-300">{p.reasoning}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500 py-2">No significant chart patterns detected in recent price action.</p>
          )}

          <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-2">
            {patterns.map((p, i) => (
              <div key={i} className={cn(
                "px-3 py-2 rounded-lg text-xs border flex items-center justify-between",
                p.detected 
                  ? "bg-indigo-500/10 text-indigo-300 border-indigo-500/20" 
                  : "bg-slate-800/30 text-slate-600 border-slate-700/20"
              )}>
                <span>{p.name}</span>
                {p.detected && <span className="text-indigo-400">{(p.confidence * 100).toFixed(0)}%</span>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
