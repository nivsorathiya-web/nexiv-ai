from cbm_brain.agent_council import CBMAgentCouncil
from cbm_brain.ipo_engine import CBMIPOEngine

class CBMDecisionEngine:
    """
    Delivers direct, actionable investment decisions for any Stock or IPO:
    - INVEST NOW
    - HOLD
    - EXIT & REMOVE MONEY NOW
    """
    
    @classmethod
    def evaluate_stock_action(cls, ticker_symbol):
        analysis = CBMAgentCouncil.analyze_ticker(ticker_symbol)
        p = analysis["profile"]
        f = analysis["forensics"]
        v = analysis["valuation"]
        r = analysis["risk_and_sizing"]
        
        current_price = p["current_price"]
        intrinsic_val = v["dcf"]["intrinsic_value_per_share"]
        mos = v["margin_of_safety_pct"]
        z_score = f["altman_z"]["z_score"]
        z_zone = f["altman_z"]["zone"]
        m_score = f["beneish_m"]["m_score"]
        f_score = f["piotroski_f"]["f_score"]
        kelly = r["recommended_kelly_allocation_pct"]
        
        # Action Synthesis
        reasons_for = []
        reasons_against = []
        
        # Forensics checks
        if "SAFE" in z_zone:
            reasons_for.append(f"Balance sheet is rock-solid (Altman Z: {z_score:.2f})")
        else:
            reasons_against.append(f"Elevated credit/insolvency risk (Altman Z: {z_score:.2f})")
            
        if m_score <= -1.78:
            reasons_for.append("Earnings quality is verified clean (Beneish M-Score confirms low manipulation)")
        else:
            reasons_against.append(f"Earnings manipulation/revenue pull-forward flagged (Beneish M-Score: {m_score:.2f})")

        if f_score >= 7:
            reasons_for.append(f"Strong fundamental business momentum (Piotroski F-Score: {f_score}/9)")
        elif f_score <= 4:
            reasons_against.append(f"Weak fundamental deterioration (Piotroski F-Score: {f_score}/9)")

        # Target Price & Stop Loss
        target_price = round(max(intrinsic_val, current_price * 1.15 if mos > 10 else current_price * 0.95), 2)
        stop_loss = round(max(current_price * 0.85, v["graham_ncav"]["ncav_per_share"] if v["graham_ncav"]["ncav_per_share"] > 0 else current_price * 0.85), 2)
        expected_gain = round(((target_price - current_price) / max(current_price, 0.01)) * 100.0, 1)

        # Direct Decision Matrix
        if mos >= 20 and "SAFE" in z_zone and m_score <= -1.78:
            action = "INVEST & BUY NOW"
            action_code = "BUY"
            action_color = "#10B981" # Green
            horizon = "1 to 3 Years (Value Compounding)"
            risk_level = "LOW TO MODERATE"
            summary_advice = f"Substantial margin of safety (+{mos:.1f}%) with clean accounting. Strong opportunity to allocate capital."
        elif mos >= 5 and "DISTRESS" not in z_zone and m_score <= -1.78:
            action = "ACCUMULATE / BUY ON DIPS"
            action_code = "ACCUMULATE"
            action_color = "#34D399"
            horizon = "1 to 2 Years"
            risk_level = "MODERATE"
            summary_advice = f"Fairly priced compounder with slight upside (+{mos:.1f}%). Safe to invest in tranches."
        elif mos >= -15 and "DISTRESS" not in z_zone and m_score <= -1.50:
            action = "HOLD / DO NOT ADD MONEY"
            action_code = "HOLD"
            action_color = "#F59E0B" # Yellow/Amber
            horizon = "Hold Existing Position"
            risk_level = "MODERATE"
            summary_advice = "The business is fundamentally strong but fully valued. If you own it, hold; do not add fresh capital at this price."
        else:
            action = "EXIT & REMOVE MONEY NOW"
            action_code = "SELL"
            action_color = "#EF4444" # Red
            horizon = "Immediate Liquidation / Avoid"
            risk_level = "HIGH RISK"
            summary_advice = f"Priced at a significant premium to fundamental cash flow (Margin of safety: {mos:.1f}%), or accounting red flags detected. Protect capital and exit."

        return {
            "symbol": p["symbol"],
            "company_name": p["company_name"],
            "current_price": current_price,
            "action": action,
            "action_code": action_code,
            "action_color": action_color,
            "target_price": target_price,
            "expected_gain_pct": expected_gain,
            "stop_loss_price": stop_loss,
            "time_horizon": horizon,
            "risk_level": risk_level,
            "recommended_allocation_pct": kelly,
            "summary_advice": summary_advice,
            "reasons_for": reasons_for,
            "reasons_against": reasons_against,
            "raw_analysis": analysis
        }

    @classmethod
    def evaluate_ipo_action(cls, ipo_data):
        ipo_res = CBMIPOEngine.evaluate_ipo(**ipo_data)
        score = ipo_res["score"]
        mos = ipo_res["margin_of_safety_pct"]
        fresh_pct = ipo_res["fresh_pct"]
        runway = ipo_res["runway_months"]
        
        if score >= 75 and mos >= 15:
            action = "APPLY NOW (LONG-TERM COMPOUNDER)"
            action_code = "APPLY_LONG"
            action_color = "#10B981"
            horizon = "Hold for 1 to 3 Years"
            expected_gain = f"+{mos:.1f}% intrinsic upside"
            advice = "High quality offering: capital is entering the company for expansion with a safe cash runway and positive margin of safety."
        elif score >= 50 or (fresh_pct >= 60 and runway >= 18):
            action = "APPLY FOR LISTING GAINS ONLY"
            action_code = "APPLY_FLIP"
            action_color = "#F59E0B"
            horizon = "Sell on Day 1 of Listing"
            expected_gain = "+10% to +25% First-Day Pop"
            advice = "Good retail/institutional momentum for listing pop, but long-term economics warrant taking profits on Day 1."
        else:
            action = "DO NOT APPLY (AVOID)"
            action_code = "AVOID"
            action_color = "#EF4444"
            horizon = "Avoid / Do Not Submit Application"
            expected_gain = "Negative Expected Value"
            advice = "High risk of post-listing crash due to heavy promoter exit (OFS), overvaluation, or short cash runway."

        return {
            "company_name": ipo_res["company_name"],
            "sector": ipo_res["sector"],
            "offer_price_range": ipo_res["offer_price_range"],
            "offer_price_mid": ipo_res["offer_price_mid"],
            "action": action,
            "action_code": action_code,
            "action_color": action_color,
            "time_horizon": horizon,
            "expected_gain": expected_gain,
            "summary_advice": advice,
            "score": score,
            "raw_ipo": ipo_res
        }
