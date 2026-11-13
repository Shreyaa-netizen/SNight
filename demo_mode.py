"""Demo mode: a self-playing walkthrough for the pitch (client-side, placeholder data)."""

import streamlit as st

try:
    from shared import apply_theme, safenight_map, sos_bubble
    from data_adapter import START, END, WALK_KMH, get_route_result
except ImportError:
    from ui.shared import apply_theme, safenight_map, sos_bubble
    from ui.data_adapter import START, END, WALK_KMH, get_route_result

st.set_page_config(page_title="SafeNight demo", page_icon="🌙", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid=\"stSidebar\"],[data-testid=\"stSidebarCollapsedControl\"]{display:none !important}</style>", unsafe_allow_html=True)

with st.container(key="hdr"):
    h1, h2, h3 = st.columns([4, 1.5, 1.5])
with h1:
    st.markdown('<div class="sn-head"><span class="sn-title">SafeNight demo</span>'
                '<span class="sn-sub">A guided tour with placeholder data</span></div>', unsafe_allow_html=True)
with h2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("frontend_demo.py")
apply_theme(slot=h3)
sos_bubble()

safenight_map(mode="demo", routes=get_route_result("normal"), hazards=[
    {"lat": 12.9347, "lon": 77.6214, "label": "Broken streetlight", "status": "confirmed"},
    {"lat": 12.9362, "lon": 77.6226, "label": "Dark path", "status": "new"},
], start=START, end=END, beta=2.0, beta_max=5.0, walk_kmh=WALK_KMH, key="demo")
