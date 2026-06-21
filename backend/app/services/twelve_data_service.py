import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

import httpx
import pandas as pd
from fastapi import HTTPException

from app.config import TWELVEDATA_API_KEY

logger = logging.getLogger(__name__)


class _CacheEntry:
    """Simple in-memory cache entry with timestamp."""

    def __init__(self, data: Any, timestamp: float) -> None:
        self.data = data
        self.timestamp = timestamp
    

class TwelveDataService:
    """Async-capable market data service backed by Twelve Data REST API.

    Provides stock search, quotes, company profiles, historical time series,
    and snapshot assembly for Indian equities (NSE / BSE).
    """

    BASE_URL: str = "https://api.twelvedata.com"
    TTL: int = 60  # seconds

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or TWELVEDATA_API_KEY
        if not self.api_key:
            logger.warning(
                "TwelveData API key is not configured. "
                "Set TWELVEDATA_API_KEY in your .env file."
            )
        self._cache: Dict[str, _CacheEntry] = {}
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={"Accept": "application/json"},
        )
    def normalize_symbol(self, symbol: str) -> str:
        """
        Convert Yahoo Finance symbols to Twelve Data format.
        """

        if symbol.endswith(".NS"):
            return symbol.replace(".NS", ":NSE")

        if symbol.endswith(".BO"):
            return symbol.replace(".BO", ":BSE")

        return symbol

    # ── Cache helpers ─────────────────────────────────────────────

    def _cache_key(self, method: str, symbol: str) -> str:
        return f"{method}:{symbol.upper()}"

    def _get_cached(self, key: str) -> Any:
        entry = self._cache.get(key)
        if entry is not None and (time.time() - entry.timestamp) < self.TTL:
            logger.debug("Cache hit for %s", key)
            return entry.data
        return None

    def _set_cached(self, key: str, data: Any) -> None:
        self._cache[key] = _CacheEntry(data, time.time())
        logger.debug("Cache set for %s", key)

    # ── HTTP helpers ────────────────────────────────────────────────

    def _handle_http_error(self, response: httpx.Response) -> None:
        """Raise FastAPI HTTPException for known status codes."""
        if response.status_code == 401:
            logger.error("TwelveData API 401 Unauthorized — check TWELVEDATA_API_KEY")
            raise HTTPException(
                status_code=401, detail="TwelveData API key is invalid"
            )
        elif response.status_code == 403:
            logger.error("TwelveData API 403 Forbidden")
            raise HTTPException(
                status_code=403, detail="TwelveData API access is forbidden"
            )
        elif response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Requested resource not found on TwelveData",
            )
        elif response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="TwelveData API rate limit exceeded. Please retry later.",
            )
        elif response.status_code >= 500:
            logger.error(
                "TwelveData API %s Server Error", response.status_code
            )
            raise HTTPException(
                status_code=502, detail="TwelveData API is experiencing issues"
            )

    async def _request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an async GET against the Twelve Data API.

        Args:
            endpoint: Twelve Data endpoint path (e.g. ``quote``).
            params: Query parameters excluding ``apikey``.

        Returns:
            Parsed JSON response dict.

        Raises:
            HTTPException: On HTTP errors, timeouts, connection issues,
                or Twelve Data ``status == error``.
        """
        params = {k: v for k, v in params.items() if v is not None}
        params["apikey"] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"

        safe_params = {k: v for k, v in params.items() if k != "apikey"}
        logger.info(
            "TwelveData request: %s params=%s", endpoint, safe_params
        )

        try:
            response = await self._client.get(url, params=params)
            print("\nURL:", response.request.url)
            print("STATUS:", response.status_code)
            print("BODY:", response.text)
            self._handle_http_error(response)
            data = response.json()

            # Twelve Data embeds errors inside JSON for some failures
            if data.get("status") == "error":
                msg = data.get("message", "Unknown TwelveData error")
                logger.error("TwelveData API error: %s", msg)
                raise HTTPException(
                    status_code=400, detail=f"TwelveData error: {msg}"
                )

            return data
        except httpx.TimeoutException:
            logger.error("TwelveData request timeout: %s", endpoint)
            raise HTTPException(
                status_code=504,
                detail="TwelveData API request timed out",
            )
        except httpx.ConnectError:
            logger.error("TwelveData connection error: %s", endpoint)
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to TwelveData API",
            )
        except HTTPException:
            raise
        except Exception as exc:
            logger.error("TwelveData unexpected error: %s", exc)
            raise HTTPException(
                status_code=500,
                detail=f"TwelveData client error: {str(exc)}",
            )

    # ── Public API methods ─────────────────────────────────────────

    async def search_stock(self, query: str) -> Dict[str, Any]:
        """Search for stock symbols using Twelve Data Symbol Search.

        Args:
            query: Search term (e.g. ``TCS``, ``Infosys``).

        Returns:
            Raw Twelve Data JSON response containing ``data`` list.
        """
        cache_key = self._cache_key("search", query)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._request("symbol_search", {"symbol": query})
        self._set_cached(cache_key, data)
        return data

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)
        print(symbol)
        """Fetch real-time quote for a symbol.

        Args:
            symbol: Twelve Data symbol (e.g. ``TCS.NS``).

        Returns:
            Quote dict with fields such as ``close``, ``previous_close``,
            ``volume``, ``fifty_two_week``, etc.
        """
        cache_key = self._cache_key("quote", symbol)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._request("quote", {"symbol": symbol})
        self._set_cached(cache_key, data)
        return data

    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)
        print("Profile Symbol:", symbol)
        """Fetch company profile for a symbol.

        Args:
            symbol: Twelve Data symbol (e.g. ``TCS.NS``).

        Returns:
            Profile dict with ``name``, ``sector``, ``industry``,
            ``market_cap``, ``pe_ratio``, ``pb_ratio``, etc.
        """
        cache_key = self._cache_key("profile", symbol)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._request("profile", {"symbol": symbol})
        self._set_cached(cache_key, data)
        return data

    async def get_price(self, symbol: str) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)
        """Fetch current price for a symbol.

        Args:
            symbol: Twelve Data symbol (e.g. ``TCS.NS``).

        Returns:
            Price dict with ``price`` and ``timestamp``.
        """
        cache_key = self._cache_key("price", symbol)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = await self._request("price", {"symbol": symbol})
        self._set_cached(cache_key, data)
        return data

    async def get_time_series(self, symbol: str) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)
        """Return OHLCV time series for multiple lookback periods.

        Periods returned: ``1d``, ``1w``, ``1m``, ``3m``, ``6m``, ``1y``.

        Args:
            symbol: Twelve Data symbol (e.g. ``TCS.NS``).

        Returns:
            Dict mapping period key to Twelve Data time-series JSON.
        """
        cache_key = self._cache_key("timeseries", symbol)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        periods: Dict[str, Dict[str, Any]] = {
            "1d": {"interval": "5min", "outputsize": 78},
            "1w": {"interval": "1h", "outputsize": 50},
            "1m": {"interval": "1day", "outputsize": 22},
            "3m": {"interval": "1day", "outputsize": 66},
            "6m": {"interval": "1day", "outputsize": 126},
            "1y": {"interval": "1day", "outputsize": 252},
        }

        result: Dict[str, Any] = {}
        for period_key, cfg in periods.items():
            try:
                data = await self._request("time_series", {
                    "symbol": symbol,
                    "interval": cfg["interval"],
                    "outputsize": cfg["outputsize"],
                })
                result[period_key] = data
            except HTTPException:
                # If one period fails, record empty values but continue
                result[period_key] = {"values": []}

        self._set_cached(cache_key, result)
        return result
    async def get_snapshot(
        self,
        symbol: str,
        quote: Dict[str, Any] = None,
        profile: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)

        print("=" * 80)
        print("SNAPSHOT REQUEST")
        print("Symbol:", symbol)
        print("=" * 80)

        # ------------------------
        # Get Quote
        # ------------------------
        if quote is None:
            try:
                quote = await self.get_quote(symbol)
                print("\nQUOTE RESPONSE:")
                print(quote)
            except Exception as e:
                print("\nQUOTE FAILED:")
                print(repr(e))
                raise

        # ------------------------
        # Get Profile
        # ------------------------
        if profile is None:
            try:
                profile = await self.get_company_profile(symbol)
                print("\nPROFILE RESPONSE:")
                print(profile)
            except Exception as e:
                print("\nPROFILE FAILED (continuing without profile)")
                print(repr(e))
                profile = {}

        # ------------------------
        # Price Data
        # ------------------------
        current_price = (
            self._safe_float(quote.get("close"))
            or self._safe_float(quote.get("price"))
            or 0.0
        )

        prev_close = (
            self._safe_float(quote.get("previous_close"))
            or self._safe_float(quote.get("prev_close"))
            or 0.0
        )

        change = current_price - prev_close
        change_pct = (change / prev_close * 100.0) if prev_close else 0.0

        # ------------------------
        # Market Cap
        # ------------------------
        market_cap_raw = profile.get("market_cap")
        market_cap_str = "N/A"

        if market_cap_raw is not None:
            try:
                mc = float(market_cap_raw)

                if mc >= 1e12:
                    market_cap_str = f"{mc / 1e12:.2f}T INR"
                elif mc >= 1e9:
                    market_cap_str = f"{mc / 1e9:.2f}B INR"
                elif mc >= 1e6:
                    market_cap_str = f"{mc / 1e6:.2f}M INR"
                else:
                    market_cap_str = f"{mc:.2f} INR"

            except Exception:
                market_cap_str = str(market_cap_raw)

        # ------------------------
        # 52 Week
        # ------------------------
        week_52 = quote.get("fifty_two_week", {})

        week_52_high = (
            self._safe_float(quote.get("fifty_two_week_high"))
            or self._safe_float(week_52.get("high"))
        )

        week_52_low = (
            self._safe_float(quote.get("fifty_two_week_low"))
            or self._safe_float(week_52.get("low"))
        )

        # ------------------------
        # Final Snapshot
        # ------------------------
        snapshot = {
            "name": profile.get("name") or quote.get("name") or symbol,
            "nse_symbol": symbol,
            "current_price": round(current_price, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "market_cap": market_cap_str,
            "sector": profile.get("sector") or "N/A",
            "industry": profile.get("industry") or "N/A",
            "pe_ratio": self._safe_float(profile.get("pe_ratio")),
            "pb_ratio": self._safe_float(profile.get("pb_ratio")),
            "dividend_yield": self._safe_float(profile.get("dividend_yield")),
            "week_52_high": week_52_high,
            "week_52_low": week_52_low,
            "avg_volume": self._safe_int(
                quote.get("average_volume") or quote.get("avg_volume")
            ),
        }

        print("\nFINAL SNAPSHOT:")
        print(snapshot)
        print("=" * 80)

        return snapshot
        # ── Backward-compatible helpers for internal analyzers ──────

    async def get_historical_data(
        self, symbol: str, period: str = "1y", interval: str = "1d"
    ) -> pd.DataFrame:
        symbol = self.normalize_symbol(symbol)
        """Fetch historical OHLCV as a DataFrame compatible with yfinance output.

        Args:
            symbol: Twelve Data symbol (e.g. ``TCS.NS``).
            period: Lookback period (``1d``, ``5d``, ``1mo``, ``3mo``,
                ``6mo``, ``1y``, ``2y``, ``5y``).
            interval: Ignored — Twelve Data interval is derived from
                ``period``.

        Returns:
            DataFrame with columns ``Open``, ``High``, ``Low``, ``Close``,
            ``Volume`` and a ``Date`` index.
        """
        mapping: Dict[str, Dict[str, Any]] = {
            "1d": {"interval": "5min", "outputsize": 78},
            "5d": {"interval": "1h", "outputsize": 35},
            "1mo": {"interval": "1day", "outputsize": 22},
            "3mo": {"interval": "1day", "outputsize": 66},
            "6mo": {"interval": "1day", "outputsize": 126},
            "1y": {"interval": "1day", "outputsize": 252},
            "2y": {"interval": "1day", "outputsize": 504},
            "5y": {"interval": "1week", "outputsize": 260},
        }
        cfg = mapping.get(period, mapping["1y"])
        print("=" * 80)
        print("HISTORICAL REQUEST")
        print("Symbol:", symbol)
        print("Interval:", cfg["interval"])
        print("Outputsize:", cfg["outputsize"])
        print("=" * 80)
        data = await self._request("time_series", {
            "symbol": symbol,
            "interval": cfg["interval"],
            "outputsize": cfg["outputsize"],
        })

        values = data.get("values", [])
        if not values:
            raise ValueError(
                f"No historical data returned for {symbol}"
            )

        df = pd.DataFrame(values)
        # Ensure numeric columns
        for col in ("open", "high", "low", "close", "volume"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Parse datetime and sort ascending
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime").reset_index(drop=True)

        # Rename to yfinance-compatible column names
        rename_map = {
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
            "datetime": "Date",
        }
        df = df.rename(
            columns={k: v for k, v in rename_map.items() if k in df.columns}
        )
        if "Date" in df.columns:
            df.set_index("Date", inplace=True)

        return df

    async def get_stock_info(
        self,
        symbol: str,
        quote: Dict[str, Any] = None,
        profile: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        symbol = self.normalize_symbol(symbol)
        """Return a dict mimicking yfinance ``Ticker.info`` for internal analyzers.

        Fields not available from Twelve Data are returned as ``None`` so
        downstream analyzers do not crash.
        """
        if quote is None:
            quote = await self.get_quote(symbol)

        if profile is None:
            profile = await self.get_company_profile(symbol)

        current_price = (
            self._safe_float(quote.get("close"))
            or self._safe_float(quote.get("price"))
            or 0.0
        )
        prev_close = (
            self._safe_float(quote.get("previous_close")) or 0.0
        )

        div_yield = self._safe_float(profile.get("dividend_yield"))
        dividend_yield_decimal = (
            (div_yield / 100.0) if div_yield else None
        )

        week_52 = quote.get("fifty_two_week", {})

        return {
            "longName": (
                profile.get("name") or quote.get("name") or symbol
            ),
            "shortName": (
                profile.get("name") or quote.get("name") or symbol
            ),
            "currentPrice": current_price,
            "regularMarketPrice": current_price,
            "previousClose": prev_close,
            "regularMarketPreviousClose": prev_close,
            "marketCap": self._safe_float(profile.get("market_cap")),
            "sector": profile.get("sector") or "N/A",
            "industry": profile.get("industry") or "N/A",
            "trailingPE": self._safe_float(profile.get("pe_ratio")),
            "forwardPE": self._safe_float(profile.get("pe_ratio")),
            "priceToBook": self._safe_float(profile.get("pb_ratio")),
            "fiftyTwoWeekHigh": (
                self._safe_float(quote.get("fifty_two_week_high"))
                or self._safe_float(week_52.get("high"))
            ),
            "fiftyTwoWeekLow": (
                self._safe_float(quote.get("fifty_two_week_low"))
                or self._safe_float(week_52.get("low"))
            ),
            "averageVolume": self._safe_int(
                quote.get("average_volume") or quote.get("avg_volume")
            ),
            "dividendYield": dividend_yield_decimal,
            # Fields not available on Twelve Data free tier — return None
            # gracefully so downstream analyzers do not crash.
            "returnOnEquity": None,
            "returnOnAssets": None,
            "debtToEquity": None,
            "heldPercentInsiders": None,
            "heldPercentInstitutions": None,
            "beta": None,
        }

    async def get_financials(self, symbol: str) -> Dict[str, Any]:
        """Return empty financials structure.

        Twelve Data free tier does not expose full income statements or
        balance sheets for Indian equities.  All keys are present with
        ``None`` / empty values so the fundamental analyzer never crashes.
        """
        return {
            "revenue": {},
            "profit": {},
            "eps": {},
            "total_debt": None,
            "total_equity": None,
            "free_cash_flow": {},
            "quarterly_revenue": {},
            "quarterly_profit": {},
        }

    async def get_holders(self, symbol: str) -> Dict[str, Any]:
        """Return empty holders structure.

        Twelve Data free tier does not expose institutional holder lists
        for Indian equities.
        """
        return {"institutional": []}

    # ── Safe type converters ───────────────────────────────────────

    @staticmethod
    def _safe_float(val: Any) -> Optional[float]:
        if val is None or val == "" or val == "N/A" or val == "null":
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_int(val: Any) -> Optional[int]:
        if val is None or val == "" or val == "N/A" or val == "null":
            return None
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None
