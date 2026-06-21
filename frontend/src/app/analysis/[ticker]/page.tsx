"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, Loader2 } from "lucide-react";
import Link from "next/link";
import { analyzeStock, getStockSnapshot } from "@/lib/api";
import { AnalysisReport, StockSnapshot } from "@/types";
import CompanySnapshot from "@/components/CompanySnapshot";
import ExecutiveSummary from "@/components/ExecutiveSummary";
import TechnicalAnalysis from "@/components/TechnicalAnalysis";
import CandlestickPatterns from "@/components/CandlestickPatterns";
import ChartPatterns from "@/components/ChartPatterns";
import TrendStrength from "@/components/TrendStrength";
import MomentumAnalysis from "@/components/MomentumAnalysis";
import FundamentalAnalysis from "@/components/FundamentalAnalysis";
import NewsSentiment from "@/components/NewsSentiment";
import RiskAssessment from "@/components/RiskAssessment";
import TradingPlan from "@/components/TradingPlan";
import AIConfidence from "@/components/AIConfidence";
import AIChat from "@/components/AIChat";

export default function AnalysisPage() {
  const params = useParams();
  const ticker = decodeURIComponent(params.ticker as string);
  
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [snapshot, setSnapshot] = useState<StockSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [reportData, snapshotData] = await Promise.all([
          analyzeStock(ticker),
          getStockSnapshot(ticker),
        ]);
        setReport(reportData);
        setSnapshot(snapshotData);
      } catch (err: any) {
        setError(err.message || "Failed to load analysis");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [ticker]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <Loader2 className="w-10 h-10 animate-spin text-indigo-400 mx-auto" />
          <p className="text-slate-400">Analyzing {ticker}...</p>
          <p className="text-xs text-slate-600">Fetching market data and running AI analysis</p>
        </div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <p className="text-rose-400">{error || "Something went wrong"}</p>
          <Link href="/" className="text-indigo-400 hover:text-indigo-300 underline">
            Go back home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link href="/" className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
            <ArrowLeft className="w-5 h-5 text-slate-400" />
          </Link>
          <div>
            <h1 className="text-lg font-semibold text-slate-100">{snapshot?.name || ticker}</h1>
            <p className="text-sm text-slate-500">{ticker} • {snapshot?.sector}</p>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Analysis Column */}
          <div className="lg:col-span-2 space-y-6">
            {snapshot && <CompanySnapshot snapshot={snapshot} />}
            <ExecutiveSummary summary={report.executive_summary} />
            <TrendStrength trend={report.trend_strength} confidence={report.ai_confidence.trend} />
            <TechnicalAnalysis analysis={report.technical_analysis} />
            <CandlestickPatterns patterns={report.candlestick_patterns} />
            <ChartPatterns patterns={report.chart_patterns} />
            <MomentumAnalysis analysis={report.momentum_analysis} />
            <FundamentalAnalysis analysis={report.fundamental_analysis} />
            <NewsSentiment sentiment={report.news_sentiment} />
            <RiskAssessment risk={report.risk_assessment} />
            <TradingPlan plan={report.trading_plan} />
            <AIConfidence confidence={report.ai_confidence} />
          </div>

          {/* Chat Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-20">
              <AIChat ticker={ticker} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
