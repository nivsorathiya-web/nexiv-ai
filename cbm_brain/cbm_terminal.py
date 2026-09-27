import argparse
import sys
from cbm_brain.agent_council import CBMAgentCouncil
from cbm_brain.ipo_engine import CBMIPOEngine

def print_header(title):
    print("=" * 82)
    print("  " + title)
    print("=" * 82)

def print_section(title):
    print()
    print("-" * 82)
    print(">> " + title)
    print("-" * 82)

def display_stock_report(analysis):
    p = analysis["profile"]
    bm = analysis["benchmark"]
    f = analysis["forensics"]
    v = analysis["valuation"]
    r = analysis["risk_and_sizing"]
    dcf = v["dcf"]

    sym = p["symbol"]
    cname = p["company_name"]
    print_header("CBM INSTITUTIONAL VALUATION & FORENSIC AUDIT: " + sym + " (" + cname + ")")
    
    sec = p["sector"]
    ind = p["industry"]
    cntry = p["country"]
    print("Sector: %s | Industry: %s | Country: %s" % (sec, ind, cntry))
    
    price = p["current_price"]
    mcap_b = p["market_cap"] / 1e9
    beta = p["beta"]
    print("Current Price: $%.2f | Market Cap: $%.2fB | Beta: %.2f" % (price, mcap_b, beta))
    
    rev_b = p["revenue"] / 1e9
    ebit_b = p["ebit"] / 1e9
    fcf_b = p["free_cash_flow"] / 1e9
    print("Revenue (TTM): $%.2fB | EBIT: $%.2fB | Free Cash Flow: $%.2fB" % (rev_b, ebit_b, fcf_b))

    print_section("1. FORENSIC AUDIT & SHENANIGANS DETECTION (Schilit, Beneish & Altman)")
    z = f["altman_z"]
    m = f["beneish_m"]
    piot = f["piotroski_f"]
    sloan = f["sloan_accrual"]
    
    print("• Altman Z-Score:      %.2f  -->  %s" % (z["z_score"], z["zone"]))
    print("• Beneish M-Score:     %.2f (Threshold: -1.78)  -->  %s" % (m["m_score"], m["manipulation_risk"]))
    print("• Piotroski F-Score:   %d/%d  -->  %s" % (piot["f_score"], piot["max_score"], piot["rating"]))
    print("• Sloan Accrual Ratio: %.4f  -->  %s" % (sloan["accrual_ratio"], sloan["quality_rating"]))

    print_section("2. DETERMINISTIC VALUATION & CASH FLOW MODEL (Damodaran & McKinsey)")
    wacc_pct = v["wacc"] * 100.0
    coe_pct = v["cost_of_equity"] * 100.0
    print("• Calibrated WACC:            %.2f%% (Cost of Equity: %.2f%%)" % (wacc_pct, coe_pct))
    
    bm_wacc = bm.get("wacc", 0.08) * 100.0
    bm_ev_ebitda = bm.get("ev_to_ebitda", 15.0)
    print("• NYU Stern Benchmark WACC:   %.2f%% | EV/EBITDA: %.1fx" % (bm_wacc, bm_ev_ebitda))
    
    ev_b = dcf["enterprise_value"] / 1e9
    tv_pct = dcf["terminal_value_share_pct"]
    print("• Enterprise Value (PV DCF):  $%.2f Billion" % ev_b)
    print("• Terminal Value Share:       %.1f%% of Enterprise Value" % tv_pct)
    
    net_cash_b = (p["cash"] - p["total_debt"]) / 1e9
    eq_b = dcf["equity_value"] / 1e9
    iv = dcf["intrinsic_value_per_share"]
    print("• Net Cash / (Debt) Bridge:   $%.2f Billion" % net_cash_b)
    print("• Equity Value:               $%.2f Billion" % eq_b)
    print("• INTRINSIC VALUE PER SHARE:  $%.2f" % iv)
    
    mos = v["margin_of_safety_pct"]
    mos_sign = "+" if mos > 0 else ""
    print("• MARGIN OF SAFETY:           %s%.2f%% relative to market price ($%.2f)" % (mos_sign, mos, price))

    print_section("3. CIO EXECUTIVE VERDICT & QUANTITATIVE POSITION SIZING (Buffett, Marks & Thorp)")
    print("★ FINAL CIO VERDICT:          %s" % r["verdict"])
    print("★ KELLY CRITERION SIZING:     %.1f%% Maximum Capital Allocation" % r["recommended_kelly_allocation_pct"])
    print("• Graham Net-Net Floor:       $%.2f per share (Liquidation Floor)" % r["downside_liquidation_floor"])
    print("=" * 82 + "\n")

def display_ipo_report(ipo):
    print_header("CBM INSTITUTIONAL IPO INTELLIGENCE SCORECARD: " + ipo["company_name"])
    print("Sector: %s (Matched Benchmark: %s)" % (ipo["sector"], str(ipo.get("matched_industry"))))
    print("Offer Price Range: %s (Mid-Point: $%.2f)" % (ipo["offer_price_range"], ipo["offer_price_mid"]))
    post_b = ipo["post_money_valuation"] / 1e9
    print("Implied Post-Money Valuation: $%.2f Billion" % post_b)

    print_section("1. OFFER CAPITAL ALLOCATION & DILUTION (Jay Ritter Metrics)")
    print("• Fresh Issue (Company Growth): %.1f%%" % ipo["fresh_pct"])
    print("• Offer for Sale (Promoter Exit): %.1f%%" % ipo["ofs_pct"])

    print_section("2. UNIT ECONOMICS & CASH RUNWAY (Damodaran Startup Framework)")
    print("• Rule of 40 Score:             %.1f%%" % ipo["rule_of_40_score"])
    runway_str = ("%.0f Months" % ipo["runway_months"]) if ipo["runway_months"] < 900 else "Positive Cash Flow (Self-Funding)"
    print("• Post-IPO Cash Runway:         %s" % runway_str)
    print("• Implied EV / Sales Multiple:  %.2fx (Industry Benchmark: %.2fx)" % (ipo["implied_ev_sales"], ipo["benchmark_ev_sales"]))

    print_section("3. INTRINSIC VALUATION & DECISION MATRIX")
    print("• Damodaran DCF Fair Value:     $%.2f per share" % ipo["intrinsic_value_per_share"])
    mos = ipo["margin_of_safety_pct"]
    mos_sign = "+" if mos > 0 else ""
    print("• Margin of Safety:             %s%.1f%%" % (mos_sign, mos))
    print("• Institutional Score:          %d/100" % ipo["score"])
    print("★ FINAL IPO VERDICT:            %s" % ipo["verdict"])

    if ipo["positive_factors"]:
        print("\n[+] Positive Catalysts:")
        for factor in ipo["positive_factors"]:
            print("    ✔ " + str(factor))
    if ipo["risk_flags"]:
        print("\n[-] Risk Flags:")
        for risk in ipo["risk_flags"]:
            print("    ✘ " + str(risk))
    print("=" * 82 + "\n")

def main():
    parser = argparse.ArgumentParser(description="CBM Autonomous Institutional Financial Intelligence Brain")
    parser.add_argument("--ticker", "-t", type=str, help="Stock ticker symbol (e.g., AAPL, NVDA, TSLA, MSFT, RELIANCE.NS)")
    parser.add_argument("--ipo", action="store_true", help="Launch interactive IPO evaluation scanner")
    parser.add_argument("--sample-ipo", action="store_true", help="Run a sample high-growth IPO evaluation")
    args = parser.parse_args()

    if args.ticker:
        print("\n[CBM Brain] Fetching real-time market data and financial statements for " + args.ticker.upper() + "...")
        try:
            analysis = CBMAgentCouncil.analyze_ticker(args.ticker)
            display_stock_report(analysis)
        except Exception as e:
            print("[Error] Failed to analyze ticker %s: %s" % (args.ticker, e))
            sys.exit(1)
    elif args.sample_ipo:
        print("\n[CBM Brain] Running Institutional IPO Intelligence Engine on Sample Tech IPO...")
        ipo_res = CBMIPOEngine.evaluate_ipo(
            company_name="ApexAI Cloud Technologies",
            sector="Software",
            offer_price_min=28.0,
            offer_price_max=32.0,
            shares_offered=25_000_000,
            fresh_issue_shares=20_000_000,
            ofs_shares=5_000_000,
            pre_ipo_shares=100_000_000,
            annual_revenue=420_000_000,
            annual_growth_rate=0.48,
            operating_cash_flow=55_000_000,
            pre_ipo_cash=150_000_000
        )
        display_ipo_report(ipo_res)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
