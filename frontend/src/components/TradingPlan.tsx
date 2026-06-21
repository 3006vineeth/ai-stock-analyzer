import { TradingPlan } from "@/types";
import { ChevronDown, Target, ArrowUp, ArrowDown, Shield, Crosshair, TrendingUp, AlertCircle } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  plan: TradingPlan;
}

export default function TradingPlanCard({ plan }: Props) {
  const [expanded, setExpanded] = useState(true);

  const items = [
    { label: "Entry Zone", value: plan.entry_zone, icon: Target, color: "text-indigo-400" },
    { label: "Key Support", value: plan.key_support, icon: ArrowDown, color: "text-emerald-400" },
    { label: "Key Resistance", value: plan.key_resistance, icon: ArrowUp, color: "text-rose-400" },
    { label: "Upside Scenario", value: plan.upside_scenario, icon: TrendingUp, color: "text-emerald-400" },
    { label: "Downside Scenario", value: plan.downside_scenario, icon: TrendingUp, color: "text-rose-400" },
    { label: "Stop Loss Area", value: plan.stop_loss_area, icon: Shield, color: "text-amber-400" },
    { label: "Risk:Reward", value: plan.risk_reward, icon: Crosshair, color: "text-indigo-400" },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Target className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">Trading Plan</h3>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {items.map((item) => (
              <div key={item.label} className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/30">
                <div className={cn("flex items-center gap-2 mb-1", item.color)}>
                  <item.icon className="w-3.5 h-3.5" />
                  <span className="text-xs">{item.label}</span>
                </div>
                <p className="text-sm font-medium text-slate-200">{item.value}</p>
              </div>
            ))}
          </div>

          <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4 flex gap-3">
            <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-amber-300 mb-1">Disclaimer</p>
              <p className="text-sm text-slate-400">{plan.disclaimer} These are analytical scenarios based on technical and fundamental data, not guarantees of future performance. Always do your own research and consider your risk tolerance before making any investment decisions.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
