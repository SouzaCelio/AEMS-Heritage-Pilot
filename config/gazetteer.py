"""
AEMS Heritage Pipeline - Local Gazetteer Configuration
Contains known locations in Offa, Kwara State, Nigeria
with their approximate GPS coordinates.

Source: Community knowledge from Offa Heritage Documentation Initiative
Last updated: June 2026
"""

OFFA_GAZETTEER = {
    # ==========================================
    # CITY-LEVEL REFERENCES
    # ==========================================
    "offa": {"lat": 8.1560, "lon": 4.7227, "type": "city"},
    "offa kwara": {"lat": 8.1560, "lon": 4.7227, "type": "city"},
    "offa kwara state": {"lat": 8.1560, "lon": 4.7227, "type": "city"},
    "offa kwara nigeria": {"lat": 8.1560, "lon": 4.7227, "type": "city"},

    # ==========================================
    # DISTRICTS / NEIGHBORHOODS
    # ==========================================
    "ibolo": {"lat": 8.1520, "lon": 4.7180, "type": "district"},
    "ajegunle": {"lat": 8.1600, "lon": 4.7250, "type": "district"},
    "alubata": {"lat": 8.1580, "lon": 4.7200, "type": "district"},
    "balogun": {"lat": 8.1540, "lon": 4.7240, "type": "district"},
    "ojomu": {"lat": 8.1500, "lon": 4.7260, "type": "district"},
    "igbodun": {"lat": 8.1620, "lon": 4.7190, "type": "district"},
    "asalofa": {"lat": 8.1570, "lon": 4.7280, "type": "district"},
    "essa": {"lat": 8.1530, "lon": 4.7210, "type": "district"},
    "shawo": {"lat": 8.1550, "lon": 4.7230, "type": "district"},
    "ilemona": {"lat": 8.1590, "lon": 4.7270, "type": "district"},
    "bolorunduro": {"lat": 8.1610, "lon": 4.7220, "type": "district"},
    "oke-igbala": {"lat": 8.1560, "lon": 4.7250, "type": "district"},
    "oke-iyanu": {"lat": 8.1570, "lon": 4.7240, "type": "district"},
    "nawairu deen": {"lat": 8.1540, "lon": 4.7260, "type": "district"},
    "igbo-oro": {"lat": 8.1580, "lon": 4.7210, "type": "district"},
    "ayaba": {"lat": 8.1550, "lon": 4.7270, "type": "district"},
    "anilelerin": {"lat": 8.1560, "lon": 4.7280, "type": "district"},
    "pandora": {"lat": 8.1570, "lon": 4.7290, "type": "district"},
    "ajelanwa": {"lat": 8.1580, "lon": 4.7300, "type": "district"},

    # ==========================================
    # LANDMARKS & INSTITUTIONS
    # ==========================================
    "one innovation hub": {"lat": 8.1565, "lon": 4.7235, "type": "landmark"},
    "summit university": {"lat": 8.1600, "lon": 4.7200, "type": "university"},
    "archers club hall": {"lat": 8.1550, "lon": 4.7240, "type": "landmark"},
    "hengee resort": {"lat": 8.1550, "lon": 4.7220, "type": "landmark"},
    "ayaba river": {"lat": 8.1550, "lon": 4.7270, "type": "river"},

    # ==========================================
    # RELIGIOUS SITES
    # ==========================================
    "central mosque": {"lat": 8.1560, "lon": 4.7250, "type": "mosque"},
    "central mosque popo road": {"lat": 8.1555, "lon": 4.7245, "type": "mosque"},
    "agara idera central mosque": {"lat": 8.1540, "lon": 4.7260, "type": "mosque"},
    "ajegunle central mosque": {"lat": 8.1600, "lon": 4.7250, "type": "mosque"},
    "akinale compound mosque": {"lat": 8.1580, "lon": 4.7200, "type": "mosque"},
    "anwar-ul islam central mosque": {"lat": 8.1570, "lon": 4.7230, "type": "mosque"},
    "alubata oju-irin mosque": {"lat": 8.1580, "lon": 4.7200, "type": "mosque"},
    "christ apostolic church": {"lat": 8.1560, "lon": 4.7250, "type": "church"},
    "ecwa evangelical church": {"lat": 8.1570, "lon": 4.7260, "type": "church"},

    # ==========================================
    # EDUCATIONAL INSTITUTIONS
    # ==========================================
    "lgea school": {"lat": 8.1560, "lon": 4.7240, "type": "school"},
    "ecwa lgea primary school": {"lat": 8.1570, "lon": 4.7250, "type": "school"},
    "community lgea primary school": {"lat": 8.1600, "lon": 4.7250, "type": "school"},
    "ayo ni o nursery & primary school": {"lat": 8.1550, "lon": 4.7260, "type": "school"},
    "bishop smith lgea school": {"lat": 8.1560, "lon": 4.7230, "type": "school"},
    "al-hisan school": {"lat": 8.1570, "lon": 4.7240, "type": "school"},
    "ansar-ud-deen college": {"lat": 8.1580, "lon": 4.7250, "type": "school"},
    "anwar-ul islam nursery and primary school": {"lat": 8.1590, "lon": 4.7260, "type": "school"},
    "arolus college of education": {"lat": 8.1590, "lon": 4.7270, "type": "school"},

    # ==========================================
    # HEALTH FACILITIES
    # ==========================================
    "abike memorial clinic": {"lat": 8.1560, "lon": 4.7240, "type": "health"},
    "ajegunle basic health center": {"lat": 8.1600, "lon": 4.7250, "type": "health"},
    "basic health care center": {"lat": 8.1570, "lon": 4.7230, "type": "health"},

    # ==========================================
    # BUSINESSES & SERVICES
    # ==========================================
    "a&t store": {"lat": 8.1560, "lon": 4.7240, "type": "business"},
    "cravepot": {"lat": 8.1570, "lon": 4.7250, "type": "business"},
    "de-unique kitchen": {"lat": 8.1580, "lon": 4.7260, "type": "business"},
    "ascent lodge and club": {"lat": 8.1590, "lon": 4.7270, "type": "business"},
}

# Precision thresholds for fuzzy matching
FUZZY_MATCH_THRESHOLD = 0.60