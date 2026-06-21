"""
AEMS Heritage Pipeline - Interactive Map Generator
Phase 4: Generates an interactive Folium-based HTML map
from the geocoded heritage dataset.

Author: Celio Soares de Souza (UNESP)
License: MIT
"""

import os
import sys
import argparse
import webbrowser
import pandas as pd
import folium
from folium.plugins import MarkerCluster

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from src.core.utils import load_csv

# Color scheme by precision level
PRECISION_COLORS = {
    'exact_match': 'green',
    'partial_match': 'blue',
    'fuzzy_match_0.97': 'orange',
    'fuzzy_match_0.95': 'orange',
    'fuzzy_match_0.90': 'orange',
    'fuzzy_match_0.85': 'orange',
    'fuzzy_match_0.80': 'orange',
    'fuzzy_match_0.75': 'orange',
    'fuzzy_match_0.70': 'orange',
    'fuzzy_match_0.65': 'orange',
    'fuzzy_match_0.60': 'orange',
    'city_fallback': 'purple',
    'failed': 'red',
    'no_location_found': 'gray',
}


def generate_map(input_csv: str, output_html: str) -> None:
    """Generate an interactive HTML map from geocoded heritage data."""

    print("=" * 70)
    print("PHASE 4: Interactive Map Generation")
    print("=" * 70)

    df = load_csv(input_csv)
    df_with_gps = df[df['Has_Inferred_GPS'] == True].copy()
    print(f"Loaded {len(df_with_gps)} geocoded images")

    if len(df_with_gps) == 0:
        print("✗ No geocoded images found. Cannot generate map.")
        return

    # Map center
    center_lat = df_with_gps['Inferred_Latitude'].mean()
    center_lon = df_with_gps['Inferred_Longitude'].mean()
    print(f"✓ Map center: ({center_lat:.6f}, {center_lon:.6f})")

    # Base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles='OpenStreetMap'
    )

    # Marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_with_gps.iterrows():
        lat = row['Inferred_Latitude']
        lon = row['Inferred_Longitude']
        precision = row.get('Geocoding_Precision', 'unknown')
        color = PRECISION_COLORS.get(precision, 'gray')

        filename = row['Filename']
        description = row.get('Description', 'No description')
        location = row.get('Inferred_Location', 'Unknown location')
        commons_url = row.get('Commons_URL', '')

        if description and len(description) > 200:
            description = description[:200] + '...'

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 300px;">
            <h4 style="margin: 0 0 10px 0; color: #333;">{filename}</h4>
            <p style="margin: 5px 0; font-size: 12px;">
                <strong>Location:</strong> {location}
            </p>
            <p style="margin: 5px 0; font-size: 12px;">
                <strong>Precision:</strong> {precision}
            </p>
            <p style="margin: 5px 0; font-size: 11px; color: #666;">
                {description}
            </p>
            <a href="{commons_url}" target="_blank" style="font-size: 11px;">
                View on Wikimedia Commons
            </a>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=filename,
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(marker_cluster)

    print(f"✓ Added {len(df_with_gps)} markers")

    # Legend
    legend_html = f"""
    <div style="position: fixed; bottom: 50px; left: 50px; width: 260px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px;">
        <h4 style="margin: 0 0 10px 0;">Precision Legend</h4>
        <p style="margin: 5px 0;"><span style="color: green;">●</span> Exact Match</p>
        <p style="margin: 5px 0;"><span style="color: blue;">●</span> Partial Match</p>
        <p style="margin: 5px 0;"><span style="color: orange;">●</span> Fuzzy Match</p>
        <p style="margin: 5px 0;"><span style="color: purple;">●</span> City Fallback</p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 11px;">
            Total: {len(df_with_gps)} heritage assets
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Title
    title_html = """
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:18px; padding: 15px; text-align: center;">
        <h3 style="margin: 0;">Cultural Heritage of Offa, Nigeria</h3>
        <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
            AEMS Heritage Pipeline — Automated Geospatial Mapping
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # Save
    m.save(output_html)
    print(f"✓ Map saved to: {output_html}")

    try:
        webbrowser.open(f'file://{os.path.realpath(output_html)}')
    except Exception as e:
        print(f"  [INFO] Could not auto-open browser: {e}")


def main():
    parser = argparse.ArgumentParser(description="AEMS Heritage Map Generator")
    parser.add_argument(
        "--input", default="data/offa_data_with_inferred_gps.csv",
        help="Input CSV with geocoded data"
    )
    parser.add_argument(
        "--output", default="output/offa_heritage_map.html",
        help="Output HTML map file"
    )
    args = parser.parse_args()
    generate_map(args.input, args.output)


if __name__ == "__main__":
    main()