"""
AEMS Heritage Pipeline - Data Extraction Module
Handles retrieval of image metadata from Wikimedia Commons
and extraction of location references from text.
"""

import requests
import re
import html
from typing import Optional

WIKIMEDIA_API_URL = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = (
    "AEMS-Heritage-Pipeline/2.1 "
    "(UNESP Research Project; contact: celio.s.souza@unesp.br) "
    "Python/requests"
)
HEADERS = {"User-Agent": USER_AGENT}


def get_image_description(filename: str) -> Optional[str]:
    """
    Retrieve the description of an image from Wikimedia Commons
    using the extmetadata API endpoint.

    Args:
        filename: Name of the file (with or without 'File:' prefix)

    Returns:
        Cleaned description text, or None if unavailable
    """
    if not filename.startswith("File:"):
        filename = f"File:{filename}"

    params = {
        "action": "query",
        "format": "json",
        "titles": filename,
        "prop": "imageinfo",
        "iiprop": "extmetadata",
    }

    try:
        response = requests.get(
            WIKIMEDIA_API_URL, params=params, headers=HEADERS, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        for page_id in pages:
            imageinfo_list = pages[page_id].get("imageinfo", [])
            if not imageinfo_list:
                continue

            extmetadata = imageinfo_list[0].get("extmetadata", {})
            desc_raw = extmetadata.get("ImageDescription", {}).get("value", "")

            if desc_raw:
                desc_clean = re.sub(r"<[^>]+>", " ", desc_raw)
                desc_clean = re.sub(r"\s+", " ", desc_clean).strip()
                desc_clean = html.unescape(desc_clean)

                if desc_clean and len(desc_clean) > 10:
                    return desc_clean

        return None

    except Exception as e:
        print(f"   [ERROR] Failed to fetch description for {filename}: {e}")
        return None


def extract_location_from_text(text: str, filename: str = "") -> Optional[str]:
    """
    Extract potential location names from description text or filename
    using pattern matching.

    Args:
        text: Description text to parse
        filename: Original filename (used as fallback)

    Returns:
        Extracted location name, or None if no pattern matches
    """
    if not text and not filename:
        return None

    # Regex patterns ordered from most specific to most generic
    patterns = [
        r"(?:at|in|held at|located at|near)\s+([A-Z][^,\.]+(?:,\s*[A-Z][^,\.]+)?)",
        r"(?:at|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"^([A-Z][^,\.]+(?:,\s*[A-Z][^,\.]+)?)",
        r"^([^,]+(?:,\s*[^,]+)?)",
    ]

    # Try extraction from description text first
    if text:
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                location = matches[0].strip()
                # Remove trailing clauses (dates, descriptions, etc.)
                location = re.sub(r"\s+on\s+\d+.*$", "", location)
                location = re.sub(r"\s+where.*$", "", location)
                location = re.sub(r"\s+during.*$", "", location)
                location = re.sub(r"\s+is\s+a.*$", "", location)
                location = location.strip()

                if location and len(location) > 3:
                    location = re.sub(r"^(The|A|An)\s+", "", location)
                    if location and len(location) > 3:
                        return location

    # Fallback: extract from filename
    if filename:
        clean_name = re.sub(
            r"\s+\d+\.(jpg|jpeg|png)$", "", filename, flags=re.IGNORECASE
        )
        clean_name = re.sub(
            r"\.(jpg|jpeg|png)$", "", clean_name, flags=re.IGNORECASE
        )
        clean_name = re.sub(
            r"^(File:|IMG_|DSC_|Photo_?)", "", clean_name, flags=re.IGNORECASE
        )

        if "," in clean_name:
            location = clean_name.split(",")[0].strip()
        else:
            location = clean_name.strip()

        location = re.sub(
            r"\s+(01|02|03|view|exterior|interior).*$",
            "",
            location,
            flags=re.IGNORECASE,
        )
        location = location.strip()

        if location and len(location) > 3:
            return location

    return None