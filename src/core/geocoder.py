"""
AEMS Heritage Pipeline - Geocoding Module
Fuzzy matching against a local gazetteer for offline geocoding.
"""

import re
from typing import Tuple, Optional
from difflib import SequenceMatcher

# Import gazetteer from config
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.gazetteer import OFFA_GAZETTEER, FUZZY_MATCH_THRESHOLD


def _normalize_location(name: str) -> str:
    """Normalize a location name for matching."""
    name = name.lower().strip()
    stop_words = [
        'front', 'view', 'exterior', 'interior', 'left', 'right',
        'wing', 'image', 'of', 'the'
    ]
    for word in stop_words:
        name = name.replace(word, '')
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def fuzzy_match_location(
    location_name: str,
    threshold: float = FUZZY_MATCH_THRESHOLD
) -> Tuple[Optional[float], Optional[float], Optional[str], str]:
    """
    Match a location name against the local gazetteer using a
    multi-tier strategy: exact match → partial match → fuzzy match → city fallback.

    Args:
        location_name: Raw location name to geocode
        threshold: Minimum similarity ratio for fuzzy matching

    Returns:
        Tuple of (latitude, longitude, display_name, precision_level)
    """
    if not location_name:
        return None, None, None, "no_input"

    normalized = _normalize_location(location_name)

    # Strategy 1: Exact match
    if normalized in OFFA_GAZETTEER:
        entry = OFFA_GAZETTEER[normalized]
        return entry['lat'], entry['lon'], location_name, "exact_match"

    # Strategy 2: Partial match (substring containment)
    for key, entry in OFFA_GAZETTEER.items():
        if key in normalized or normalized in key:
            return entry['lat'], entry['lon'], location_name, "partial_match"

    # Strategy 3: Fuzzy matching via SequenceMatcher
    best_match = None
    best_score = 0

    for key, entry in OFFA_GAZETTEER.items():
        score = SequenceMatcher(None, normalized, key).ratio()
        if score > best_score and score >= threshold:
            best_score = score
            best_match = (
                entry['lat'], entry['lon'], location_name,
                f"fuzzy_match_{best_score:.2f}"
            )

    if best_match:
        return best_match

    # Strategy 4: City-level fallback if "offa" appears in the name
    if 'offa' in normalized:
        entry = OFFA_GAZETTEER['offa']
        return entry['lat'], entry['lon'], location_name, "city_fallback"

    return None, None, None, "not_found"