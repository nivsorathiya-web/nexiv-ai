import os
import json
from nexiv_brain import nexiv_config as cfg

class CBMDatasetParser:
    _instance = None
    
    def __init__(self):
        self.data = {"sectors": {}, "countries": {}, "macro": {}}
        self.risk_free_rate = cfg.DEFAULT_US_RISK_FREE
        self._load_compiled_data()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CBMDatasetParser()
        return cls._instance

    def _load_compiled_data(self):
        if os.path.exists(cfg.COMPILED_SECTOR_DATA):
            try:
                with open(cfg.COMPILED_SECTOR_DATA, "r") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"[Nexiv] Could not read compiled data: {e}")
                
    def find_industry_benchmark(self, sector_query):
        q = str(sector_query).strip().lower()
        res = {
            "query": sector_query,
            "matched_industry": None,
            "beta": 1.0,
            "cost_of_equity": 0.09,
            "wacc": 0.085,
            "debt_to_capital": 0.20,
            "gross_margin": 0.40,
            "operating_margin": 0.15,
            "net_margin": 0.10,
            "ev_to_ebitda": 14.0,
            "ev_to_sales": 2.5,
            "pe_ratio": 22.0
        }
        
        sectors = self.data.get("sectors", {})
        # Exact match or substring match
        matched_sec = None
        for s_name in sectors:
            if q in s_name or s_name in q:
                matched_sec = s_name
                break
        if not matched_sec:
            words = [w for w in q.split() if len(w) > 3]
            for s_name in sectors:
                for w in words:
                    if w in s_name:
                        matched_sec = s_name
                        break
                if matched_sec:
                    break

        if matched_sec:
            s_data = sectors[matched_sec]
            res["matched_industry"] = matched_sec.title()
            res["wacc"] = s_data.get("wacc", 0.085)
            res["beta"] = s_data.get("beta", 1.0)
            res["gross_margin"] = s_data.get("gross_margin", 0.40)
            res["operating_margin"] = s_data.get("operating_margin", 0.15)
            res["net_margin"] = s_data.get("net_margin", 0.10)
            res["ev_to_ebitda"] = s_data.get("ev_to_ebitda", 14.0)
            res["ev_to_sales"] = s_data.get("ev_to_sales", 2.5)
            res["pe_ratio"] = s_data.get("pe_ratio", 22.0)
            res["cost_of_equity"] = res["wacc"] + 0.015

        return res

    def get_country_equity_risk_premium(self, country_name="United States"):
        c = str(country_name).strip().lower()
        if "india" in c:
            return cfg.DEFAULT_INDIA_ERP
        countries = self.data.get("countries", {})
        for cntry, vals in countries.items():
            if c in cntry or cntry in c:
                return vals.get("erp", cfg.DEFAULT_MATURE_ERP)
        return cfg.DEFAULT_MATURE_ERP

    def get_risk_free_rate(self, country_name="United States"):
        c = str(country_name).strip().lower()
        if "india" in c:
            return cfg.DEFAULT_INDIA_RISK_FREE
        return cfg.DEFAULT_US_RISK_FREE
