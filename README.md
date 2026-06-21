# AEMS Heritage Pipeline

**Automated Geospatial Mapping for Cultural Heritage Preservation**

Part of the **Adaptive Environmental Modeling System (AEMS)** framework,
developed by the Digital Sovereignty for Heritage initiative in
partnership with the **Offa Heritage Documentation Initiative** and
**Wikimedia Contributors Nigeria**.

![Map Preview](docs/map_preview.png)

## Overview

This pipeline processes community-documented heritage photographs from
[ Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Digital_Heritage_Documentation_Initiative)
and automatically:

1. **Extracts metadata** (descriptions, dates, authors) via the Wikimedia API
2. **Identifies location references** using pattern matching
3. **Geocodes locations** using a specialized local gazetteer (offline)
4. **Generates an interactive map** of heritage assets

### Key Results (Offa Pilot)

| Metric | Value |
|--------|-------|
| Images processed | 500 |
| Unique locations identified | 46 |
| Successfully geocoded | 40 (87%) |
| Images with inferred GPS | 321 (64.2%) |
| External API dependency | **Zero** (100% offline) |

## Architecture

┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Wikimedia Commons API │
│ → Extract image descriptions & metadata │
├─────────────────────────────────────────────────────────────┤
│ Phase 1.5: Pattern Matching │
│ → Regex-based location extraction from text │
├─────────────────────────────────────────────────────────────┤
│ Phase 2.1: Local Gazetteer Geocoding │
│ → Fuzzy matching against 53+ known Offa locations │
│ → Multi-tier strategy: exact → partial → fuzzy → fallback │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: Interactive Map │
│ → Folium-based HTML map with clustered markers │
└─────────────────────────────────────────────────────────────┘


## Installation

```bash
# Clone the repository
git clone https://github.com/SouzaCelio/AEMS-Heritage-Pilot.git
cd aems-heritage-pipeline

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

python -m src.pipeline --input data/offa_raw_data.csv --output data/offa_data_with_inferred_gps.csv

python -m src.map_generator --input data/offa_data_with_inferred_gps.csv --output output/offa_heritage_map.html

aems-heritage-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── gazetteer.py          # Local gazetteer of Offa locations
├── src/
│   ├── core/
│   │   ├── extractor.py      # Wikimedia API & text extraction
│   │   ├── geocoder.py       # Gazetteer-based geocoding
│   │   └── utils.py          # I/O utilities
│   ├── pipeline.py           # Main orchestrator
│   └── map_generator.py      # Folium map generator
├── data/                     # Input/output CSV files
├── output/                   # Generated HTML maps
├── docs/                     # Documentation
└── reports/                  # Technical reports

Scientific Context
    This pipeline is a concrete implementation of the AEMS (Adaptive
    Environmental Modeling System) framework, specifically adapted for
    Digital Public Infrastructure (DPI) applications in cultural heritage
    preservation. 

    The project demonstrates how Bayesian-aware, uncertainty-quantifying
    architectures can be adapted beyond environmental monitoring to support
    community-driven knowledge sovereignty in the Global South.

    Related Publications
    Souza, C.S. (2026). Programmable Environmental Governance: A
    Cybernetic-Bayesian Framework for Adaptive Environmental Intelligence.
    Manuscript invited for full submission, Harvard Data Science Review.
  
Collaboration
This project is developed in collaboration with:
    Salako Lukman Olamilekan — Offa Heritage Documentation Initiative
    UNESP — São Paulo State University, Brazil
    Wikimedia Community User Group Nigeria

License
    MIT License — see LICENSE file for details.

Contact
    Celio Soares de Souza
    MSc Candidate in Environmental Sciences
    UNESP — Universidade Estadual Paulista
    Email: celio.s.souza@unesp.br
    ORCID: 0009-0000-1565-3803