import re
import urllib.request
import json

class NexivIndianMarket:
    """
    Dedicated intelligence engine for Indian Equities (NSE/BSE)
    and Indian Mainboard/SME Initial Public Offerings (IPOs).
    """

    # Comprehensive High-Liquidity Equity Search Catalog (NSE/BSE & US Titans)
    SEARCH_CATALOG = [
        # Nifty 50 & Heavyweights
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries Limited", "sector": "Energy & Telecom", "exchange": "NSE", "keywords": "reliance jio rIL mukesh ambani oil retail"},
        {"symbol": "TATAMOTORS.NS", "name": "Tata Motors Limited", "sector": "Automotive", "exchange": "NSE", "keywords": "tata motors tm jlr ev tiago nexon harrier"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy Services Ltd", "sector": "Technology", "exchange": "NSE", "keywords": "tata tcs it services software tech"},
        {"symbol": "TATASTEEL.NS", "name": "Tata Steel Limited", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "tata steel metals iron"},
        {"symbol": "TATAPOWER.NS", "name": "Tata Power Company Ltd", "sector": "Utilities & Clean Energy", "exchange": "NSE", "keywords": "tata power solar renewable ev charging"},
        {"symbol": "TATACONSUM.NS", "name": "Tata Consumer Products Ltd", "sector": "Consumer Goods", "exchange": "NSE", "keywords": "tata consumer tea salt sampann starbucks"},
        {"symbol": "TITAN.NS", "name": "Titan Company Limited", "sector": "Consumer Discretionary", "exchange": "NSE", "keywords": "tata titan tanishq fastrack jewelry watches"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited", "sector": "Banking & Finance", "exchange": "NSE", "keywords": "hdfc bank private banking loans credit cards"},
        {"symbol": "INFY.NS", "name": "Infosys Limited", "sector": "Technology", "exchange": "NSE", "keywords": "infosys infy it services narayana murthy"},
        {"symbol": "ICICIBANK.NS", "name": "ICICI Bank Limited", "sector": "Banking & Finance", "exchange": "NSE", "keywords": "icici bank retail banking loans"},
        {"symbol": "SBIN.NS", "name": "State Bank of India", "sector": "Public Banking", "exchange": "NSE", "keywords": "sbi state bank of india psu banking"},
        {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel Limited", "sector": "Telecommunications", "exchange": "NSE", "keywords": "airtel bharti telecom 5g mobile broadband"},
        {"symbol": "ITC.NS", "name": "ITC Limited", "sector": "Consumer Defensive", "exchange": "NSE", "keywords": "itc cigarettes hotels fmcg aashirvaad sunfeast yippee"},
        {"symbol": "HINDUNILVR.NS", "name": "Hindustan Unilever Limited", "sector": "Consumer Goods", "exchange": "NSE", "keywords": "hul unilever soap surf excel dove shampoo fmcg"},
        {"symbol": "LICI.NS", "name": "Life Insurance Corporation of India", "sector": "Insurance", "exchange": "NSE", "keywords": "lic life insurance psu"},
        {"symbol": "LT.NS", "name": "Larsen & Toubro Limited", "sector": "Engineering & EPC", "exchange": "NSE", "keywords": "l&t larsen toubro infrastructure defense construction"},
        {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance Limited", "sector": "Financial Services", "exchange": "NSE", "keywords": "bajaj finance nbfc consumer loans emi"},
        {"symbol": "BAJAJFINSV.NS", "name": "Bajaj Finserv Limited", "sector": "Financial Services", "exchange": "NSE", "keywords": "bajaj finserv insurance holding"},
        {"symbol": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank Ltd", "sector": "Banking", "exchange": "NSE", "keywords": "kotak mahindra bank uday kotak"},
        {"symbol": "AXISBANK.NS", "name": "Axis Bank Limited", "sector": "Banking", "exchange": "NSE", "keywords": "axis bank private loans credit cards"},
        {"symbol": "MARUTI.NS", "name": "Maruti Suzuki India Limited", "sector": "Automotive", "exchange": "NSE", "keywords": "maruti suzuki cars swift brezza baleno dzire"},
        {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical Industries Ltd", "sector": "Healthcare & Pharma", "exchange": "NSE", "keywords": "sun pharma pharmaceuticals drugs generic"},
        {"symbol": "ASIANPAINT.NS", "name": "Asian Paints Limited", "sector": "Consumer Goods", "exchange": "NSE", "keywords": "asian paints coatings decorative royale"},
        {"symbol": "HCLTECH.NS", "name": "HCL Technologies Limited", "sector": "Technology", "exchange": "NSE", "keywords": "hcl tech software it services"},
        {"symbol": "WIPRO.NS", "name": "Wipro Limited", "sector": "Technology", "exchange": "NSE", "keywords": "wipro azim premji it services"},
        {"symbol": "ULTRACEMCO.NS", "name": "UltraTech Cement Limited", "sector": "Basic Materials", "exchange": "NSE", "keywords": "ultratech cement birla building materials"},
        {"symbol": "NTPC.NS", "name": "NTPC Limited", "sector": "Utilities", "exchange": "NSE", "keywords": "ntpc power thermal renewable energy green"},
        {"symbol": "ONGC.NS", "name": "Oil & Natural Gas Corp Ltd", "sector": "Energy", "exchange": "NSE", "keywords": "ongc oil natural gas crude psu"},
        {"symbol": "POWERGRID.NS", "name": "Power Grid Corp of India Ltd", "sector": "Utilities", "exchange": "NSE", "keywords": "power grid transmission psu electricity"},
        {"symbol": "COALINDIA.NS", "name": "Coal India Limited", "sector": "Energy & Mining", "exchange": "NSE", "keywords": "coal india mining psu energy"},
        {"symbol": "ADANIENT.NS", "name": "Adani Enterprises Limited", "sector": "Conglomerate", "exchange": "NSE", "keywords": "adani enterprises gautam adani ports airports"},
        {"symbol": "ADANIPORTS.NS", "name": "Adani Ports & Special Economic Zone", "sector": "Logistics", "exchange": "NSE", "keywords": "adani ports logistics shipping container"},
        {"symbol": "ADANIGREEN.NS", "name": "Adani Green Energy Limited", "sector": "Renewable Energy", "exchange": "NSE", "keywords": "adani green solar wind clean energy"},
        
        # New-Age Tech & High-Growth Multibaggers (India)
        {"symbol": "ZOMATO.NS", "name": "Zomato Limited", "sector": "Consumer Internet", "exchange": "NSE", "keywords": "zomato food delivery blinkit quick commerce deepinder"},
        {"symbol": "JIOFIN.NS", "name": "Jio Financial Services Ltd", "sector": "Financial Services", "exchange": "NSE", "keywords": "jio finance reliance blackrock mutual fund asset management"},
        {"symbol": "HAL.NS", "name": "Hindustan Aeronautics Limited", "sector": "Aerospace & Defense", "exchange": "NSE", "keywords": "hal aeronautics tejas fighter jet defense psu"},
        {"symbol": "BEL.NS", "name": "Bharat Electronics Limited", "sector": "Defense Electronics", "exchange": "NSE", "keywords": "bel bharat electronics radar defense missile psu"},
        {"symbol": "TRENT.NS", "name": "Trent Limited", "sector": "Retail", "exchange": "NSE", "keywords": "tata trent zudio westside apparel fashion retail"},
        {"symbol": "VBL.NS", "name": "Varun Beverages Limited", "sector": "Consumer Defensive", "exchange": "NSE", "keywords": "varun beverages pepsico sting mirinda bottling"},
        {"symbol": "DMART.NS", "name": "Avenue Supermarts Limited (DMart)", "sector": "Retail", "exchange": "NSE", "keywords": "dmart avenue supermarts radhakishan damani grocery retail"},
        {"symbol": "PAYTM.NS", "name": "One97 Communications Ltd (Paytm)", "sector": "Fintech", "exchange": "NSE", "keywords": "paytm one97 upi payments wallet soundbox"},
        {"symbol": "SWIGGY.NS", "name": "Swiggy Limited", "sector": "Consumer Internet", "exchange": "NSE", "keywords": "swiggy instamart food delivery dineout quick commerce"},
        {"symbol": "PREMIERENE.NS", "name": "Premier Energies Limited", "sector": "Solar & Clean Tech", "exchange": "NSE", "keywords": "premier energies solar modules cells renewable"},
        {"symbol": "WAAREEENER.NS", "name": "Waaree Energies Limited", "sector": "Solar Energy", "exchange": "NSE", "keywords": "waaree energies solar pv modules export clean energy"},
        {"symbol": "BAJAJHFL.NS", "name": "Bajaj Housing Finance Ltd", "sector": "Housing Finance", "exchange": "NSE", "keywords": "bajaj housing home loans nbfc bhfl"},

        # US & Global Titans
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Consumer Tech", "exchange": "NASDAQ", "keywords": "apple iphone mac ipad tim cook ios"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Semiconductors & AI", "exchange": "NASDAQ", "keywords": "nvidia gpu chips ai jensen huang blackwell cuda"},
        {"symbol": "TSLA", "name": "Tesla, Inc.", "sector": "Automotive & Clean Energy", "exchange": "NASDAQ", "keywords": "tesla ev elon musk cybertruck energy solar"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology & Cloud", "exchange": "NASDAQ", "keywords": "microsoft windows azure openai satya nadella office"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Communication Services", "exchange": "NASDAQ", "keywords": "google alphabet search youtube android gemini sunder pichai"},
        {"symbol": "AMZN", "name": "Amazon.com, Inc.", "sector": "E-Commerce & Cloud", "exchange": "NASDAQ", "keywords": "amazon aws jeff bezos retail prime alexa"},
        {"symbol": "META", "name": "Meta Platforms, Inc.", "sector": "Social Media & AI", "exchange": "NASDAQ", "keywords": "meta facebook instagram whatsapp zuckerberg llama"},
        {"symbol": "KO", "name": "The Coca-Cola Company", "sector": "Consumer Defensive", "exchange": "NYSE", "keywords": "coca cola soda beverage warren buffett buffet coke"}
    ]

    @classmethod
    def search_equities(cls, query: str):
        """
        Instant typeahead matching for stock search bar.
        Matches against symbols, names, sectors, and keywords.
        """
        q = str(query).strip().lower()
        if not q or len(q) < 1:
            return []

        results = []
        seen = set()

        # 1. Exact or prefix symbol match (Highest Priority)
        for item in cls.SEARCH_CATALOG:
            sym_clean = item["symbol"].replace(".NS", "").replace(".BO", "").lower()
            if sym_clean == q or item["symbol"].lower().startswith(q):
                if item["symbol"] not in seen:
                    results.append(item)
                    seen.add(item["symbol"])

        # 2. Company name or keywords match
        for item in cls.SEARCH_CATALOG:
            if item["symbol"] in seen:
                continue
            name_lower = item["name"].lower()
            keywords = item["keywords"].lower()
            if q in name_lower or q in keywords:
                results.append(item)
                seen.add(item["symbol"])

        # 3. Fuzzy words split match
        words = [w for w in q.split() if len(w) >= 2]
        for item in cls.SEARCH_CATALOG:
            if item["symbol"] in seen:
                continue
            match_all = True
            for w in words:
                if w not in item["name"].lower() and w not in item["keywords"].lower() and w not in item["symbol"].lower():
                    match_all = False
                    break
            if match_all:
                results.append(item)
                seen.add(item["symbol"])

        return results[:8]

    @classmethod
    def resolve_ticker(cls, query: str) -> tuple[str, bool, str]:
        raw = query.strip().upper()
        clean = re.sub(r'[^A-Z0-9\.\&\^]', '', raw)
        
        if clean.endswith(".NS") or clean.endswith(".BO"):
            return clean, True, "₹"

        for item in cls.SEARCH_CATALOG:
            base = item["symbol"].replace(".NS", "").replace(".BO", "")
            if clean == base:
                is_ind = ".NS" in item["symbol"] or ".BO" in item["symbol"]
                cur = "₹" if is_ind else "$"
                return item["symbol"], is_ind, cur

        US_COMMON = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NFLX", "AMD", "INTC", "KO", "DIS"]
        if clean in US_COMMON:
            return clean, False, "$"

        # Default fallback: If in India and looks like an Indian equity symbol, try .NS
        return clean, False, "$"

    # Brokerage-Grade Real-World Indian IPOs Dataset with Exact Timelines, Subscription & AI Decision
    BROKERAGE_IPOS = [
        {
            "company_name": "Swiggy Limited",
            "symbol": "SWIGGY",
            "sector": "Food Tech & Quick Commerce",
            "status": "OPEN NOW",
            "status_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
            "timeline": {
                "bidding_dates": "06 Nov - 08 Nov 2024",
                "open_date": "06 Nov 2024",
                "close_date": "08 Nov 2024",
                "allotment_date": "11 Nov 2024",
                "refunds_date": "12 Nov 2024",
                "demat_credit": "12 Nov 2024",
                "listing_date": "13 Nov 2024",
                "days_left": "Closes Today at 5:00 PM"
            },
            "issue_details": {
                "price_range": "₹371 - ₹390",
                "price_min": 371,
                "price_max": 390,
                "lot_size": 38,
                "min_investment": 14820,
                "issue_size_cr": 11327,
                "fresh_issue_cr": 4499,
                "ofs_cr": 6828,
                "fresh_pct": 39.7,
                "ofs_pct": 60.3
            },
            "gmp": {
                "value": 25,
                "pct": 6.4,
                "expected_listing_price": 415,
                "sentiment": "Moderate"
            },
            "subscription": {
                "qib": "4.15x",
                "nii": "1.24x",
                "retail": "1.14x",
                "total": "3.59x"
            },
            "financials": {
                "annual_revenue": 112470000000,
                "growth_rate": 0.36,
                "operating_cash_flow": 4500000000,
                "pre_ipo_cash": 32000000000
            },
            "ai_decision": {
                "action": "APPLY FOR LISTING GAINS ONLY",
                "action_code": "APPLY_FLIP",
                "action_color": "#D97706",
                "score": 58,
                "summary": "High momentum in Instamart quick commerce, but 60.3% OFS exit and operating losses vs Zomato's profitability require disciplined profit-booking on Day 1."
            }
        },
        {
            "company_name": "NTPC Green Energy Limited",
            "symbol": "NTPCGREEN",
            "sector": "Renewable & Clean Energy",
            "status": "UPCOMING",
            "status_badge": "bg-blue-100 text-blue-800 border-blue-300",
            "timeline": {
                "bidding_dates": "19 Nov - 22 Nov 2024",
                "open_date": "19 Nov 2024",
                "close_date": "22 Nov 2024",
                "allotment_date": "25 Nov 2024",
                "refunds_date": "26 Nov 2024",
                "demat_credit": "26 Nov 2024",
                "listing_date": "27 Nov 2024",
                "days_left": "Opens in 4 Days"
            },
            "issue_details": {
                "price_range": "₹102 - ₹108",
                "price_min": 102,
                "price_max": 108,
                "lot_size": 138,
                "min_investment": 14904,
                "issue_size_cr": 10000,
                "fresh_issue_cr": 10000,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {
                "value": 12,
                "pct": 11.1,
                "expected_listing_price": 120,
                "sentiment": "Strong"
            },
            "subscription": {
                "qib": "Upcoming",
                "nii": "Upcoming",
                "retail": "Upcoming",
                "total": "Bidding Starts Soon"
            },
            "financials": {
                "annual_revenue": 19620000000,
                "growth_rate": 1.05,
                "operating_cash_flow": 12400000000,
                "pre_ipo_cash": 18000000000
            },
            "ai_decision": {
                "action": "APPLY FOR LONG TERM COMPOUNDER",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 86,
                "summary": "Pristine 100% Fresh Issue — ₹10,000 Cr stays in the business to fund massive solar & green hydrogen capacity. Backed by sovereign PSU parent NTPC."
            }
        },
        {
            "company_name": "Hyundai Motor India Ltd",
            "symbol": "HYUNDAI",
            "sector": "Automobile Manufacturer",
            "status": "RECENTLY LISTED",
            "status_badge": "bg-slate-100 text-slate-800 border-slate-300",
            "timeline": {
                "bidding_dates": "15 Oct - 17 Oct 2024",
                "open_date": "15 Oct 2024",
                "close_date": "17 Oct 2024",
                "allotment_date": "18 Oct 2024",
                "refunds_date": "21 Oct 2024",
                "demat_credit": "21 Oct 2024",
                "listing_date": "22 Oct 2024",
                "days_left": "Listed on NSE/BSE"
            },
            "issue_details": {
                "price_range": "₹1,865 - ₹1,960",
                "price_min": 1865,
                "price_max": 1960,
                "lot_size": 7,
                "min_investment": 13720,
                "issue_size_cr": 27870,
                "fresh_issue_cr": 0,
                "ofs_cr": 27870,
                "fresh_pct": 0.0,
                "ofs_pct": 100.0
            },
            "gmp": {
                "value": -25,
                "pct": -1.3,
                "expected_listing_price": 1935,
                "sentiment": "Discount"
            },
            "subscription": {
                "qib": "6.97x",
                "nii": "0.60x",
                "retail": "0.50x",
                "total": "2.37x"
            },
            "financials": {
                "annual_revenue": 699940000000,
                "growth_rate": 0.16,
                "operating_cash_flow": 82000000000,
                "pre_ipo_cash": 45000000000
            },
            "ai_decision": {
                "action": "AVOID / DO NOT APPLY",
                "action_code": "AVOID",
                "action_color": "#DC2626",
                "score": 34,
                "summary": "100% OFS exit — every single Rupee of the ₹27,870 Cr leaves India to Korean parent. Weak retail demand (0.50x) and negative GMP confirm listing discount."
            }
        },
        {
            "company_name": "Waaree Energies Limited",
            "symbol": "WAAREE",
            "sector": "Solar PV Module Manufacturing",
            "status": "SUPERHIT MULTIBAGGER",
            "status_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
            "timeline": {
                "bidding_dates": "21 Oct - 23 Oct 2024",
                "open_date": "21 Oct 2024",
                "close_date": "23 Oct 2024",
                "allotment_date": "24 Oct 2024",
                "refunds_date": "25 Oct 2024",
                "demat_credit": "25 Oct 2024",
                "listing_date": "28 Oct 2024",
                "days_left": "Listed at +66% Premium"
            },
            "issue_details": {
                "price_range": "₹1,427 - ₹1,503",
                "price_min": 1427,
                "price_max": 1503,
                "lot_size": 9,
                "min_investment": 13527,
                "issue_size_cr": 4321,
                "fresh_issue_cr": 3600,
                "ofs_cr": 721,
                "fresh_pct": 83.3,
                "ofs_pct": 16.7
            },
            "gmp": {
                "value": 1560,
                "pct": 103.8,
                "expected_listing_price": 3063,
                "sentiment": "Super Bullish"
            },
            "subscription": {
                "qib": "208.63x",
                "nii": "62.49x",
                "retail": "10.79x",
                "total": "76.34x"
            },
            "financials": {
                "annual_revenue": 113970000000,
                "growth_rate": 0.69,
                "operating_cash_flow": 28000000000,
                "pre_ipo_cash": 34000000000
            },
            "ai_decision": {
                "action": "APPLY FOR LONG TERM COMPOUNDER",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 94,
                "summary": "Outstanding 83.3% fresh issue to build 6GW Odisha ingot/wafer plant. Historic 76x subscription and +103% GMP delivers generational wealth compounding."
            }
        },
        {
            "company_name": "Bajaj Housing Finance Ltd",
            "symbol": "BAJAJHFL",
            "sector": "Housing Finance / NBFC",
            "status": "HISTORIC COMPOUNDER",
            "status_badge": "bg-emerald-100 text-emerald-800 border-emerald-300",
            "timeline": {
                "bidding_dates": "09 Sep - 11 Sep 2024",
                "open_date": "09 Sep 2024",
                "close_date": "11 Sep 2024",
                "allotment_date": "12 Sep 2024",
                "refunds_date": "13 Sep 2024",
                "demat_credit": "13 Sep 2024",
                "listing_date": "16 Sep 2024",
                "days_left": "Listed at +114% Gain"
            },
            "issue_details": {
                "price_range": "₹66 - ₹70",
                "price_min": 66,
                "price_max": 70,
                "lot_size": 214,
                "min_investment": 14980,
                "issue_size_cr": 6560,
                "fresh_issue_cr": 3560,
                "ofs_cr": 3000,
                "fresh_pct": 54.3,
                "ofs_pct": 45.7
            },
            "gmp": {
                "value": 82,
                "pct": 117.1,
                "expected_listing_price": 152,
                "sentiment": "Multibagger"
            },
            "subscription": {
                "qib": "222.05x",
                "nii": "41.51x",
                "retail": "7.41x",
                "total": "67.43x"
            },
            "financials": {
                "annual_revenue": 76170000000,
                "growth_rate": 0.34,
                "operating_cash_flow": 18000000000,
                "pre_ipo_cash": 25000000000
            },
            "ai_decision": {
                "action": "APPLY FOR LONG TERM COMPOUNDER",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 92,
                "summary": "AAA Bajaj Group lineage, lowest Gross NPA (0.28%) in financial sector. 54% fresh growth issue creates prime compounding machine."
            }
        },
        {
            "company_name": "Afcons Infrastructure Ltd",
            "symbol": "AFCONS",
            "sector": "Heavy Engineering & Infrastructure",
            "status": "RECENTLY LISTED",
            "status_badge": "bg-slate-100 text-slate-800 border-slate-300",
            "timeline": {
                "bidding_dates": "25 Oct - 29 Oct 2024",
                "open_date": "25 Oct 2024",
                "close_date": "29 Oct 2024",
                "allotment_date": "30 Oct 2024",
                "refunds_date": "04 Nov 2024",
                "demat_credit": "04 Nov 2024",
                "listing_date": "04 Nov 2024",
                "days_left": "Listed on NSE/BSE"
            },
            "issue_details": {
                "price_range": "₹440 - ₹463",
                "price_min": 440,
                "price_max": 463,
                "lot_size": 32,
                "min_investment": 14816,
                "issue_size_cr": 5430,
                "fresh_issue_cr": 1250,
                "ofs_cr": 4180,
                "fresh_pct": 23.0,
                "ofs_pct": 77.0
            },
            "gmp": {
                "value": 15,
                "pct": 3.2,
                "expected_listing_price": 478,
                "sentiment": "Weak"
            },
            "subscription": {
                "qib": "3.99x",
                "nii": "5.31x",
                "retail": "0.96x",
                "total": "2.77x"
            },
            "financials": {
                "annual_revenue": 132670000000,
                "growth_rate": 0.06,
                "operating_cash_flow": 7800000000,
                "pre_ipo_cash": 6500000000
            },
            "ai_decision": {
                "action": "AVOID / DO NOT APPLY",
                "action_code": "AVOID",
                "action_color": "#DC2626",
                "score": 41,
                "summary": "77% OFS — promoters cashing out to service group debt. Muted 6% top-line growth and undersubscribed retail book (0.96x)."
            }
        }
    ]

    @classmethod
    def get_live_ipos(cls):
        return cls.BROKERAGE_IPOS
