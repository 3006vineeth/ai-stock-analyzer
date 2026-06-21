"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Search, TrendingUp, BarChart3, ShieldCheck, Brain } from "lucide-react";
import { cn } from "@/lib/utils";
import { searchStocks } from "@/lib/api";
import type { StockSearchResult } from "@/types";

const POPULAR_STOCKS = [
  { name: "Reliance Industries", ticker: "RELIANCE.NS", sector: "Energy" },
  { name: "Tata Motors", ticker: "TATAMOTORS.NS", sector: "Automotive" },
  { name: "Infosys", ticker: "INFY.NS", sector: "IT" },
  { name: "HDFC Bank", ticker: "HDFCBANK.NS", sector: "Banking" },
  { name: "ICICI Bank", ticker: "ICICIBANK.NS", sector: "Banking" },
  { name: "TCS", ticker: "TCS.NS", sector: "IT" },
];

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<StockSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);

  const handleSearch = useCallback(async (value: string) => {
    setQuery(value);
    if (value.length < 2) {
      setResults([]);
      setShowDropdown(false);
      return;
    }
    setLoading(true);
    try {
      const data = await searchStocks(value);
      setResults(data);
      setShowDropdown(true);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSelect = (ticker: string) => {
    setShowDropdown(false);
    router.push(`/analysis/${encodeURIComponent(ticker)}`);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 relative overflow-hidden">
      {/* Background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_80%)]" />
      
      <div className="relative z-10 w-full max-w-2xl text-center space-y-8">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Brain className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI Stock Analyzer
          </h1>
        </div>

        <p className="text-slate-400 text-lg max-w-md mx-auto">
          Professional AI-powered stock analysis for the Indian market. Understand any stock in seconds.
        </p>

        {/* Search Bar */}
        <div className="relative w-full max-w-xl mx-auto">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => handleSearch(e.target.value)}
              placeholder="Search by company name or ticker (e.g., Reliance, TCS, HDFC)"
              className="w-full pl-12 pr-4 py-4 bg-slate-800/80 border border-slate-700 rounded-2xl text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
            />
            {loading && (
              <div className="absolute right-4 top-1/2 -translate-y-1/2">
                <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
              </div>
            )}
          </div>

          {/* Dropdown */}
          {showDropdown && results.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-slate-800 border border-slate-700 rounded-xl shadow-2xl overflow-hidden z-50">
              {results.map((stock) => (
                <button
                  key={stock.nse_symbol}
                  onClick={() => handleSelect(stock.nse_symbol)}
                  className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-700/50 transition-colors text-left"
                >
                  <div>
                    <p className="font-medium text-slate-100">{stock.name}</p>
                    <p className="text-sm text-slate-400">{stock.nse_symbol} • {stock.sector}</p>
                  </div>
                  <BarChart3 className="w-4 h-4 text-slate-500" />
                </button>
              ))}
            </div>
          )}
          {showDropdown && query.length >= 2 && results.length === 0 && !loading && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-slate-800 border border-slate-700 rounded-xl shadow-2xl p-4 text-slate-400 text-center z-50">
              No stocks found
            </div>
          )}
        </div>

        {/* Popular Stocks */}
        <div className="space-y-3">
          <p className="text-sm text-slate-500 font-medium">Popular Stocks</p>
          <div className="flex flex-wrap justify-center gap-2">
            {POPULAR_STOCKS.map((stock) => (
              <button
                key={stock.ticker}
                onClick={() => handleSelect(stock.ticker)}
                className="px-4 py-2 bg-slate-800/60 border border-slate-700/50 rounded-lg text-sm text-slate-300 hover:bg-slate-700/60 hover:border-slate-600 transition-all"
              >
                {stock.name}
              </button>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-8">
          {[
            { icon: TrendingUp, title: "Technical Analysis", desc: "20+ indicators & patterns" },
            { icon: BarChart3, title: "Fundamental Analysis", desc: "Financial health & valuation" },
            { icon: ShieldCheck, title: "Risk Assessment", desc: "Multi-factor risk scoring" },
          ].map((feature) => (
            <div key={feature.title} className="p-4 bg-slate-800/40 border border-slate-700/30 rounded-xl">
              <feature.icon className="w-6 h-6 text-indigo-400 mb-2" />
              <h3 className="font-medium text-slate-200">{feature.title}</h3>
              <p className="text-sm text-slate-500">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
