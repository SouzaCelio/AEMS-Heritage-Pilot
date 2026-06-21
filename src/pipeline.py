"""
AEMS Heritage Pipeline - Main Orchestrator
Phase 1 → Phase 1.5 → Phase 2.1 (integrated)

Processes Wikimedia Commons images, extracts metadata,
and performs offline geocoding via local gazetteer.

Author: Celio Soares de Souza (UNESP)
Collaborator: Salako Lukman Olamilekan (Offa Heritage Initiative)
License: MIT
"""

import os
import sys
import time
import argparse
import pandas as pd

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from src.core.extractor import get_image_description, extract_location_from_text
from src.core.geocoder import fuzzy_match_location
from src.core.utils import load_csv, save_csv


def run_phase1_extraction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phase 1: Extract descriptions and raw metadata from Wikimedia Commons.
    """
    print("\n" + "=" * 70)
    print("PHASE 1: Metadata Extraction from Wikimedia Commons")
    print("=" * 70)

    enriched_rows = []
    total = len(df)

    for i, row in df.iterrows():
        filename = row['Filename']
        print(f"[{i+1}/{total}] Processing: {filename}")

        description = get_image_description(filename)

        row_data = row.to_dict()
        row_data['Description'] = description
        enriched_rows.append(row_data)

        if (i + 1) % 50 == 0:
            print(f"   ✓ Processed {i+1}/{total} descriptions")
        time.sleep(0.3)

    return pd.DataFrame(enriched_rows)


def run_phase1_5_geocoding(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phase 1.5/2.1: Geocode locations using local gazetteer.
    """
    print("\n" + "=" * 70)
    print("PHASE 1.5: Semantic Geocoding (Local Gazetteer)")
    print("=" * 70)

    # Extract unique locations
    unique_locations = set()
    location_map = {}

    for _, row in df.iterrows():
        filename = row['Filename']
        description = row.get('Description')
        location = extract_location_from_text(
            description if description else "", filename
        )
        if location:
            unique_locations.add(location)
        location_map[filename] = (description, location)

    print(f"✓ Found {len(unique_locations)} unique locations to geocode")

    # Geocode unique locations
    geocode_cache = {}
    for idx, location in enumerate(unique_locations, 1):
        print(f"\n[{idx}/{len(unique_locations)}] {location}")
        lat, lon, display_name, precision = fuzzy_match_location(location)

        if lat and lon:
            print(f"   ✓ ({lat:.6f}, {lon:.6f}) [{precision}]")
            geocode_cache[location] = (lat, lon, display_name, precision)
        else:
            print(f"   ✗ Not found in gazetteer")

    # Build final dataframe
    final_rows = []
    for _, row in df.iterrows():
        filename = row['Filename']
        description, location = location_map.get(filename, (None, None))

        row_data = row.to_dict()
        row_data['Description'] = description
        row_data['Inferred_Location'] = location

        if location and location in geocode_cache:
            lat, lon, display_name, precision = geocode_cache[location]
            row_data['Inferred_Latitude'] = lat
            row_data['Inferred_Longitude'] = lon
            row_data['Display_Name'] = display_name
            row_data['Geocoding_Precision'] = precision
            row_data['Has_Inferred_GPS'] = True
        else:
            row_data['Inferred_Latitude'] = None
            row_data['Inferred_Longitude'] = None
            row_data['Display_Name'] = None
            row_data['Geocoding_Precision'] = (
                'failed' if location else 'no_location_found'
            )
            row_data['Has_Inferred_GPS'] = False

        final_rows.append(row_data)

    return pd.DataFrame(final_rows)


def print_summary(df: pd.DataFrame) -> None:
    """Print execution summary statistics."""
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    print(f"  Total images processed: {len(df)}")
    print(f"  Images with inferred GPS: {df['Has_Inferred_GPS'].sum()}")
    print(f"  Images without GPS: {len(df) - df['Has_Inferred_GPS'].sum()}")
    success_rate = (df['Has_Inferred_GPS'].sum() / len(df)) * 100
    print(f"  Success rate: {success_rate:.1f}%")

    print("\nPrecision Distribution:")
    precision_counts = df['Geocoding_Precision'].value_counts()
    for precision, count in precision_counts.items():
        print(f"   - {precision}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="AEMS Heritage Pipeline - Offa Digital Sovereignty"
    )
    parser.add_argument(
        "--input", default="data/offa_raw_data.csv",
        help="Input CSV file path"
    )
    parser.add_argument(
        "--output", default="data/offa_data_with_inferred_gps.csv",
        help="Output CSV file path"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("AEMS Heritage Pipeline v2.1")
    print("Offa Heritage Documentation Initiative")
    print("Adaptive Environmental Modeling System (AEMS)")
    print("=" * 70)

    # Load input data
    df = load_csv(args.input)
    print(f"✓ Loaded {len(df)} images from {args.input}")

    # Execute pipeline phases
    df_enriched = run_phase1_extraction(df)
    df_final = run_phase1_5_geocoding(df_enriched)

    # Save output
    save_csv(df_final, args.output)
    print(f"\nOutput saved to: {args.output}")

    # Print summary
    print_summary(df_final)

    print("\n" + "=" * 70)
    print("Pipeline execution completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()