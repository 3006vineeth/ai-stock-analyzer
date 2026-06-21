import { NewsSentiment } from "@/types";
import { ChevronDown, Newspaper, ThumbsUp, ThumbsDown, Minus } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  sentiment: NewsSentiment;
}

const sentimentConfig = {
  Positive: { color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/20", icon: ThumbsUp },
  Negative: { color: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/20", icon: ThumbsDown },
  Neutral: { color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/20", icon: Minus },
};

export default function NewsSentimentCard({ sentiment }: Props) {
  const [expanded, setExpanded] = useState(true);
  const overall = sentimentConfig[sentiment.overall as keyof typeof sentimentConfig] || sentimentConfig.Neutral;
  const OverallIcon = overall.icon;

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Newspaper className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-semibold text-slate-100">News & Sentiment</h3>
        </div>
        <div className="flex items-center gap-3">
          <span className={cn("px-2 py-0.5 text-xs rounded-full border flex items-center gap-1", overall.bg, overall.border, overall.color)}>
            <OverallIcon className="w-3 h-3" />
            {sentiment.overall}
          </span>
          <ChevronDown className={cn("w-5 h-5 text-slate-500 transition-transform", expanded && "rotate-180")} />
        </div>
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-4">
          <p className="text-sm text-slate-400">{sentiment.summary}</p>
          
          <div className="space-y-3">
            {sentiment.items.map((item, i) => {
              const cfg = sentimentConfig[item.sentiment as keyof typeof sentimentConfig] || sentimentConfig.Neutral;
              const ItemIcon = cfg.icon;
              return (
                <div key={i} className={cn("bg-slate-800/50 rounded-lg p-3 border", cfg.border)}>
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <p className="text-sm text-slate-200">{item.title}</p>
                      <p className="text-xs text-slate-500 mt-1">{item.source}</p>
                    </div>
                    <span className={cn("px-2 py-0.5 text-xs rounded-full flex items-center gap-1 shrink-0", cfg.bg, cfg.color)}>
                      <ItemIcon className="w-3 h-3" />
                      {item.sentiment}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-2">{item.impact}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
