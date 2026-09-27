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
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from nexiv_brain.decision_engine import CBMDecisionEngine
from nexiv_brain.indian_market import NexivIndianMarket
from nexiv_brain import nexiv_config as cfg

app = FastAPI(title="Nexiv.AI • Autonomous Institutional Financial Intelligence", version="3.0.0")

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

@app.get("/favicon.ico")
def get_favicon():
    svg_favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44">
      <defs>
        <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FCD34D"/>
          <stop offset="40%" stop-color="#F59E0B"/>
          <stop offset="70%" stop-color="#D97706"/>
          <stop offset="100%" stop-color="#92400E"/>
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="40" height="40" rx="10" fill="#0F172A" stroke="url(#g)" stroke-width="2"/>
      <path d="M11 32 V 12 L 23 28 V 12" stroke="url(#g)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M23 28 L 33 12" stroke="#10B981" stroke-width="3" stroke-linecap="round"/>
      <polygon points="33,7 35,10 39,10 36,12.5 37.5,15.5 33,13.5 29,15.5 30.5,12.5 27.5,10 31.5,10" fill="#FDE68A"/>
    </svg>"""
    return Response(content=svg_favicon, media_type="image/svg+xml")

@app.get("/api/search")
def search_stocks(q: str = ""):
    return NexivIndianMarket.search_equities(q)

@app.get("/api/stock/{ticker}")
def analyze_stock(ticker: str):
    try:
        t = ticker.strip()
        res = CBMDecisionEngine.evaluate_stock_action(t)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ipos/live")
def get_live_ipos():
    return NexivIndianMarket.get_live_ipos()

@app.post("/api/ipo/analyze")
def analyze_ipo(data: IPOSubmission):
    try:
        res = CBMDecisionEngine.evaluate_ipo_action(data.dict())
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge")
def get_knowledge_summary():
    graph_path = cfg.MASTER_KNOWLEDGE_GRAPH
    try:
        if os.path.exists(graph_path):
            with open(graph_path) as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "status": "Codified Vault Active",
        "total_pages": 5053,
        "books_catalog": [
            {"title": "Investment Valuation (3rd Ed)", "author": "Aswath Damodaran", "pages": 949},
            {"title": "Measuring and Managing Value (7th Ed)", "author": "McKinsey & Co. (Tim Koller)", "pages": 862},
            {"title": "Security Analysis (7th Ed)", "author": "Benjamin Graham & David Dodd", "pages": 1135},
            {"title": "Principles of Corporate Finance (7th Ed)", "author": "Richard Brealey & Stewart Myers", "pages": 1062},
            {"title": "Advances in Financial Machine Learning", "author": "Marcos López de Prado", "pages": 489},
            {"title": "The Most Important Thing", "author": "Howard Marks", "pages": 244},
            {"title": "Financial Shenanigans (4th Ed)", "author": "Howard M. Schilit", "pages": 312}
        ]
    }

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nexiv.AI • Autonomous Institutional Financial Intelligence</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.ico">
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
                    <p class="text-[10px] font-semibold text-slate-500 tracking-wider">INDIA & GLOBAL • 5,053 PAGES • LIVE</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span class="relative flex h-2 w-2 mr-1.5">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                    NSE / BSE LIVE
                </span>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-xl mx-auto px-4 pt-4">

        <!-- Navigation Segmented Control -->
        <div class="flex rounded-2xl bg-slate-100 p-1 mb-4 border border-slate-200/80 shadow-inner">
            <button id="tab-stock-btn" onclick="switchTab('stock')" class="flex-1 py-2 text-xs font-bold rounded-xl bg-white text-slate-900 shadow-sm transition-all flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-chart-line text-emerald-600"></i>
                <span>Stock Decision</span>
            </button>
            <button id="tab-ipo-btn" onclick="switchTab('ipo')" class="flex-1 py-2 text-xs font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-rocket text-amber-600"></i>
                <span>Indian IPOs & GMP</span>
            </button>
            <button id="tab-vault-btn" onclick="switchTab('vault')" class="flex-1 py-2 text-xs font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-book-bookmark text-slate-600"></i>
                <span>7 Titans Vault</span>
            </button>
        </div>

        <!-- 1. STOCK DECISION SECTION -->
        <section id="stock-section" class="space-y-4">
            <!-- Search & Autocomplete Card -->
            <div class="luxury-card rounded-2xl p-4 transition-all relative">
                <div class="flex items-center justify-between mb-2">
                    <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">LIVE TYPEAHEAD SEARCH</label>
                    <span class="text-[10px] font-semibold text-slate-400">SEARCH ANY INDIAN OR US STOCK</span>
                </div>
                
                <div class="relative flex space-x-2">
                    <div class="relative flex-1">
                        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-xs"></i>
                        <input type="text" id="ticker-input" value="RELIANCE" placeholder="Type stock name (e.g. Tata, HDFC, Zomato, Reliance)" 
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
                    <button onclick="quickStock('RELIANCE')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">RELIANCE</button>
                    <button onclick="quickStock('TATAMOTORS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">TATA MOTORS</button>
                    <button onclick="quickStock('TCS')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">TCS</button>
                    <button onclick="quickStock('HDFCBANK')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">HDFC BANK</button>
                    <button onclick="quickStock('ZOMATO')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">ZOMATO</button>
                    <button onclick="quickStock('NVDA')" class="px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-slate-100 text-xs text-slate-700 font-mono font-semibold border border-slate-200/60 active:scale-95 transition-all">NVDA</button>
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

        <!-- 3. KNOWLEDGE VAULT SECTION -->
        <section id="vault-section" class="hidden space-y-4">
            <div class="luxury-card rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-2.5">
                    <div class="flex items-center space-x-2">
                        <div class="w-8 h-8 rounded-lg bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700">
                            <i class="fa-solid fa-landmark text-sm"></i>
                        </div>
                        <div>
                            <h2 class="text-sm font-bold text-slate-900">Ingested 7 Titans Vault</h2>
                            <p class="text-[10px] text-slate-500">5,053 Pages Codified into Nexiv Engine</p>
                        </div>
                    </div>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                        100% BUNDLED
                    </span>
                </div>
                <div id="vault-books-list" class="space-y-2.5"></div>
            </div>
        </section>

    </main>

    <script>
        let searchDebounceTimeout = null;
        let cachedIPOs = [];

        function switchTab(tab) {
            document.getElementById('stock-section').classList.add('hidden');
            document.getElementById('ipo-section').classList.add('hidden');
            document.getElementById('vault-section').classList.add('hidden');

            const inactiveClass = "flex-1 py-2 text-xs font-semibold rounded-xl text-slate-500 hover:text-slate-800 transition-all flex items-center justify-center space-x-1.5";
            const activeClass = "flex-1 py-2 text-xs font-bold rounded-xl bg-white text-slate-900 shadow-sm transition-all flex items-center justify-center space-x-1.5";

            document.getElementById('tab-stock-btn').className = inactiveClass;
            document.getElementById('tab-ipo-btn').className = inactiveClass;
            document.getElementById('tab-vault-btn').className = inactiveClass;

            if (tab === 'stock') {
                document.getElementById('stock-section').classList.remove('hidden');
                document.getElementById('tab-stock-btn').className = activeClass;
            } else if (tab === 'ipo') {
                document.getElementById('ipo-section').classList.remove('hidden');
                document.getElementById('tab-ipo-btn').className = activeClass;
                loadLiveIPOs();
            } else if (tab === 'vault') {
                document.getElementById('vault-section').classList.remove('hidden');
                document.getElementById('tab-vault-btn').className = activeClass;
                loadVault();
            }
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

            dropdown.innerHTML = matches.map(m => `
                <div onclick="selectSearchResult('${m.symbol}')" class="px-3.5 py-2.5 hover:bg-slate-50 cursor-pointer flex items-center justify-between border-b border-slate-100 last:border-b-0 transition-colors">
                    <div>
                        <div class="text-xs font-bold text-slate-900">${m.name}</div>
                        <div class="text-[10px] font-mono font-semibold text-slate-500">${m.symbol} • ${m.sector}</div>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[9px] font-bold ${m.exchange === 'NSE' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-blue-50 text-blue-700 border border-blue-200'}">
                        ${m.exchange}
                    </span>
                </div>
            `).join('');

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
            const p = data.raw_analysis.profile;
            const f = data.raw_analysis.forensics;
            const v = data.raw_analysis.valuation;
            const r = data.raw_analysis.risk_and_sizing;
            const syn = data.raw_analysis.council_synthesis;
            const cur = data.currency || (data.is_indian ? "₹" : "$");

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

            const upsidePct = data.expected_gain_pct;
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
                            <p class="text-xs font-semibold text-slate-500 font-mono">${p.symbol} • ${p.sector} • ${p.country}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">LIVE PRICE</span>
                            <span class="text-lg font-black font-mono text-slate-900">${cur}${p.current_price.toFixed(2)}</span>
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
                                <span class="text-base font-black font-mono text-slate-900">${cur}${data.target_price.toFixed(2)}</span>
                                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded border ${upsideClass}">${upsidePct > 0 ? '+' : ''}${upsidePct.toFixed(1)}%</span>
                            </div>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">STOP-LOSS FLOOR</span>
                            <div class="flex items-baseline space-x-1.5 mt-0.5">
                                <span class="text-base font-black font-mono text-rose-600">${cur}${data.stop_loss_price.toFixed(2)}</span>
                                <span class="text-[10px] font-bold text-slate-400">Defense</span>
                            </div>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">MARGIN OF SAFETY</span>
                            <span class="text-sm font-black font-mono ${v.margin_of_safety_pct >= 0 ? 'text-emerald-700' : 'text-rose-600'}">
                                ${v.margin_of_safety_pct > 0 ? '+' : ''}${v.margin_of_safety_pct.toFixed(1)}% vs DCF
                            </span>
                        </div>
                        <div class="bg-slate-50/90 p-3 rounded-2xl border border-slate-200/70">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">TIME HORIZON</span>
                            <span class="text-xs font-bold text-slate-800 truncate block mt-0.5">${data.time_horizon}</span>
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

                    <div class="space-y-2 text-xs">
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">1</span>
                            <div>
                                <span class="font-bold text-slate-900">Valuation Agent:</span>
                                <span class="text-slate-600 ml-1">${syn.valuation_agent.verdict} • DCF Value: ${cur}${v.dcf.intrinsic_value_per_share.toFixed(2)}</span>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-blue-100 text-blue-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">2</span>
                            <div>
                                <span class="font-bold text-slate-900">Forensics Agent:</span>
                                <span class="text-slate-600 ml-1">${syn.forensic_agent.verdict} • Altman Z: ${f.altman_z.z_score.toFixed(2)} (${f.altman_z.zone})</span>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">3</span>
                            <div>
                                <span class="font-bold text-slate-900">Risk & Sizing Agent:</span>
                                <span class="text-slate-600 ml-1">${syn.risk_sizing_agent.verdict} • Kelly Sizing: ${r.recommended_kelly_allocation_pct.toFixed(1)}% of capital</span>
                            </div>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200/60 flex items-start space-x-2.5">
                            <span class="w-5 h-5 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">4</span>
                            <div>
                                <span class="font-bold text-slate-900">Market Cycle Agent:</span>
                                <span class="text-slate-600 ml-1">${syn.market_cycle_agent.verdict} • Horizon: ${data.time_horizon}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- FORENSIC AUDIT CHECKLIST -->
                <div class="luxury-card rounded-2xl p-4 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-shield-halved text-emerald-600 text-xs"></i>
                            <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">Forensics & Shenanigans Shield</h3>
                        </div>
                        <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">SCHILIT AUDIT</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Altman Z-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${f.altman_z.z_score.toFixed(2)}</span>
                            <span class="text-[10px] font-bold ${f.altman_z.zone === 'SAFE ZONE' ? 'text-emerald-700' : 'text-rose-600'} block mt-0.5">${f.altman_z.zone}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Beneish M-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${f.beneish_m.m_score.toFixed(2)}</span>
                            <span class="text-[10px] font-bold ${f.beneish_m.m_score > -1.78 ? 'text-rose-600' : 'text-emerald-700'} block mt-0.5">${f.beneish_m.manipulation_risk}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Piotroski F-Score</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${f.piotroski_f.f_score}/9</span>
                            <span class="text-[10px] font-bold text-slate-600 block mt-0.5">${f.piotroski_f.rating}</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Sloan Accruals</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${f.sloan_accrual.accrual_ratio.toFixed(3)}</span>
                            <span class="text-[10px] font-bold text-slate-600 block mt-0.5">${f.sloan_accrual.quality_rating}</span>
                        </div>
                    </div>
                </div>

                <!-- VALUATION ARCHITECTURE -->
                <div class="luxury-card rounded-2xl p-4 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-calculator text-blue-600 text-xs"></i>
                            <h3 class="text-xs font-bold text-slate-900 uppercase tracking-wide">Valuation & Capital Allocation</h3>
                        </div>
                        <span class="text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-200">DAMODARAN DCF</span>
                    </div>

                    <div class="space-y-2.5 text-xs">
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Damodaran DCF Intrinsic Value</span>
                            <span class="font-mono font-bold text-slate-900 text-sm">${cur}${v.dcf.intrinsic_value_per_share.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Margin of Safety vs Current Price</span>
                            <span class="font-mono font-bold ${v.margin_of_safety_pct >= 0 ? 'text-emerald-700' : 'text-rose-600'}">
                                ${v.margin_of_safety_pct > 0 ? '+' : ''}${v.margin_of_safety_pct.toFixed(2)}%
                            </span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Benchmark Cost of Capital (WACC)</span>
                            <span class="font-mono font-bold text-slate-700">${(v.wacc * 100).toFixed(2)}%</span>
                        </div>
                        <div class="flex justify-between items-center py-1 border-b border-slate-100">
                            <span class="font-medium text-slate-500">Graham Net-Net Liquidation Floor</span>
                            <span class="font-mono font-bold text-slate-700">${cur}${v.graham_ncav.ncav_per_share.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center py-1">
                            <span class="font-medium text-slate-500">Kelly Optimal Capital Allocation</span>
                            <span class="font-mono font-bold text-emerald-700">${r.recommended_kelly_allocation_pct.toFixed(1)}% of Portfolio</span>
                        </div>
                    </div>
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
                        </div>
                        <span class="text-right">
                            <span class="text-[9px] font-bold text-slate-400 block uppercase">ISSUE SIZE</span>
                            <span class="text-xs font-extrabold font-mono text-slate-900">₹${ipo.issue_details.issue_size_cr.toLocaleString()} Cr</span>
                        </span>
                    </div>

                    <!-- Brokerage 4-Step Interactive Timeline -->
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200/60">
                        <div class="flex items-center justify-between text-[10px] font-semibold text-slate-400 mb-1">
                            <span>TIMELINE SCHEDULE</span>
                            <span class="text-amber-700 font-bold">${ipo.timeline.days_left}</span>
                        </div>
                        <div class="grid grid-cols-4 gap-1 text-center text-[10px] pt-1">
                            <div class="bg-white p-1.5 rounded-lg border border-slate-200/50">
                                <span class="block text-slate-400 text-[8px] uppercase">BIDDING</span>
                                <span class="font-bold text-slate-800 truncate block">${ipo.timeline.bidding_dates}</span>
                            </div>
                            <div class="bg-white p-1.5 rounded-lg border border-slate-200/50">
                                <span class="block text-slate-400 text-[8px] uppercase">ALLOTMENT</span>
                                <span class="font-bold text-slate-800 truncate block">${ipo.timeline.allotment_date}</span>
                            </div>
                            <div class="bg-white p-1.5 rounded-lg border border-slate-200/50">
                                <span class="block text-slate-400 text-[8px] uppercase">DEMAT CREDIT</span>
                                <span class="font-bold text-slate-800 truncate block">${ipo.timeline.demat_credit}</span>
                            </div>
                            <div class="bg-white p-1.5 rounded-lg border border-slate-200/50">
                                <span class="block text-slate-400 text-[8px] uppercase">LISTING DAY</span>
                                <span class="font-bold text-slate-800 truncate block">${ipo.timeline.listing_date}</span>
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
            const ipo = data.raw_ipo;

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
                            <p class="text-xs font-semibold text-slate-500 font-mono">${data.sector} • Band: ${data.offer_price_range}</p>
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
                            <span class="text-base font-black font-mono text-emerald-700 mt-0.5 block">${ipo.fresh_pct.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Promoter Exit (OFS)</span>
                            <span class="text-base font-black font-mono text-rose-600 mt-0.5 block">${ipo.ofs_pct.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Rule of 40 Score</span>
                            <span class="text-base font-black font-mono text-blue-600 mt-0.5 block">${ipo.rule_of_40_score.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200/60">
                            <span class="text-[10px] font-bold text-slate-400 block uppercase">Expected Listing Return</span>
                            <span class="text-base font-black font-mono text-slate-900 mt-0.5 block">${data.expected_gain}</span>
                        </div>
                    </div>
                </div>
            `;
            container.scrollIntoView({ behavior: 'smooth' });
        }

        async function loadVault() {
            const list = document.getElementById('vault-books-list');
            list.innerHTML = `
                <!-- 1. Damodaran -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-100 text-amber-800">VALUATION</span>
                            <h4 class="text-xs font-bold text-slate-900">Investment Valuation (3rd Ed)</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Aswath Damodaran • 949 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">FCFF, Terminal Growth, Equity Risk Premiums, Sector WACCs</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 2. McKinsey -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-blue-100 text-blue-800">CORPORATE</span>
                            <h4 class="text-xs font-bold text-slate-900">Valuation: Measuring Value of Companies (7th Ed)</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">McKinsey & Co. (Tim Koller) • 862 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">Key Value Driver, ROIC vs WACC Spread, Continuing Value</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 3. Graham & Dodd -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-800">VALUE</span>
                            <h4 class="text-xs font-bold text-slate-900">Security Analysis (7th Ed)</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Benjamin Graham & David Dodd • 1,135 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">Margin of Safety, Net-Net Working Capital, Liquidation Floor</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 4. Brealey Myers -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-indigo-100 text-indigo-800">FINANCE</span>
                            <h4 class="text-xs font-bold text-slate-900">Principles of Corporate Finance (7th Ed)</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Richard Brealey & Stewart Myers • 1,062 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">Capital Structure, Pecking Order Theory, Cost of Capital</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 5. Marcos Lopez de Prado -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-slate-200 text-slate-800">QUANT ML</span>
                            <h4 class="text-xs font-bold text-slate-900">Advances in Financial Machine Learning</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Marcos López de Prado • 489 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">Fractional Differentiation, Triple Barrier, Bet Sizing</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 6. Howard Marks -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-100 text-amber-800">CYCLES</span>
                            <h4 class="text-xs font-bold text-slate-900">The Most Important Thing</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Howard Marks (Oaktree) • 244 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">Credit Cycles, Second-Level Thinking, Asymmetric Risk</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>

                <!-- 7. Howard Schilit -->
                <div class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 flex items-center justify-between">
                    <div>
                        <div class="flex items-center space-x-1.5">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-rose-100 text-rose-800">FORENSICS</span>
                            <h4 class="text-xs font-bold text-slate-900">Financial Shenanigans (4th Ed)</h4>
                        </div>
                        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Howard M. Schilit • 312 pages digested</p>
                        <p class="text-[10px] text-slate-400 mt-0.5">7 Earnings Shenanigans, 4 Cash Flow Tricks, Fake Revenue</p>
                    </div>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">BUNDLED</span>
                </div>
            `;
        }

        // Initialize with default stock
        window.addEventListener('DOMContentLoaded', () => {
            analyzeStock();
        });
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
