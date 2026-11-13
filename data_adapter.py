"""SafeNight UI data adapter  --  THE SWAP POINT for integration.

The UI only talks to the functions in this file. Right now they return placeholder
data. At integration, Member 1 (routes) and Member 4 (hazards) replace the bodies,
keeping the same return shapes. Nothing else in ui/ needs to change.

Route contract (the doc's contract, plus OPTIONAL geometry for the map):
    route_result = {
        "shortest":   {"distance_m": 850,  "risk_indicator": 0.42,
                       "path": [[lat, lon], ...],          # optional, for the map
                       "segment_risk": [0.3, 0.5, ...]},   # optional, for the card strip
        "lower_risk": {"distance_m": 1100, "risk_indicator": 0.25, "path": [...], "segment_risk": [...]},
    }
    risk_indicator = None  ->  the UI shows a "Data limited" state.
    get_route_result() returns None  ->  the UI shows a "No route found" state.
All values below are illustrative placeholders, not verified SafeNight predictions.
"""

import copy

import streamlit as st

HAZARD_TYPES = ["broken_streetlight", "dark_path", "blocked_footpath", "other_infrastructure"]
HAZARD_LABELS = {
    "broken_streetlight": "Broken streetlight",
    "dark_path": "Dark path",
    "blocked_footpath": "Blocked footpath",
    "other_infrastructure": "Other infrastructure issue",
}
WALK_KMH = 5  # shown to the user; used for the walking-time estimate

START = {"lat": 12.9340, "lon": 77.6180, "name": "Start"}
END = {"lat": 12.9353, "lon": 77.6258, "name": "End"}

_SHORT_PATH = [[12.9340, 77.6180], [12.9342, 77.6192], [12.9345, 77.6204], [12.9347, 77.6216],
               [12.9348, 77.6228], [12.9350, 77.6240], [12.9352, 77.6250], [12.9353, 77.6258]]
_LOW_PATH = [[12.9340, 77.6180], [12.9333, 77.6185], [12.9325, 77.6192], [12.9318, 77.6201],
             [12.9314, 77.6212], [12.9314, 77.6224], [12.9318, 77.6235], [12.9327, 77.6244],
             [12.9338, 77.6251], [12.9347, 77.6255], [12.9353, 77.6258]]
_SHORT_SEG = [.30, .35, .55, .62, .58, .45, .40, .38, .35, .30, .28, .30]
_LOW_SEG = [.20, .18, .22, .25, .30, .28, .24, .22, .26, .27, .25, .22]

_BASE_HAZARDS = [
    {"lat": 12.9347, "lon": 77.6214, "label": "Broken streetlight", "status": "confirmed"},
    {"lat": 12.9362, "lon": 77.6226, "label": "Dark path", "status": "new"},
]


def get_route_result(state: str = "normal", source: str = "", dest: str = ""):
    """SWAP POINT (Member 1). state: 'normal' | 'limited' | 'no_route' (demo switch only)."""
    if state == "no_route":
        return None
    short = {"distance_m": 850, "risk_indicator": 0.42, "path": _SHORT_PATH, "segment_risk": _SHORT_SEG}
    low = {"distance_m": 1100, "risk_indicator": 0.25, "path": _LOW_PATH, "segment_risk": _LOW_SEG}
    if state == "limited":
        short = dict(short, risk_indicator=None, segment_risk=None)
        low = dict(low, risk_indicator=None, segment_risk=None)
    return {"shortest": short, "lower_risk": low}


def get_hazards():
    """SWAP POINT (Member 4: get_active_hazards). Placeholder keeps reports in this browser session only."""
    if "hazards" not in st.session_state:
        st.session_state["hazards"] = copy.deepcopy(_BASE_HAZARDS)
    return st.session_state["hazards"]


def submit_hazard(lat: float, lon: float, hazard_type: str, description: str = ""):
    """SWAP POINT (Member 4: add_hazard). Returns (ok, message). Placeholder: nothing is saved to a database."""
    if hazard_type not in HAZARD_TYPES:
        return False, "Pick a hazard category."
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return False, "Location is out of range. Latitude must be -90 to 90 and longitude -180 to 180."
    if len(description) > 200:
        return False, "Description is too long (200 characters max)."
    get_hazards().append({"lat": lat, "lon": lon, "label": HAZARD_LABELS[hazard_type], "status": "new"})
    return True, f"Report received: {HAZARD_LABELS[hazard_type]}. It starts as unverified. Demo only, nothing is saved yet."
