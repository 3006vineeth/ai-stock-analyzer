import { RiskAssessment } from "@/types";
import { ChevronDown, ShieldAlert, AlertTriangle, TrendingUp, Building2, Layers, Globe } from "lucide-react";
import { useState } from "react";
import { cn, getRiskColor } from "@/lib/utils";

interface Props {
  risk: RiskAssessment;
}

export default function RiskAssessmentCard({ risk }: Props) {
  const [expanded, setExpanded] = useState(true);

  const riskItems = [
    { label: "Volatility", value: risk.volatility_risk, icon: TrendingUp },
    { label: "Financial", value: risk.financial_risk, icon: Building2 },
    { label: "Business", value: risk.business_risk, icon: Layers },
    { label: "Sector", value: risk.sector_risk, icon: Layers },
    { label: "Market", value: risk.market_risk, icon: Globe },
  ];

  const scoreColor = getRiskColor(risk.score);

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <ShieldAlert className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Risk Assessment</h3>
        </div>
        <div className="flex items-center gap-3">
          <span className={cn("px-3 py-1 text-sm font-bold rounded-full border", scoreColor.replace("text-", "bg-").replace("400", "500/10") + " " + scoreColor + " border-" + scoreColor.replace("text-", "").replace("400", "500/20"))}>
            {risk.score}/10
          </span>
          <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
        </div>
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          {/* Risk Score Gauge */}
          <div className="bg-slate-800/50 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-slate-400">Overall Risk Score</span>
              <span className={cn("text-2xl font-bold", scoreColor)}>{risk.score}</span>
            </div>
            <div className="h-4 bg-slate-700 rounded-full overflow-hidden flex">
              <div className="flex-1 bg-emerald-500/30" />
              <div className="flex-1 bg-amber-500/30" />
              <div className="flex-1 bg-rose-500/30" />
              <div className="flex-1 bg-rose-700/30" />
            </div>
            <div className="flex justify-between mt-1 text-xs text-slate-500">
              <span>Low (1-3)</span>
              <span>Moderate (4-6)</span>
              <span>High (7-8)</span>
              <span>Very High (9-10)</span>
            </div>
            <div className="relative h-0">
              <div
                className={cn("absolute -top-5 w-3 h-3 rounded-full border-2 border-white shadow", scoreColor.replace("text-", "bg-"))}
                style={{ left: `${(risk.score / 10) * 100}%`, transform: "translateX(-50%)" }}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {riskItems.map((item) => (
              <div key={item.label} className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
                <div className="flex items-center gap-2 text-slate-500 mb-1">
                  <item.icon className="w-3.5 h-3.5" />
                  <span className="text-xs">{item.label} Risk</span>
                </div>
                <p className="text-sm text-slate-300">{item.value}</p>
              </div>
            ))}
          </div>

          <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4 flex gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <p className="text-sm text-slate-300">{risk.reasoning}</p>
          </div>
        </div>
      )}
    </div>
  );
}
