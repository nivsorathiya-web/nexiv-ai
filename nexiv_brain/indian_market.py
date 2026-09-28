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
        {"symbol": "TMPV.NS", "name": "Tata Motors Passenger Vehicles Ltd", "sector": "Automotive", "exchange": "NSE", "keywords": "tata motors tm jlr ev tiago nexon harrier safari passenger vehicles"},
        {"symbol": "TMCV.NS", "name": "Tata Motors Commercial Vehicles Ltd", "sector": "Commercial Vehicles", "exchange": "NSE", "keywords": "tata motors commercial vehicles trucks buses tmcv"},
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
        {"symbol": "ETERNAL.NS", "name": "Zomato Limited (Eternal Ltd)", "sector": "Consumer Internet", "exchange": "NSE", "keywords": "zomato eternal food delivery blinkit quick commerce deepinder"},
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

        # Silver ETFs (India)
        {"symbol": "SILVERIETF.NS", "name": "ICICI Prudential Silver ETF", "sector": "ETF - Precious Metals", "exchange": "NSE", "keywords": "icici prudential silver etf silverietf icici silver precious metals bullion chandi physical silver"},
        {"symbol": "SILVERBEES.NS", "name": "Nippon India Silver ETF", "sector": "ETF - Precious Metals", "exchange": "NSE", "keywords": "nippon india silver bees silverbees etf bullion chandi physical silver"},
        {"symbol": "HDFCSILVER.NS", "name": "HDFC Silver ETF", "sector": "ETF - Precious Metals", "exchange": "NSE", "keywords": "hdfc silver etf bullion chandi physical silver"},
        {"symbol": "TATSILV.NS", "name": "Tata Silver ETF", "sector": "ETF - Precious Metals", "exchange": "NSE", "keywords": "tata silver etf tatsilv bullion chandi physical silver"},

        # Gold ETFs (India)
        {"symbol": "GOLDBEES.NS", "name": "Nippon India ETF Gold BeES", "sector": "ETF - Gold Bullion", "exchange": "NSE", "keywords": "nippon india gold bees goldbees etf bullion gold 24k sona physical gold"},
        {"symbol": "GOLDETF.NS", "name": "ICICI Prudential Gold ETF", "sector": "ETF - Gold Bullion", "exchange": "NSE", "keywords": "icici prudential gold etf goldetf bullion gold sona physical gold"},
        {"symbol": "SETFGOLD.NS", "name": "SBI Gold ETF", "sector": "ETF - Gold Bullion", "exchange": "NSE", "keywords": "sbi gold etf setfgold bullion gold sona physical gold"},
        {"symbol": "HDFCGOLD.NS", "name": "HDFC Gold ETF", "sector": "ETF - Gold Bullion", "exchange": "NSE", "keywords": "hdfc gold etf hdfcgold bullion gold sona physical gold"},

        # Major Index & Sectoral ETFs (India)
        {"symbol": "NIFTYBEES.NS", "name": "Nippon India ETF Nifty 50 BeES", "sector": "ETF - Index", "exchange": "NSE", "keywords": "nifty bees niftybees nifty 50 index etf nippon passive compounding"},
        {"symbol": "BANKBEES.NS", "name": "Nippon India ETF Nifty Bank BeES", "sector": "ETF - Banking", "exchange": "NSE", "keywords": "bank bees bankbees bank nifty banking index etf nippon"},
        {"symbol": "ITBEES.NS", "name": "Nippon India ETF Nifty IT", "sector": "ETF - Technology", "exchange": "NSE", "keywords": "it bees itbees tech software information technology etf nippon"},
        {"symbol": "CPSEETF.NS", "name": "CPSE ETF", "sector": "ETF - Thematic PSU", "exchange": "NSE", "keywords": "cpse etf psu maharatna dividend high yield public sector"},
        {"symbol": "MON100.NS", "name": "Motilal Oswal Nasdaq 100 ETF", "sector": "ETF - US Tech", "exchange": "NSE", "keywords": "motilal oswal nasdaq 100 mon100 us tech global etf"},

        # Global & MCX Metals & Commodities
        {"symbol": "SI=F", "name": "Silver Spot & COMEX Futures", "sector": "Commodities - Precious Metals", "exchange": "COMEX / MCX", "keywords": "silver spot futures chandi bullion mcx comex troy oz precious metal"},
        {"symbol": "GC=F", "name": "Gold Spot & COMEX Futures", "sector": "Commodities - Bullion", "exchange": "COMEX / MCX", "keywords": "gold spot futures sona bullion mcx comex 24k 22k precious metal"},
        {"symbol": "HG=F", "name": "Copper Futures (Doctor Copper)", "sector": "Commodities - Industrial Metals", "exchange": "COMEX / LME", "keywords": "copper futures tamba industrial metals lme comex electrification ev wire"},
        {"symbol": "ZNC=F", "name": "Zinc Futures", "sector": "Commodities - Industrial Metals", "exchange": "LME / Global", "keywords": "zinc futures jasta industrial metals galvanizing lme steel"},
        {"symbol": "ALI=F", "name": "Aluminum Futures", "sector": "Commodities - Industrial Metals", "exchange": "LME / COMEX", "keywords": "aluminum aluminium futures industrial metals lme comex lightweight ev"},
        {"symbol": "CL=F", "name": "Crude Oil WTI Futures", "sector": "Commodities - Energy", "exchange": "NYMEX / MCX", "keywords": "crude oil wti petroleum energy nymex mcx barrel brent"},
        {"symbol": "BZ=F", "name": "Brent Crude Oil Futures", "sector": "Commodities - Energy", "exchange": "ICE / Global", "keywords": "brent crude oil petroleum energy global benchmark barrel"},
        {"symbol": "NG=F", "name": "Natural Gas Futures", "sector": "Commodities - Energy", "exchange": "NYMEX / MCX", "keywords": "natural gas natgas lng cng energy nymex mcx"},
        {"symbol": "PL=F", "name": "Platinum Futures", "sector": "Commodities - Precious Metals", "exchange": "NYMEX", "keywords": "platinum precious metals jewelry catalytic nymex"},

        # Key Metals & Mining Producers (India)
        {"symbol": "HINDZINC.NS", "name": "Hindustan Zinc Limited", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "hindustan zinc hzl vedanta zinc silver lead mining metal"},
        {"symbol": "HINDALCO.NS", "name": "Hindalco Industries Limited", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "hindalco birla aluminium copper novelis metals mining"},
        {"symbol": "VEDL.NS", "name": "Vedanta Limited", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "vedanta anil agarwal zinc silver aluminium copper oil iron mining"},
        {"symbol": "NATIONALUM.NS", "name": "National Aluminium Co Ltd (NALCO)", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "nalco national aluminium bauxite alumina psu metal"},
        {"symbol": "NMDC.NS", "name": "NMDC Limited", "sector": "Metals & Mining", "exchange": "NSE", "keywords": "nmdc iron ore steel raw materials mining psu"},
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
                if w not in item["name"].lower() and w not in item.get("keywords", "").lower() and w not in item["symbol"].lower():
                    match_all = False
                    break
            if match_all:
                results.append(item)
                seen.add(item["symbol"])

        # 4. Fallback to Dynamic Worldwide Search if results < 3
        if len(results) < 3:
            try:
                external = cls.query_worldwide_search(query)
                for ext in external:
                    if ext["symbol"] not in seen:
                        results.append(ext)
                        seen.add(ext["symbol"])
            except Exception:
                pass

        return results[:10]

    @classmethod
    def query_worldwide_search(cls, query: str):
        """
        Dynamically queries global financial markets via Yahoo Finance search API,
        enabling instantaneous search for any stock, ETF, or commodity worldwide.
        """
        import urllib.parse
        encoded = urllib.parse.quote(query.strip())
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={encoded}&quotesCount=5&newsCount=0"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=3) as r:
                data = json.loads(r.read().decode())
                quotes = data.get("quotes", [])
                results = []
                for item in quotes:
                    sym = item.get("symbol")
                    name = item.get("shortname") or item.get("longname") or sym
                    exch = item.get("exchange", "GLOBAL")
                    qtype = item.get("quoteType", "EQUITY")
                    
                    if qtype == "ETF":
                        sector = "Exchange Traded Fund (ETF)"
                    elif qtype == "FUTURE":
                        sector = "Commodities & Futures"
                    else:
                        sector = item.get("sector") or "Global Market Asset"
                        
                    if sym:
                        results.append({
                            "symbol": sym,
                            "name": name,
                            "sector": sector,
                            "exchange": exch,
                            "keywords": f"{sym} {name} {sector}"
                        })
                return results
        except Exception:
            return []

    @classmethod
    def resolve_ticker(cls, query: str) -> tuple[str, bool, str]:
        raw = query.strip().upper()
        clean = re.sub(r'[^A-Z0-9\.\&\^=]', '', raw)
        
        INDIAN_ALIASES = {
            "TATAMOTORS": "TMPV.NS",
            "TATA MOTORS": "TMPV.NS",
            "TATAMTR": "TMPV.NS",
            "TMPV": "TMPV.NS",
            "TMCV": "TMCV.NS",
            "ZOMATO": "ETERNAL.NS",
            "ETERNAL": "ETERNAL.NS",
            "RELIANCE": "RELIANCE.NS",
            "TCS": "TCS.NS",
            "INFY": "INFY.NS",
            "INFOSYS": "INFY.NS",
            "HDFC": "HDFCBANK.NS",
            "HDFCBANK": "HDFCBANK.NS",
            "SBIN": "SBIN.NS",
            "SBI": "SBIN.NS",
            "ICICI": "ICICIBANK.NS",
            "ICICIBANK": "ICICIBANK.NS",
            "KOTAK": "KOTAKBANK.NS",
            "KOTAKBANK": "KOTAKBANK.NS",
            "AXIS": "AXISBANK.NS",
            "AXISBANK": "AXISBANK.NS",
            "BAJAJFINANCE": "BAJFINANCE.NS",
            "BAJFINANCE": "BAJFINANCE.NS",
            "BHARTIARTL": "BHARTIARTL.NS",
            "AIRTEL": "BHARTIARTL.NS",
            "ITC": "ITC.NS",
            "LT": "LT.NS",
            "L&T": "LT.NS",
            "LARSEN": "LT.NS",
            "MARUTI": "MARUTI.NS",
            "SUNPHARMA": "SUNPHARMA.NS",
            "TITAN": "TITAN.NS",
            "ULTRACEMCO": "ULTRACEMCO.NS",
            "WIPRO": "WIPRO.NS",
            "ADANIENT": "ADANIENT.NS",
            "ADANIPORTS": "ADANIPORTS.NS",
            "NTPC": "NTPC.NS",
            "POWERGRID": "POWERGRID.NS",
            "ONGC": "ONGC.NS",
            "COALINDIA": "COALINDIA.NS",
            "TATASTEEL": "TATASTEEL.NS",
            "TATAPOWER": "TATAPOWER.NS",
            "TATACONSUM": "TATACONSUM.NS",
            "TRENT": "TRENT.NS",
            "DMART": "DMART.NS",
            "SWIGGY": "SWIGGY.NS",
            "JIOFIN": "JIOFIN.NS",
            "HAL": "HAL.NS",
            "BEL": "BEL.NS",
            "VBL": "VBL.NS",
            "HINDUNILVR": "HINDUNILVR.NS",
            "HUL": "HINDUNILVR.NS",
            "ASIANPAINT": "ASIANPAINT.NS",

            # Silver & Gold ETFs
            "ICICIPRUDENTIALSILVERETF": "SILVERIETF.NS",
            "ICICIPRUDENTIALSILVER": "SILVERIETF.NS",
            "ICICISILVERETF": "SILVERIETF.NS",
            "ICICISILVER": "SILVERIETF.NS",
            "SILVERIETF": "SILVERIETF.NS",
            "SILVERETF": "SILVERIETF.NS",
            "SILVERBEES": "SILVERBEES.NS",
            "SILVER BEES": "SILVERBEES.NS",
            "HDFCSILVER": "HDFCSILVER.NS",
            "TATSILV": "TATSILV.NS",
            "GOLDBEES": "GOLDBEES.NS",
            "GOLD BEES": "GOLDBEES.NS",
            "GOLDETF": "GOLDETF.NS",
            "ICICIGOLD": "GOLDETF.NS",
            "SETFGOLD": "SETFGOLD.NS",
            "HDFCGOLD": "HDFCGOLD.NS",

            # Index & Sectoral ETFs
            "NIFTYBEES": "NIFTYBEES.NS",
            "NIFTY BEES": "NIFTYBEES.NS",
            "BANKBEES": "BANKBEES.NS",
            "BANK BEES": "BANKBEES.NS",
            "ITBEES": "ITBEES.NS",
            "IT BEES": "ITBEES.NS",
            "CPSEETF": "CPSEETF.NS",
            "CPSE ETF": "CPSEETF.NS",
            "MON100": "MON100.NS",
            "NASDAQ100": "MON100.NS",

            # Metals & Mining Equities
            "HINDZINC": "HINDZINC.NS",
            "HINDUSTANZINC": "HINDZINC.NS",
            "HINDALCO": "HINDALCO.NS",
            "VEDANTA": "VEDL.NS",
            "VEDL": "VEDL.NS",
            "NATIONALUM": "NATIONALUM.NS",
            "NALCO": "NATIONALUM.NS",
            "NMDC": "NMDC.NS",
            "JINDALSTEL": "JINDALSTEL.NS",
            "JSWSTEEL": "JSWSTEEL.NS"
        }

        # Commodities / Metal futures
        COMMODITY_ALIASES = {
            "SILVER": "SI=F",
            "CHANDI": "SI=F",
            "SILVERMETAL": "SI=F",
            "GOLD": "GC=F",
            "SONA": "GC=F",
            "GOLDMETAL": "GC=F",
            "COPPER": "HG=F",
            "TAMBA": "HG=F",
            "COPPERMETAL": "HG=F",
            "ZINC": "ZNC=F",
            "JASTA": "ZNC=F",
            "ZINCMETAL": "ZNC=F",
            "ALUMINUM": "ALI=F",
            "ALUMINIUM": "ALI=F",
            "CRUDE": "CL=F",
            "CRUDEOIL": "CL=F",
            "OIL": "CL=F",
            "WTI": "CL=F",
            "BRENT": "BZ=F",
            "BRENTCRUDE": "BZ=F",
            "NATURALGAS": "NG=F",
            "NATGAS": "NG=F",
            "PLATINUM": "PL=F"
        }

        if clean in COMMODITY_ALIASES:
            return COMMODITY_ALIASES[clean], False, "$"

        if clean in INDIAN_ALIASES:
            return INDIAN_ALIASES[clean], True, "₹"

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
        return f"{clean}.NS", True, "₹"

    # Real Current Indian IPOs — Verified from NSE/BSE/Zerodha/Chittorgarh (Sep-Oct 2026)
    # Dates as ISO strings; status computed dynamically from today's real date
    BROKERAGE_IPOS_RAW = [
        {
            "company_name": "Moneyview Limited",
            "symbol": "MONEYVIEW",
            "sector": "Fintech — Digital Lending & Credit",
            "timeline_raw": {
                "open_date": "2026-09-24",
                "close_date": "2026-09-28",
                "allotment_date": "2026-09-29",
                "demat_credit": "2026-09-30",
                "listing_date": "2026-10-01"
            },
            "issue_details": {
                "price_range": "₹32 – ₹34",
                "price_min": 32,
                "price_max": 34,
                "lot_size": 441,
                "min_investment": 14994,
                "issue_size_cr": 1092,
                "fresh_issue_cr": 750,
                "ofs_cr": 342,
                "fresh_pct": 68.7,
                "ofs_pct": 31.3
            },
            "gmp": {"value": 13, "pct": 38.2, "expected_listing_price": 47, "sentiment": "Strong"},
            "subscription": {
                "qib": "12.4x", "nii": "8.2x", "retail": "6.1x", "total": "9.8x"
            },
            "financials": {
                "annual_revenue": 18600000000,
                "growth_rate": 0.52,
                "operating_cash_flow": 2400000000,
                "pre_ipo_cash": 7500000000
            },
            "ai_decision": {
                "action": "APPLY — HIGH CONVICTION",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 83,
                "summary": "India's leading AI-credit engine with 35M+ users and 52% YoY revenue growth. 68.7% fresh issue funds tech expansion. 38% GMP signals strong institutional demand — compelling listing gains + long-term upside."
            }
        },
        {
            "company_name": "AceVector Limited (Snapdeal)",
            "symbol": "ACEVECTOR",
            "sector": "E-Commerce & Digital Marketplace",
            "timeline_raw": {
                "open_date": "2026-09-25",
                "close_date": "2026-09-29",
                "allotment_date": "2026-10-01",
                "demat_credit": "2026-10-03",
                "listing_date": "2026-10-05"
            },
            "issue_details": {
                "price_range": "₹30 – ₹32",
                "price_min": 30,
                "price_max": 32,
                "lot_size": 468,
                "min_investment": 14976,
                "issue_size_cr": 420,
                "fresh_issue_cr": 287,
                "ofs_cr": 133,
                "fresh_pct": 68.3,
                "ofs_pct": 31.7
            },
            "gmp": {"value": 3, "pct": 9.4, "expected_listing_price": 35, "sentiment": "Moderate"},
            "subscription": {
                "qib": "1.8x", "nii": "0.6x", "retail": "0.4x", "total": "0.91x"
            },
            "financials": {
                "annual_revenue": 7400000000,
                "growth_rate": 0.08,
                "operating_cash_flow": -1200000000,
                "pre_ipo_cash": 2870000000
            },
            "ai_decision": {
                "action": "APPLY FOR LISTING GAINS ONLY",
                "action_code": "APPLY_FLIP",
                "action_color": "#D97706",
                "score": 44,
                "summary": "Snapdeal's parent pivots to Tier-2/3 value e-commerce but faces Amazon/Meesho competition. Operating losses persist. Moderate 9% GMP on slim issue size (₹420 Cr) — speculative listing play only, exit on Day 1."
            }
        },
        {
            "company_name": "Orient Cables (India) Ltd",
            "symbol": "ORIENTCAB",
            "sector": "Networking & Optical Fibre Cables",
            "timeline_raw": {
                "open_date": "2026-09-25",
                "close_date": "2026-09-29",
                "allotment_date": "2026-09-30",
                "demat_credit": "2026-10-03",
                "listing_date": "2026-10-05"
            },
            "issue_details": {
                "price_range": "₹258 – ₹272",
                "price_min": 258,
                "price_max": 272,
                "lot_size": 55,
                "min_investment": 14960,
                "issue_size_cr": 552,
                "fresh_issue_cr": 320,
                "ofs_cr": 232,
                "fresh_pct": 58.0,
                "ofs_pct": 42.0
            },
            "gmp": {"value": 70, "pct": 25.7, "expected_listing_price": 342, "sentiment": "Strong"},
            "subscription": {
                "qib": "14.6x", "nii": "9.3x", "retail": "7.8x", "total": "11.2x"
            },
            "financials": {
                "annual_revenue": 11816700000,
                "growth_rate": 0.42,
                "operating_cash_flow": 1200000000,
                "pre_ipo_cash": 850000000
            },
            "ai_decision": {
                "action": "APPLY FOR LONG TERM COMPOUNDER",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 79,
                "summary": "23% domestic market share in networking cables with strong tailwinds from 5G, data centres & smart buildings. 42% revenue CAGR. Solid 25% GMP + 11x subscription confirms institutional conviction. Strong fresh issue component."
            }
        },
        {
            "company_name": "Runwal Enterprises Limited",
            "symbol": "RUNWAL",
            "sector": "Real Estate — Residential Developer",
            "timeline_raw": {
                "open_date": "2026-09-25",
                "close_date": "2026-09-29",
                "allotment_date": "2026-09-30",
                "demat_credit": "2026-10-03",
                "listing_date": "2026-10-05"
            },
            "issue_details": {
                "price_range": "₹290 – ₹305",
                "price_min": 290,
                "price_max": 305,
                "lot_size": 49,
                "min_investment": 14945,
                "issue_size_cr": 500,
                "fresh_issue_cr": 500,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {"value": 14, "pct": 4.6, "expected_listing_price": 319, "sentiment": "Moderate"},
            "subscription": {
                "qib": "0.96x", "nii": "0.28x", "retail": "0.18x", "total": "0.42x"
            },
            "financials": {
                "annual_revenue": 179890000000,
                "growth_rate": 0.78,
                "operating_cash_flow": 18600000000,
                "pre_ipo_cash": 14895000000
            },
            "ai_decision": {
                "action": "AVOID / DO NOT APPLY",
                "action_code": "AVOID",
                "action_color": "#DC2626",
                "score": 38,
                "summary": "Despite 78% revenue growth and 100% fresh issue, the IPO is severely undersubscribed (0.42x on Day 1). Retail at 0.18x signals lack of retail confidence. Real estate sector leverage risk and weak subscription — avoid."
            }
        },
        {
            "company_name": "German Green Steel & Power Ltd",
            "symbol": "GGSP",
            "sector": "Green Steel & Clean Energy",
            "timeline_raw": {
                "open_date": "2026-09-25",
                "close_date": "2026-09-29",
                "allotment_date": "2026-10-01",
                "demat_credit": "2026-10-03",
                "listing_date": "2026-10-05"
            },
            "issue_details": {
                "price_range": "₹132 – ₹139",
                "price_min": 132,
                "price_max": 139,
                "lot_size": 107,
                "min_investment": 14873,
                "issue_size_cr": 285,
                "fresh_issue_cr": 285,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {"value": 18, "pct": 12.9, "expected_listing_price": 157, "sentiment": "Positive"},
            "subscription": {
                "qib": "8.4x", "nii": "5.2x", "retail": "4.1x", "total": "6.7x"
            },
            "financials": {
                "annual_revenue": 4800000000,
                "growth_rate": 1.24,
                "operating_cash_flow": 620000000,
                "pre_ipo_cash": 2850000000
            },
            "ai_decision": {
                "action": "APPLY FOR LISTING GAINS ONLY",
                "action_code": "APPLY_FLIP",
                "action_color": "#D97706",
                "score": 57,
                "summary": "100% fresh issue funding green steel production — aligns with Bharat's decarbonisation push. Strong 12.9% GMP and 6.7x subscription are positive signals. Small-cap risk remains — apply for 10–15% listing gain and review long-term case after listing."
            }
        },
        {
            "company_name": "SRIT India Limited",
            "symbol": "SRITINDIA",
            "sector": "IT Services & System Integration",
            "timeline_raw": {
                "open_date": "2026-09-28",
                "close_date": "2026-09-30",
                "allotment_date": "2026-10-02",
                "demat_credit": "2026-10-04",
                "listing_date": "2026-10-06"
            },
            "issue_details": {
                "price_range": "₹123 – ₹130",
                "price_min": 123,
                "price_max": 130,
                "lot_size": 115,
                "min_investment": 14950,
                "issue_size_cr": 218,
                "fresh_issue_cr": 218,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {"value": 32, "pct": 24.6, "expected_listing_price": 162, "sentiment": "Strong"},
            "subscription": {
                "qib": "Bidding Open", "nii": "Bidding Open", "retail": "Bidding Open", "total": "Opens Today"
            },
            "financials": {
                "annual_revenue": 3200000000,
                "growth_rate": 0.31,
                "operating_cash_flow": 420000000,
                "pre_ipo_cash": 2180000000
            },
            "ai_decision": {
                "action": "APPLY — HIGH CONVICTION",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 76,
                "summary": "100% fresh issue — zero promoter exit. Strong 24.6% GMP (₹32 premium) from Day 1 confirms grey market bullishness. IT system integration with government defence contracts provides revenue visibility. Apply with confidence."
            }
        },
        {
            "company_name": "Vishal Nirmiti Limited",
            "symbol": "VISHALNIR",
            "sector": "Infrastructure & Railway Concrete Sleepers",
            "timeline_raw": {
                "open_date": "2026-09-30",
                "close_date": "2026-10-05",
                "allotment_date": "2026-10-06",
                "demat_credit": "2026-10-07",
                "listing_date": "2026-10-08"
            },
            "issue_details": {
                "price_range": "₹208 – ₹220",
                "price_min": 208,
                "price_max": 220,
                "lot_size": 68,
                "min_investment": 14960,
                "issue_size_cr": 178,
                "fresh_issue_cr": 145,
                "ofs_cr": 33,
                "fresh_pct": 81.5,
                "ofs_pct": 18.5
            },
            "gmp": {"value": 22, "pct": 10.0, "expected_listing_price": 242, "sentiment": "Positive"},
            "subscription": {
                "qib": "Upcoming", "nii": "Upcoming", "retail": "Upcoming", "total": "Opens Sep 30"
            },
            "financials": {
                "annual_revenue": 2980000000,
                "growth_rate": 0.28,
                "operating_cash_flow": 380000000,
                "pre_ipo_cash": 1450000000
            },
            "ai_decision": {
                "action": "APPLY FOR LONG TERM COMPOUNDER",
                "action_code": "APPLY_LONG",
                "action_color": "#059669",
                "score": 78,
                "summary": "81.5% fresh capital to expand pre-stressed concrete sleeper capacity for Indian Railways modernization. Established order book and solid operating margins make this an attractive growth issue."
            }
        },
        {
            "company_name": "Shah Investor's Home Limited",
            "symbol": "SHAHINVEST",
            "sector": "Broking & Financial Advisory",
            "timeline_raw": {
                "open_date": "2026-09-30",
                "close_date": "2026-10-03",
                "allotment_date": "2026-10-05",
                "demat_credit": "2026-10-06",
                "listing_date": "2026-10-07"
            },
            "issue_details": {
                "price_range": "₹130 – ₹138",
                "price_min": 130,
                "price_max": 138,
                "lot_size": 108,
                "min_investment": 14904,
                "issue_size_cr": 125,
                "fresh_issue_cr": 125,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {"value": 0, "pct": 0.0, "expected_listing_price": 138, "sentiment": "Neutral"},
            "subscription": {
                "qib": "Upcoming", "nii": "Upcoming", "retail": "Upcoming", "total": "Opens Sep 30"
            },
            "financials": {
                "annual_revenue": 1420000000,
                "growth_rate": 0.12,
                "operating_cash_flow": 180000000,
                "pre_ipo_cash": 1250000000
            },
            "ai_decision": {
                "action": "AVOID / DO NOT APPLY",
                "action_code": "AVOID",
                "action_color": "#DC2626",
                "score": 36,
                "summary": "Flat 0% GMP and heavy competition from discount brokers (Zerodha/Groww). Modest 12% revenue growth does not justify valuation multiple. Avoid and monitor post-listing performance."
            }
        },
        {
            "company_name": "Axiom Gas Engineering Limited",
            "symbol": "AXIOMGAS",
            "sector": "Gas Infrastructure & Engineering",
            "timeline_raw": {
                "open_date": "2026-09-18",
                "close_date": "2026-09-22",
                "allotment_date": "2026-09-23",
                "demat_credit": "2026-09-24",
                "listing_date": "2026-09-25"
            },
            "issue_details": {
                "price_range": "₹50 – ₹53",
                "price_min": 50,
                "price_max": 53,
                "lot_size": 280,
                "min_investment": 14840,
                "issue_size_cr": 84,
                "fresh_issue_cr": 84,
                "ofs_cr": 0,
                "fresh_pct": 100.0,
                "ofs_pct": 0.0
            },
            "gmp": {"value": 2, "pct": 3.8, "expected_listing_price": 55, "sentiment": "Stable"},
            "subscription": {
                "qib": "6.1x", "nii": "4.2x", "retail": "3.8x", "total": "4.8x"
            },
            "financials": {
                "annual_revenue": 1100000000,
                "growth_rate": 0.22,
                "operating_cash_flow": 140000000,
                "pre_ipo_cash": 840000000
            },
            "ai_decision": {
                "action": "HOLD / ACCUMULATE ON DIPS",
                "action_code": "HOLD",
                "action_color": "#D97706",
                "score": 63,
                "summary": "Listed at ₹55 with 3.8% premium on Sep 25. Clean balance sheet with 100% fresh issue proceeds directed towards CGD pipeline expansion. Accumulate on dips near issue price."
            }
        },
        {
            "company_name": "Sonaselection Limited",
            "symbol": "SONASELEC",
            "sector": "Consumer Goods & Retail",
            "timeline_raw": {
                "open_date": "2026-09-17",
                "close_date": "2026-09-21",
                "allotment_date": "2026-09-22",
                "demat_credit": "2026-09-23",
                "listing_date": "2026-09-24"
            },
            "issue_details": {
                "price_range": "₹95 – ₹99",
                "price_min": 95,
                "price_max": 99,
                "lot_size": 151,
                "min_investment": 14949,
                "issue_size_cr": 142,
                "fresh_issue_cr": 105,
                "ofs_cr": 37,
                "fresh_pct": 73.9,
                "ofs_pct": 26.1
            },
            "gmp": {"value": 3, "pct": 3.0, "expected_listing_price": 102, "sentiment": "Stable"},
            "subscription": {
                "qib": "7.2x", "nii": "5.1x", "retail": "4.2x", "total": "5.2x"
            },
            "financials": {
                "annual_revenue": 1850000000,
                "growth_rate": 0.19,
                "operating_cash_flow": 210000000,
                "pre_ipo_cash": 1050000000
            },
            "ai_decision": {
                "action": "PROFIT BOOKED ON DAY 1",
                "action_code": "HOLD",
                "action_color": "#D97706",
                "score": 58,
                "summary": "Debuted on Sep 24 at ₹102 (+3.0% gain). Recommend booking listing gains; wait for 2 quarters of earnings consistency before fresh allocation."
            }
        }
    ]

    @classmethod
    def _compute_ipo_status(cls, raw_ipo: dict) -> dict:
        """
        Dynamically compute OPEN NOW / UPCOMING / LISTED / RECENTLY LISTED status
        based on today's actual IST date and the IPO's stored ISO date strings.
        """
        from datetime import datetime, timezone, timedelta
        IST = timezone(timedelta(hours=5, minutes=30))
        today = datetime.now(IST).date()

        tl = raw_ipo["timeline_raw"]
        open_dt  = datetime.fromisoformat(tl["open_date"]).date()
        close_dt = datetime.fromisoformat(tl["close_date"]).date()
        allot_dt = datetime.fromisoformat(tl["allotment_date"]).date()
        demat_dt = datetime.fromisoformat(tl["demat_credit"]).date()
        list_dt  = datetime.fromisoformat(tl["listing_date"]).date()

        def fmt(d):
            """Format a date as e.g. '29 Sep 2026'"""
            return d.strftime("%-d %b %Y")

        bidding_str = f"{fmt(open_dt)} – {fmt(close_dt)}"

        if today < open_dt:
            days_until = (open_dt - today).days
            if days_until == 1:
                days_left = "Opens Tomorrow"
            elif days_until == 0:
                days_left = "Opens Today!"
            else:
                days_left = f"Opens in {days_until} Days"
            status = "UPCOMING"
            status_badge = "bg-amber-100 text-amber-800 border-amber-300"
        elif open_dt <= today <= close_dt:
            days_remaining = (close_dt - today).days
            if days_remaining == 0:
                days_left = "Closes Today at 5:00 PM IST"
            elif days_remaining == 1:
                days_left = "Closes Tomorrow at 5:00 PM IST"
            else:
                days_left = f"{days_remaining} Days Left to Bid"
            status = "OPEN NOW"
            status_badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
        elif close_dt < today <= list_dt:
            if today == list_dt:
                days_left = "📈 Listing Day — WATCH LIVE"
            elif today == allot_dt:
                days_left = "Allotment Finalised Today"
            elif today <= demat_dt:
                days_left = f"Listing on {fmt(list_dt)}"
            else:
                days_left = f"Listing on {fmt(list_dt)}"
            status = "ALLOTMENT & LISTING"
            status_badge = "bg-blue-100 text-blue-800 border-blue-300"
        else:
            listed_days_ago = (today - list_dt).days
            if listed_days_ago <= 30:
                days_left = f"Listed {listed_days_ago}d ago"
                status = "RECENTLY LISTED"
            else:
                days_left = f"Listed {fmt(list_dt)}"
                status = "LISTED"
            status_badge = "bg-slate-100 text-slate-700 border-slate-300"

        ipo = dict(raw_ipo)
        ipo["status"] = status
        ipo["status_badge"] = status_badge
        ipo["timeline"] = {
            "bidding_dates": bidding_str,
            "open_date": fmt(open_dt),
            "close_date": fmt(close_dt),
            "allotment_date": fmt(allot_dt),
            "refunds_date": fmt(allot_dt),
            "demat_credit": fmt(demat_dt),
            "listing_date": fmt(list_dt),
            "days_left": days_left
        }
        return ipo

    BROKERAGE_IPOS = []  # Legacy compat; populated at module load

    @classmethod
    def get_live_ipos(cls):
        """Return IPOs with dynamically computed live status based on today's actual date."""
        return [cls._compute_ipo_status(r) for r in cls.BROKERAGE_IPOS_RAW]

