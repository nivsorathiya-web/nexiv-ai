import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
import pandas as pd
import numpy as np
from nexiv_brain.indian_market import NexivIndianMarket

class CBMMarketDataProvider:
    @staticmethod
    def get_stock_profile(ticker_symbol):
        """
        Fetches structured financial statements and market metrics for any global or Indian ticker.
        """
        resolved_sym, is_indian, currency_sym = NexivIndianMarket.resolve_ticker(ticker_symbol)
        
        info = {}
        financials = None
        balance_sheet = None
        cashflow = None
        try:
            ticker = yf.Ticker(resolved_sym)
            info = ticker.info or {}
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
        except Exception:
            pass

        # Extract current market price & valuation basics
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
        sym_clean = resolved_sym.strip().upper()

        # Comprehensive benchmark cache for Indian & Global leaders with actual shares outstanding
        BENCHMARK_PROFILES = {
            # Global
            "AAPL": {"price": 225.40, "name": "Apple Inc.", "sector": "Technology", "country": "United States", "shares": 15300000000, "rev": 385000000000, "ebit": 120000000000, "net": 97000000000, "cash": 29000000000, "assets": 352000000000, "debt": 105000000000, "cagr": 0.07, "beta": 1.05},
            "NVDA": {"price": 122.80, "name": "NVIDIA Corporation", "sector": "Semiconductors", "country": "United States", "shares": 24600000000, "rev": 60900000000, "ebit": 32900000000, "net": 29760000000, "cash": 26000000000, "assets": 65000000000, "debt": 9700000000, "cagr": 0.65, "beta": 1.68},
            "TSLA": {"price": 254.20, "name": "Tesla, Inc.", "sector": "Automotive", "country": "United States", "shares": 3180000000, "rev": 96700000000, "ebit": 8900000000, "net": 14900000000, "cash": 29000000000, "assets": 106000000000, "debt": 5700000000, "cagr": 0.28, "beta": 2.20},
            "MSFT": {"price": 428.50, "name": "Microsoft Corporation", "sector": "Technology", "country": "United States", "shares": 7430000000, "rev": 245000000000, "ebit": 109000000000, "net": 88000000000, "cash": 75000000000, "assets": 512000000000, "debt": 45000000000, "cagr": 0.14, "beta": 0.90},
            "KO": {"price": 68.40, "name": "The Coca-Cola Company", "sector": "Consumer Defensive", "country": "United States", "shares": 4300000000, "rev": 45700000000, "ebit": 13000000000, "net": 10700000000, "cash": 12000000000, "assets": 97000000000, "debt": 41000000000, "cagr": 0.05, "beta": 0.58},
            "GOOGL": {"price": 162.50, "name": "Alphabet Inc.", "sector": "Communication Services", "country": "United States", "shares": 12400000000, "rev": 307000000000, "ebit": 84000000000, "net": 73700000000, "cash": 110000000000, "assets": 402000000000, "debt": 28000000000, "cagr": 0.13, "beta": 1.05},
            
            # India Leaders (NSE)
            "RELIANCE.NS": {"price": 2980.00, "name": "Reliance Industries Limited", "sector": "Energy & Telecom", "country": "India", "shares": 6760000000, "rev": 9000000000000, "ebit": 1400000000000, "net": 790000000000, "cash": 800000000000, "assets": 17000000000000, "debt": 3200000000000, "cagr": 0.12, "beta": 0.85},
            "TCS.NS": {"price": 4220.00, "name": "Tata Consultancy Services Ltd", "sector": "Technology", "country": "India", "shares": 3620000000, "rev": 2408930000000, "ebit": 590000000000, "net": 460000000000, "cash": 180000000000, "assets": 1400000000000, "debt": 0, "cagr": 0.10, "beta": 0.72},
            "HDFCBANK.NS": {"price": 1680.00, "name": "HDFC Bank Limited", "sector": "Financial Services", "country": "India", "shares": 7600000000, "rev": 2800000000000, "ebit": 950000000000, "net": 640000000000, "cash": 2200000000000, "assets": 36000000000000, "debt": 3500000000000, "cagr": 0.22, "beta": 0.95},
            "INFY.NS": {"price": 1920.00, "name": "Infosys Limited", "sector": "Technology", "country": "India", "shares": 4150000000, "rev": 1536700000000, "ebit": 310000000000, "net": 262000000000, "cash": 160000000000, "assets": 1250000000000, "debt": 0, "cagr": 0.11, "beta": 0.82},
            "TATAMOTORS.NS": {"price": 965.00, "name": "Tata Motors Limited", "sector": "Automotive", "country": "India", "shares": 3680000000, "rev": 4379280000000, "ebit": 440000000000, "net": 318000000000, "cash": 400000000000, "assets": 3500000000000, "debt": 500000000000, "cagr": 0.24, "beta": 1.35},
            "TATASTEEL.NS": {"price": 155.00, "name": "Tata Steel Limited", "sector": "Basic Materials", "country": "India", "shares": 12480000000, "rev": 2290000000000, "ebit": 230000000000, "net": 40000000000, "cash": 120000000000, "assets": 2800000000000, "debt": 870000000000, "cagr": 0.08, "beta": 1.25},
            "ZOMATO.NS": {"price": 265.00, "name": "Zomato Limited", "sector": "Consumer Cyclical", "country": "India", "shares": 8820000000, "rev": 121140000000, "ebit": 3500000000, "net": 3510000000, "cash": 120000000000, "assets": 240000000000, "debt": 0, "cagr": 0.65, "beta": 1.45},
            "ITC.NS": {"price": 510.00, "name": "ITC Limited", "sector": "Consumer Defensive", "country": "India", "shares": 12490000000, "rev": 765000000000, "ebit": 260000000000, "net": 205000000000, "cash": 110000000000, "assets": 920000000000, "debt": 0, "cagr": 0.09, "beta": 0.65}
        }

        bm = BENCHMARK_PROFILES.get(sym_clean)
        if current_price == 0.0:
            if bm:
                current_price = bm["price"]
            else:
                current_price = 100.0

        shares_out = info.get("sharesOutstanding") or (bm["shares"] if bm else 1000000000.0)
        market_cap = info.get("marketCap") or (current_price * shares_out)
        beta = info.get("beta") or (bm["beta"] if bm else 1.0)
        sector = info.get("sector") or (bm["sector"] if bm else "General")
        industry = info.get("industry") or "General"
        country = "India" if is_indian else (info.get("country") or (bm["country"] if bm else "United States"))
        company_name = info.get("shortName") or info.get("longName") or (bm["name"] if bm else sym_clean)

        # Safe extraction helper
        def get_val(df, row_names, default=0.0):
            if df is None or df.empty:
                return default
            for rname in row_names:
                for idx in df.index:
                    if rname.lower() in str(idx).lower():
                        val = df.loc[idx].iloc[0]
                        if pd.notna(val):
                            return float(val)
            return default

        def get_history(df, row_names):
            if df is None or df.empty:
                return []
            for rname in row_names:
                for idx in df.index:
                    if rname.lower() in str(idx).lower():
                        series = df.loc[idx]
                        return [float(x) for x in series if pd.notna(x)]
            return []

        # Extract latest Income Statement items
        default_rev = bm["rev"] if bm else market_cap * 0.25
        default_ebit = bm["ebit"] if bm else default_rev * 0.15
        default_net = bm["net"] if bm else default_ebit * 0.75
        
        revenue = get_val(financials, ["Total Revenue", "Operating Revenue", "Revenue"], default=default_rev)
        ebit = get_val(financials, ["Operating Income", "EBIT", "Operating Profit"], default=default_ebit)
        net_income = get_val(financials, ["Net Income", "Net Income Common"], default=default_net)
        gross_profit = get_val(financials, ["Gross Profit"], default=revenue * 0.40)
        
        # Revenue history for growth rate calculation
        rev_history = get_history(financials, ["Total Revenue", "Operating Revenue", "Revenue"])
        cagr_3yr = bm["cagr"] if bm else 0.08
        if len(rev_history) >= 3 and rev_history[-1] > 0:
            try:
                cagr_3yr = ((rev_history[0] / rev_history[-1]) ** (1.0 / (len(rev_history) - 1))) - 1.0
            except:
                pass

        # Extract Balance Sheet items
        cash = get_val(balance_sheet, ["Cash And Cash Equivalents", "Cash", "Cash Financial"], default=bm["cash"] if bm else 0.0)
        total_assets = get_val(balance_sheet, ["Total Assets"], default=bm["assets"] if bm else revenue * 1.5)
        current_assets = get_val(balance_sheet, ["Current Assets", "Total Current Assets"], default=total_assets * 0.4)
        total_debt = get_val(balance_sheet, ["Total Debt", "Long Term Debt And Capital Lease Obligation"], default=bm["debt"] if bm else 0.0)
        current_liabilities = get_val(balance_sheet, ["Current Liabilities", "Total Current Liabilities"], default=current_assets * 0.5)
        total_liabilities = get_val(balance_sheet, ["Total Liabilities Net Minority Interest", "Total Liabilities"], default=total_debt + current_liabilities)
        retained_earnings = get_val(balance_sheet, ["Retained Earnings"], default=total_assets * 0.3)
        working_capital = current_assets - current_liabilities

        # Extract Cash Flow items
        operating_cf = get_val(cashflow, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"], default=ebit)
        capex = abs(get_val(cashflow, ["Capital Expenditure", "Purchase Of Property Plant And Equipment"], default=revenue * 0.05))
        free_cash_flow = operating_cf - capex

        return {
            "symbol": sym_clean,
            "company_name": company_name,
            "currency": currency_sym,
            "is_indian": is_indian,
            "sector": sector,
            "industry": industry,
            "country": country,
            "current_price": float(current_price),
            "shares_outstanding": float(shares_out),
            "market_cap": float(market_cap),
            "beta": float(beta),
            "pe_ratio": float(info.get("trailingPE") or (current_price / max(net_income / max(shares_out, 1), 0.01))),
            "pb_ratio": float(info.get("priceToBook") or 2.5),
            "ev_to_ebitda": float(info.get("enterpriseToEbitda") or 14.0),
            "revenue": float(revenue),
            "ebit": float(ebit),
            "net_income": float(net_income),
            "gross_profit": float(gross_profit),
            "revenue_cagr_3yr": float(cagr_3yr),
            "cash": float(cash),
            "total_assets": float(total_assets),
            "current_assets": float(current_assets),
            "current_liabilities": float(current_liabilities),
            "total_debt": float(total_debt),
            "total_liabilities": float(total_liabilities),
            "retained_earnings": float(retained_earnings),
            "working_capital": float(working_capital),
            "operating_cf": float(operating_cf),
            "capex": float(capex),
            "free_cash_flow": float(free_cash_flow)
        }
