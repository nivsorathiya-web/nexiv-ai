import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
import pandas as pd
import numpy as np

class CBMMarketDataProvider:
    @staticmethod
    def get_stock_profile(ticker_symbol):
        """
        Fetches structured financial statements and market metrics for any global ticker.
        """
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info or {}
        
        # Financial statements
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow

        # Extract current market price & valuation basics
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
        shares_out = info.get("sharesOutstanding") or 1.0
        market_cap = info.get("marketCap") or (current_price * shares_out)
        beta = info.get("beta") or 1.0
        sector = info.get("sector") or "General"
        industry = info.get("industry") or "General"
        country = info.get("country") or "United States"

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
        revenue = get_val(financials, ["Total Revenue", "Operating Revenue", "Revenue"], default=market_cap * 0.25)
        ebit = get_val(financials, ["Operating Income", "EBIT", "Operating Profit"], default=revenue * 0.15)
        net_income = get_val(financials, ["Net Income", "Net Income Common"], default=ebit * 0.75)
        gross_profit = get_val(financials, ["Gross Profit"], default=revenue * 0.40)
        
        # Revenue history for growth rate calculation
        rev_history = get_history(financials, ["Total Revenue", "Operating Revenue", "Revenue"])
        cagr_3yr = 0.08
        if len(rev_history) >= 3 and rev_history[-1] > 0:
            try:
                cagr_3yr = ((rev_history[0] / rev_history[-1]) ** (1.0 / (len(rev_history) - 1))) - 1.0
            except:
                pass

        # Extract Balance Sheet items
        cash = get_val(balance_sheet, ["Cash And Cash Equivalents", "Cash", "Cash Financial"], default=0.0)
        total_assets = get_val(balance_sheet, ["Total Assets"], default=revenue * 1.5)
        current_assets = get_val(balance_sheet, ["Current Assets", "Total Current Assets"], default=total_assets * 0.4)
        total_debt = get_val(balance_sheet, ["Total Debt", "Long Term Debt And Capital Lease Obligation"], default=0.0)
        current_liabilities = get_val(balance_sheet, ["Current Liabilities", "Total Current Liabilities"], default=current_assets * 0.5)
        total_liabilities = get_val(balance_sheet, ["Total Liabilities Net Minority Interest", "Total Liabilities"], default=total_debt + current_liabilities)
        retained_earnings = get_val(balance_sheet, ["Retained Earnings"], default=total_assets * 0.3)
        working_capital = current_assets - current_liabilities

        # Extract Cash Flow items
        operating_cf = get_val(cashflow, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"], default=ebit)
        capex = abs(get_val(cashflow, ["Capital Expenditure", "Purchase Of Property Plant And Equipment"], default=revenue * 0.05))
        free_cash_flow = operating_cf - capex

        return {
            "symbol": ticker_symbol.upper(),
            "company_name": info.get("shortName") or info.get("longName") or ticker_symbol.upper(),
            "sector": sector,
            "industry": industry,
            "country": country,
            "current_price": float(current_price),
            "shares_outstanding": float(shares_out),
            "market_cap": float(market_cap),
            "beta": float(beta),
            "pe_ratio": float(info.get("trailingPE") or 0.0),
            "pb_ratio": float(info.get("priceToBook") or 0.0),
            "ev_to_ebitda": float(info.get("enterpriseToEbitda") or 0.0),
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
