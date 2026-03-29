import yfinance as yf
import pandas as pd
import streamlit as st

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin
from pyrate_limiter import Duration, Rate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """
    Custom session class that combines both caching (to avoid redundant network calls)
    and rate limiting (to prevent API bans).
    """
    pass

# Configure the Rate Limiter: Max 2 requests per 5 seconds.
rate_limit = Limiter(Rate(2, Duration.SECOND * 5))

# Instantiate the shielded session using a local SQLite database for caching.
safe_session = CachedLimiterSession(
    limiter = rate_limit,
    backend = SQLiteCache("yfinance_cache.sqlite"),
)

# Intercept the default yfinance Ticker initialization.
_original_ticker_init = yf.Ticker.__init__

def _patched_ticker_init(self, ticker, session = None, *args, **kwargs):
    """
    Intercepts the creation of a yfinance Ticker.
    If no session is explicitly provided, it silently injects our 'safe_session'.
    This protects both our direct service calls and the underlying AI agent tool calls 
    (like YFinanceTools) without needing to alter their source code.
    """
    if session is None:
        session = safe_session
    _original_ticker_init(self, ticker, session = session, *args, **kwargs)

# Apply the patch globally across the yfinance library
yf.Ticker.__init__ = _patched_ticker_init

class MarketDataService:
    """
    Service class responsible for fetching, processing, and providing 
    financial market data.
    """

    def __init__(self, default_period: str = "6mo"):
        """
        Initializes the market data service with default parameters.
        """
        self.default_period = default_period

    def fetch_data(self, ticker: str) -> pd.DataFrame:
        """
        Wrapper method to fetch historical data using the instance's default period.
        
        Args:
            ticker (str): The stock ticker symbol (e.g., 'AAPL').
            
        Returns:
            pd.DataFrame: The historical stock data.
        """
        return self._get_historical_data(ticker, self.default_period)

    # =========================================================================
    # WHY WE USE @staticmethod:
    # 
    # Streamlit's @st.cache_data works by hashing all the arguments passed 
    # to a function. If this were a regular instance method, Python would 
    # implicitly pass 'self' (the entire class instance) as the first argument.
    # 
    # Hashing 'self' is problematic for two reasons:
    # 1. It often contains unhashable types (like open connections or complex objects), 
    #    causing Streamlit to crash.
    # 2. Even if it hashes, the memory address of 'self' changes every time 
    #    the class is instantiated, which would invalidate the cache immediately.
    # 
    # By using @staticmethod, we strip 'self' from the equation. Streamlit 
    # now only hashes the simple string arguments ('ticker' and 'period'), 
    # allowing the cache to work perfectly and safely with yfinance.
    # =========================================================================
    @staticmethod
    @st.cache_data(show_spinner=False, ttl=3600)
    def _get_historical_data(ticker: str, period: str) -> pd.DataFrame:
        """
        Retrieves historical price data for a specific stock ticker from Yahoo Finance.
        Uses Streamlit cache to avoid redundant API calls and speed up the UI.
        Added a TTL (Time To Live) of 1 hour (3600s) to refresh data automatically.
        
        Args:
            ticker (str): The stock ticker symbol.
            period (str): The time period for historical data (e.g., '6mo').
            
        Returns:
            pd.DataFrame: A DataFrame containing the historical stock data.
        """
        stock = yf.Ticker(ticker)
        historical_data = stock.history(period=period)
        
        # Reset index to make 'Date' a standard column instead of an index
        historical_data.reset_index(inplace=True)
        
        return historical_data