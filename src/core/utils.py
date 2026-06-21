"""
AEMS Heritage Pipeline - Utility Functions
Common I/O operations and cache management.
"""

import pandas as pd
import json
import os
from typing import Dict, Tuple, Optional


def load_csv(filepath: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(filepath)


def save_csv(df: pd.DataFrame, filepath: str) -> None:
    """Save a pandas DataFrame to a CSV file."""
    df.to_csv(filepath, index=False, encoding='utf-8')


def load_cache(cache_file: str) -> Dict:
    """Load geocoding cache from disk."""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(cache: Dict, cache_file: str) -> None:
    """Save geocoding cache to disk."""
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)