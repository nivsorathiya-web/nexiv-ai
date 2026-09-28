import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
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

# Load environment variables from .env if present
env_file = os.path.join(PROJECT_ROOT, ".env")
if os.path.isfile(env_file):
    try:
        with open(env_file, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))
    except Exception:
        pass

# Gemini AI Configuration
DEFAULT_GEMINI_API_KEY = ""
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_GEMINI_API_KEY)

