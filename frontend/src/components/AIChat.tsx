"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { sendChatMessage } from "@/lib/api";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Props {
  ticker: string;
}

export default function AIChat({ ticker }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: `I've analyzed ${ticker}. Ask me anything about the technical setup, support levels, risks, or trading scenarios.` },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const response = await sendChatMessage(ticker, userMessage);
      setMessages((prev) => [...prev, { role: "assistant", content: response.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that question. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestions = [
    "Why is RSI important?",
    "Explain the support levels",
    "Is this good for swing trading?",
    "What are the main risks?",
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl overflow-hidden flex flex-col h-[600px]">
      <div className="px-4 py-3 border-b border-slate-700/50 flex items-center gap-2">
        <Bot className="w-5 h-5 text-indigo-400" />
        <h3 className="font-semibold text-slate-100">AI Analyst</h3>
        <span className="text-xs text-slate-500 ml-auto">{ticker}</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={cn("flex gap-3", msg.role === "user" && "flex-row-reverse")}>
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
              msg.role === "assistant" ? "bg-indigo-500/20" : "bg-slate-700"
            )}>
              {msg.role === "assistant" ? (
                <Bot className="w-4 h-4 text-indigo-400" />
              ) : (
                <User className="w-4 h-4 text-slate-400" />
              )}
            </div>
            <div className={cn(
              "max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed",
              msg.role === "assistant" 
                ? "bg-slate-800/80 text-slate-300 border border-slate-700/30" 
                : "bg-indigo-500/20 text-indigo-100 border border-indigo-500/20"
            )}>
              {msg.content}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="bg-slate-800/80 rounded-xl px-4 py-3 border border-slate-700/30">
              <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
            </div>
          </div>
        )}
        <div ref={scrollRef} />

        {/* Suggestions */}
        {messages.length === 1 && (
          <div className="pt-2">
            <p className="text-xs text-slate-500 mb-2">Suggested questions:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => { setInput(s); }}
                  className="px-3 py-1.5 bg-slate-800/50 border border-slate-700/30 rounded-lg text-xs text-slate-400 hover:text-slate-200 hover:border-slate-600 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="p-3 border-t border-slate-700/50">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask about this analysis..."
            className="flex-1 px-4 py-2.5 bg-slate-800/80 border border-slate-700/50 rounded-xl text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500/30"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-4 py-2.5 bg-indigo-500/20 border border-indigo-500/30 rounded-xl text-indigo-400 hover:bg-indigo-500/30 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
