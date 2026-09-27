import os
import json
import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from cbm_brain.decision_engine import CBMDecisionEngine
from cbm_brain import cbm_config as cfg

app = FastAPI(title="CBM Institutional Financial Intelligence AI Brain", version="2.0.0")

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
    country: str = "United States"

@app.get("/api/stock/{ticker}")
def analyze_stock(ticker: str):
    try:
        t = ticker.strip().upper()
        res = CBMDecisionEngine.evaluate_stock_action(t)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ipo/analyze")
def analyze_ipo(data: IPOSubmission):
    try:
        res = CBMDecisionEngine.evaluate_ipo_action(data.dict())
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge")
def get_knowledge_summary():
    vault_dir = os.path.join(cfg.CBM_DIR, "brain_knowledge")
    graph_path = os.path.join(vault_dir, "master_codified_knowledge_graph.json")
    if os.path.exists(graph_path):
        with open(graph_path) as f:
            return json.load(f)
    return {"status": "Knowledge vault not yet compiled."}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CBM Financial AI Brain</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen pb-20">

    <!-- Top Mobile Navigation Header -->
    <header class="sticky top-0 z-50 glass px-4 py-3 flex items-center justify-between border-b border-slate-800">
        <div class="flex items-center space-x-2">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-bold text-lg">
                <i class="fa-solid fa-brain"></i>
            </div>
            <div>
                <h1 class="text-base font-bold text-white tracking-wide">CBM AI BRAIN</h1>
                <p class="text-[10px] text-emerald-400 font-medium">5,053 PAGES • 7 TITANS • LIVE FEED</p>
            </div>
        </div>
        <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>LIVE
            </span>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-xl mx-auto px-4 pt-4">

        <!-- Navigation Tabs -->
        <div class="flex rounded-xl bg-slate-900 p-1 mb-4 border border-slate-800">
            <button id="tab-stock-btn" onclick="switchTab('stock')" class="flex-1 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition-all flex items-center justify-center space-x-1.5 shadow-sm">
                <i class="fa-solid fa-chart-line"></i>
                <span>Stock Decision</span>
            </button>
            <button id="tab-ipo-btn" onclick="switchTab('ipo')" class="flex-1 py-2 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-rocket"></i>
                <span>IPO Scanner</span>
            </button>
            <button id="tab-vault-btn" onclick="switchTab('vault')" class="flex-1 py-2 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-book-bookmark"></i>
                <span>7 Books Vault</span>
            </button>
        </div>

        <!-- 1. STOCK TAB -->
        <section id="stock-section" class="space-y-4">
            <!-- Search Card -->
            <div class="glass rounded-2xl p-4 shadow-xl">
                <label class="block text-xs font-semibold text-slate-400 mb-1.5">ENTER ANY GLOBAL TICKER</label>
                <div class="flex space-x-2">
                    <input type="text" id="ticker-input" value="AAPL" placeholder="e.g. NVDA, AAPL, TSLA, KO" 
                           class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-sm font-semibold uppercase text-white focus:outline-none focus:border-emerald-500 transition-colors">
                    <button onclick="analyzeStock()" id="analyze-btn" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2.5 rounded-xl text-sm transition-colors flex items-center space-x-1.5 shadow-lg shadow-emerald-900/30">
                        <span>Audit</span>
                        <i class="fa-solid fa-arrow-right text-xs"></i>
                    </button>
                </div>
                <!-- Quick Ticker Chips -->
                <div class="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-slate-800/80">
                    <span class="text-[10px] text-slate-500 self-center mr-1">Quick:</span>
                    <button onclick="quickStock('NVDA')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">NVDA</button>
                    <button onclick="quickStock('AAPL')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">AAPL</button>
                    <button onclick="quickStock('TSLA')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">TSLA</button>
                    <button onclick="quickStock('KO')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">KO</button>
                    <button onclick="quickStock('GOOGL')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">GOOGL</button>
                    <button onclick="quickStock('RELIANCE.NS')" class="px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-mono">RELIANCE</button>
                </div>
            </div>

            <!-- Loading Spinner -->
            <div id="stock-loading" class="hidden text-center py-10 space-y-3">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-emerald-500 border-t-transparent"></div>
                <p class="text-xs text-slate-400">Auditing balance sheet, calculating Damodaran DCF, checking Schilit shenanigans...</p>
            </div>

            <!-- Stock Results Container -->
            <div id="stock-result" class="space-y-4"></div>
        </section>

        <!-- 2. IPO TAB -->
        <section id="ipo-section" class="hidden space-y-4">
            <div class="glass rounded-2xl p-4 shadow-xl space-y-3">
                <div class="flex items-center justify-between">
                    <h2 class="text-sm font-bold text-white">IPO Evaluator (Damodaran & Jay Ritter)</h2>
                    <span class="text-[10px] text-emerald-400">Rule of 40 • Runway • Dilution</span>
                </div>
                <div class="space-y-2">
                    <div>
                        <label class="text-[11px] text-slate-400">Company Name</label>
                        <input type="text" id="ipo-name" value="ApexAI Cloud Technologies" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] text-slate-400">Sector</label>
                            <input type="text" id="ipo-sector" value="Software" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                        </div>
                        <div>
                            <label class="text-[11px] text-slate-400">Price Band ($)</label>
                            <div class="flex space-x-1">
                                <input type="number" id="ipo-pmin" value="28" class="w-1/2 bg-slate-900 border border-slate-700 rounded-lg px-2 py-1.5 text-xs text-white">
                                <input type="number" id="ipo-pmax" value="32" class="w-1/2 bg-slate-900 border border-slate-700 rounded-lg px-2 py-1.5 text-xs text-white">
                            </div>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] text-slate-400">Revenue (Annual $)</label>
                            <input type="number" id="ipo-rev" value="420000000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                        </div>
                        <div>
                            <label class="text-[11px] text-slate-400">Annual Growth Rate (e.g. 0.48)</label>
                            <input type="number" step="0.01" id="ipo-growth" value="0.48" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="text-[11px] text-slate-400">Fresh Shares</label>
                            <input type="number" id="ipo-fresh" value="20000000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                        </div>
                        <div>
                            <label class="text-[11px] text-slate-400">OFS Shares (Promoter Exit)</label>
                            <input type="number" id="ipo-ofs" value="5000000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white">
                        </div>
                    </div>
                    <button onclick="evaluateIPO()" class="w-full mt-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl text-xs transition-colors shadow-lg">
                        Run Institutional IPO Audit
                    </button>
                </div>
            </div>

            <div id="ipo-result" class="space-y-4"></div>
        </section>

        <!-- 3. KNOWLEDGE VAULT TAB -->
        <section id="vault-section" class="hidden space-y-4">
            <div class="glass rounded-2xl p-4 shadow-xl">
                <div class="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
                    <h2 class="text-sm font-bold text-white flex items-center space-x-2">
                        <i class="fa-solid fa-graduation-cap text-emerald-400"></i>
                        <span>Ingested AI Knowledge Vault</span>
                    </h2>
                    <span class="text-[10px] text-emerald-400 font-mono">5,053 PAGES INGESTED</span>
                </div>
                <div id="vault-books-list" class="space-y-2.5"></div>
            </div>
        </section>

    </main>

    <script>
        function switchTab(tab) {
            document.getElementById('stock-section').classList.add('hidden');
            document.getElementById('ipo-section').classList.add('hidden');
            document.getElementById('vault-section').classList.add('hidden');

            document.getElementById('tab-stock-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center space-x-1.5";
            document.getElementById('tab-ipo-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center space-x-1.5";
            document.getElementById('tab-vault-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center space-x-1.5";

            if (tab === 'stock') {
                document.getElementById('stock-section').classList.remove('hidden');
                document.getElementById('tab-stock-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition-all flex items-center justify-center space-x-1.5 shadow-sm";
            } else if (tab === 'ipo') {
                document.getElementById('ipo-section').classList.remove('hidden');
                document.getElementById('tab-ipo-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition-all flex items-center justify-center space-x-1.5 shadow-sm";
            } else if (tab === 'vault') {
                document.getElementById('vault-section').classList.remove('hidden');
                document.getElementById('tab-vault-btn').className = "flex-1 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition-all flex items-center justify-center space-x-1.5 shadow-sm";
                loadVault();
            }
        }

        function quickStock(ticker) {
            document.getElementById('ticker-input').value = ticker;
            analyzeStock();
        }

        async function analyzeStock() {
            const ticker = document.getElementById('ticker-input').value.trim();
            if (!ticker) return;

            document.getElementById('stock-loading').classList.remove('hidden');
            document.getElementById('stock-result').innerHTML = "";

            try {
                const resp = await fetch(`/api/stock/${ticker}`);
                const data = await resp.json();
                renderStockResult(data);
            } catch (err) {
                document.getElementById('stock-result').innerHTML = `<div class="p-4 rounded-xl bg-red-500/20 border border-red-500/40 text-red-300 text-xs">Failed to analyze ${ticker}: ${err.message}</div>`;
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

            let badgeClass = "bg-red-500/20 text-red-400 border-red-500/40";
            let badgeIcon = "fa-triangle-exclamation";
            if (data.action_code === "BUY" || data.action_code === "ACCUMULATE") {
                badgeClass = "bg-emerald-500/20 text-emerald-400 border-emerald-500/40";
                badgeIcon = "fa-circle-check";
            } else if (data.action_code === "HOLD") {
                badgeClass = "bg-amber-500/20 text-amber-400 border-amber-500/40";
                badgeIcon = "fa-hand";
            }

            container.innerHTML = `
                <!-- Big Action Card -->
                <div class="glass rounded-2xl p-5 border-2 shadow-2xl relative overflow-hidden" style="border-color: ${data.action_color};">
                    <div class="flex items-center justify-between mb-3">
                        <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border ${badgeClass}">
                            <i class="fa-solid ${badgeIcon}"></i>
                            <span>${data.action}</span>
                        </span>
                        <span class="text-xs text-slate-400 font-mono">${p.symbol} • $${p.current_price.toFixed(2)}</span>
                    </div>

                    <div class="text-sm font-semibold text-white mb-2">${data.company_name}</div>
                    <p class="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">${data.summary_advice}</p>

                    <!-- Key Action Digits Grid -->
                    <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800">
                        <div class="bg-slate-900/80 p-2.5 rounded-xl text-center">
                            <span class="block text-[10px] text-slate-400 font-medium">TARGET PRICE</span>
                            <span class="text-sm font-bold text-emerald-400">$${data.target_price.toFixed(2)}</span>
                        </div>
                        <div class="bg-slate-900/80 p-2.5 rounded-xl text-center">
                            <span class="block text-[10px] text-slate-400 font-medium">STOP-LOSS FLOOR</span>
                            <span class="text-sm font-bold text-red-400">$${data.stop_loss_price.toFixed(2)}</span>
                        </div>
                        <div class="bg-slate-900/80 p-2.5 rounded-xl text-center">
                            <span class="block text-[10px] text-slate-400 font-medium">HORIZON</span>
                            <span class="text-[11px] font-bold text-slate-200 mt-0.5 block">${data.time_horizon}</span>
                        </div>
                    </div>
                </div>

                <!-- Forensic Audit Breakdown -->
                <div class="glass rounded-2xl p-4 space-y-3">
                    <h3 class="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                        <i class="fa-solid fa-magnifying-glass-chart text-amber-400"></i>
                        <span>1. Forensic Audit (Schilit, Beneish & Altman)</span>
                    </h3>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Altman Z-Score</span>
                            <span class="font-bold text-slate-100">${f.altman_z.z_score.toFixed(2)}</span>
                            <span class="text-[10px] text-emerald-400 block mt-0.5">${f.altman_z.zone}</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Beneish M-Score</span>
                            <span class="font-bold text-slate-100">${f.beneish_m.m_score.toFixed(2)}</span>
                            <span class="text-[10px] ${f.beneish_m.m_score > -1.78 ? 'text-red-400' : 'text-emerald-400'} block mt-0.5">${f.beneish_m.manipulation_risk}</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Piotroski F-Score</span>
                            <span class="font-bold text-slate-100">${f.piotroski_f.f_score}/9</span>
                            <span class="text-[10px] text-slate-300 block mt-0.5">${f.piotroski_f.rating}</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Sloan Cash Accruals</span>
                            <span class="font-bold text-slate-100">${f.sloan_accrual.accrual_ratio.toFixed(4)}</span>
                            <span class="text-[10px] text-slate-300 block mt-0.5">${f.sloan_accrual.quality_rating}</span>
                        </div>
                    </div>
                </div>

                <!-- Valuation Architecture Breakdown -->
                <div class="glass rounded-2xl p-4 space-y-3">
                    <h3 class="text-xs font-bold text-slate-300 flex items-center space-x-1.5">
                        <i class="fa-solid fa-calculator text-blue-400"></i>
                        <span>2. Deterministic Valuation (Damodaran & McKinsey)</span>
                    </h3>
                    <div class="space-y-2 text-xs">
                        <div class="flex justify-between py-1 border-b border-slate-800">
                            <span class="text-slate-400">Damodaran DCF Intrinsic Value</span>
                            <span class="font-bold text-white">$${v.dcf.intrinsic_value_per_share.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-slate-800">
                            <span class="text-slate-400">Margin of Safety</span>
                            <span class="font-bold ${v.margin_of_safety_pct >= 0 ? 'text-emerald-400' : 'text-red-400'}">${v.margin_of_safety_pct > 0 ? '+' : ''}${v.margin_of_safety_pct.toFixed(2)}%</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-slate-800">
                            <span class="text-slate-400">Calibrated WACC / Cost of Capital</span>
                            <span class="font-bold text-slate-200">${(v.wacc * 100).toFixed(2)}%</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-slate-800">
                            <span class="text-slate-400">Graham Net-Net Liquidation Floor</span>
                            <span class="font-bold text-slate-200">$${v.graham_ncav.ncav_per_share.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between py-1">
                            <span class="text-slate-400">Kelly Sizing Max Allocation</span>
                            <span class="font-bold text-emerald-400">${r.recommended_kelly_allocation_pct.toFixed(1)}%</span>
                        </div>
                    </div>
                </div>
            `;
        }

        async function evaluateIPO() {
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
                pre_ipo_cash: 100000000
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

            container.innerHTML = `
                <div class="glass rounded-2xl p-5 border-2 shadow-2xl space-y-3" style="border-color: ${data.action_color};">
                    <div class="flex items-center justify-between">
                        <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold bg-slate-900 border" style="border-color: ${data.action_color}; color: ${data.action_color};">
                            <i class="fa-solid fa-flag"></i>
                            <span>${data.action}</span>
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Score: ${data.score}/100</span>
                    </div>

                    <h3 class="text-sm font-bold text-white">${data.company_name}</h3>
                    <p class="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">${data.summary_advice}</p>

                    <div class="grid grid-cols-2 gap-2 text-xs pt-2">
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Fresh Issue %</span>
                            <span class="font-bold text-emerald-400">${ipo.fresh_pct.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Promoter Exit (OFS)</span>
                            <span class="font-bold text-red-400">${ipo.ofs_pct.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Rule of 40 Score</span>
                            <span class="font-bold text-blue-400">${ipo.rule_of_40_score.toFixed(1)}%</span>
                        </div>
                        <div class="bg-slate-900 p-2.5 rounded-xl">
                            <span class="text-[10px] text-slate-400 block">Intrinsic DCF Fair Value</span>
                            <span class="font-bold text-white">$${ipo.intrinsic_value_per_share.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `;
        }

        async function loadVault() {
            const resp = await fetch('/api/knowledge');
            const data = await resp.json();
            const list = document.getElementById('vault-books-list');
            list.innerHTML = "";

            data.books_catalog.forEach(b => {
                list.innerHTML += `
                    <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800 flex items-center justify-between">
                        <div>
                            <h4 class="text-xs font-bold text-white">${b.title}</h4>
                            <p class="text-[10px] text-slate-400">${b.author} • ${b.pages} pages</p>
                        </div>
                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                            DIGESTED
                        </span>
                    </div>
                `;
            });
        }

        // Run default stock on load
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
    uvicorn.run("cbm_server:app", host="0.0.0.0", port=8000, reload=False)
