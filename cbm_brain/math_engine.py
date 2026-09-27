import numpy as np

class CBMValuationEngine:
    """
    Deterministic Valuation Engine implementing Damodaran, McKinsey, and Graham & Dodd.
    Zero LLM Math Hallucination.
    """
    
    @staticmethod
    def calculate_wacc(cost_of_equity, pre_tax_cost_of_debt, tax_rate, equity_value, debt_value):
        total_cap = equity_value + debt_value
        if total_cap <= 0:
            return cost_of_equity
        we = equity_value / total_cap
        wd = debt_value / total_cap
        after_tax_cod = pre_tax_cost_of_debt * (1 - tax_rate)
        return (we * cost_of_equity) + (wd * after_tax_cod)

    @staticmethod
    def calculate_cost_of_equity(risk_free_rate, beta, equity_risk_premium):
        return risk_free_rate + (beta * equity_risk_premium)

    @staticmethod
    def run_dcf_model(
        current_revenue,
        base_operating_margin,
        target_operating_margin,
        growth_rates,
        wacc,
        tax_rate,
        sales_to_capital_ratio,
        cash_and_equivalents,
        total_debt,
        shares_outstanding,
        terminal_growth_rate=0.030,
        terminal_roic=None
    ):
        """
        Damodaran Multi-Stage Free Cash Flow to Firm (FCFF) DCF Model.
        """
        if terminal_roic is None:
            terminal_roic = wacc  # In long-run, competitive forces push ROIC toward WACC

        # Enforce Damodaran boundary rule: terminal growth cannot exceed risk-free rate proxy
        terminal_growth_rate = min(terminal_growth_rate, 0.040)
        
        years = len(growth_rates)
        revenues = []
        ebit_list = []
        nopat_list = []
        reinvestment_list = []
        fcff_list = []
        pv_fcff_list = []

        rev = current_revenue
        for yr, g in enumerate(growth_rates, start=1):
            rev = rev * (1 + g)
            revenues.append(rev)
            
            # Linearly transition operating margin to target margin
            current_margin = base_operating_margin + (target_operating_margin - base_operating_margin) * (yr / years)
            ebit = rev * current_margin
            ebit_list.append(ebit)
            
            nopat = ebit * (1 - tax_rate)
            nopat_list.append(nopat)
            
            # Reinvestment = delta Revenue / (Sales to Capital Ratio)
            delta_rev = rev - (revenues[-2] if yr > 1 else current_revenue)
            reinvestment = delta_rev / max(sales_to_capital_ratio, 0.5)
            reinvestment_list.append(reinvestment)
            
            fcff = nopat - reinvestment
            fcff_list.append(fcff)
            
            pv = fcff / ((1 + wacc) ** yr)
            pv_fcff_list.append(pv)

        # Terminal Year calculations
        terminal_rev = revenues[-1] * (1 + terminal_growth_rate)
        terminal_ebit = terminal_rev * target_operating_margin
        terminal_nopat = terminal_ebit * (1 - tax_rate)
        
        # Damodaran Terminal Reinvestment Rate = g / ROIC
        terminal_reinvestment_rate = terminal_growth_rate / max(terminal_roic, 0.05)
        terminal_reinvestment = terminal_nopat * terminal_reinvestment_rate
        terminal_fcff = terminal_nopat - terminal_reinvestment
        
        # Terminal Value
        terminal_wacc = max(wacc - 0.005, terminal_growth_rate + 0.01) # Slight convergence
        terminal_value = terminal_fcff / (terminal_wacc - terminal_growth_rate)
        pv_terminal_value = terminal_value / ((1 + wacc) ** years)

        enterprise_value = sum(pv_fcff_list) + pv_terminal_value
        equity_value = enterprise_value + cash_and_equivalents - total_debt
        intrinsic_value_per_share = equity_value / max(shares_outstanding, 1)

        return {
            "enterprise_value": float(enterprise_value),
            "equity_value": float(equity_value),
            "intrinsic_value_per_share": float(intrinsic_value_per_share),
            "pv_operating_cash_flows": float(sum(pv_fcff_list)),
            "pv_terminal_value": float(pv_terminal_value),
            "terminal_value_share_pct": float((pv_terminal_value / max(enterprise_value, 1)) * 100),
            "projected_fcff": [float(x) for x in fcff_list]
        }

    @staticmethod
    def calculate_mckinsey_value(nopat_next_year, growth_rate, roic, wacc):
        """
        McKinsey Key Value Driver Formula:
        Value = [NOPAT * (1 - g/ROIC)] / (WACC - g)
        """
        if wacc <= growth_rate:
            return 0.0
        reinvestment_rate = growth_rate / max(roic, 0.01)
        free_cash_flow = nopat_next_year * (1 - reinvestment_rate)
        return free_cash_flow / (wacc - growth_rate)

    @staticmethod
    def calculate_graham_net_net(current_assets, total_liabilities, shares_outstanding):
        ncav = current_assets - total_liabilities
        ncav_per_share = ncav / max(shares_outstanding, 1)
        return {
            "ncav_total": float(ncav),
            "ncav_per_share": float(ncav_per_share),
            "is_net_net": ncav_per_share > 0
        }


class CBMForensicsEngine:
    """
    Forensic Auditing Engine implementing Beneish M-Score, Altman Z-Score,
    Piotroski F-Score, and Sloan Accrual Anomaly.
    """

    @staticmethod
    def calculate_altman_z_score(working_capital, retained_earnings, ebit, market_equity, total_liabilities, total_assets, revenue, is_manufacturing=False):
        if total_assets <= 0:
            return {"z_score": 0.0, "zone": "Unknown"}
            
        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = market_equity / max(total_liabilities, 1.0)
        x5 = revenue / total_assets
        
        if is_manufacturing:
            z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5
            safe_thresh, distress_thresh = 2.99, 1.81
        else:
            # Altman Z-Double-Prime for services/tech/general
            z = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
            safe_thresh, distress_thresh = 2.60, 1.10
            
        if z >= safe_thresh:
            zone = "SAFE (Low Insolvency Risk)"
        elif z <= distress_thresh:
            zone = "DISTRESS (High Insolvency Risk)"
        else:
            zone = "GREY ZONE (Moderate Risk)"
            
        return {
            "z_score": float(round(z, 2)),
            "zone": zone,
            "components": {"x1_liquidity": round(x1, 3), "x2_reinvested_profits": round(x2, 3), "x3_operating_efficiency": round(x3, 3), "x4_leverage": round(x4, 3)}
        }

    @staticmethod
    def calculate_beneish_m_score(dsri=1.0, gmi=1.0, aqi=1.0, sgi=1.0, depi=1.0, sgai=1.0, lvgi=1.0, tata=0.0):
        """
        Beneish 8-variable manipulation detector.
        M-Score > -1.78 indicates high probability of accounting manipulation.
        """
        m = -4.84 + (0.920 * dsri) + (0.528 * gmi) + (0.404 * aqi) + (0.892 * sgi) + (0.115 * depi) - (0.172 * sgai) + (4.037 * tata) + (0.0327 * lvgi)
        is_manipulator = m > -1.78
        return {
            "m_score": float(round(m, 2)),
            "manipulation_risk": "HIGH (Earnings Manipulation Flagged)" if is_manipulator else "LOW (Unlikely Manipulator)",
            "threshold": -1.78
        }

    @staticmethod
    def calculate_piotroski_f_score(
        net_income_positive,
        operating_cf_positive,
        roa_increasing,
        cf_greater_than_ni,
        leverage_decreasing,
        current_ratio_increasing,
        no_dilution_shares,
        gross_margin_increasing,
        asset_turnover_increasing
    ):
        points = [
            int(net_income_positive),
            int(operating_cf_positive),
            int(roa_increasing),
            int(cf_greater_than_ni),
            int(leverage_decreasing),
            int(current_ratio_increasing),
            int(no_dilution_shares),
            int(gross_margin_increasing),
            int(asset_turnover_increasing)
        ]
        score = sum(points)
        if score >= 8:
            rating = "ELITE (Strong Financial Health)"
        elif score >= 5:
            rating = "AVERAGE (Stable Profile)"
        else:
            rating = "WEAK (Fundamental Deterioration)"
        return {"f_score": score, "rating": rating, "max_score": 9}

    @staticmethod
    def calculate_sloan_accrual(net_income, operating_cash_flow, total_assets):
        if total_assets <= 0:
            return 0.0
        accrual_ratio = (net_income - operating_cash_flow) / total_assets
        return {
            "accrual_ratio": float(round(accrual_ratio, 4)),
            "quality_rating": "HIGH CASH QUALITY" if accrual_ratio < 0.05 else "LOW QUALITY ACCRUAL HEAVY"
        }


class CBMQuantRiskEngine:
    """
    López de Prado & Ed Thorp Quantitative Position Sizing & Margin of Safety.
    """
    
    @staticmethod
    def calculate_margin_of_safety(current_price, intrinsic_value):
        if current_price <= 0:
            return 0.0
        mos_pct = ((intrinsic_value - current_price) / current_price) * 100.0
        return float(round(mos_pct, 2))

    @staticmethod
    def calculate_kelly_fraction(win_probability, win_loss_ratio, max_allocation=0.25):
        """
        Half-Kelly Criterion for risk management.
        f* = (p*b - q) / b
        """
        p = win_probability
        q = 1.0 - p
        b = win_loss_ratio
        if b <= 0:
            return 0.0
        full_kelly = (p * b - q) / b
        half_kelly = max(0.0, full_kelly * 0.5)
        return float(round(min(half_kelly, max_allocation), 4))
