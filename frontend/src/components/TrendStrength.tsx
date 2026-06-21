import { TrendingUp, TrendingDown, Activity, Minus, ChevronDown } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  trend: string;
  confidence: number;
}

const TREND_CONFIG: Record<string, { color: string; bg: string; border: string; icon: any }> = {
  "Strong Bullish": { color: "text-emerald-300", bg: "bg-emerald-500/10", border: "border-emerald-500/20", icon: TrendingUp },
  "Bullish": { color: "text-emerald-400", bg: "bg-emerald-500/5", border: "border-emerald-500/10", icon: TrendingUp },
  "Neutral": { color: "text-amber-400", bg: "bg-amber-500/5", border: "border-amber-500/10", icon: Minus },
  "Bearish": { color: "text-rose-400", bg: "bg-rose-500/5", border: "border-rose-500/10", icon: TrendingDown },
  "Strong Bearish": { color: "text-rose-300", bg: "bg-rose-500/10", border: "border-rose-500/20", icon: TrendingDown },
};

export default function TrendStrength({ trend, confidence }: Props) {
  const [expanded, setExpanded] = useState(true);
  const config = TREND_CONFIG[trend] || TREND_CONFIG["Neutral"];
  const Icon = config.icon;

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Activity className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Trend Strength</h3>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6">
          <div className={cn("rounded-xl p-6 border", config.bg, config.border)}>
            <div className="flex items-center gap-4">
              <div className={cn("w-14 h-14 rounded-full flex items-center justify-center", config.bg, "border", config.border)}>
                <Icon className={cn("w-7 h-7", config.color)} />
              </div>
              <div>
                <h4 className={cn("text-2xl font-bold", config.color)}>{trend}</h4>
                <p className="text-sm text-slate-400 mt-1">
                  Confidence: {(confidence * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            {/* Trend meter */}
            <div className="mt-6">
              <div className="flex justify-between text-xs text-slate-500 mb-2">
                <span>Strong Bearish</span>
                <span>Neutral</span>
                <span>Strong Bullish</span>
              </div>
              <div className="h-3 bg-slate-700 rounded-full overflow-hidden flex">
                <div className="flex-1 bg-gradient-to-r from-rose-600 to-rose-400" />
                <div className="flex-1 bg-gradient-to-r from-rose-400 to-amber-400" />
                <div className="flex-1 bg-gradient-to-r from-amber-400 to-emerald-400" />
                <div className="flex-1 bg-gradient-to-r from-emerald-400 to-emerald-600" />
              </div>
              {/* Marker */}
              <div className="relative h-0">
                <div
                  className="absolute -top-4 w-4 h-4 bg-white rounded-full border-2 border-slate-600 shadow-lg"
                  style={{ left: `${((confidence * 100) + 50)}%`, transform: "translateX(-50%)" }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
