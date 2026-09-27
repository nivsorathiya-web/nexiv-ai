import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "brain_knowledge")

COMPILED_SECTOR_DATA = os.path.join(DATASETS_DIR, "compiled_sector_data.json")
MASTER_KNOWLEDGE_GRAPH = os.path.join(KNOWLEDGE_DIR, "master_codified_knowledge_graph.json")

# Macro Defaults
DEFAULT_US_RISK_FREE = 0.0425
DEFAULT_INDIA_RISK_FREE = 0.0705  # 10Y Indian Government Benchmark Bond yield (G-Sec)
DEFAULT_MATURE_ERP = 0.0460
DEFAULT_INDIA_ERP = 0.0708        # Damodaran ERP for India (Baa3 rating)
DEFAULT_TERMINAL_GROWTH_US = 0.030
DEFAULT_TERMINAL_GROWTH_INDIA = 0.055  # Long-term nominal GDP growth rate for India
