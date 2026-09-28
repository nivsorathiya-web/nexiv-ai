import re
import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta

from nexiv_brain.indian_market import NexivIndianMarket
from nexiv_brain.market_data import CBMMarketDataProvider
from nexiv_brain.decision_engine import CBMDecisionEngine
from nexiv_brain import nexiv_config as cfg

class NexivChatEngine:
    """
    Unified Conversational Intelligence Engine for Nexiv.AI.
    Combines:
    1. Gemini 1.5 Flash LLM (when API key is provided) for 100% natural conversational fluency,
       tolerating casual English, grammatical typos, and Hinglish.
    2. Deep Autonomous Council Brain (fallback with 0 external API keys needed)
       synthesizing 5,053 pages of financial literature and real-time exchange data.
    """

    @classmethod
    def load_titans_knowledge_summary(cls) -> str:
        """Load condensed summaries of all 7 Titans books for LLM system prompt."""
        summary_lines = []
        k_dir = cfg.KNOWLEDGE_DIR
        for fn in sorted(os.listdir(k_dir)):
            if fn.endswith(".json") and fn != "master_codified_knowledge_graph.json":
                fp = os.path.join(k_dir, fn)
                try:
                    with open(fp, "r") as f:
                        d = json.load(f)
                        title = d.get("title", fn)
                        author = d.get("author", "")
                        pages = d.get("total_pages", "")
                        principles = d.get("core_principles_and_laws", [])
                        summary_lines.append(f"• Book: {title} by {author} ({pages} pages)")
                        for p in principles[:4]:
                            summary_lines.append(f"   - {p}")
                except Exception:
                    pass
        return "\n".join(summary_lines)

    @classmethod
    def call_gemini_api(cls, prompt: str, api_key: str, history=None) -> str:
        """Call Google Gemini 1.5 Flash API via direct REST."""
        titans_context = cls.load_titans_knowledge_summary()
        current_ipos = NexivIndianMarket.get_live_ipos()
        ipo_briefs = [f"{i['company_name']} ({i['status']}) - Price: {i['issue_details']['price_range']}, GMP: {i['gmp']['pct']}%, Action: {i['ai_decision']['action']}" for i in current_ipos[:6]]

        system_instruction = f"""You are the Master AI Council of Nexiv.AI — an autonomous, institutional-grade financial intelligence engine.
You have fully digested and mastered 5,053 pages of financial literature across the 7 Titans:
{titans_context}

CRITICAL USER UNDERSTANDING RULES:
1. The user may write in casual, informal, or grammatically imperfect English, or Hinglish (e.g. 'can i buy this', 'tell me good share', 'remove money from this', 'should i apply in this ipo').
2. NEVER correct the user's grammar, spelling, or phrasing.
3. Understand their core intention deeply and immediately.
4. Respond in simple, clear, powerful, and friendly language, yet backed by institutional precision.
5. Provide actionable answers: CLEAR VERDICT (Buy / Hold / Sell / Avoid), Target Price, Margin of Safety, and explain WHY using the 7 Titans rules.

CURRENT REAL-WORLD MARKET DATA CONTEXT (Sep-Oct 2026):
Active Indian IPOs:
{chr(10).join(ipo_briefs)}
Always state exact facts: Moneyview, Snapdeal/AceVector, Orient Cables, Runwal Enterprises, German Green Steel, and SRIT India are the real current Indian IPOs.
"""

        contents = []
        if history and isinstance(history, list):
            for h in history[-6:]:
                role = "user" if h.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h.get("content", "")}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1000
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        return "I processed your request, but could not retrieve a complete response from Gemini."

    @classmethod
    def autonomous_brain_response(cls, user_text: str) -> str:
        """
        Deep Autonomous Council Brain (Zero API Key fallback).
        Analyzes intent, matches stock/IPO entities, retrieves book knowledge,
        and generates an institutional-grade personalized answer.
        """
        raw = user_text.lower().strip()

        # 1. Detect if a stock is mentioned
        matched_stock = None
        for item in NexivIndianMarket.SEARCH_CATALOG:
            sym_clean = item["symbol"].replace(".NS", "").replace(".BO", "").lower()
            name_lower = item["name"].lower()
            kw_lower = item["keywords"].lower()
            
            # Direct symbol check
            tokens = re.findall(r'[a-z0-9]+', raw)
            if sym_clean in tokens or sym_clean in raw:
                matched_stock = item
                break
            # Specific alias & typo triggers
            if any(w in raw for w in ["tata motor", "tatamotor", "tatamotors", "tata"]):
                matched_stock = {"symbol": "TMPV.NS", "name": "Tata Motors Passenger Vehicles Ltd"}
                break
            if any(w in raw for w in ["zomato", "zomto", "blinkit", "eternal"]):
                matched_stock = {"symbol": "ETERNAL.NS", "name": "Zomato Limited (Eternal Ltd)"}
                break
            if any(w in raw for w in ["reliance", "relince", "relianc", "jio", "ambani"]) or "ril" in tokens:
                matched_stock = {"symbol": "RELIANCE.NS", "name": "Reliance Industries Limited"}
                break
            if any(w in raw for w in ["sbi", "state bank", "sbin"]):
                matched_stock = {"symbol": "SBIN.NS", "name": "State Bank of India"}
                break
            if "hdfc" in raw:
                matched_stock = {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited"}
                break
            if any(w in raw for w in ["infosys", "infy", "infosis"]):
                matched_stock = {"symbol": "INFY.NS", "name": "Infosys Limited"}
                break
            if "tcs" in tokens or "tata consult" in raw:
                matched_stock = {"symbol": "TCS.NS", "name": "Tata Consultancy Services Ltd"}
                break
            if "itc" in tokens:
                matched_stock = {"symbol": "ITC.NS", "name": "ITC Limited"}
                break
            if "apple" in raw or "aapl" in tokens:
                matched_stock = {"symbol": "AAPL", "name": "Apple Inc."}
                break
            if "nvidia" in raw or "nvda" in tokens:
                matched_stock = {"symbol": "NVDA", "name": "NVIDIA Corporation"}
                break
            if "tesla" in raw or "tsla" in tokens:
                matched_stock = {"symbol": "TSLA", "name": "Tesla, Inc."}
                break

        if matched_stock:
            try:
                dec = CBMDecisionEngine.evaluate_stock_action(matched_stock["symbol"])
                cur = dec["currency"]
                price = dec["current_price"]
                action = dec["action"]
                target = dec["target_price"]
                gain = dec["expected_gain_pct"]
                advice = dec["summary_advice"]
                source = dec["price_source"]
                ts = dec["price_timestamp"]

                # Extract council rationale
                reasons_for = dec.get("reasons_for", [])
                reasons_against = dec.get("reasons_against", [])

                reply = f"### 🏛️ Nexiv AI Council Analysis: **{dec['company_name']}**\n\n"
                reply += f"• **Live Market Price**: **{cur}{price:.2f}** ({source} @ {ts})\n"
                reply += f"• **Council Executive Action**: **{action}**\n"
                reply += f"• **Intrinsic Valuation Target**: **{cur}{target:.2f}** ({gain:+.1f}% upside)\n"
                reply += f"• **Suggested Stop-Loss**: **{cur}{dec['stop_loss_price']:.2f}** | Risk Level: **{dec['risk_level']}**\n\n"
                reply += f"**Council Synthesis (from the 7 Titans)**:\n{advice}\n\n"
                
                if reasons_for:
                    reply += "**Bullish Pillars (Graham & Damodaran)**:\n"
                    for r in reasons_for[:2]:
                        reply += f"  ✅ {r}\n"
                if reasons_against:
                    reply += "\n**Forensic & Cycle Flags (Schilit & Marks)**:\n"
                    for r in reasons_against[:2]:
                        reply += f"  ⚠️ {r}\n"

                reply += f"\n💡 *Recommendation*: {'You can allocate capital here with strict adherence to position sizing.' if 'INVEST' in action else 'Avoid adding fresh capital; maintain discipline and protect liquidity.'}"
                return reply
            except Exception as e:
                pass

        # 2. Detect if an IPO is mentioned
        ipos = NexivIndianMarket.get_live_ipos()
        for ipo in ipos:
            c_name = ipo["company_name"].lower()
            if any(w in raw for w in c_name.split()[:2] if len(w) > 3) or ipo["symbol"].lower() in raw:
                action = ipo["ai_decision"]["action"]
                summary = ipo["ai_decision"]["summary"]
                gmp = ipo["gmp"]
                price = ipo["issue_details"]["price_range"]
                lot = ipo["issue_details"]["lot_size"]
                min_inv = ipo["issue_details"]["min_investment"]
                bidding = ipo["timeline"]["bidding_dates"]
                fresh_pct = ipo["issue_details"]["fresh_pct"]
                ofs_pct = ipo["issue_details"]["ofs_pct"]

                reply = f"### 🚀 IPO Verdict: **{ipo['company_name']}**\n\n"
                reply += f"• **Status**: **{ipo['status']}** ({ipo['timeline']['days_left']})\n"
                reply += f"• **Bidding Dates**: **{bidding}**\n"
                reply += f"• **Price Range**: **{price}** (Lot: {lot} shares | Min Investment: ₹{min_inv:,})\n"
                reply += f"• **Grey Market Premium (GMP)**: **₹{gmp['value']} (+{gmp['pct']}%)** — Est. Listing: ₹{gmp['expected_listing_price']}\n"
                reply += f"• **Issue Structure (Jay Ritter Law)**: **{fresh_pct:.1f}% Fresh Issue** vs **{ofs_pct:.1f}% OFS**\n\n"
                reply += f"• **AI Council Action**: **{action}**\n\n"
                reply += f"**Institutional Thesis**:\n{summary}\n\n"
                if ofs_pct > 50:
                    reply += "⚠️ *Jay Ritter Warning*: Over 50% OFS indicates heavy promoter liquidity exit. Historically, high-OFS issues underperform 3-year benchmarks.\n"
                elif fresh_pct > 65:
                    reply += "✅ *Growth Alignment*: Over 65% of proceeds enter company balance sheet for real expansion rather than secondary investor cashouts.\n"
                return reply

        # 3. Check for specific Titans book concepts
        if any(w in raw for w in ["schilit", "shenanigan", "fraud", "manipulat", "accounting trick", "fake revenue", "fake profit", "fake account", "fake accounting", "lying on balance sheet", "balance sheet lie", "cheat", "scam"]):
            return """### 🔍 Howard Schilit's 7 Financial Shenanigans (from *Financial Shenanigans*, 4th Ed)

Nexiv AI's Forensic Auditor tests every company against these 7 exact rules:
1. **Recording Revenue Too Soon**: Shipping products before delivery dates, billing before completion.
2. **Recording Bogus Revenue**: Recording transactions that lack economic substance or circular cash deals.
3. **Boosting Income with One-Time Gains**: Selling assets and disguising gains as regular operating profits.
4. **Shifting Current Expenses to Later Periods**: Capitalizing regular operating expenses on the balance sheet.
5. **Employing Other Techniques to Hide Losses**: Creating hidden liabilities or failing to record severance/bad debt.
6. **Shifting Current Income to Later Periods**: Creating 'cookie-jar' reserves in good years to artificially smooth bad years.
7. **Shifting Future Expenses to Current Period**: Taking an massive one-time 'big bath' write-off to make future quarters look hyper-profitable.

💡 *Our Council Flag*: When Days Sales Outstanding (DSO) or Receivables grow faster than Revenue, Schilit warns of aggressive revenue pulling."""

        if any(w in raw for w in ["margin of safety", "graham", "dodd", "buffett", "value investing", "safe price", "fair price", "net net", "liquidation floor"]):
            return """### 🛡️ Benjamin Graham & David Dodd's Margin of Safety (from *Security Analysis*, 7th Ed)

The central pillar of institutional capital preservation:
• **The Concept**: Never pay full price for future projections. The intrinsic value of a business must exceed its current market price by at least **25% to 35%** (the Margin of Safety).
• **Why It Protects You**: If future earnings miss forecasts, if macroeconomic interest rates surge, or if management makes an error, your capital is protected because you bought at an asset-backed discount.
• **Graham's Core Rule**: *"The function of the margin of safety is, in essence, that of rendering unnecessary an accurate estimate of the future."*

💡 In Nexiv.AI, our engine calculates Graham's Net-Net Liquidation Value and Earning Power Value (EPV) before greenlighting any stock purchase."""

        if any(w in raw for w in ["damodaran", "dcf", "wacc", "discounted cash flow", "discounted cash", "valuation", "intrinsic value", "cost of capital", "how to value"]):
            return """### 📊 Aswath Damodaran's Valuation Framework (from *Investment Valuation*, 3rd Ed)

Professor Damodaran's immutable laws encoded into Nexiv.AI:
1. **Cash Flow is Reality, Accounting Profit is an Opinion**: Focus exclusively on Free Cash Flow to the Firm (FCFF) — Net Operating Profit After Tax (NOPAT) minus Reinvestment.
2. **Cost of Capital (WACC)**: In India, WACC must reflect the 10-Year Indian Government Bond yield (~7.05%) plus India's Country Risk Premium (Damodaran Baa3 ERP: ~7.08%).
3. **The Reinvestment Hurdle**: Growth without Return on Invested Capital (ROIC) greater than WACC destroys shareholder value.
4. **Terminal Value Discipline**: A company's terminal growth rate can NEVER exceed the long-term risk-free GDP growth rate of the economy in which it operates (~5.5% in India)."""

        if any(w in raw for w in ["ritter", "ipo rule", "underpricing", "listing gain", "grey market", "gmp meaning", "how ipo works"]):
            return """### 📈 Professor Jay Ritter's IPO Laws (University of Florida IPO Database)

Learnings from 40+ years of global and Indian IPO performance:
1. **The First-Day Underpricing Paradox**: High-GMP IPOs pop 20%–50% on Day 1 to reward institutional anchor investors (QIBs), but retail investors who buy at the peak often get trapped.
2. **The 3-Year Underperformance Curve**: Over 70% of heavily hyped IPOs underperform market indices over 3 years unless they generate genuine operating cash flow.
3. **The OFS Red Flag**: Issues where Offer for Sale (OFS) exceeds 50% have statistically lower 5-year compounding returns than 100% Fresh Issue offerings."""

        if any(w in raw for w in ["lopez de prado", "marcos", "bet size", "sizing", "kelly", "how much money", "allocation"]):
            return """### ⚖️ Marcos López de Prado's Quantitative Bet Sizing (from *Advances in Financial Machine Learning*)

Capital Preservation & Sizing Laws:
1. **Never Bet the Farm**: Even the highest-conviction thesis has non-zero probability of ruin.
2. **Half-Kelly Criterion**: We compute the Kelly fraction $f^* = \frac{p \cdot b - q}{b}$ and scale down by 50% (Half-Kelly) to prevent drawdowns from market volatility.
3. **Triple Barrier Defense**: Every position has three simultaneous barriers — Profit Take Target, Stop-Loss Floor, and Time Horizon Expiration."""

        if any(w in raw for w in ["howard marks", "marks", "oaktree", "cycle", "bear market", "bull market", "second level"]):
            return """### 🔄 Howard Marks' Market Cycles & Risk (from *The Most Important Thing*)

Principles from Oaktree Capital's legendary chairman:
1. **Rule Number One**: Most things will prove to be cyclical.
2. **Rule Number Two**: Some of the greatest opportunities for gain and loss come when other people forget Rule Number One.
3. **Second-Level Thinking**: First-level thinking says: *"It's a good company, let's buy the stock."* Second-level thinking says: *"It's a good company, but everybody thinks it's a great company, and it's not. So the stock is overrated and overpriced; let's sell."*"""

        # 4. General Financial Guidance
        return f"""### 🧠 Nexiv AI Council Assistant

I understand your question! Here is how our **7 Titans AI Brain** approaches your capital:

1. **Individual Stocks**: Search any stock (e.g. *Reliance, Tata Motors, Zomato, SBI, Infosys*) in the search bar or ask me directly — I will pull the **live exchange quote** and run our 4-agent council.
2. **Current Indian IPOs**: Ask about any live IPO (e.g. *Moneyview, Snapdeal/AceVector, Orient Cables, Runwal, SRIT India*) to check bidding status, GMP, and Jay Ritter underpricing score.
3. **Forensics & Accounting**: Ask how we detect fraud using *Howard Schilit's 7 Shenanigans*.
4. **Valuation & Margin of Safety**: Ask about *Damodaran's DCF models* or *Graham & Dodd's Margin of Safety*.

💬 *Tip: You can ask me in any language or casual English (e.g. "is tata motor good to buy today?", "moneyview ipo apply or avoid?", "how to know if company is lying on balance sheet?").*"""

    @classmethod
    def answer(cls, user_text: str, history=None, api_key: str = None) -> str:
        """Main entry point for conversational questions."""
        # 1. Check if Gemini API key is provided
        active_key = api_key or os.environ.get("GEMINI_API_KEY")
        if active_key and len(active_key.strip()) > 10:
            try:
                return cls.call_gemini_api(user_text, active_key.strip(), history)
            except Exception as e:
                # Graceful fallback to autonomous brain on API error
                pass

        # 2. Autonomous Brain Fallback
        return cls.autonomous_brain_response(user_text)
