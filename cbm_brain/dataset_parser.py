import os
import pandas as pd
import numpy as np
from cbm_brain import cbm_config as cfg

class CBMDatasetParser:
    _instance = None
    
    def __init__(self):
        self.wacc_df = None
        self.margins_df = None
        self.multiples_df = None
        self.capex_df = None
        self.erp_df = None
        self.risk_free_rate = cfg.DEFAULT_RISK_FREE_RATE
        self._load_all()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CBMDatasetParser()
        return cls._instance

    def _load_all(self):
        self._load_wacc()
        self._load_margins()
        self._load_multiples()
        self._load_capex()
        self._load_erp()
        self._load_fred_rate()

    def _clean_industry_name(self, series):
        return series.astype(str).str.strip().str.lower()

    def _load_wacc(self):
        try:
            xl = pd.ExcelFile(cfg.WACC_DATASET)
            df = xl.parse("Industry Averages", header=18)
            df = df.dropna(subset=["Industry Name"])
            df = df[~df["Industry Name"].astype(str).str.contains("Total|Average", case=False, na=False)]
            df["key"] = self._clean_industry_name(df["Industry Name"])
            self.wacc_df = df
        except Exception as e:
            print(f"[Warning] Failed to parse WACC dataset: {e}")

    def _load_margins(self):
        try:
            xl = pd.ExcelFile(cfg.MARGIN_DATASET)
            df = xl.parse("Industry Averages", header=8)
            df = df.dropna(subset=["Industry Name"])
            df = df[~df["Industry Name"].astype(str).str.contains("Total|Average", case=False, na=False)]
            df["key"] = self._clean_industry_name(df["Industry Name"])
            self.margins_df = df
        except Exception as e:
            print(f"[Warning] Failed to parse Margins dataset: {e}")

    def _load_multiples(self):
        try:
            xl = pd.ExcelFile(cfg.MULTIPLES_DATASET)
            df = xl.parse("Industry Averages", header=8)
            df = df.dropna(subset=["Industry Name"])
            df = df[~df["Industry Name"].astype(str).str.contains("Total|Average", case=False, na=False)]
            df["key"] = self._clean_industry_name(df["Industry Name"])
            self.multiples_df = df
        except Exception as e:
            print(f"[Warning] Failed to parse Multiples dataset: {e}")

    def _load_capex(self):
        try:
            xl = pd.ExcelFile(cfg.CAPEX_DATASET)
            df = xl.parse("Industry Averages", header=7)
            df = df.dropna(subset=["Industry Name"])
            df = df[~df["Industry Name"].astype(str).str.contains("Total|Average", case=False, na=False)]
            df["key"] = self._clean_industry_name(df["Industry Name"])
            self.capex_df = df
        except Exception as e:
            print(f"[Warning] Failed to parse CapEx dataset: {e}")

    def _load_erp(self):
        try:
            xl = pd.ExcelFile(cfg.ERP_DATASET)
            # Find the sheet with countries
            target_sheet = "ERPs by country" if "ERPs by country" in xl.sheet_names else xl.sheet_names[0]
            df = xl.parse(target_sheet, header=7)
            if "Country" in df.columns:
                df = df.dropna(subset=["Country"])
                df["key"] = df["Country"].astype(str).str.strip().str.lower()
                self.erp_df = df
        except Exception as e:
            print(f"[Warning] Failed to parse ERP dataset: {e}")

    def _load_fred_rate(self):
        try:
            df = pd.read_csv(cfg.FRED_10Y_DATASET)
            valid = df[df["DGS10"] != "."]["DGS10"].astype(float)
            if len(valid) > 0:
                self.risk_free_rate = valid.iloc[-1] / 100.0
        except Exception as e:
            print(f"[Warning] Using default risk-free rate: {e}")

    def find_industry_benchmark(self, sector_query):
        q = str(sector_query).strip().lower()
        res = {
            "query": sector_query,
            "matched_industry": None,
            "beta": 1.0,
            "cost_of_equity": 0.09,
            "wacc": 0.08,
            "debt_to_capital": 0.20,
            "gross_margin": 0.40,
            "operating_margin": 0.15,
            "net_margin": 0.10,
            "ev_to_ebitda": 14.0,
            "ev_to_sales": 2.5,
            "pe_ratio": 22.0
        }
        
        if self.wacc_df is not None:
            matches = self.wacc_df[self.wacc_df["key"].str.contains(q, na=False)]
            if len(matches) == 0:
                # try matching individual words
                words = q.split()
                for w in words:
                    if len(w) > 3:
                        matches = self.wacc_df[self.wacc_df["key"].str.contains(w, na=False)]
                        if len(matches) > 0:
                            break
            if len(matches) > 0:
                row = matches.iloc[0]
                res["matched_industry"] = str(row["Industry Name"])
                res["beta"] = float(row.get("Beta", 1.0))
                res["cost_of_equity"] = float(row.get("Cost of Equity", 0.09))
                res["wacc"] = float(row.get("Cost of Capital", 0.08))
                res["debt_to_capital"] = float(row.get("D/(D+E)", 0.20))
                
        # Merge margins
        if self.margins_df is not None and res["matched_industry"]:
            m_match = self.margins_df[self.margins_df["key"] == res["matched_industry"].lower()]
            if len(m_match) > 0:
                m_row = m_match.iloc[0]
                # Damodaran margins columns
                for col in m_match.columns:
                    cl = col.lower()
                    if "gross margin" in cl and pd.notna(m_row[col]):
                        res["gross_margin"] = float(m_row[col])
                    elif "operating margin" in cl and pd.notna(m_row[col]):
                        res["operating_margin"] = float(m_row[col])
                    elif "net margin" in cl and pd.notna(m_row[col]):
                        res["net_margin"] = float(m_row[col])
                        
        # Merge multiples
        if self.multiples_df is not None and res["matched_industry"]:
            mul_match = self.multiples_df[self.multiples_df["key"] == res["matched_industry"].lower()]
            if len(mul_match) > 0:
                mul_row = mul_match.iloc[0]
                for col in mul_match.columns:
                    cl = col.lower()
                    if "ev/ebitda" in cl and pd.notna(mul_row[col]):
                        try: res["ev_to_ebitda"] = float(mul_row[col])
                        except: pass
                    elif "ev/sales" in cl and pd.notna(mul_row[col]):
                        try: res["ev_to_sales"] = float(mul_row[col])
                        except: pass
                    elif "pe" in cl and pd.notna(mul_row[col]):
                        try: res["pe_ratio"] = float(mul_row[col])
                        except: pass
                        
        return res

    def get_country_equity_risk_premium(self, country_name="United States"):
        c = str(country_name).strip().lower()
        if self.erp_df is not None:
            match = self.erp_df[self.erp_df["key"].str.contains(c, na=False)]
            if len(match) > 0:
                row = match.iloc[0]
                for col in match.columns:
                    if "total equity risk premium" in col.lower() or "erp" in col.lower():
                        val = row[col]
                        try:
                            return float(val)
                        except:
                            pass
        return cfg.DEFAULT_MATURE_ERP
