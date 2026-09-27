import numpy as np
from cbm_brain.dataset_parser import CBMDatasetParser
from cbm_brain.math_engine import CBMValuationEngine, CBMQuantRiskEngine

class CBMIPOEngine:
    """
    Institutional IPO Evaluation Engine built on Damodaran Startup Valuation
    and Jay Ritter Empirical IPO Statistics.
    """
    
    @staticmethod
    def evaluate_ipo(
        company_name,
        sector,
        offer_price_min,
        offer_price_max,
        shares_offered,
        fresh_issue_shares,
        ofs_shares,
        pre_ipo_shares,
        annual_revenue,
        annual_growth_rate,
        operating_cash_flow,
        pre_ipo_cash,
        monthly_cash_burn=None,
        country="United States"
    ):
        parser = CBMDatasetParser.get_instance()
        bm = parser.find_industry_benchmark(sector)
        rf = parser.risk_free_rate
        erp = parser.get_country_equity_risk_premium(country)

        offer_price_mid = (offer_price_min + offer_price_max) / 2.0
        total_post_ipo_shares = pre_ipo_shares + fresh_issue_shares
        
        # Proceeds & Dilution
        fresh_proceeds = fresh_issue_shares * offer_price_mid
        ofs_proceeds = ofs_shares * offer_price_mid
        total_proceeds = shares_offered * offer_price_mid
        
        fresh_pct = (fresh_issue_shares / max(shares_offered, 1)) * 100.0
        ofs_pct = (ofs_shares / max(shares_offered, 1)) * 100.0
        
        post_money_valuation = total_post_ipo_shares * offer_price_mid
        post_ipo_cash = pre_ipo_cash + fresh_proceeds
        implied_ev = post_money_valuation - post_ipo_cash
        
        # Valuation Multiples
        implied_ev_sales = implied_ev / max(annual_revenue, 1.0)
        benchmark_ev_sales = bm.get("ev_to_sales", 3.0)
        multiple_discount_pct = ((benchmark_ev_sales - implied_ev_sales) / max(benchmark_ev_sales, 0.1)) * 100.0

        # Cash Runway
        if monthly_cash_burn is None or monthly_cash_burn <= 0:
            if operating_cash_flow < 0:
                monthly_cash_burn = abs(operating_cash_flow) / 12.0
            else:
                monthly_cash_burn = 0.0

        if monthly_cash_burn > 0:
            runway_months = post_ipo_cash / monthly_cash_burn
        else:
            runway_months = 999.0  # Self-funding / positive operating cash flow

        # Unit Economics: Rule of 40
        fcf_margin_pct = (operating_cash_flow / max(annual_revenue, 1.0)) * 100.0
        growth_pct = annual_growth_rate * 100.0
        rule_of_40_score = growth_pct + fcf_margin_pct

        # Damodaran Fast-Growth DCF Intrinsic Value
        growth_path = [annual_growth_rate, annual_growth_rate * 0.85, annual_growth_rate * 0.70, annual_growth_rate * 0.55, 0.10]
        wacc = bm.get("wacc", 0.085)
        dcf_result = CBMValuationEngine.run_dcf_model(
            current_revenue=annual_revenue,
            base_operating_margin=max(fcf_margin_pct / 100.0, -0.20),
            target_operating_margin=bm.get("operating_margin", 0.18),
            growth_rates=growth_path,
            wacc=wacc,
            tax_rate=0.21,
            sales_to_capital_ratio=1.5,
            cash_and_equivalents=post_ipo_cash,
            total_debt=0.0,
            shares_outstanding=total_post_ipo_shares,
            terminal_growth_rate=min(rf, 0.030)
        )
        
        intrinsic_val = dcf_result["intrinsic_value_per_share"]
        margin_of_safety = CBMQuantRiskEngine.calculate_margin_of_safety(offer_price_mid, intrinsic_val)

        # Jay Ritter Empirical Scorecard Logic
        score = 0
        risk_flags = []
        positive_factors = []

        # 1. Fresh vs OFS Test (Max 25 pts)
        if fresh_pct >= 70:
            score += 25
            positive_factors.append(f"Strong expansion focus: {fresh_pct:.1f}% Fresh Capital")
        elif ofs_pct > 60:
            score -= 15
            risk_flags.append(f"Heavy promoter exit: {ofs_pct:.1f}% Offer for Sale (OFS)")
        else:
            score += 10

        # 2. Runway Test (Max 25 pts)
        if runway_months >= 24:
            score += 25
            positive_factors.append(f"Safe cash runway: {runway_months:.0f} months (Self-funding/High Liquidity)")
        elif runway_months < 12:
            score -= 25
            risk_flags.append(f"Dangerously short runway: {runway_months:.0f} months")
        else:
            score += 15

        # 3. Rule of 40 Test (Max 25 pts)
        if rule_of_40_score >= 40:
            score += 25
            positive_factors.append(f"Elite Rule of 40 score: {rule_of_40_score:.1f}%")
        elif rule_of_40_score >= 20:
            score += 15
        else:
            score -= 10
            risk_flags.append(f"Weak efficiency: Rule of 40 score is only {rule_of_40_score:.1f}%")

        # 4. Valuation & Margin of Safety (Max 25 pts)
        if margin_of_safety >= 20:
            score += 25
            positive_factors.append(f"Strong Margin of Safety: +{margin_of_safety:.1f}% intrinsic DCF upside")
        elif margin_of_safety >= 0:
            score += 15
            positive_factors.append(f"Fairly priced: +{margin_of_safety:.1f}% intrinsic upside")
        else:
            score -= 20
            risk_flags.append(f"Overvalued by {abs(margin_of_safety):.1f}% relative to DCF")

        score = max(0, min(100, score))

        # Final Verdict
        if score >= 75 and margin_of_safety >= 15:
            verdict = "SUBSCRIBE (High Conviction Long-Term)"
        elif score >= 50:
            verdict = "NEUTRAL / SPECULATIVE FOR LISTING GAINS"
        else:
            verdict = "AVOID (High Risk / Overpriced / Promoter Dilution)"

        return {
            "company_name": company_name,
            "sector": sector,
            "matched_industry": bm.get("matched_industry"),
            "offer_price_range": f"${offer_price_min:.2f} - ${offer_price_max:.2f}",
            "offer_price_mid": offer_price_mid,
            "post_money_valuation": post_money_valuation,
            "fresh_pct": fresh_pct,
            "ofs_pct": ofs_pct,
            "implied_ev_sales": implied_ev_sales,
            "benchmark_ev_sales": benchmark_ev_sales,
            "multiple_discount_pct": multiple_discount_pct,
            "runway_months": runway_months,
            "rule_of_40_score": rule_of_40_score,
            "intrinsic_value_per_share": intrinsic_val,
            "margin_of_safety_pct": margin_of_safety,
            "score": score,
            "verdict": verdict,
            "positive_factors": positive_factors,
            "risk_flags": risk_flags
        }
