import { MomentumAnalysis } from "@/types";
import { ChevronDown, Zap, TrendingUp, Volume2, BarChart3 } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  analysis: MomentumAnalysis;
}

export default function MomentumAnalysisCard({ analysis }: Props) {
  const [expanded, setExpanded] = useState(true);

  const items = [
    { label: "Price Momentum", value: analysis.price_momentum, icon: TrendingUp },
    { label: "Volume Momentum", value: analysis.volume_momentum, icon: Volume2 },
    { label: "Relative Strength", value: analysis.relative_strength, icon: BarChart3 },
    { label: "Volatility", value: analysis.volatility, icon: Zap },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Zap className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Momentum Analysis</h3>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {items.map((item) => (
              <div key={item.label} className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <item.icon className="w-3.5 h-3.5" />
                  <span className="text-xs">{item.label}</span>
                </div>
                <p className="text-sm text-slate-300">{item.value}</p>
              </div>
            ))}
          </div>
          <p className="text-sm text-slate-400 leading-relaxed bg-slate-800/30 rounded-lg p-3">{analysis.summary}</p>
        </div>
      )}
    </div>
  );
}
