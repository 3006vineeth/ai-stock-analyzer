import { StockSnapshot } from "@/types";
import { TrendingUp, TrendingDown, BarChart3, Building2, Layers, Percent, ArrowUpDown, Activity } from "lucide-react";
import { formatCurrency, formatPercent, cn } from "@/lib/utils";

interface Props {
  snapshot: StockSnapshot;
}

export default function CompanySnapshot({ snapshot }: Props) {
  const isPositive = snapshot.change >= 0;

  const metrics = [
    { label: "Market Cap", value: snapshot.market_cap, icon: Building2 },
    { label: "Sector", value: snapshot.sector, icon: Layers },
    { label: "Industry", value: snapshot.industry, icon: Activity },
    { label: "PE Ratio", value: snapshot.pe_ratio?.toFixed(2) || "N/A", icon: Percent },
    { label: "PB Ratio", value: snapshot.pb_ratio?.toFixed(2) || "N/A", icon: BarChart3 },
    { label: "Div Yield", value: snapshot.dividend_yield ? `${snapshot.dividend_yield}%` : "N/A", icon: Percent },
    { label: "52W High", value: snapshot.week_52_high ? formatCurrency(snapshot.week_52_high) : "N/A", icon: TrendingUp },
    { label: "52W Low", value: snapshot.week_52_low ? formatCurrency(snapshot.week_52_low) : "N/A", icon: TrendingDown },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">{snapshot.name}</h2>
          <p className="text-slate-500 text-sm">{snapshot.nse_symbol}</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-slate-100">{formatCurrency(snapshot.current_price)}</p>
          <p className={cn("text-sm font-medium", isPositive ? "text-emerald-400" : "text-rose-400")}>
            {isPositive ? "+" : ""}{snapshot.change.toFixed(2)} ({formatPercent(snapshot.change_percent)})
          </p>
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {metrics.map((m) => (
          <div key={m.label} className="bg-slate-800/50 rounded-lg p-3">
            <div className="flex items-center gap-2 text-slate-500 mb-1">
              <m.icon className="w-3.5 h-3.5" />
              <span className="text-xs">{m.label}</span>
            </div>
            <p className="text-sm font-medium text-slate-200">{m.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
