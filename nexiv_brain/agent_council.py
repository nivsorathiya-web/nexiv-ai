import numpy as np
from nexiv_brain.dataset_parser import CBMDatasetParser
from nexiv_brain.math_engine import CBMValuationEngine, CBMForensicsEngine, CBMQuantRiskEngine
from nexiv_brain.market_data import CBMMarketDataProvider

class CBMAgentCouncil:
    """
    Autonomous Multi-Agent Council combining:
    - Forensic Auditor (Schilit & Beneish)
    - Valuation Architect (Damodaran & McKinsey)
    - Cycle & Macro Strategist (Marks & Dalio)
    - Chief Investment Officer (Buffett, Thorp & López de Prado)
    """
    
    @classmethod
    def analyze_ticker(cls, ticker_symbol):
        profile = CBMMarketDataProvider.get_stock_profile(ticker_symbol)
        parser = CBMDatasetParser.get_instance()
        bm = parser.find_industry_benchmark(profile["sector"] + " " + profile["industry"])
        rf = parser.risk_free_rate
        erp = parser.get_country_equity_risk_premium(profile["country"])

        # 1. Forensic Audit
        z_res = CBMForensicsEngine.calculate_altman_z_score(
            working_capital=profile["working_capital"],
            retained_earnings=profile["retained_earnings"],
            ebit=profile["ebit"],
            market_equity=profile["market_cap"],
            total_liabilities=profile["total_liabilities"],
            total_assets=profile["total_assets"],
            revenue=profile["revenue"]
        )
        
        # Beneish M-Score estimation
        dsri = 1.05
        gmi = 1.02
        aqi = 1.00
        sgi = max(0.5, 1.0 + profile["revenue_cagr_3yr"])
        depi = 1.00
        sgai = 1.00
        lvgi = profile["total_liabilities"] / max(profile["total_assets"], 1.0)
        tata = (profile["net_income"] - profile["operating_cf"]) / max(profile["total_assets"], 1.0)
        
        m_res = CBMForensicsEngine.calculate_beneish_m_score(dsri, gmi, aqi, sgi, depi, sgai, lvgi, tata)
        sloan_res = CBMForensicsEngine.calculate_sloan_accrual(profile["net_income"], profile["operating_cf"], profile["total_assets"])
        
        # Piotroski F-Score estimate
        f_res = CBMForensicsEngine.calculate_piotroski_f_score(
            net_income_positive=profile["net_income"] > 0,
            operating_cf_positive=profile["operating_cf"] > 0,
            roa_increasing=True,
            cf_greater_than_ni=profile["operating_cf"] >= profile["net_income"],
            leverage_decreasing=profile["total_debt"] < profile["total_assets"] * 0.4,
            current_ratio_increasing=profile["current_assets"] > profile["current_liabilities"],
            no_dilution_shares=True,
            gross_margin_increasing=True,
            asset_turnover_increasing=True
        )

        # 2. Valuation Architecture
        cost_of_equity = CBMValuationEngine.calculate_cost_of_equity(rf, profile["beta"], erp)
        pre_tax_cod = rf + 0.015  # Benchmark default spread
        wacc = CBMValuationEngine.calculate_wacc(
            cost_of_equity=cost_of_equity,
            pre_tax_cost_of_debt=pre_tax_cod,
            tax_rate=0.21,
            equity_value=profile["market_cap"],
            debt_value=profile["total_debt"]
        )

        # DCF Projections
        current_margin = profile["ebit"] / max(profile["revenue"], 1.0)
        target_margin = max(current_margin, bm.get("operating_margin", 0.18))
        growth_rates = [
            max(0.04, min(profile["revenue_cagr_3yr"], 0.25)),
            max(0.04, min(profile["revenue_cagr_3yr"] * 0.85, 0.20)),
            max(0.03, min(profile["revenue_cagr_3yr"] * 0.70, 0.15)),
            max(0.03, min(profile["revenue_cagr_3yr"] * 0.55, 0.10)),
            0.05
        ]
        
        dcf = CBMValuationEngine.run_dcf_model(
            current_revenue=profile["revenue"],
            base_operating_margin=current_margin,
            target_operating_margin=target_margin,
            growth_rates=growth_rates,
            wacc=wacc,
            tax_rate=0.21,
            sales_to_capital_ratio=2.0,
            cash_and_equivalents=profile["cash"],
            total_debt=profile["total_debt"],
            shares_outstanding=profile["shares_outstanding"],
            terminal_growth_rate=min(rf, 0.030)
        )

        # Graham Net-Net Floor
        graham = CBMValuationEngine.calculate_graham_net_net(
            current_assets=profile["current_assets"],
            total_liabilities=profile["total_liabilities"],
            shares_outstanding=profile["shares_outstanding"]
        )

        # Margin of Safety & Sizing
        intrinsic_val = dcf["intrinsic_value_per_share"]
        current_price = profile["current_price"]
        mos = CBMQuantRiskEngine.calculate_margin_of_safety(current_price, intrinsic_val)
        
        # Kelly Sizing
        win_prob = 0.65 if mos > 15 and z_res["zone"].startswith("SAFE") else 0.50
        win_loss = 2.0 if mos > 25 else 1.2
        kelly_alloc = CBMQuantRiskEngine.calculate_kelly_fraction(win_prob, win_loss, max_allocation=0.20)

        # CIO Decision Logic
        if mos >= 20 and z_res["zone"].startswith("SAFE") and m_res["m_score"] <= -1.78:
            verdict = "STRONG BUY (Substantial Margin of Safety & Clean Financials)"
        elif mos >= 5 and not z_res["zone"].startswith("DISTRESS"):
            verdict = "ACCUMULATE / BUY (Fair Value Compounder)"
        elif mos >= -15 and not z_res["zone"].startswith("DISTRESS"):
            verdict = "HOLD / FAIRLY VALUED (High Quality, Await Pullback)"
        else:
            verdict = "AVOID / OVERVALUED (Negative Margin of Safety or Elevated Risk)"

        return {
            "profile": profile,
            "benchmark": bm,
            "forensics": {
                "altman_z": z_res,
                "beneish_m": m_res,
                "piotroski_f": f_res,
                "sloan_accrual": sloan_res
            },
            "valuation": {
                "wacc": wacc,
                "cost_of_equity": cost_of_equity,
                "dcf": dcf,
                "graham_ncav": graham,
                "margin_of_safety_pct": mos
            },
            "risk_and_sizing": {
                "recommended_kelly_allocation_pct": kelly_alloc * 100.0,
                "downside_liquidation_floor": graham["ncav_per_share"],
                "verdict": verdict
            }
        }
