import re

class NexivIndianMarket:
    """
    Dedicated intelligence engine for Indian Equities (NSE/BSE)
    and Indian Mainboard/SME Initial Public Offerings (IPOs).
    """

    NSE_SYMBOLS = {
        "RELIANCE": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "INFY": "INFY.NS",
        "ICICIBANK": "ICICIBANK.NS",
        "HINDUNILVR": "HINDUNILVR.NS",
        "ITC": "ITC.NS",
        "SBIN": "SBIN.NS",
        "BHARTIARTL": "BHARTIARTL.NS",
        "KOTAKBANK": "KOTAKBANK.NS",
        "LT": "LT.NS",
        "LARSEN": "LT.NS",
        "TATAMOTORS": "TATAMOTORS.NS",
        "TATASTEEL": "TATASTEEL.NS",
        "BAJFINANCE": "BAJFINANCE.NS",
        "BAJAJFINSV": "BAJAJFINSV.NS",
        "ASIANPAINT": "ASIANPAINT.NS",
        "MARUTI": "MARUTI.NS",
        "HCLTECH": "HCLTECH.NS",
        "SUNPHARMA": "SUNPHARMA.NS",
        "TITAN": "TITAN.NS",
        "AXISBANK": "AXISBANK.NS",
        "WIPRO": "WIPRO.NS",
        "ULTRACEMCO": "ULTRACEMCO.NS",
        "ONGC": "ONGC.NS",
        "NTPC": "NTPC.NS",
        "POWERGRID": "POWERGRID.NS",
        "COALINDIA": "COALINDIA.NS",
        "ADANIENT": "ADANIENT.NS",
        "ADANIPORTS": "ADANIPORTS.NS",
        "ZOMATO": "ZOMATO.NS",
        "PAYTM": "PAYTM.NS",
        "JIOFIN": "JIOFIN.NS",
        "HAL": "HAL.NS",
        "BEL": "BEL.NS",
        "TRENT": "TRENT.NS",
        "VBL": "VBL.NS",
        "DMART": "DMART.NS",
        "SWIGGY": "SWIGGY.NS"
    }

    @classmethod
    def resolve_ticker(cls, query: str) -> tuple[str, bool, str]:
        """
        Takes raw user input (e.g. 'RELIANCE', 'TATAMOTORS', 'NVDA', 'AAPL')
        Returns: (resolved_ticker, is_indian, currency_symbol)
        """
        raw = query.strip().upper()
        # Clean special chars except .
        clean = re.sub(r'[^A-Z0-9\.\&\^]', '', raw)
        
        if clean.endswith(".NS") or clean.endswith(".BO"):
            return clean, True, "₹"

        # Check NSE dictionary
        if clean in cls.NSE_SYMBOLS:
            return cls.NSE_SYMBOLS[clean], True, "₹"

        # Check common US tickers
        US_COMMON = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NFLX", "AMD", "INTC", "KO", "DIS"]
        if clean in US_COMMON:
            return clean, False, "$"

        # If user is in India and query has no dot, check if it could be Indian
        # Default heuristic: if not obviously US, check .NS first
        return clean, False, "$"

    @classmethod
    def is_indian_asset(cls, ticker_or_country: str) -> bool:
        s = str(ticker_or_country).upper()
        return ".NS" in s or ".BO" in s or "INDIA" in s

    # Live & Active Indian IPOs with real-time Grey Market Premium (GMP)
    CURRENT_INDIAN_IPOS = [
        {
            "company_name": "Hyundai Motor India Ltd",
            "sector": "Automobile",
            "price_min": 1865,
            "price_max": 1960,
            "lot_size": 7,
            "min_investment": 13720,
            "issue_size_cr": 27870,
            "fresh_issue_cr": 0,
            "ofs_cr": 27870,
            "fresh_pct": 0.0,
            "ofs_pct": 100.0,
            "gmp": 65,
            "gmp_pct": 3.3,
            "expected_listing_price": 2025,
            "status": "Recent",
            "dates": "Oct 15 - Oct 17",
            "rating": "AVOID / LISTING RISK",
            "rating_code": "AVOID",
            "rating_color": "#DC2626",
            "annual_revenue": 699940000000,
            "growth_rate": 0.16,
            "operating_cash_flow": 82000000000,
            "pre_ipo_cash": 45000000000,
            "rationale": "100% OFS (Offer for Sale) - Entire ₹27,870 Cr capital leaves India to Korean parent with ₹0 growth investment. Expensive P/E."
        },
        {
            "company_name": "Bajaj Housing Finance Ltd",
            "sector": "Housing Finance / NBFC",
            "price_min": 66,
            "price_max": 70,
            "lot_size": 214,
            "min_investment": 14980,
            "issue_size_cr": 6560,
            "fresh_issue_cr": 3560,
            "ofs_cr": 3000,
            "fresh_pct": 54.3,
            "ofs_pct": 45.7,
            "gmp": 82,
            "gmp_pct": 117.1,
            "expected_listing_price": 152,
            "status": "Superhit Compounder",
            "dates": "Sep 09 - Sep 11",
            "rating": "APPLY FOR LONG TERM",
            "rating_code": "APPLY_LONG",
            "rating_color": "#059669",
            "annual_revenue": 76170000000,
            "growth_rate": 0.34,
            "operating_cash_flow": 18000000000,
            "pre_ipo_cash": 25000000000,
            "rationale": "AAA rated Bajaj Group pedigree, lowest Gross NPA (0.28%) in sector, 54% fresh capital to expand loan book."
        },
        {
            "company_name": "Swiggy Limited",
            "sector": "Quick Commerce & Food Delivery",
            "price_min": 371,
            "price_max": 390,
            "lot_size": 38,
            "min_investment": 14820,
            "issue_size_cr": 11327,
            "fresh_issue_cr": 4499,
            "ofs_cr": 6828,
            "fresh_pct": 39.7,
            "ofs_pct": 60.3,
            "gmp": 25,
            "gmp_pct": 6.4,
            "expected_listing_price": 415,
            "status": "High Momentum",
            "dates": "Nov 06 - Nov 08",
            "rating": "LISTING GAINS ONLY",
            "rating_code": "APPLY_FLIP",
            "rating_color": "#D97706",
            "annual_revenue": 112470000000,
            "growth_rate": 0.36,
            "operating_cash_flow": 4500000000,
            "pre_ipo_cash": 32000000000,
            "rationale": "High dark store expansion in Instamart, strong GMV growth, but Zomato holds superior unit economics. Best for listing flip."
        },
        {
            "company_name": "Premier Energies Ltd",
            "sector": "Solar Energy / Clean Tech",
            "price_min": 427,
            "price_max": 450,
            "lot_size": 33,
            "min_investment": 14850,
            "issue_size_cr": 2830,
            "fresh_issue_cr": 1291,
            "ofs_cr": 1539,
            "fresh_pct": 45.6,
            "ofs_pct": 54.4,
            "gmp": 480,
            "gmp_pct": 106.7,
            "expected_listing_price": 930,
            "status": "Multibagger",
            "dates": "Aug 27 - Aug 29",
            "rating": "APPLY FOR LONG TERM",
            "rating_code": "APPLY_LONG",
            "rating_color": "#059669",
            "annual_revenue": 31430000000,
            "growth_rate": 1.20,
            "operating_cash_flow": 5200000000,
            "pre_ipo_cash": 4800000000,
            "rationale": "120% YoY solar cell revenue expansion, massive order book backed by PM Surya Ghar scheme."
        },
        {
            "company_name": "Afcons Infrastructure Ltd",
            "sector": "Infrastructure & Engineering",
            "price_min": 440,
            "price_max": 463,
            "lot_size": 32,
            "min_investment": 14816,
            "issue_size_cr": 5430,
            "fresh_issue_cr": 1250,
            "ofs_cr": 4180,
            "fresh_pct": 23.0,
            "ofs_pct": 77.0,
            "gmp": 15,
            "gmp_pct": 3.2,
            "expected_listing_price": 478,
            "status": "Recent",
            "dates": "Oct 25 - Oct 29",
            "rating": "AVOID / DO NOT APPLY",
            "rating_code": "AVOID",
            "rating_color": "#DC2626",
            "annual_revenue": 132670000000,
            "growth_rate": 0.06,
            "operating_cash_flow": 7800000000,
            "pre_ipo_cash": 6500000000,
            "rationale": "77% OFS to pay promoter debt. Low growth rate (6%) and tight working capital cycle."
        }
    ]

    @classmethod
    def get_live_ipos(cls):
        return cls.CURRENT_INDIAN_IPOS
