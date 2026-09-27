import os

CBM_DIR = "/Users/nivsorathiya/Documents/CBM"
DATASETS_DIR = os.path.join(CBM_DIR, "datasets")

# Datasets Paths
WACC_DATASET = os.path.join(DATASETS_DIR, "cost_of_capital_by_sector.xls")
ERP_DATASET = os.path.join(DATASETS_DIR, "country_equity_risk_premiums.xls")
MARGIN_DATASET = os.path.join(DATASETS_DIR, "operating_margins_by_sector.xls")
CAPEX_DATASET = os.path.join(DATASETS_DIR, "capex_and_reinvestment_by_sector.xls")
MULTIPLES_DATASET = os.path.join(DATASETS_DIR, "valuation_multiples_by_sector.xls")
FAMA_FRENCH_DATASET = os.path.join(DATASETS_DIR, "F-F_Research_Data_Factors.csv")
FRED_10Y_DATASET = os.path.join(DATASETS_DIR, "fred_10y_treasury_yield.csv")
FRED_FEDFUNDS_DATASET = os.path.join(DATASETS_DIR, "fred_fed_funds_rate.csv")
RITTER_IPO_STATS = os.path.join(DATASETS_DIR, "jay_ritter_ipo_statistics.pdf")

# Master Textbooks
DAMODARAN_PDF = os.path.join(CBM_DIR, "investment-valuation-3rd-edition.pdf")
MCKINSEY_PDF = os.path.join(CBM_DIR, "Mesuaring-and-Managing-Value-of-Company-7th-version.pdf")
GRAHAM_DODD_PDF = os.path.join(CBM_DIR, "security-analysis-seventh-edition-principles-and-techniques-7nbsped-1264932405-9781264932405_compress.pdf")
BREALEY_MYERS_PDF = os.path.join(CBM_DIR, "BREALEY-MYERS-Principles-of-Corporate-Finance-7e.pdf")
LOPEZ_DE_PRADO_PDF = os.path.join(CBM_DIR, "advances-in-financial-machine-learning-1nbsped-9781119482109-9781119482116-9781119482086.pdf")
SCHILIT_PDF = os.path.join(CBM_DIR, "financial-shenanigans-fourth-edition-how-to-detect-accounting-gimmicks-amp-fraud-in-financial-reports-9781260117271-1260117278-9781260117264-126011726x.pdf")
HOWARD_MARKS_PDF = os.path.join(CBM_DIR, "The Most Important Thing Illumi - Howard Marks.pdf")

# Default Global Macro Parameters
DEFAULT_RISK_FREE_RATE = 0.0425
DEFAULT_MATURE_ERP = 0.0460
DEFAULT_TERMINAL_GROWTH = 0.030
