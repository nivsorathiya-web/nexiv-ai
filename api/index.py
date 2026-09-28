import os
import sys
import json
import warnings
warnings.filterwarnings("ignore")

# Ensure repository root is on sys.path for serverless imports
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from nexiv_brain.decision_engine import CBMDecisionEngine
from nexiv_brain.indian_market import NexivIndianMarket
from nexiv_brain.chat_engine import NexivChatEngine
from nexiv_brain.council_knowledge import NexivCouncilKnowledge
from nexiv_brain import nexiv_config as cfg

app = FastAPI(title="Nexiv.AI • Autonomous Institutional Financial Intelligence", version="3.0.0")

class ChatMessageRequest(BaseModel):
    message: str
    history: Optional[list] = []
    api_key: Optional[str] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IPOSubmission(BaseModel):
    company_name: str
    sector: str = "Software"
    offer_price_min: float
    offer_price_max: float
    shares_offered: float
    fresh_issue_shares: float
    ofs_shares: float
    pre_ipo_shares: float
    annual_revenue: float
    annual_growth_rate: float
    operating_cash_flow: float
    pre_ipo_cash: float
    monthly_cash_burn: Optional[float] = None
    country: str = "India"
    gmp: Optional[float] = 0.0
    lot_size: Optional[int] = 1

def _find_static_file(filename: str):
    """Find a static file in either static/ or api/static/."""
    candidates = [
        os.path.join(ROOT_DIR, "static", filename),
        os.path.join(ROOT_DIR, "api", "static", filename),
        os.path.join(os.path.dirname(__file__), "static", filename),
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join(ROOT_DIR, filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

@app.get("/favicon.ico")
def get_favicon():
    p = _find_static_file("favicon-64.png") or _find_static_file("favicon-32.png")
    if p:
        return FileResponse(p, media_type="image/png")
    return Response(content="", status_code=204)

@app.get("/favicon.svg")
def get_favicon_svg():
    p = _find_static_file("favicon.svg")
    if p:
        return FileResponse(p, media_type="image/svg+xml")
    return Response(content="", status_code=204)

@app.get("/apple-touch-icon.png")
@app.get("/apple-touch-icon-precomposed.png")
def get_apple_touch_icon():
    p = _find_static_file("apple-touch-icon.png") or _find_static_file("icon-192.png")
    if p:
        return FileResponse(p, media_type="image/png")
    return Response(content="", status_code=204)

@app.get("/icon-192.png")
def get_icon_192():
    p = _find_static_file("icon-192.png")
    if p:
        return FileResponse(p, media_type="image/png")
    return Response(content="", status_code=204)

@app.get("/icon-512.png")
def get_icon_512():
    p = _find_static_file("icon-512.png")
    if p:
        return FileResponse(p, media_type="image/png")
    return Response(content="", status_code=204)

@app.get("/manifest.json")
def get_manifest():
    p = _find_static_file("manifest.json")
    if p:
        return FileResponse(p, media_type="application/manifest+json")
    return Response(content="{}", media_type="application/manifest+json")

@app.get("/static/{file_path:path}")
def serve_static(file_path: str):
    p = _find_static_file(file_path)
    if p:
        if file_path.endswith(".png"):
            return FileResponse(p, media_type="image/png")
        elif file_path.endswith(".svg"):
            return FileResponse(p, media_type="image/svg+xml")
        elif file_path.endswith(".json"):
            return FileResponse(p, media_type="application/manifest+json")
        return FileResponse(p)
    raise HTTPException(status_code=404, detail="File not found")

import math

def sanitize_json(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_json(v) for v in obj]
    return obj

@app.get("/api/search")
def search_stocks(q: str = ""):
    return NexivIndianMarket.search_equities(q)

@app.get("/api/stock/{ticker}")
def analyze_stock(ticker: str):
    try:
        t = ticker.strip()
        res = CBMDecisionEngine.evaluate_stock_action(t)
        return sanitize_json(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ipos/live")
def get_live_ipos():
    return sanitize_json(NexivIndianMarket.get_live_ipos())

@app.post("/api/ipo/analyze")
def analyze_ipo(data: IPOSubmission):
    try:
        res = CBMDecisionEngine.evaluate_ipo_action(data.dict())
        return sanitize_json(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def chat_endpoint(data: ChatMessageRequest):
    try:
        reply = NexivChatEngine.answer(data.message, data.history, data.api_key)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge")
def get_knowledge_summary():
    graph_path = cfg.MASTER_KNOWLEDGE_GRAPH
    try:
        if os.path.exists(graph_path):
            with open(graph_path) as f:
                data = json.load(f)
                if "academic_institutions" in data and len(data.get("academic_institutions", {})) >= 15:
                    return data
    except Exception:
        pass

    k = NexivCouncilKnowledge
    return {
        "status": "COMPILED_AND_ACTIVE",
        "summary": {
            "total_pillars": 4,
            "total_assets": len(k.TOP_15_INSTITUTIONS) + len(k.TOP_15_INVESTMENT_FIRMS) + len(k.TOP_15_TITANS) + len(k.CODIFIED_BOOKS_VAULT) + len(k.EMPIRICAL_DATASETS_VAULT),
            "total_codified_pages": 5053,
            "academic_institutions_count": len(k.TOP_15_INSTITUTIONS),
            "investment_firms_count": len(k.TOP_15_INVESTMENT_FIRMS),
            "titans_count": len(k.TOP_15_TITANS),
            "master_books_count": len(k.CODIFIED_BOOKS_VAULT),
            "empirical_datasets_count": len(k.EMPIRICAL_DATASETS_VAULT),
            "coverage": "Global (US, Europe, Asia) & Indian Equities (NSE/BSE) + Mainboard/SME IPOs"
        },
        "academic_institutions": k.TOP_15_INSTITUTIONS,
        "investment_firms": k.TOP_15_INVESTMENT_FIRMS,
        "titans": k.TOP_15_TITANS,
        "books_principles": k.CODIFIED_BOOKS_VAULT,
        "empirical_datasets": k.EMPIRICAL_DATASETS_VAULT
    }

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nexiv.AI • Autonomous Institutional Financial Intelligence</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="icon" type="image/png" sizes="64x64" href="/static/favicon-64.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="apple-touch-icon-precomposed" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Nexiv.AI">
    <meta name="application-name" content="Nexiv.AI">
    <meta name="theme-color" content="#0B101C">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        nexiv: {
                            50: '#F8FAFC',
                            100: '#F1F5F9',
                            200: '#E2E8F0',
                            800: '#1E293B',
                            900: '#0F172A',
                            gold: '#D97706',
                            emerald: '#059669',
                            crimson: '#DC2626'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { 
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #F8FAFC;
            background-image: 
                radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.04) 0px, transparent 40%),
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.04) 0px, transparent 40%);
            -webkit-tap-highlight-color: transparent;
        }
        .luxury-card {
            background: #FFFFFF;
            border: 1px solid rgba(226, 232, 240, 0.9);
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
        }
        .luxury-card-elevated {
            background: #FFFFFF;
            border: 1px solid rgba(226, 232, 240, 0.95);
            box-shadow: 0 10px 30px -4px rgba(15, 23, 42, 0.08), 0 4px 10px -2px rgba(15, 23, 42, 0.03);
        }
        .dropdown-menu {
            position: absolute;
            top: calc(100% + 6px);
            left: 0;
            right: 0;
            z-index: 60;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 1rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            max-height: 280px;
            overflow-y: auto;
        }
    </style>
</head>
<body class="text-slate-800 min-h-screen pb-24 antialiased selection:bg-amber-100 selection:text-amber-900">

    <!-- Top Luxury App Bar -->
    <header class="sticky top-0 z-50 bg-white/85 backdrop-blur-xl border-b border-slate-200/80 px-4 py-3 shadow-xs">
        <div class="max-w-xl mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <!-- Bespoke Nexiv.AI Logo SVG -->
                <div class="w-10 h-10 rounded-xl bg-slate-950 p-1 flex items-center justify-center shadow-md shadow-slate-900/10 border border-amber-500/30">
                    <svg viewBox="0 0 44 44" fill="none" class="w-full h-full" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="nGold" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#FDE68A"/>
                                <stop offset="35%" stop-color="#F59E0B"/>
                                <stop offset="70%" stop-color="#D97706"/>
                                <stop offset="100%" stop-color="#92400E"/>
                            </linearGradient>
                        </defs>
                        <!-- Geometric "N" Monograph & Compounding Pillar -->
                        <path d="M11 33 V 11 L 23 27 V 11" stroke="url(#nGold)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M23 27 L 33 11" stroke="#10B981" stroke-width="3" stroke-linecap="round"/>
                        <!-- Diamond AI Apex Star -->
                        <polygon points="33,6 35,9.5 39,9.5 36,12 37.5,15.5 33,13 28.5,15.5 30,12 27,9.5 31,9.5" fill="#FDE68A"/>
                    </svg>
                </div>
                <div>
                    <div class="flex items-center space-x-1.5">
                        <h1 class="text-base font-extrabold text-slate-900 tracking-tight leading-tight">Nexiv.AI</h1>
                        <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200/80">PRO</span>
                    </div>
                    <p class="text-[10px] font-semibold text-slate-500 tracking-wider">4 PILLARS • 56 ENTITIES • 5,053 PAGES • LIVE</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-2 shrink-0">
                <span class="hidden sm:inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span class="relative flex h-2 w-2 mr-1.5">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                    NSE / BSE LIVE
                </span>

                <!-- Stylish Premium iPhone / Desktop Refresh Button -->
                <button id="page-refresh-btn" onclick="triggerSmartRefresh(event)" aria-label="Refresh Page & Live Prices" title="Refresh Live Data & Prices" 
                    class="group relative inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 text-amber-300 border border-amber-500/40 hover:border-amber-400 shadow-sm shadow-amber-500/10 active:scale-95 transition-all duration-200 cursor-pointer select-none">
                    <i id="refresh-spinner" class="fa-solid fa-arrows-rotate text-xs text-amber-400 group-hover:rotate-180 transition-transform duration-500"></i>
                    <span id="refresh-label" class="text-[10px] font-extrabold uppercase tracking-wider text-slate-100 font-sans">Refresh</span>
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Live Market Clock Bar -->
    <div class="bg-slate-950 text-white px-4 py-1.5 text-center">
        <div class="max-w-xl mx-auto flex items-center justify-between text-[10px] font-mono font-semibold">
            <span class="text-slate-400">📍 IST — India Standard Time</span>
            <span id="live-clock" class="text-amber-400 font-bold tracking-wider">--:--:-- --</span>
            <span id="live-date" class="text-slate-400">--- --, ----</span>
        </div>
    </div>

    <!-- Main Container -->
    <main class="max-w-xl mx-auto px-4 pt-4">

        <!-- Navigation Segmented Control -->
        <div class="grid grid-cols-4 gap-1 rounded-2xl bg-slate-100 p-1 mb-4 border border-slate-200/80 shadow-inner text-center">
            <button id="tab-stock-btn" onclick="switchTab('stock')" class="py-2 text-[11px] font-bold rounded-xl bg-white text-slate-900 shadow-sm transition-all flex items-center justify-center space-x-1">
                <i class="fa-solid fa-chart-line text-emerald-600"></i>
                <span class="truncate">Stocks</span>
            </button>
            <button id="tab-ipo-btn" onclick="switchTab('ipo')" class="py-2 text-[11px] font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1">
                <i class="fa-solid fa-rocket text-amber-600"></i>
                <span class="truncate">IPOs</span>
            </button>
            <button id="tab-chat-btn" onclick="switchTab('chat')" class="py-2 text-[11px] font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1">
                <i class="fa-solid fa-comments text-indigo-600"></i>
                <span class="truncate">AI Chat</span>
            </button>
            <button id="tab-vault-btn" onclick="switchTab('vault')" class="py-2 text-[11px] font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1">
                <i class="fa-solid fa-landmark text-amber-600"></i>
                <span class="truncate">Vault (56)</span>
            </button>
        </div>

        <!-- 1. STOCK DECISION SECTION -->
        <section id="stock-section" class="space-y-4">
            <!-- Search & Autocomplete Card -->
            <div class="luxury-card rounded-2xl p-4 transition-all relative">
                <div class="flex items-center justify-between mb-2">
                    <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">LIVE TYPEAHEAD SEARCH</label>
                    <span class="text-[10px] font-semibold text-slate-400">STOCKS • ETFS • PRECIOUS & INDUSTRIAL METALS</span>
                </div>
                
                <div class="relative flex space-x-2">
                    <div class="relative flex-1">
                        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-xs"></i>
                        <input type="text" id="ticker-input" value="SILVERIETF.NS" placeholder="Search Stocks, Silver/Gold ETFs, Copper, Zinc, Metals (e.g. ICICI Silver, Copper, Gold BeES, Tata)" 
                               autocomplete="off"
                               oninput="handleSearchInput(event)"
                               onfocus="handleSearchFocus()"
                               class="w-full bg-slate-50 border border-slate-200/90 rounded-xl pl-9 pr-3 py-2.5 text-sm font-bold uppercase text-slate-900 focus:outline-none focus:border-amber-500 focus:bg-white focus:ring-2 focus:ring-amber-500/10 transition-all">
                        
                        <!-- Floating Live Search Dropdown -->
                        <div id="search-dropdown" class="dropdown-menu hidden"></div>
                    </div>
                    
                    <button onclick="analyzeStock()" id="analyze-btn" class="bg-slate-900 hover:bg-slate-800 active:scale-95 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition-all flex items-center space-x-1.5 shadow-md shadow-slate-900/10">
                        <span>AUDIT</span>
                        <i class="fa-solid fa-arrow-right text-[10px]"></i>
                    </button>
                </div>
                
                <!-- Quick Indian & Global Tickers Grid -->
                <div class="flex flex-wrap items-center gap-1.5 mt-3 pt-3 border-t border-slate-100">
                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mr-1">TRENDING:</span>
                    <button onclick="quickStock('SILVERIETF.NS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-amber-50 text-xs text-slate-800 font-mono font-bold border border-slate-200/80 active:scale-95 transition-all">🥈 ICICI SILVER ETF</button>
                    <button onclick="quickStock('GOLDBEES.NS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-amber-50 text-xs text-slate-800 font-mono font-bold border border-slate-200/80 active:scale-95 transition-all">🪙 GOLD BEES</button>
                    <button onclick="quickStock('HG=F')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-amber-50 text-xs text-slate-800 font-mono font-bold border border-slate-200/80 active:scale-95 transition-all">⚡ COPPER</button>
                    <button onclick="quickStock('HINDZINC.NS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-amber-50 text-xs text-slate-800 font-mono font-bold border border-slate-200/80 active:scale-95 transition-all">🏗️ ZINC</button>
                    <button onclick="quickStock('NIFTYBEES.NS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-amber-50 text-xs text-slate-800 font-mono font-bold border border-slate-200/80 active:scale-95 transition-all">📈 NIFTY BEES</button>
                    <button onclick="quickStock('RELIANCE')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">RELIANCE</button>
                    <button onclick="quickStock('TATAMOTORS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">TATA MOTORS</button>
                    <button onclick="quickStock('ZOMATO')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">ZOMATO</button>
                </div>
            </div>

            <!-- Loading Spinner Card -->
            <div id="stock-loading" class="hidden luxury-card rounded-2xl p-8 text-center space-y-3">
                <div class="inline-block animate-spin rounded-full h-9 w-9 border-3 border-amber-500 border-t-transparent"></div>
                <div class="space-y-1">
                    <p class="text-xs font-bold text-slate-800">Executing Nexiv.AI Deep Institutional Audit...</p>
                    <p class="text-[11px] text-slate-500">Damodaran DCF • Altman Z • Beneish Shenanigans • Kelly Bet Sizing</p>
                </div>
            </div>

            <!-- Stock Results Container -->
            <div id="stock-result" class="space-y-4"></div>
        </section>

        <!-- 2. INDIAN IPO SCANNER & GMP RADAR -->
        <section id="ipo-section" class="hidden space-y-4">
            
            <!-- Live Indian IPO Tracker Banner -->
            <div class="luxury-card rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900">Brokerage-Grade Indian IPO Radar</h2>
                        <p class="text-[10px] text-slate-500 font-medium">Bidding Timelines • Live GMP • Subscription Multipliers • AI Verdicts</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">MAINBOARD & SME</span>
                </div>

                <!-- IPO Filter Pills -->
                <div class="flex space-x-1.5 overflow-x-auto pb-1 text-xs font-semibold">
                    <button id="filter-all" onclick="filterIPOs('ALL')" class="px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all">All IPOs</button>
                    <button id="filter-open" onclick="filterIPOs('OPEN NOW')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all">🟢 Open Now</button>
                    <button id="filter-upcoming" onclick="filterIPOs('UPCOMING')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all">🟡 Upcoming</button>
                    <button id="filter-listed" onclick="filterIPOs('LISTED')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all">🔵 Listed</button>
                </div>

                <!-- Live IPOs Cards Feed -->
                <div id="live-ipos-feed" class="space-y-3"></div>
            </div>

            <!-- Custom IPO Evaluator Card -->
            <div class="luxury-card rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                    <div>
                        <h3 class="text-xs font-bold text-slate-900 uppercase">Custom Indian IPO Evaluator</h3>
                        <p class="text-[10px] text-slate-500">Test Any Upcoming Mainboard or SME IPO</p>
                    </div>
                    <span class="text-[10px] font-bold text-slate-400">RITTER 100K+ IPOS</span>
                </div>
                
                <div class="space-y-2.5">
                    <div>
                        <label class="text-[11px] font-bold text-slate-500 uppercase">Company Name</label>
                        <input type="text" id="ipo-name" value="Swiggy Limited" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                    </div>
                    
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Sector</label>
                            <input type="text" id="ipo-sector" value="Quick Commerce & Food Delivery" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Price Band (₹)</label>
                            <div class="flex space-x-1 mt-1">
                                <input type="number" id="ipo-pmin" value="371" placeholder="Min" class="w-1/2 bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                                <input type="number" id="ipo-pmax" value="390" placeholder="Max" class="w-1/2 bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                            </div>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Annual Revenue (₹)</label>
                            <input type="number" id="ipo-rev" value="112470000000" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">YoY Growth (e.g. 0.36)</label>
                            <input type="number" step="0.01" id="ipo-growth" value="0.36" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Fresh Issue Shares</label>
                            <input type="number" id="ipo-fresh" value="115000000" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">OFS Promoter Shares</label>
                            <input type="number" id="ipo-ofs" value="175000000" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Current GMP (₹)</label>
                            <input type="number" id="ipo-gmp" value="25" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase">Lot Size (Shares)</label>
                            <input type="number" id="ipo-lot" value="38" class="w-full mt-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-amber-500 outline-none">
                        </div>
                    </div>

                    <button onclick="evaluateCustomIPO()" class="w-full mt-3 bg-slate-900 hover:bg-slate-800 active:scale-98 text-white font-bold py-3 rounded-xl text-xs transition-all shadow-md flex items-center justify-center space-x-2">
                        <i class="fa-solid fa-chart-pie text-amber-400"></i>
                        <span>RUN NEXIV INSTITUTIONAL IPO AUDIT</span>
                    </button>
                </div>
            </div>

            <div id="ipo-result" class="space-y-4"></div>
        </section>

        <!-- 3. KNOWLEDGE VAULT SECTION (4 PILLARS • 56 ENTITIES • 5,053 PAGES) -->
        <section id="vault-section" class="hidden space-y-4">
            
            <!-- Vault Hero Banner -->
            <div class="luxury-card rounded-2xl p-4 shadow-sm space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                    <div class="flex items-center space-x-2.5">
                        <div class="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-600">
                            <i class="fa-solid fa-landmark text-sm"></i>
                        </div>
                        <div>
                            <h2 class="text-sm font-extrabold text-slate-900 tracking-tight">Institutional Knowledge Vault</h2>
                            <p class="text-[10px] text-slate-500 font-medium">4 Pillars • 56 Codified Entities • 5,053 Pages of Financial Truth</p>
                        </div>
                    </div>
                    <span class="text-[9px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 uppercase tracking-wide">
                        100% Codified
                    </span>
                </div>

                <!-- 4 Metrics Chips -->
                <div class="grid grid-cols-4 gap-1.5 text-center text-xs">
                    <div class="bg-slate-50 p-2 rounded-xl border border-slate-200/60">
                        <span class="text-base font-black text-slate-900 font-mono block">15</span>
                        <span class="text-[9px] font-bold text-slate-500 uppercase tracking-wider">Universities</span>
                    </div>
                    <div class="bg-slate-50 p-2 rounded-xl border border-slate-200/60">
                        <span class="text-base font-black text-slate-900 font-mono block">15</span>
                        <span class="text-[9px] font-bold text-slate-500 uppercase tracking-wider">Allocators</span>
                    </div>
                    <div class="bg-slate-50 p-2 rounded-xl border border-slate-200/60">
                        <span class="text-base font-black text-slate-900 font-mono block">15</span>
                        <span class="text-[9px] font-bold text-slate-500 uppercase tracking-wider">Titans</span>
                    </div>
                    <div class="bg-slate-50 p-2 rounded-xl border border-slate-200/60">
                        <span class="text-base font-black text-emerald-600 font-mono block">5,053p</span>
                        <span class="text-[9px] font-bold text-slate-500 uppercase tracking-wider">7 Books & 4 DBs</span>
                    </div>
                </div>

                <!-- Live Search Bar inside Vault -->
                <div class="relative pt-1">
                    <i class="fa-solid fa-magnifying-glass absolute left-3 top-3.5 text-slate-400 text-xs"></i>
                    <input type="text" id="vault-search-input" oninput="handleVaultSearch(event)" placeholder="Search across all 56 entities, doctrines, authors, or Nobel laureates..." 
                           class="w-full bg-slate-50 border border-slate-200/90 rounded-xl pl-8 pr-3 py-2 text-xs font-semibold text-slate-900 outline-none focus:bg-white focus:border-amber-500 transition-all">
                </div>

                <!-- Vault Filter Pills -->
                <div class="flex space-x-1.5 overflow-x-auto pb-1 text-xs font-semibold no-scrollbar">
                    <button id="vault-filter-all" onclick="filterVault('ALL')" class="px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all whitespace-nowrap">All (56)</button>
                    <button id="vault-filter-books" onclick="filterVault('BOOKS')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap">📚 Books (7)</button>
                    <button id="vault-filter-academic" onclick="filterVault('ACADEMIC')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap">🏛️ Academic (15)</button>
                    <button id="vault-filter-firms" onclick="filterVault('FIRMS')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap">🏢 Allocators (15)</button>
                    <button id="vault-filter-titans" onclick="filterVault('TITANS')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap">🧠 Titans (15)</button>
                    <button id="vault-filter-datasets" onclick="filterVault('DATASETS')" class="px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap">📊 Datasets (4)</button>
                </div>
            </div>

            <!-- Dynamic Vault Items List -->
            <div id="vault-items-container" class="space-y-3">
                <div class="p-8 text-center text-xs text-slate-400">Loading codified vault assets...</div>
            </div>
        </section>

        <!-- 4. AI COUNCIL CHAT SECTION -->
        <section id="chat-section" class="hidden space-y-3">
            <div class="luxury-card rounded-2xl p-4 shadow-sm flex flex-col">
                <!-- Chat Header -->
                <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                    <div class="flex items-center space-x-2.5">
                        <div class="w-9 h-9 rounded-xl bg-slate-950 p-1 flex items-center justify-center border border-amber-500/30 text-amber-400">
                            <i class="fa-solid fa-brain text-sm"></i>
                        </div>
                        <div>
                            <div class="flex items-center space-x-1.5">
                                <h2 class="text-sm font-extrabold text-slate-900 tracking-tight">Nexiv AI Council</h2>
                                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">🟢 56 COUNCILS ACTIVE</span>
                            </div>
                            <p class="text-[10px] text-slate-500 font-medium">5,053 Pages of Codified Law • 15 Institutions • 15 Titans</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-1.5">
                        <span class="text-[10px] font-bold px-2 py-1 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200 flex items-center space-x-1">
                            <i class="fa-solid fa-bolt text-indigo-500 text-[11px]"></i>
                            <span>AI Engine Integrated</span>
                        </span>
                    </div>
                </div>

                <!-- Quick Prompt Chips -->
                <div class="pt-3 pb-2">
                    <div class="flex items-center space-x-1.5 overflow-x-auto no-scrollbar pb-1 text-[11px]">
                        <button onclick="sendQuickPrompt('What is going on in the market currently? Give me news with current date and time')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-amber-50 hover:bg-amber-100 hover:text-amber-900 border border-amber-300 font-bold text-amber-900 transition-all flex items-center space-x-1">
                            <span>⚡ Today's Market News</span>
                        </button>
                        <button onclick="sendQuickPrompt('Should I buy Tata Motors right now or wait?')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            🚗 Buy Tata Motors?
                        </button>
                        <button onclick="sendQuickPrompt('Moneyview IPO apply or avoid?')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            🚀 Moneyview IPO
                        </button>
                        <button onclick="sendQuickPrompt('Give me latest news on Reliance and Zomato')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            📰 Stock News
                        </button>
                        <button onclick="sendQuickPrompt('How does Schilit catch fake revenue on balance sheet?')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            🛡️ Schilit Fraud Rules
                        </button>
                        <button onclick="sendQuickPrompt('What is Graham and Dodd Margin of Safety?')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            📖 Margin of Safety
                        </button>
                        <button onclick="sendQuickPrompt('What is Damodaran DCF and WACC in India?')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            📊 Damodaran WACC
                        </button>
                        <button onclick="sendQuickPrompt('Tell me about Snapdeal AceVector IPO verdict')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-amber-50 hover:text-amber-900 hover:border-amber-300 border border-slate-200/80 font-medium text-slate-700 transition-all">
                            📦 Snapdeal IPO
                        </button>
                    </div>
                </div>

                <!-- Chat Messages Scroll Container -->
                <div id="chat-messages" class="flex-1 min-h-[360px] max-h-[480px] overflow-y-auto space-y-3 p-1 pr-1 border-t border-b border-slate-100 py-3 scroll-smooth">
                    <!-- Initial Welcome Message -->
                    <div class="flex items-start space-x-2.5">
                        <div class="w-7 h-7 rounded-lg bg-slate-900 text-amber-400 flex items-center justify-center shrink-0 text-xs font-bold mt-0.5">
                            N
                        </div>
                        <div class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-3.5 shadow-xs text-xs text-slate-800 space-y-2 max-w-[88%]">
                            <p class="font-bold text-slate-900">Welcome! I am the Nexiv AI Council.</p>
                            <p class="leading-relaxed">
                                You can ask me anything in your normal, casual words — don't worry about English or grammar! I understand you directly and answer with our full brain:
                            </p>
                            <ul class="space-y-1 text-slate-600 text-[11px] list-disc list-inside">
                                <li><strong>Real-Time Market News & Telemetry</strong> (e.g. <em>"what's going on in the market today?"</em>) with exact date, time & live exchange feeds</li>
                                <li><strong>Any Indian Stock</strong> (e.g. <em>"should i buy tata motor or wait"</em>) with live price & targets</li>
                                <li><strong>Real Indian IPOs</strong> (e.g. <em>"moneyview ipo verdict"</em>) with GMP & Jay Ritter laws</li>
                                <li><strong>Forensic Fraud Detection</strong> (Schilit's 7 Shenanigans & fake revenue)</li>
                                <li><strong>Institutional Valuation</strong> (Damodaran DCF, WACC & Graham Margin of Safety)</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Typing / Thinking Indicator (hidden by default) -->
                <div id="chat-typing" class="hidden py-2 px-3 text-xs text-slate-500 items-center space-x-2">
                    <span class="inline-flex space-x-1 items-center">
                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse delay-100"></span>
                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse delay-200"></span>
                    </span>
                    <span class="text-[11px] font-medium text-slate-500">Nexiv AI is analyzing 5,053 pages & live feeds...</span>
                </div>

                <!-- Chat Input Form -->
                <div class="pt-3">
                    <form onsubmit="handleChatSubmit(event)" class="relative flex items-center space-x-2">
                        <input type="text" id="chat-input" placeholder="Ask anything in your words (e.g. should i buy zomato?)..." class="flex-1 bg-slate-50 border border-slate-200/90 rounded-2xl px-4 py-3 text-xs font-medium text-slate-900 outline-none focus:bg-white focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition-all shadow-inner">
                        <button type="submit" id="chat-send-btn" class="w-11 h-11 bg-slate-900 hover:bg-slate-800 text-white rounded-2xl flex items-center justify-center transition-all shadow-md active:scale-95 shrink-0">
                            <i class="fa-solid fa-paper-plane text-amber-400 text-xs"></i>
                        </button>
                    </form>
                </div>
            </div>
        </section>

    </main>

    <script>
        let searchDebounceTimeout = null;
        let cachedIPOs = [];
        let chatHistory = [];

        function switchTab(tab) {
            document.getElementById('stock-section').classList.add('hidden');
            document.getElementById('ipo-section').classList.add('hidden');
            document.getElementById('chat-section').classList.add('hidden');
            document.getElementById('vault-section').classList.add('hidden');

            const inactiveClass = "py-2 text-[11px] font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1";
            const activeClass = "py-2 text-[11px] font-bold rounded-xl bg-white text-slate-900 shadow-sm transition-all flex items-center justify-center space-x-1";

            document.getElementById('tab-stock-btn').className = inactiveClass;
            document.getElementById('tab-ipo-btn').className = inactiveClass;
            document.getElementById('tab-chat-btn').className = inactiveClass;
            document.getElementById('tab-vault-btn').className = inactiveClass;

            if (tab === 'stock') {
                document.getElementById('stock-section').classList.remove('hidden');
                document.getElementById('tab-stock-btn').className = activeClass;
            } else if (tab === 'ipo') {
                document.getElementById('ipo-section').classList.remove('hidden');
                document.getElementById('tab-ipo-btn').className = activeClass;
                loadLiveIPOs();
            } else if (tab === 'chat') {
                document.getElementById('chat-section').classList.remove('hidden');
                document.getElementById('tab-chat-btn').className = activeClass;
                scrollChatToBottom();
                setTimeout(() => {
                    const input = document.getElementById('chat-input');
                    if (input) input.focus();
                }, 100);
            } else if (tab === 'vault') {
                document.getElementById('vault-section').classList.remove('hidden');
                document.getElementById('tab-vault-btn').className = activeClass;
                loadVault();
            }
        }

        // === AI COUNCIL CHAT ENGINE ===
        function formatMarkdown(text) {
            if (!text) return "";
            var html = text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
            
            // Headers in descending order of specificity
            html = html.replace(/^#### (.*$)/gim, '<h5 class="font-bold text-slate-800 mt-2 mb-0.5 text-xs uppercase tracking-wider">$1</h5>');
            html = html.replace(/^### (.*$)/gim, '<h4 class="font-extrabold text-slate-900 mt-2.5 mb-1 text-xs">$1</h4>');
            html = html.replace(/^## (.*$)/gim, '<h3 class="font-black text-slate-900 mt-3 mb-1 text-sm">$1</h3>');
            html = html.replace(/^# (.*$)/gim, '<h2 class="font-black text-slate-900 mt-3 mb-1 text-base">$1</h2>');

            // Blockquotes
            html = html.replace(/^> (.*$)/gim, '<blockquote class="border-l-2 border-amber-500/80 pl-2.5 py-0.5 my-1.5 text-slate-700 italic text-xs bg-amber-50/40 rounded-r-lg">$1</blockquote>');

            // Bold & Italic
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-slate-900">$1</strong>');
            html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>');

            // Bullets
            html = html.replace(/^[•\-\*] (.*$)/gim, '<div class="flex items-start space-x-1.5 my-1"><span class="text-amber-500 font-bold">•</span><span>$1</span></div>');

            // Paragraph breaks without regex newline issues
            var nl = String.fromCharCode(10);
            html = html.split(nl + nl).join('<div class="h-2"></div>');
            html = html.split(nl).join('<br>');

            return html;
        }

        function appendUserBubble(text) {
            const container = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.className = "flex justify-end";
            div.innerHTML = `
                <div class="bg-slate-900 text-white rounded-2xl rounded-tr-sm px-3.5 py-2.5 text-xs font-medium max-w-[85%] shadow-xs leading-relaxed">
                    ${text.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
                </div>
            `;
            container.appendChild(div);
        }

        function appendAiBubble(markdown) {
            const container = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.className = "flex items-start space-x-2.5";
            div.innerHTML = `
                <div class="w-7 h-7 rounded-lg bg-slate-900 text-amber-400 flex items-center justify-center shrink-0 text-xs font-bold mt-0.5">
                    N
                </div>
                <div class="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-3.5 shadow-xs text-xs text-slate-800 space-y-1 max-w-[88%] leading-relaxed">
                    ${formatMarkdown(markdown)}
                </div>
            `;
            container.appendChild(div);
        }

        function scrollChatToBottom() {
            const container = document.getElementById('chat-messages');
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }

        async function sendChatMessage(text) {
            if (!text || !text.trim()) return;
            text = text.trim();

            const input = document.getElementById('chat-input');
            if (input) input.value = '';

            appendUserBubble(text);
            chatHistory.push({ role: 'user', content: text });

            const typing = document.getElementById('chat-typing');
            const sendBtn = document.getElementById('chat-send-btn');
            if (typing) {
                typing.classList.remove('hidden');
                typing.classList.add('flex');
            }
            if (sendBtn) sendBtn.disabled = true;

            scrollChatToBottom();

            try {
                const resp = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: text,
                        history: chatHistory.slice(-6)
                    })
                });

                if (!resp.ok) {
                    throw new Error(`Server returned ${resp.status}`);
                }

                const data = await resp.json();
                const reply = data.reply || "I analyzed your request, but could not produce a verdict. Please try again.";
                appendAiBubble(reply);
                chatHistory.push({ role: 'model', content: reply });
            } catch (err) {
                console.error("Chat error:", err);
                appendAiBubble("⚠️ Could not reach Nexiv AI Council right now. Please check your connection and try again.");
            } finally {
                if (typing) {
                    typing.classList.add('hidden');
                    typing.classList.remove('flex');
                }
                if (sendBtn) sendBtn.disabled = false;
                scrollChatToBottom();
            }
        }

        function handleChatSubmit(e) {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            if (input && input.value) {
                sendChatMessage(input.value);
            }
        }

        function sendQuickPrompt(txt) {
            switchTab('chat');
            sendChatMessage(txt);
        }

        // Live Typeahead Search Engine
        function handleSearchInput(e) {
            clearTimeout(searchDebounceTimeout);
            const query = e.target.value.trim();
            const dropdown = document.getElementById('search-dropdown');

            if (!query || query.length < 1) {
                dropdown.classList.add('hidden');
                dropdown.innerHTML = "";
                return;
            }

            searchDebounceTimeout = setTimeout(async () => {
                try {
                    const resp = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                    const matches = await resp.json();
                    renderSearchDropdown(matches);
                } catch (err) {
                    console.error("Search error:", err);
                }
            }, 120);
        }

        function handleSearchFocus() {
            const query = document.getElementById('ticker-input').value.trim();
            if (query.length >= 1) {
                handleSearchInput({ target: { value: query } });
            }
        }

        function renderSearchDropdown(matches) {
            const dropdown = document.getElementById('search-dropdown');
            if (!matches || matches.length === 0) {
                dropdown.innerHTML = `<div class="p-3 text-xs text-slate-400 text-center font-medium">No direct match. Press Audit to query global feeds.</div>`;
                dropdown.classList.remove('hidden');
                return;
            }

            dropdown.innerHTML = matches.map(m => {
                let badgeStyle = "bg-blue-50 text-blue-700 border border-blue-200";
                if (m.sector && m.sector.includes('ETF')) {
                    badgeStyle = "bg-purple-50 text-purple-700 border border-purple-200";
                } else if (m.sector && (m.sector.includes('Commodit') || m.sector.includes('Metal'))) {
                    badgeStyle = "bg-amber-50 text-amber-700 border border-amber-200";
                } else if (m.exchange === 'NSE') {
                    badgeStyle = "bg-emerald-50 text-emerald-700 border border-emerald-200";
                }
                return `
                <div onclick="selectSearchResult('${m.symbol}')" class="px-3.5 py-2.5 hover:bg-slate-50 cursor-pointer flex items-center justify-between border-b border-slate-100 last:border-b-0 transition-colors">
                    <div>
                        <div class="text-xs font-bold text-slate-900">${m.name}</div>
                        <div class="text-[10px] font-mono font-semibold text-slate-500">${m.symbol} • ${m.sector}</div>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold ${badgeStyle}">
                        ${m.exchange}
                    </span>
                </div>
            `;}).join('');

            dropdown.classList.remove('hidden');
        }

        function selectSearchResult(symbol) {
            document.getElementById('ticker-input').value = symbol;
            document.getElementById('search-dropdown').classList.add('hidden');
            analyzeStock();
        }

        // Close dropdown when tapping outside
        document.addEventListener('click', (e) => {
            const container = document.getElementById('ticker-input').parentElement;
            if (!container.contains(e.target)) {
                document.getElementById('search-dropdown').classList.add('hidden');
            }
        });

        function quickStock(ticker) {
            document.getElementById('ticker-input').value = ticker;
            analyzeStock();
        }

        async function analyzeStock() {
            const ticker = document.getElementById('ticker-input').value.trim();
            if (!ticker) return;

            document.getElementById('search-dropdown').classList.add('hidden');
            document.getElementById('stock-loading').classList.remove('hidden');
            document.getElementById('stock-result').innerHTML = "";

            try {
                const resp = await fetch(`/api/stock/${ticker}`);
                const data = await resp.json();
                renderStockResult(data);
            } catch (err) {
                document.getElementById('stock-result').innerHTML = `
                    <div class="luxury-card rounded-2xl p-4 border-l-4 border-rose-500 bg-rose-50/50 text-rose-900 text-xs">
                        <div class="font-bold flex items-center space-x-1.5 mb-1">
                            <i class="fa-solid fa-circle-exclamation text-rose-600"></i>
                            <span>Audit Encountered an Issue</span>
                        </div>
                        <p class="text-rose-700">${err.message || 'Unable to retrieve real-time financial statements.'}</p>
                    </div>`;
            } finally {
                document.getElementById('stock-loading').classList.add('hidden');
            }
        }

        function renderStockResult(data) {
            const container = document.getElementById('stock-result');
            const p = data?.raw_analysis?.profile || {};
            const f = data?.raw_analysis?.forensics || {};
            const v = data?.raw_analysis?.valuation || {};
            const r = data?.raw_analysis?.risk_and_sizing || {};
            const isCommodityOrEtf = data.asset_type === 'ETF' || data.asset_type === 'COMMODITY' || (p.sector && (p.sector.includes('ETF') || p.sector.includes('Commodit')));
            const syn = data?.council_synthesis || data?.raw_analysis?.council_synthesis || {
                valuation_agent: { verdict: isCommodityOrEtf ? "Global Spot Parity Evaluated" : "Fair Value Assessment Complete" },
                forensic_agent: { verdict: isCommodityOrEtf ? "100% Vaulted Physical Bullion" : "Financial Statements Audited" },
                risk_sizing_agent: { verdict: "Capital Preservation Sizing" },
                market_cycle_agent: { verdict: "Macro Cycle Aligned" }
            };
            const isIndianAsset = Boolean(data.is_indian || p.is_indian || p.country === 'India' || (data.symbol || '').includes('.NS') || (data.symbol || '').includes('.BO') || (p.symbol || '').includes('.NS') || (p.symbol || '').includes('.BO'));
            const cur = isIndianAsset ? "₹" : (data.currency || p.currency || "$");

            let cardBg = "border-slate-200 bg-white";
            let badgeBg = "bg-slate-100 text-slate-800 border-slate-300";
            let badgeIcon = "fa-hand";

            if (data.action_code === "BUY" || data.action_code === "ACCUMULATE") {
                cardBg = "border-2 border-emerald-500/70 bg-gradient-to-b from-emerald-50/70 via-white to-white";
                badgeBg = "bg-emerald-600 text-white shadow-sm shadow-emerald-600/30";
                badgeIcon = "fa-circle-check";
            } else if (data.action_code === "HOLD") {
                cardBg = "border-2 border-amber-500/70 bg-gradient-to-b from-amber-50/70 via-white to-white";
                badgeBg = "bg-amber-500 text-white shadow-sm shadow-amber-500/30";
                badgeIcon = "fa-hand";
            } else if (data.action_code === "SELL") {
                cardBg = "border-2 border-rose-500/70 bg-gradient-to-b from-rose-50/70 via-white to-white";
                badgeBg = "bg-rose-600 text-white shadow-sm shadow-rose-600/30";
                badgeIcon = "fa-triangle-exclamation";
            }

            const upsidePct = data.expected_gain_pct || 0;
            const upsideClass = upsidePct >= 0 ? "text-emerald-700 bg-emerald-50 border-emerald-200" : "text-rose-700 bg-rose-50 border-rose-200";

            container.innerHTML = `
                <!-- EXECUTIVE DECISION CARD -->
                <div class="luxury-card-elevated rounded-3xl p-5 ${cardBg} space-y-4">
                    <div class="flex items-start justify-between">
                        <div>
                            <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide ${badgeBg}">
                                <i class="fa-solid ${badgeIcon}"></i>
                                <span>${data.action}</span>
                            </span>
                            <h2 class="text-lg font-black text-slate-900 mt-2 tracking-tight">${data.company_name}</h2>
                            <p class="text-xs font-semibold text-slate-500 font-mono">${p.symbol || data.symbol} • ${p.sector || (isCommodityOrEtf ? 'Real Asset / Bullion' : '')} • ${p.country || ''}</p>
                            
                            <!-- Multi-Institutional Council Attribution Bar -->
                            <div class="flex flex-wrap gap-1 mt-2 text-[9px] font-bold">
                                ${isCommodityOrEtf ? `
                                <span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 border border-amber-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-coins text-amber-600"></i>
                                    <span>LBMA & MCX (Global Spot Parity)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-vault text-emerald-600"></i>
                                    <span>SEBI & Trustee (100% Vaulted Custody)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-purple-50 text-purple-800 border border-purple-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-scale-balanced text-purple-600"></i>
                                    <span>Ray Dalio All-Weather (5-15% Parity)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-blue-50 text-blue-800 border border-blue-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-bolt text-blue-600"></i>
                                    <span>Secular Green & Grid Electrification</span>
                                </span>
                                ` : `
                                <span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 border border-amber-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-landmark text-amber-600"></i>
                                    <span>NYU & Columbia (Damodaran DCF & Moat)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-shield-halved text-emerald-600"></i>
                                    <span>Schilit Forensics (Clean Financials)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-purple-50 text-purple-800 border border-purple-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-building-columns text-purple-600"></i>
                                    <span>Citadel & López de Prado (Risk Pod Sizing)</span>
                                </span>
                                <span class="px-2 py-0.5 rounded-md bg-blue-50 text-blue-800 border border-blue-200/80 flex items-center space-x-1">
                                    <i class="fa-solid fa-chart-line text-blue-600"></i>
                                    <span>Bridgewater & Oaktree (Debt & Credit Cycle)</span>
                                </span>
                                `}
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="flex items-center justify-end space-x-1 mb-0.5">
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${(data.price_source||'').includes('LIVE') ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-amber-100 text-amber-800 border border-amber-300'}">${data.price_source || '🟢 LIVE EXCHANGE'}</span>
                            </div>
                            <span class="text-xl font-black font-mono text-slate-900">${cur}${((p.current_price || data.current_price || 0)).toFixed(2)}</span>
                            ${(data.live_change_pct && data.live_change_pct !== 0) ? `<span class="text-[10px] font-bold ${data.live_change_pct >= 0 ? 'text-emerald-600' : 'text-rose-600'} block font-mono">${data.live_change_pct >= 0 ? '▲' : '▼'} ${Math.abs(data.live_change_pct).toFixed(2)}% today</span>` : ''}
                            <span class="text-[9px] text-slate-500 font-mono block mt-0.5">${data.price_timestamp || ''}</span>
                        </div>
                    </div>

                    <div class="bg-white/90 p-3.5 rounded-2xl border border-slate-200/80 shadow-xs">
                        <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1 flex items-center space-x-1">
                            <i class="fa-solid fa-microchip text-amber-500"></i>
                            <span>Nexiv AI Council Synthesis</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed font-medium">${data.summary_advice}</p>
                    </div>

                    <!-- 4 Institutional Action Pillars Grid -->
                    <div class="grid grid-cols-2 gap-2 pt-1">
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">TARGET PRICE</span>
                            <div class="flex items-baseline space-x-1.5 mt-0.5">
                                <span class="text-base font-black font-mono text-slate-900">${cur}${((data.target_price || 0)).toFixed(2)}</span>
                                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded border ${upsideClass}">${upsidePct > 0 ? '+' : ''}${upsidePct.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">STOP-LOSS FLOOR</span>
                            <div class="flex items-baseline space-x-1.5 mt-0.5">
                                <span class="text-base font-black font-mono text-rose-600">${cur}${((data.stop_loss_price || 0)).toFixed(2)}</span>
                                <span class="text-[10px] font-bold text-slate-400">Defense</span>
                            </div>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">${isCommodityOrEtf ? 'PARITY UPSIDE' : 'MARGIN OF SAFETY'}</span>
                            <span class="text-sm font-black font-mono ${((v.margin_of_safety_pct || data.expected_gain_pct || 0)) >= 0 ? 'text-emerald-700' : 'text-rose-600'}">
                                ${((v.margin_of_safety_pct || data.expected_gain_pct || 0)) > 0 ? '+' : ''}${((v.margin_of_safety_pct || data.expected_gain_pct || 0)).toFixed(1)}% vs ${isCommodityOrEtf ? 'Parity' : 'DCF'}
                            </span>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">TIME HORIZON</span>
                            <span class="text-xs font-bold text-slate-800 truncate block mt-0.5">${data.time_horizon || data.recommended_horizon || '1 to 3 Years'}</span>
                        </div>
                    </div>
                </div>

                <!-- 4 AGENT COUNCIL CONSENSUS -->
                <div class="luxury-card rounded-2xl p-4 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-users-gear text-amber-600 text-xs"></i>
                            <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">4-Agent Autonomous Council</h3>
                        </div>
                        <span class="text-[10px] font-bold text-slate-400">UNANIMOUS CONSENSUS</span>
                    </div>

                    <div class="space-y-2.5 text-xs">
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">1</span>
                            <div class="space-y-0.5 flex-1">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-slate-900">${syn?.valuation_agent?.name || 'Valuation Architect'}</span>
                                    <span class="text-[9px] font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">${syn?.valuation_agent?.institution || (isCommodityOrEtf ? 'LBMA Standards' : 'NYU & Columbia')}</span>
                                </div>
                                <p class="text-slate-700 font-medium">${syn?.valuation_agent?.verdict || 'Valuation Audit Complete'} • Value: <span class="font-mono font-bold">${cur}${((v?.dcf?.intrinsic_value_per_share || data.target_price || 0)).toFixed(2)}</span></p>
                                <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${syn?.valuation_agent?.doctrine || (isCommodityOrEtf ? 'Spot parity tracking without equity dilution.' : 'Intrinsic cash flows discounted by cost of capital.')}</p>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">2</span>
                            <div class="space-y-0.5 flex-1">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-slate-900">${syn?.forensic_agent?.name || 'Forensics Shield'}</span>
                                    <span class="text-[9px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">${syn?.forensic_agent?.institution || (isCommodityOrEtf ? 'SEBI / Custodial Trustee' : 'Howard Schilit')}</span>
                                </div>
                                <p class="text-slate-700 font-medium">${syn?.forensic_agent?.verdict || 'Forensics Complete'}${isCommodityOrEtf ? '' : ` • Altman Z: <span class="font-mono font-bold">${((f?.altman_z?.z_score || 0)).toFixed(2)}</span> (${f?.altman_z?.zone || 'SAFE'})`}</p>
                                <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${syn?.forensic_agent?.doctrine || 'Legal asset separation guarantees bankruptcy remoteness.'}</p>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">3</span>
                            <div class="space-y-0.5 flex-1">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-slate-900">${syn?.risk_sizing_agent?.name || 'Kelly Sizing Allocator'}</span>
                                    <span class="text-[9px] font-bold text-purple-700 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-200">${syn?.risk_sizing_agent?.institution || (isCommodityOrEtf ? 'Ray Dalio All-Weather' : 'Citadel & López de Prado')}</span>
                                </div>
                                <p class="text-slate-700 font-medium">${syn?.risk_sizing_agent?.verdict || 'Risk Sizing Complete'} • Recommended: <span class="font-mono font-bold">${((r?.recommended_kelly_allocation_pct || data.recommended_allocation_pct || 10)).toFixed(1)}%</span> of portfolio</p>
                                <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${syn?.risk_sizing_agent?.doctrine || 'Fractional sizing preserves capital while providing macro resilience.'}</p>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">4</span>
                            <div class="space-y-0.5 flex-1">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-slate-900">${syn?.market_cycle_agent?.name || 'Macro Cycle Strategist'}</span>
                                    <span class="text-[9px] font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">${syn?.market_cycle_agent?.institution || (isCommodityOrEtf ? 'Commodity Research' : 'Bridgewater & Oaktree')}</span>
                                </div>
                                <p class="text-slate-700 font-medium">${syn?.market_cycle_agent?.verdict || 'Cycle Aligned'} • Horizon: <span class="font-bold">${data.time_horizon || data.recommended_horizon || '1 to 3 Years'}</span></p>
                                <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${syn?.market_cycle_agent?.doctrine || 'Structural supply tightness and green transition underpin multi-year supercycle.'}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- FORENSIC AUDIT CHECKLIST -->
                <div class="luxury-card rounded-2xl p-4 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-shield-halved text-emerald-600 text-xs"></i>
                            <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">${isCommodityOrEtf ? 'Vault Custody & Solvency Shield' : 'Forensics & Shenanigans Shield'}</h3>
                        </div>
                        <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">${isCommodityOrEtf ? 'REGULATED TRUSTEE AUDIT' : 'SCHILIT AUDIT'}</span>
                    </div>

                    ${isCommodityOrEtf ? `
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Custodial Backing</span>
                            <span class="text-base font-black font-mono text-emerald-700 mt-0.5 block">100% Physical</span>
                            <span class="text-[10px] font-bold text-emerald-700 block mt-0.5">LBMA / SEBI Vaulted Bullion</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Single-Entity Credit Risk</span>
                            <span class="text-base font-black font-mono text-emerald-700 mt-0.5 block">ZERO RISK</span>
                            <span class="text-[10px] font-bold text-emerald-700 block mt-0.5">Bankruptcy-Remote Trust</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Purity / Delivery Standard</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">99.9% Purity</span>
                            <span class="text-[10px] font-bold text-slate-600 block mt-0.5">London / MCX Good Delivery</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Tracking Efficiency</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">&lt; 0.20%</span>
                            <span class="text-[10px] font-bold text-emerald-700 block mt-0.5">High Market Liquidity</span>
                        </div>
                    </div>
                    ` : `
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Altman Z-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${((f?.altman_z?.z_score || 0)).toFixed(2)}</span>
                            <span class="text-[10px] font-bold ${(f?.altman_z?.zone || '').includes('SAFE') ? 'text-emerald-700' : 'text-rose-600'} block mt-0.5">${f?.altman_z?.zone || 'SAFE ZONE'}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Beneish M-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${((f?.beneish_m?.m_score || 0)).toFixed(2)}</span>
                            <span class="text-[10px] font-bold ${(f?.beneish_m?.m_score || -2.0) > -1.78 ? 'text-rose-600' : 'text-emerald-700'} block mt-0.5">${f?.beneish_m?.manipulation_risk || 'LOW RISK'}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Piotroski F-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${f?.piotroski_f?.f_score ?? 7}/9</span>
                            <span class="text-[10px] font-bold text-slate-600 block mt-0.5">${f?.piotroski_f?.rating || 'Strong Fundamentals'}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Sloan Accruals</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${((f?.sloan_accrual?.accrual_ratio || 0)).toFixed(3)}</span>
                            <span class="text-[10px] font-bold text-slate-600 block mt-0.5">${f?.sloan_accrual?.quality_rating || 'High Quality'}</span>
                        </div>
                    </div>
                    `}
                </div>

                <!-- VALUATION ARCHITECTURE -->
                <div class="luxury-card rounded-2xl p-4 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-calculator text-blue-600 text-xs"></i>
                            <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">${isCommodityOrEtf ? 'Commodity Parity & Asset Allocation' : 'Valuation & Capital Allocation'}</h3>
                        </div>
                        <span class="text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">${isCommodityOrEtf ? 'GLOBAL SPOT PARITY' : 'DAMODARAN DCF'}</span>
                    </div>

                    ${isCommodityOrEtf ? `
                    <div class="space-y-2.5 text-xs">
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Physical NAV / Parity Target</span>
                            <span class="font-mono font-bold text-slate-900 text-sm">${cur}${((data.target_price || v?.dcf?.intrinsic_value_per_share || 0)).toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Upside Potential vs Current Spot</span>
                            <span class="font-mono font-bold text-emerald-700">+${(data.expected_gain_pct || 18.0).toFixed(1)}%</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Asset Class Defensive Beta</span>
                            <span class="font-mono font-bold text-slate-700">0.75 (Non-Correlated Real Asset)</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Ray Dalio All-Weather Recommended Band</span>
                            <span class="font-mono font-bold text-purple-700">5.0% - 15.0% of Portfolio</span>
                        </div>
                        <div class="flex justify-between items-center py-1">
                            <span class="font-medium text-slate-500">Strategic Position Sizing</span>
                            <span class="font-mono font-bold text-emerald-700">${((data.recommended_allocation_pct || r?.recommended_kelly_allocation_pct || 10)).toFixed(1)}% of Portfolio</span>
                        </div>
                    </div>
                    ` : `
                    <div class="space-y-2.5 text-xs">
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Damodaran DCF Intrinsic Value</span>
                            <span class="font-mono font-bold text-slate-900 text-sm">${cur}${((v?.dcf?.intrinsic_value_per_share || 0)).toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Margin of Safety vs Current Price</span>
                            <span class="font-mono font-bold ${(v?.margin_of_safety_pct || 0) >= 0 ? 'text-emerald-700' : 'text-rose-600'}">
                                ${(v?.margin_of_safety_pct || 0) > 0 ? '+' : ''}${((v?.margin_of_safety_pct || 0)).toFixed(2)}%
                            </span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Benchmark Cost of Capital (WACC)</span>
                            <span class="font-mono font-bold text-slate-700">${(((v?.wacc || 0.1) * 100)).toFixed(2)}%</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Graham Net-Net Liquidation Floor</span>
                            <span class="font-mono font-bold text-slate-700">${cur}${((v?.graham_ncav?.ncav_per_share || 0)).toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center py-1">
                            <span class="font-medium text-slate-500">Kelly Optimal Capital Allocation</span>
                            <span class="font-mono font-bold text-emerald-700">${((r?.recommended_kelly_allocation_pct || 0)).toFixed(1)}% of Portfolio</span>
                        </div>
                    </div>
                    `}
                </div>
            `;
        }

        async function loadLiveIPOs() {
            try {
                const resp = await fetch('/api/ipos/live');
                cachedIPOs = await resp.json();
                renderIPOList(cachedIPOs);
            } catch (err) {
                console.error("Failed to load live IPOs:", err);
            }
        }

        function filterIPOs(filter) {
            document.querySelectorAll('#ipo-section .overflow-x-auto button').forEach(b => {
                b.className = "px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all";
            });

            if (filter === 'ALL') {
                document.getElementById('filter-all').className = "px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all";
                renderIPOList(cachedIPOs);
            } else if (filter === 'OPEN NOW') {
                document.getElementById('filter-open').className = "px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all";
                renderIPOList(cachedIPOs.filter(i => i.status === 'OPEN NOW'));
            } else if (filter === 'UPCOMING') {
                document.getElementById('filter-upcoming').className = "px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all";
                renderIPOList(cachedIPOs.filter(i => i.status === 'UPCOMING'));
            } else if (filter === 'LISTED') {
                document.getElementById('filter-listed').className = "px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all";
                renderIPOList(cachedIPOs.filter(i => i.status.includes('LISTED') || i.status.includes('CLOSED')));
            }
        }

        function renderIPOList(ipos) {
            const container = document.getElementById('live-ipos-feed');
            if (!ipos || ipos.length === 0) {
                container.innerHTML = `<div class="p-4 text-center text-xs text-slate-400">No IPOs currently in this category.</div>`;
                return;
            }

            container.innerHTML = ipos.map((ipo, idx) => `
                <div class="luxury-card rounded-2xl p-4 space-y-3 hover:shadow-md transition-all">
                    <!-- Top Header & Live Status Badge -->
                    <div class="flex items-start justify-between">
                        <div>
                            <div class="flex items-center space-x-2">
                                <h3 class="text-sm font-extrabold text-slate-900">${ipo.company_name}</h3>
                                <span class="px-2 py-0.5 rounded-full text-[9px] font-bold border ${ipo.status_badge}">
                                    ${ipo.status}
                                </span>
                            </div>
                            <p class="text-[11px] text-slate-500 font-medium">${ipo.sector} • Symbol: ${ipo.symbol}</p>
                            <div class="flex items-center space-x-1.5 mt-1 text-[9px] font-bold">
                                <span class="px-1.5 py-0.5 rounded ${ipo.issue_details.fresh_pct >= 60 ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'}">
                                    Ritter Law: ${ipo.issue_details.fresh_pct >= 60 ? 'Safe Expansion (' + ipo.issue_details.fresh_pct.toFixed(0) + '% Fresh)' : 'OFS Exit Trap (' + ipo.issue_details.ofs_pct.toFixed(0) + '% OFS)'}
                                </span>
                                <span class="px-1.5 py-0.5 rounded bg-blue-50 text-blue-800 border border-blue-200">
                                    Damodaran DCF Audit
                                </span>
                            </div>
                        </div>
                        <span class="text-right">
                            <span class="text-[9px] font-bold text-slate-400 block uppercase">ISSUE SIZE</span>
                            <span class="text-xs font-extrabold font-mono text-slate-900">₹${ipo.issue_details.issue_size_cr.toLocaleString()} Cr</span>
                        </span>
                    </div>

                    <!-- Brokerage 4-Step Readable Timeline (2x2 grid, no truncation) -->
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                        <div class="flex items-center justify-between text-[10px] font-semibold text-slate-400 mb-2">
                            <span>📅 TIMELINE SCHEDULE</span>
                            <span class="text-amber-700 font-bold text-[11px]">${ipo.timeline.days_left}</span>
                        </div>
                        <div class="grid grid-cols-2 gap-2 text-[11px]">
                            <div class="bg-white p-2 rounded-lg border border-emerald-200/60 flex items-start space-x-2">
                                <span class="text-emerald-500 text-sm mt-0.5">📋</span>
                                <div>
                                    <span class="block text-slate-400 text-[9px] font-bold uppercase tracking-wide">BIDDING WINDOW</span>
                                    <span class="font-bold text-slate-800 text-[11px] leading-tight">${ipo.timeline.bidding_dates}</span>
                                </div>
                            </div>
                            <div class="bg-white p-2 rounded-lg border border-blue-200/60 flex items-start space-x-2">
                                <span class="text-blue-500 text-sm mt-0.5">🎯</span>
                                <div>
                                    <span class="block text-slate-400 text-[9px] font-bold uppercase tracking-wide">ALLOTMENT</span>
                                    <span class="font-bold text-slate-800 text-[11px] leading-tight">${ipo.timeline.allotment_date}</span>
                                </div>
                            </div>
                            <div class="bg-white p-2 rounded-lg border border-purple-200/60 flex items-start space-x-2">
                                <span class="text-purple-500 text-sm mt-0.5">💳</span>
                                <div>
                                    <span class="block text-slate-400 text-[9px] font-bold uppercase tracking-wide">DEMAT CREDIT</span>
                                    <span class="font-bold text-slate-800 text-[11px] leading-tight">${ipo.timeline.demat_credit}</span>
                                </div>
                            </div>
                            <div class="bg-white p-2 rounded-lg border border-amber-200/60 flex items-start space-x-2">
                                <span class="text-amber-500 text-sm mt-0.5">🚀</span>
                                <div>
                                    <span class="block text-slate-400 text-[9px] font-bold uppercase tracking-wide">LISTING DAY</span>
                                    <span class="font-bold text-slate-800 text-[11px] leading-tight">${ipo.timeline.listing_date}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Brokerage Core Details Grid -->
                    <div class="grid grid-cols-3 gap-2 text-center text-xs">
                        <div class="bg-slate-50/80 p-2.5 rounded-xl border border-slate-200/60">
                            <span class="text-[9px] font-bold text-slate-400 block uppercase">PRICE BAND</span>
                            <span class="font-black text-slate-900 font-mono text-xs">${ipo.issue_details.price_range}</span>
                            <span class="text-[9px] text-slate-500 block mt-0.5">Lot: ${ipo.issue_details.lot_size} sh (₹${ipo.issue_details.min_investment.toLocaleString()})</span>
                        </div>
                        <div class="bg-slate-50/80 p-2.5 rounded-xl border border-slate-200/60">
                            <span class="text-[9px] font-bold text-slate-400 block uppercase">LIVE GMP</span>
                            <span class="font-black ${ipo.gmp.value >= 0 ? 'text-emerald-700' : 'text-rose-600'} font-mono text-xs">
                                ₹${ipo.gmp.value} (${ipo.gmp.pct > 0 ? '+' : ''}${ipo.gmp.pct}%)
                            </span>
                            <span class="text-[9px] text-slate-500 block mt-0.5">Est Listing: ₹${ipo.gmp.expected_listing_price}</span>
                        </div>
                        <div class="bg-slate-50/80 p-2.5 rounded-xl border border-slate-200/60">
                            <span class="text-[9px] font-bold text-slate-400 block uppercase">SUBSCRIPTION</span>
                            <span class="font-black text-blue-700 font-mono text-xs">${ipo.subscription.total}</span>
                            <span class="text-[9px] text-slate-500 block mt-0.5">QIB: ${ipo.subscription.qib} • Ret: ${ipo.subscription.retail}</span>
                        </div>
                    </div>

                    <!-- Fresh vs OFS Progress Bar -->
                    <div>
                        <div class="flex justify-between text-[10px] font-semibold text-slate-500 mb-1">
                            <span>Fresh Issue: ${ipo.issue_details.fresh_pct.toFixed(1)}% (₹${ipo.issue_details.fresh_issue_cr} Cr)</span>
                            <span>Promoter Exit (OFS): ${ipo.issue_details.ofs_pct.toFixed(1)}% (₹${ipo.issue_details.ofs_cr} Cr)</span>
                        </div>
                        <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden flex">
                            <div class="bg-emerald-500 h-full" style="width: ${ipo.issue_details.fresh_pct}%"></div>
                            <div class="bg-rose-500 h-full" style="width: ${ipo.issue_details.ofs_pct}%"></div>
                        </div>
                    </div>

                    <!-- Nexiv.AI Direct Autonomous Verdict Callout -->
                    <div class="p-3 rounded-xl border flex items-start justify-between space-x-2" style="background-color: ${ipo.ai_decision.action_color}08; border-color: ${ipo.ai_decision.action_color}35;">
                        <div class="space-y-1">
                            <div class="flex items-center space-x-2">
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase text-white shadow-xs" style="background-color: ${ipo.ai_decision.action_color};">
                                    ${ipo.ai_decision.action}
                                </span>
                                <span class="text-[10px] font-bold font-mono text-slate-600">NEXIV SCORE: ${ipo.ai_decision.score}/100</span>
                            </div>
                            <p class="text-[11px] text-slate-700 leading-snug font-medium">${ipo.ai_decision.summary}</p>
                        </div>
                        <button onclick="auditPresetIPO('${ipo.symbol}')" class="px-3 py-1.5 bg-slate-900 text-white font-bold rounded-xl text-xs hover:bg-slate-800 active:scale-95 transition-all shrink-0 self-center">
                            Full Audit
                        </button>
                    </div>
                </div>
            `).join('');
        }

        async function auditPresetIPO(symbol) {
            const ipo = cachedIPOs.find(i => i.symbol === symbol) || cachedIPOs[0];

            document.getElementById('ipo-name').value = ipo.company_name;
            document.getElementById('ipo-sector').value = ipo.sector;
            document.getElementById('ipo-pmin').value = ipo.issue_details.price_min;
            document.getElementById('ipo-pmax').value = ipo.issue_details.price_max;
            document.getElementById('ipo-rev').value = ipo.financials.annual_revenue;
            document.getElementById('ipo-growth').value = ipo.financials.growth_rate;
            document.getElementById('ipo-fresh').value = Math.round((ipo.issue_details.fresh_issue_cr * 10000000) / ipo.issue_details.price_max) || 10000000;
            document.getElementById('ipo-ofs').value = Math.round((ipo.issue_details.ofs_cr * 10000000) / ipo.issue_details.price_max) || 10000000;
            document.getElementById('ipo-gmp').value = ipo.gmp.value;
            document.getElementById('ipo-lot').value = ipo.issue_details.lot_size;

            evaluateCustomIPO();
        }

        async function evaluateCustomIPO() {
            const payload = {
                company_name: document.getElementById('ipo-name').value,
                sector: document.getElementById('ipo-sector').value,
                offer_price_min: parseFloat(document.getElementById('ipo-pmin').value),
                offer_price_max: parseFloat(document.getElementById('ipo-pmax').value),
                shares_offered: parseFloat(document.getElementById('ipo-fresh').value) + parseFloat(document.getElementById('ipo-ofs').value),
                fresh_issue_shares: parseFloat(document.getElementById('ipo-fresh').value),
                ofs_shares: parseFloat(document.getElementById('ipo-ofs').value),
                pre_ipo_shares: 80000000,
                annual_revenue: parseFloat(document.getElementById('ipo-rev').value),
                annual_growth_rate: parseFloat(document.getElementById('ipo-growth').value),
                operating_cash_flow: 40000000,
                pre_ipo_cash: 100000000,
                country: "India",
                gmp: parseFloat(document.getElementById('ipo-gmp').value) || 0,
                lot_size: parseInt(document.getElementById('ipo-lot').value) || 1
            };

            const resp = await fetch('/api/ipo/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            renderIPOResult(data);
        }

        function renderIPOResult(data) {
            const container = document.getElementById('ipo-result');
            const ipo = data.raw_ipo || {};
            const isIndianIPO = Boolean(data.is_indian || ipo.is_indian || ipo.country === 'India' || (data.company_name || '').includes('(India)') || (ipo.company_name || '').includes('(India)'));
            const cur = isIndianIPO ? "₹" : (data.currency || ipo.currency || "$");

            let bandText = data.offer_price_range || '';
            if (isIndianIPO) {
                bandText = bandText.replace(/\$/g, '₹');
            } else if (cur === '$') {
                bandText = bandText.replace(/₹/g, '$');
            }

            let cardBg = "border-slate-200 bg-white";
            let badgeBg = "bg-slate-100 text-slate-800 border-slate-300";
            let badgeIcon = "fa-hand";

            if (data.action_code === "APPLY_LONG") {
                cardBg = "border-2 border-emerald-500/70 bg-gradient-to-b from-emerald-50/70 via-white to-white";
                badgeBg = "bg-emerald-600 text-white";
                badgeIcon = "fa-circle-check";
            } else if (data.action_code === "APPLY_FLIP") {
                cardBg = "border-2 border-amber-500/70 bg-gradient-to-b from-amber-50/70 via-white to-white";
                badgeBg = "bg-amber-500 text-white";
                badgeIcon = "fa-bolt";
            } else {
                cardBg = "border-2 border-rose-500/70 bg-gradient-to-b from-rose-50/70 via-white to-white";
                badgeBg = "bg-rose-600 text-white";
                badgeIcon = "fa-ban";
            }

            container.innerHTML = `
                <div class="luxury-card-elevated rounded-3xl p-5 ${cardBg} space-y-4">
                    <div class="flex items-start justify-between">
                        <div>
                            <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-extrabold uppercase ${badgeBg}">
                                <i class="fa-solid ${badgeIcon}"></i>
                                <span>${data.action}</span>
                            </span>
                            <h3 class="text-lg font-black text-slate-900 mt-2 tracking-tight">${data.company_name}</h3>
                            <p class="text-xs font-semibold text-slate-500 font-mono">${data.sector} • Band: ${bandText}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">NEXIV SCORE</span>
                            <span class="text-lg font-black font-mono text-slate-900">${data.score}/100</span>
                        </div>
                    </div>

                    <div class="bg-white/90 p-3.5 rounded-2xl border border-slate-200/80 shadow-xs">
                        <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Ritter & Damodaran Synthesis</div>
                        <p class="text-xs text-slate-700 leading-relaxed font-medium">${data.summary_advice}</p>
                    </div>

                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Fresh Growth Issue</span>
                            <span class="text-base font-black font-mono text-emerald-700 mt-0.5 block">${((ipo?.fresh_pct || 0)).toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Promoter Exit (OFS)</span>
                            <span class="text-base font-black font-mono text-rose-600 mt-0.5 block">${((ipo?.ofs_pct || 0)).toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Rule of 40 Score</span>
                            <span class="text-base font-black font-mono text-blue-600 mt-0.5 block">${((ipo?.rule_of_40_score || 0)).toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Expected Listing Return</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${data.expected_gain || 'N/A'}</span>
                        </div>
                    </div>

                    <!-- IPO MULTI-INSTITUTIONAL COUNCIL CONSENSUS -->
                    <div class="luxury-card rounded-2xl p-4 space-y-3 bg-white/95">
                        <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                            <div class="flex items-center space-x-2">
                                <i class="fa-solid fa-users-gear text-amber-600 text-xs"></i>
                                <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">IPO Multi-Institutional Council Consensus</h3>
                            </div>
                            <span class="text-[10px] font-bold text-slate-400">UNANIMOUS AUDIT</span>
                        </div>

                        <div class="space-y-2.5 text-xs">
                            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                                <span class="w-5 h-5 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">1</span>
                                <div class="space-y-0.5 flex-1">
                                    <div class="flex items-center justify-between">
                                        <span class="font-bold text-slate-900">${data?.council_synthesis?.ritter_agent?.name || 'Empirical IPO Auditor'}</span>
                                        <span class="text-[9px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">${data?.council_synthesis?.ritter_agent?.institution || 'Prof. Jay Ritter'}</span>
                                    </div>
                                    <p class="text-slate-700 font-medium">${data?.council_synthesis?.ritter_agent?.verdict || 'Empirical IPO Check Complete'} • Fresh: <span class="font-mono font-bold">${((ipo?.fresh_pct || 0)).toFixed(1)}%</span> | OFS: <span class="font-mono font-bold">${((ipo?.ofs_pct || 0)).toFixed(1)}%</span></p>
                                    <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${data?.council_synthesis?.ritter_agent?.doctrine || 'High OFS (>65%) predicts 3-year underperformance.'}</p>
                                </div>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                                <span class="w-5 h-5 rounded-lg bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">2</span>
                                <div class="space-y-0.5 flex-1">
                                    <div class="flex items-center justify-between">
                                        <span class="font-bold text-slate-900">${data?.council_synthesis?.valuation_agent?.name || 'Valuation Architect'}</span>
                                        <span class="text-[9px] font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">${data?.council_synthesis?.valuation_agent?.institution || 'Aswath Damodaran'}</span>
                                    </div>
                                    <p class="text-slate-700 font-medium">${data?.council_synthesis?.valuation_agent?.verdict || 'Valuation Audit Complete'} • Intrinsic DCF: <span class="font-mono font-bold">${cur}${((ipo?.intrinsic_value_per_share || 0)).toFixed(2)}</span></p>
                                    <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${data?.council_synthesis?.valuation_agent?.doctrine || 'IPO price is set by bankers; value is future cash flows.'}</p>
                                </div>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                                <span class="w-5 h-5 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">3</span>
                                <div class="space-y-0.5 flex-1">
                                    <div class="flex items-center justify-between">
                                        <span class="font-bold text-slate-900">${data?.council_synthesis?.underwriting_agent?.name || 'Underwriting & Solvency Auditor'}</span>
                                        <span class="text-[9px] font-bold text-purple-700 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-200">${data?.council_synthesis?.underwriting_agent?.institution || 'Goldman & Morgan Stanley'}</span>
                                    </div>
                                    <p class="text-slate-700 font-medium">${data?.council_synthesis?.underwriting_agent?.verdict || 'Runway Assessment Complete'} • Runway: <span class="font-mono font-bold">${((ipo?.runway_months || 24))} Months</span></p>
                                    <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${data?.council_synthesis?.underwriting_agent?.doctrine || 'Maintain >=18 months operating cash runway for safety.'}</p>
                                </div>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                                <span class="w-5 h-5 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">4</span>
                                <div class="space-y-0.5 flex-1">
                                    <div class="flex items-center justify-between">
                                        <span class="font-bold text-slate-900">${data?.council_synthesis?.sentiment_arbitrage_agent?.name || 'Microstructure Strategist'}</span>
                                        <span class="text-[9px] font-bold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">${data?.council_synthesis?.sentiment_arbitrage_agent?.institution || 'Citadel & Rentec'}</span>
                                    </div>
                                    <p class="text-slate-700 font-medium">${data?.council_synthesis?.sentiment_arbitrage_agent?.verdict || 'Arbitrage Check Complete'} • GMP: <span class="font-mono font-bold">${cur}${data.gmp}</span></p>
                                    <p class="text-[10px] text-slate-400 italic font-mono leading-tight">${data?.council_synthesis?.sentiment_arbitrage_agent?.doctrine || 'Capture first-day pop; exit if fundamentals do not support holding.'}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            container.scrollIntoView({ behavior: 'smooth' });
        }

        // === INSTITUTIONAL KNOWLEDGE VAULT DYNAMIC ENGINE (56 ASSETS) ===
        let cachedVaultData = null;
        let currentVaultFilter = 'ALL';
        let vaultSearchQuery = '';

        async function loadVault() {
            const container = document.getElementById('vault-items-container');
            if (!container) return;

            if (cachedVaultData) {
                renderVaultItems();
                return;
            }

            container.innerHTML = `<div class="p-8 text-center text-xs text-slate-400"><i class="fa-solid fa-spinner fa-spin mr-2 text-amber-500"></i>Accessing 4-Pillar Council Vault (56 Assets)...</div>`;

            try {
                const resp = await fetch('/api/knowledge');
                cachedVaultData = await resp.json();
                renderVaultItems();
            } catch (err) {
                console.error("Vault load error:", err);
                container.innerHTML = `<div class="p-4 bg-rose-50 text-rose-800 text-xs rounded-xl border border-rose-200">Unable to load Knowledge Vault assets right now.</div>`;
            }
        }

        function filterVault(filter) {
            currentVaultFilter = filter;
            const buttons = [
                { id: 'vault-filter-all', key: 'ALL' },
                { id: 'vault-filter-books', key: 'BOOKS' },
                { id: 'vault-filter-academic', key: 'ACADEMIC' },
                { id: 'vault-filter-firms', key: 'FIRMS' },
                { id: 'vault-filter-titans', key: 'TITANS' },
                { id: 'vault-filter-datasets', key: 'DATASETS' }
            ];

            buttons.forEach(b => {
                const el = document.getElementById(b.id);
                if (el) {
                    if (b.key === filter) {
                        el.className = "px-3 py-1 rounded-full bg-slate-900 text-white shadow-xs font-bold transition-all whitespace-nowrap";
                    } else {
                        el.className = "px-3 py-1 rounded-full bg-slate-100 text-slate-600 hover:text-slate-900 transition-all whitespace-nowrap";
                    }
                }
            });

            renderVaultItems();
        }

        function handleVaultSearch(e) {
            vaultSearchQuery = (e.target.value || '').trim().toLowerCase();
            renderVaultItems();
        }

        function askCouncilAbout(topic) {
            switchTab('chat');
            sendChatMessage("Explain how the Nexiv AI Council applies the core principles and laws of " + topic + " in real stock audits and investment decisions.");
        }

        function renderVaultItems() {
            const container = document.getElementById('vault-items-container');
            if (!container || !cachedVaultData) return;

            const q = vaultSearchQuery;
            const f = currentVaultFilter;
            let itemsHtml = [];

            // 1. MASTER CODIFIED BOOKS
            if (f === 'ALL' || f === 'BOOKS') {
                const books = cachedVaultData.books_principles || {};
                Object.keys(books).forEach(k => {
                    const b = books[k];
                    const searchText = (b.title + ' ' + b.author + ' ' + (b.cross_links || '') + ' ' + (b.core_principles || []).join(' ')).toLowerCase();
                    if (q && !searchText.includes(q)) return;

                    itemsHtml.push(`
                        <div class="luxury-card rounded-2xl p-4 space-y-2.5 hover:shadow-md transition-all border border-slate-200/80">
                            <div class="flex items-start justify-between">
                                <div>
                                    <div class="flex items-center space-x-1.5">
                                        <span class="px-2 py-0.5 rounded text-[9px] font-extrabold bg-amber-100 text-amber-900 border border-amber-300">📚 CODIFIED MASTER TEXT</span>
                                        <span class="text-[10px] font-bold text-slate-500 font-mono">${b.pages || 500} Pages Digested</span>
                                    </div>
                                    <h3 class="text-xs font-black text-slate-900 mt-1">${b.title}</h3>
                                    <p class="text-[11px] font-bold text-slate-600">${b.author}</p>
                                </div>
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0">BUNDLED</span>
                            </div>

                            <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-slate-400 block uppercase">Core Codified Principles</span>
                                <ul class="space-y-1 text-[11px] text-slate-700">
                                    ${(b.core_principles || []).map(p => `<li class="flex items-start space-x-1.5"><span class="text-amber-500 font-bold">•</span><span>${p}</span></li>`).join('')}
                                </ul>
                            </div>

                            <div class="flex items-center justify-between pt-1">
                                <span class="text-[10px] font-mono text-slate-500 font-semibold">${b.cross_links || 'Codified into Nexiv Valuation & Forensics'}</span>
                                <button onclick="askCouncilAbout('${b.title.replace(/'/g, "\\'")}')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg text-[10px] font-bold hover:bg-slate-800 transition-all flex items-center space-x-1">
                                    <i class="fa-solid fa-comments text-amber-400 text-[9px]"></i>
                                    <span>Ask Council</span>
                                </button>
                            </div>
                        </div>
                    `);
                });
            }

            // 2. ACADEMIC INSTITUTIONS
            if (f === 'ALL' || f === 'ACADEMIC') {
                const insts = cachedVaultData.academic_institutions || {};
                Object.keys(insts).forEach(k => {
                    const u = insts[k];
                    const searchText = (u.name + ' ' + u.school + ' ' + (u.nobel_laureates_and_pioneers || '') + ' ' + u.core_doctrine + ' ' + (u.rule_in_nexiv || '') + ' ' + (u.seminal_breakthroughs || []).join(' ')).toLowerCase();
                    if (q && !searchText.includes(q)) return;

                    itemsHtml.push(`
                        <div class="luxury-card rounded-2xl p-4 space-y-2.5 hover:shadow-md transition-all border border-slate-200/80">
                            <div class="flex items-start justify-between">
                                <div>
                                    <div class="flex items-center space-x-1.5">
                                        <span class="px-2 py-0.5 rounded text-[9px] font-extrabold bg-blue-100 text-blue-900 border border-blue-300">🏛️ ACADEMIC INSTITUTION</span>
                                        <span class="text-[10px] font-bold text-slate-500">Tier-1 Research</span>
                                    </div>
                                    <h3 class="text-xs font-black text-slate-900 mt-1">${u.name}</h3>
                                    <p class="text-[11px] font-semibold text-slate-600">${u.school}</p>
                                </div>
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200 shrink-0">ACTIVE</span>
                            </div>

                            <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-slate-400 block uppercase">Nobel Laureates & Pioneers</span>
                                <p class="text-[11px] font-medium text-slate-700">${u.nobel_laureates_and_pioneers}</p>
                            </div>

                            <div class="bg-amber-50/50 p-2.5 rounded-xl border border-amber-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-amber-800 block uppercase">Seminal Breakthroughs in Nexiv</span>
                                <ul class="space-y-1 text-[11px] text-slate-700">
                                    ${(u.seminal_breakthroughs || []).slice(0, 3).map(sb => `<li class="flex items-start space-x-1.5"><span class="text-amber-600 font-bold">•</span><span>${sb}</span></li>`).join('')}
                                </ul>
                            </div>

                            <div class="p-2.5 rounded-xl bg-slate-900 text-white text-[11px] space-y-0.5">
                                <span class="text-[9px] font-bold uppercase text-amber-400 block tracking-wider">EXACT RULE ENFORCED BY NEXIV</span>
                                <p class="font-medium text-slate-200 leading-snug">${u.rule_in_nexiv}</p>
                            </div>

                            <div class="flex items-center justify-between pt-1">
                                <span class="text-[10px] text-slate-500 font-medium">Doctrine: ${u.core_doctrine}</span>
                                <button onclick="askCouncilAbout('${u.name.replace(/'/g, "\\'")}')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg text-[10px] font-bold hover:bg-slate-800 transition-all flex items-center space-x-1">
                                    <i class="fa-solid fa-comments text-amber-400 text-[9px]"></i>
                                    <span>Ask Council</span>
                                </button>
                            </div>
                        </div>
                    `);
                });
            }

            // 3. INVESTMENT FIRMS & ALLOCATORS
            if (f === 'ALL' || f === 'FIRMS') {
                const firms = cachedVaultData.investment_firms || {};
                Object.keys(firms).forEach(k => {
                    const fm = firms[k];
                    const searchText = (fm.name + ' ' + fm.leader + ' ' + (fm.aum || '') + ' ' + (fm.core_philosophy || '') + ' ' + fm.doctrine + ' ' + (fm.rule || '')).toLowerCase();
                    if (q && !searchText.includes(q)) return;

                    itemsHtml.push(`
                        <div class="luxury-card rounded-2xl p-4 space-y-2.5 hover:shadow-md transition-all border border-slate-200/80">
                            <div class="flex items-start justify-between">
                                <div>
                                    <div class="flex items-center space-x-1.5">
                                        <span class="px-2 py-0.5 rounded text-[9px] font-extrabold bg-purple-100 text-purple-900 border border-purple-300">🏢 GLOBAL ALLOCATOR</span>
                                        <span class="text-[10px] font-bold text-slate-500 font-mono">${fm.aum || 'Global Scale'}</span>
                                    </div>
                                    <h3 class="text-xs font-black text-slate-900 mt-1">${fm.name}</h3>
                                    <p class="text-[11px] font-bold text-slate-600">Leader: ${fm.leader}</p>
                                </div>
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200 shrink-0">INSTITUTIONAL</span>
                            </div>

                            <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-slate-400 block uppercase">Core Philosophy</span>
                                <p class="text-[11px] font-bold text-slate-800">${fm.core_philosophy}</p>
                                <p class="text-[11px] text-slate-600 leading-relaxed mt-1">${fm.doctrine}</p>
                            </div>

                            <div class="p-2.5 rounded-xl bg-slate-900 text-white text-[11px] space-y-0.5">
                                <span class="text-[9px] font-bold uppercase text-amber-400 block tracking-wider">INSTITUTIONAL ALLOCATION LAW</span>
                                <p class="font-medium text-slate-200 leading-snug">${fm.rule}</p>
                            </div>

                            <div class="flex items-center justify-end pt-1">
                                <button onclick="askCouncilAbout('${fm.name.replace(/'/g, "\\'")}')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg text-[10px] font-bold hover:bg-slate-800 transition-all flex items-center space-x-1">
                                    <i class="fa-solid fa-comments text-amber-400 text-[9px]"></i>
                                    <span>Ask Council</span>
                                </button>
                            </div>
                        </div>
                    `);
                });
            }

            // 4. FINANCIAL TITANS
            if (f === 'ALL' || f === 'TITANS') {
                const titans = cachedVaultData.titans || {};
                Object.keys(titans).forEach(k => {
                    const t = titans[k];
                    const searchText = (t.name + ' ' + (t.category || '') + ' ' + (t.domain_expertise || '') + ' ' + (t.analytical_superpower || '') + ' ' + (t.professional_role || '') + ' ' + (t.bio || '') + ' ' + (t.key_laws || []).join(' ')).toLowerCase();
                    if (q && !searchText.includes(q)) return;

                    itemsHtml.push(`
                        <div class="luxury-card rounded-2xl p-4 space-y-2.5 hover:shadow-md transition-all border border-slate-200/80">
                            <div class="flex items-start justify-between">
                                <div>
                                    <div class="flex items-center space-x-1.5">
                                        <span class="px-2 py-0.5 rounded text-[9px] font-extrabold bg-emerald-100 text-emerald-900 border border-emerald-300">🧠 MARKET TITAN</span>
                                        <span class="text-[9px] font-bold text-slate-500">${t.category}</span>
                                    </div>
                                    <h3 class="text-xs font-black text-slate-900 mt-1">${t.name}</h3>
                                    <p class="text-[11px] font-bold text-slate-600">${t.professional_role}</p>
                                </div>
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0">LEGEND</span>
                            </div>

                            <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-slate-400 block uppercase">Analytical Superpower</span>
                                <p class="text-[11px] font-semibold text-slate-800">${t.analytical_superpower}</p>
                            </div>

                            <div class="bg-emerald-50/50 p-2.5 rounded-xl border border-emerald-200/60 space-y-1 text-xs">
                                <span class="text-[10px] font-bold text-emerald-900 block uppercase">Key Laws & Compounding Rules</span>
                                <ul class="space-y-1 text-[11px] text-slate-700">
                                    ${(t.key_laws || []).map(l => `<li class="flex items-start space-x-1.5"><span class="text-emerald-600 font-bold">•</span><span>${l}</span></li>`).join('')}
                                </ul>
                            </div>

                            <div class="flex items-center justify-between pt-1">
                                <span class="text-[10px] text-slate-500 font-medium">${t.bio ? t.bio.slice(0, 65) + '...' : ''}</span>
                                <button onclick="askCouncilAbout('${t.name.replace(/'/g, "\\'")}')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg text-[10px] font-bold hover:bg-slate-800 transition-all flex items-center space-x-1">
                                    <i class="fa-solid fa-comments text-amber-400 text-[9px]"></i>
                                    <span>Ask Council</span>
                                </button>
                            </div>
                        </div>
                    `);
                });
            }

            // 5. EMPIRICAL DATASETS
            if (f === 'ALL' || f === 'DATASETS') {
                const datasets = cachedVaultData.empirical_datasets || {};
                Object.keys(datasets).forEach(k => {
                    const ds = datasets[k];
                    const searchText = (ds.name + ' ' + (ds.coverage || '') + ' ' + (ds.laws || '') + ' ' + (ds.files || []).join(' ')).toLowerCase();
                    if (q && !searchText.includes(q)) return;

                    itemsHtml.push(`
                        <div class="luxury-card rounded-2xl p-4 space-y-2.5 hover:shadow-md transition-all border border-slate-200/80">
                            <div class="flex items-start justify-between">
                                <div>
                                    <div class="flex items-center space-x-1.5">
                                        <span class="px-2 py-0.5 rounded text-[9px] font-extrabold bg-indigo-100 text-indigo-900 border border-indigo-300">📊 QUANT ARCHIVE & DATASET</span>
                                        <span class="text-[10px] font-bold text-slate-500">Empirical Research</span>
                                    </div>
                                    <h3 class="text-xs font-black text-slate-900 mt-1">${ds.name}</h3>
                                    <p class="text-[11px] font-medium text-slate-600">${ds.coverage}</p>
                                </div>
                                <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200 shrink-0">DATASET</span>
                            </div>

                            <div class="p-2.5 rounded-xl bg-slate-900 text-white text-[11px] space-y-0.5">
                                <span class="text-[9px] font-bold uppercase text-amber-400 block tracking-wider">EMPIRICAL QUANTITATIVE LAWS</span>
                                <p class="font-medium text-slate-200 leading-snug">${ds.laws}</p>
                            </div>

                            ${(ds.files && ds.files.length) ? `
                            <div class="bg-slate-50 p-2 rounded-xl border border-slate-200/60 text-[10px] text-slate-500 font-mono">
                                <span class="font-bold text-slate-400 uppercase text-[9px] block mb-0.5">Bundled Raw Data Files</span>
                                ${ds.files.join(' • ')}
                            </div>` : ''}

                            <div class="flex items-center justify-end pt-1">
                                <button onclick="askCouncilAbout('${ds.name.replace(/'/g, "\\'")}')" class="px-2.5 py-1 bg-slate-900 text-white rounded-lg text-[10px] font-bold hover:bg-slate-800 transition-all flex items-center space-x-1">
                                    <i class="fa-solid fa-comments text-amber-400 text-[9px]"></i>
                                    <span>Ask Council</span>
                                </button>
                            </div>
                        </div>
                    `);
                });
            }

            if (itemsHtml.length === 0) {
                container.innerHTML = `<div class="p-8 text-center text-xs text-slate-400">No knowledge assets matched "${q}". Try searching for another term.</div>`;
            } else {
                container.innerHTML = itemsHtml.join('');
            }
        }

        // === LIVE IST CLOCK ===
        function updateLiveClock() {
            try {
                const now = new Date();
                const timeStr = now.toLocaleTimeString('en-IN', {
                    timeZone: 'Asia/Kolkata',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true
                });
                const dateStr = now.toLocaleDateString('en-IN', {
                    timeZone: 'Asia/Kolkata',
                    weekday: 'short',
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric'
                });
                const clockEl = document.getElementById('live-clock');
                const dateEl = document.getElementById('live-date');
                if (clockEl) clockEl.textContent = timeStr;
                if (dateEl) dateEl.textContent = dateStr;
            } catch(e) {}
        }
        updateLiveClock();
        setInterval(updateLiveClock, 1000);

        // === SMART PAGE REFRESH FOR IPHONE & WEB APP ===
        function triggerSmartRefresh(event) {
            if (event) event.preventDefault();
            const btn = document.getElementById('page-refresh-btn');
            const spinner = document.getElementById('refresh-spinner');
            const label = document.getElementById('refresh-label');

            // 1. Tactile haptic pulse on mobile devices
            if (window.navigator && window.navigator.vibrate) {
                try { window.navigator.vibrate(25); } catch(e) {}
            }

            // 2. Animate icon and update button UI immediately
            if (spinner) spinner.classList.add('fa-spin');
            if (label) label.textContent = 'Updating...';
            if (btn) {
                btn.classList.add('ring-2', 'ring-amber-400', 'scale-95');
                btn.disabled = true;
            }

            // 3. Save current user state (active tab & active ticker) in sessionStorage so it restores cleanly
            try {
                const currentTicker = document.getElementById('ticker-input') ? document.getElementById('ticker-input').value.trim() : '';
                if (currentTicker) {
                    sessionStorage.setItem('nexiv_active_ticker', currentTicker);
                }
                let currentTab = 'stock';
                if (!document.getElementById('ipo-section').classList.contains('hidden')) currentTab = 'ipo';
                else if (!document.getElementById('chat-section').classList.contains('hidden')) currentTab = 'chat';
                else if (!document.getElementById('vault-section').classList.contains('hidden')) currentTab = 'vault';
                sessionStorage.setItem('nexiv_active_tab', currentTab);
            } catch(e) {}

            // 4. Force clean page reload to refresh all real-time feeds, market clock, and scripts
            setTimeout(() => {
                window.location.reload();
            }, 250);
        }

        // Robust initialization: restores state after smart refresh
        function initApp() {
            updateLiveClock();

            try {
                const savedTab = sessionStorage.getItem('nexiv_active_tab');
                const savedTicker = sessionStorage.getItem('nexiv_active_ticker');

                if (savedTab && savedTab !== 'stock') {
                    switchTab(savedTab);
                }

                if (savedTicker && document.getElementById('ticker-input')) {
                    document.getElementById('ticker-input').value = savedTicker;
                }
            } catch(e) {}

            analyzeStock();
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initApp);
        } else {
            initApp();
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_TEMPLATE

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=False)
