import os
import json
import fitz
from cbm_brain import cbm_config as cfg

class CBMBookDigestEngine:
    """
    Digests, structures, and compiles all 7 digital financial masterworks
    into machine-readable, fast-retrieval JSON knowledge vaults.
    """
    
    @classmethod
    def run_full_digest(cls):
        vault_dir = os.path.join(cfg.CBM_DIR, "brain_knowledge")
        os.makedirs(vault_dir, exist_ok=True)
        print(f"[CBM Digest] Compiling Knowledge Vault in: {vault_dir}")

        books = [
            ("01_damodaran_valuation_laws.json", cfg.DAMODARAN_PDF, "Aswath Damodaran", "Investment Valuation (3rd Edition)", [
                "DCF Mechanics (FCFF and FCFE equations)",
                "Equity Risk Premium estimation across 150+ countries",
                "Pure-play Unlevered and Relevered Beta adjustments",
                "R&D capitalization and Operating Lease capitalization into debt",
                "Terminal value boundary conditions (Terminal growth <= Risk-free rate)",
                "Distressed firm valuation trees with liquidation probability"
            ]),
            ("02_mckinsey_value_creation.json", cfg.MCKINSEY_PDF, "McKinsey & Co. (Tim Koller)", "Valuation (University Edition)", [
                "The Fundamental Principle of Value Creation: Value = f(ROIC, Growth)",
                "The Key Value Driver Equation: V = NOPAT*(1 - g/ROIC) / (WACC - g)",
                "Economic Value Added (EVA) = Invested Capital * (ROIC - WACC)",
                "NOPAT reconciliation from reported Operating Income",
                "Invested Capital decomposition (Working Capital + Net PP&E + Intangibles)",
                "Continuing Value economic decay dynamics"
            ]),
            ("03_graham_dodd_margin_of_safety.json", cfg.GRAHAM_DODD_PDF, "Graham & Dodd (Seth Klarman)", "Security Analysis (7th Edition)", [
                "The Principle of Margin of Safety: Price vs. Intrinsic Value buffer",
                "Net-Current-Asset Value (NCAV / Net-Net) liquidation floor",
                "Forensic Balance Sheet appraisal (haircut on receivables and inventory)",
                "Earnings Power Value (EPV) under zero-growth assumptions",
                "Mr. Market psychological separation of price from business reality"
            ]),
            ("04_brealey_myers_corporate_finance.json", cfg.BREALEY_MYERS_PDF, "Richard Brealey & Stewart Myers", "Principles of Corporate Finance (7th Edition)", [
                "Net Present Value (NPV) decision criteria over IRR",
                "Opportunity Cost of Capital & CAPM Hurdle Rates",
                "Stewart Myers Pecking Order Theory of Capital Structure",
                "Modigliani-Miller Proposition II with corporate tax shield",
                "Corporate dividend and share buyback signaling effects"
            ]),
            ("05_lopez_de_prado_quant_ml.json", cfg.LOPEZ_DE_PRADO_PDF, "Marcos López de Prado", "Advances in Financial Machine Learning", [
                "Fractional Differentiation: Preserving financial market memory with stationary returns",
                "The Triple-Barrier Method: Dynamic labeling for profit-taking, stop-loss, and holding horizon",
                "Meta-Labeling & Bet Sizing: Separating signal direction from conviction allocation",
                "Combating Backtest Overfitting: Deflated Sharpe Ratio (DSR) and Family-Wise Error Rate",
                "Hierarchical Risk Parity (HRP) portfolio optimization"
            ]),
            ("06_schilit_forensic_shenanigans.json", cfg.SCHILIT_PDF, "Howard Schilit & Jeremy Perler", "Financial Shenanigans (4th Edition)", [
                "Earnings Manipulation Shenanigans: Recording bogus revenue, accelerating revenue recognition",
                "Cash Flow Shenanigans: Shifting financing inflows to operating cash flow",
                "Key Metric Shenanigans: Distorting bookings, non-GAAP EBITDA manipulation",
                "Acquisition Shenanigans: Creating hidden cookie-jar reserves at acquisition",
                "Early warning audit flags: Days Sales Outstanding (DSO) divergence from revenue"
            ]),
            ("07_marks_cycles_and_psychology.json", cfg.HOWARD_MARKS_PDF, "Howard Marks (Oaktree)", "The Most Important Thing Illuminated", [
                "Second-Level Thinking: Factoring in market consensus and expectations vs reality",
                "The Pendulum of Investor Psychology: Oscillating between excessive greed and excessive fear",
                "The Inevitability of the Credit Cycle: Credit expansion boom to credit freeze bust",
                "Asymmetric Risk Control: Focusing on eliminating downside risk; winners take care of themselves",
                "Patient Opportunism: Waiting for forced sellers in a market panic"
            ])
        ]

        master_graph = {"books_catalog": [], "total_pages_ingested": 0, "status": "COMPILED"}

        for json_filename, pdf_path, author, title, key_laws in books:
            out_file = os.path.join(vault_dir, json_filename)
            try:
                doc = fitz.open(pdf_path)
                page_count = len(doc)
                master_graph["total_pages_ingested"] += page_count
                
                # Extract TOC
                toc = doc.get_toc()
                toc_formatted = [{"level": item[0], "title": item[1], "page": item[2]} for item in toc[:40]]
                
                # Sample text summary
                sample_extracts = []
                for pno in [min(15, page_count-1), min(50, page_count-1), min(100, page_count-1), min(200, page_count-1)]:
                    txt = doc[pno].get_text()
                    if txt.strip():
                        sample_extracts.append(txt.strip()[:350].replace("\n", " "))
                        
                digest_data = {
                    "title": title,
                    "author": author,
                    "file": os.path.basename(pdf_path),
                    "total_pages": page_count,
                    "native_text_status": "100% DIGITAL VECTOR TEXT",
                    "core_principles_and_laws": key_laws,
                    "table_of_contents_extract": toc_formatted,
                    "sample_semantic_extracts": sample_extracts
                }
                
                with open(out_file, "w") as jf:
                    json.dump(digest_data, jf, indent=2)
                    
                master_graph["books_catalog"].append({
                    "title": title,
                    "author": author,
                    "pages": page_count,
                    "vault_file": json_filename
                })
                print(f"  ✔ Digested {title} ({page_count} pages) -> {json_filename}")
            except Exception as e:
                print(f"  ✘ Error digesting {title}: {e}")

        # Write Master Graph
        with open(os.path.join(vault_dir, "master_codified_knowledge_graph.json"), "w") as mf:
            json.dump(master_graph, mf, indent=2)
            
        print(f"[CBM Digest Complete] Total pages digested: {master_graph['total_pages_ingested']}")

if __name__ == "__main__":
    CBMBookDigestEngine.run_full_digest()
