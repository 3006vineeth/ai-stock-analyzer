export interface StockSearchResult {
  name: string;
  nse_symbol: string;
  bse_symbol: string;
  sector: string;
  industry: string;
}

export interface StockSnapshot {
  name: string;
  nse_symbol: string;
  current_price: number;
  change: number;
  change_percent: number;
  market_cap: string;
  sector: string;
  industry: string;
  pe_ratio?: number;
  pb_ratio?: number;
  dividend_yield?: number;
  week_52_high?: number;
  week_52_low?: number;
  avg_volume?: number;
}

export interface TechnicalIndicator {
  name: string;
  value: any;
  signal: string;
  explanation: string;
}

export interface TechnicalAnalysis {
  trend: string;
  support_levels: number[];
  resistance_levels: number[];
  indicators: TechnicalIndicator[];
  summary: string;
}

export interface CandlestickPattern {
  name: string;
  detected: boolean;
  significance: string;
  confirmation_needed: string;
}

export interface ChartPattern {
  name: string;
  detected: boolean;
  confidence: number;
  reasoning: string;
}

export interface MomentumAnalysis {
  price_momentum: string;
  volume_momentum: string;
  relative_strength: string;
  volatility: string;
  summary: string;
}

export interface FundamentalMetrics {
  revenue_growth?: string;
  profit_growth?: string;
  eps?: number;
  roe?: number;
  roce?: number;
  debt_to_equity?: number;
  free_cash_flow?: string;
  promoter_holding?: number;
  institutional_holding?: number;
  quarterly_performance: string;
  annual_performance: string;
  valuation_assessment: string;
}

export interface NewsItem {
  title: string;
  source: string;
  sentiment: string;
  impact: string;
}

export interface NewsSentiment {
  overall: string;
  items: NewsItem[];
  summary: string;
}

export interface RiskAssessment {
  score: number;
  volatility_risk: string;
  financial_risk: string;
  business_risk: string;
  sector_risk: string;
  market_risk: string;
  reasoning: string;
}

export interface TradingPlan {
  entry_zone: string;
  key_support: string;
  key_resistance: string;
  upside_scenario: string;
  downside_scenario: string;
  stop_loss_area: string;
  risk_reward: string;
  disclaimer: string;
}

export interface AIConfidence {
  trend: number;
  technical_setup: number;
  fundamental_quality: number;
  overall: number;
  reasoning: string;
}

export interface ExecutiveSummary {
  overall_trend: string;
  strengths: string[];
  weaknesses: string[];
  market_sentiment: string;
  short_term_outlook: string;
  long_term_outlook: string;
  key_risks: string[];
}

export interface AnalysisReport {
  ticker: string;
  timestamp: string;
  executive_summary: ExecutiveSummary;
  technical_analysis: TechnicalAnalysis;
  candlestick_patterns: CandlestickPattern[];
  chart_patterns: ChartPattern[];
  trend_strength: string;
  momentum_analysis: MomentumAnalysis;
  fundamental_analysis: FundamentalMetrics;
  news_sentiment: NewsSentiment;
  risk_assessment: RiskAssessment;
  trading_plan: TradingPlan;
  ai_confidence: AIConfidence;
}

export interface ChatMessage {
  role: string;
  content: string;
}

export interface ChatResponse {
  reply: string;
  context?: Record<string, any>;
}
