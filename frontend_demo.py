"""SafeNight frontend demo (placeholder data only).

Run from the project root:
    pip install streamlit
    streamlit run ui/frontend_demo.py

Scope: UI only. No routing math, no database changes.
All data comes through ui/data_adapter.py (the single swap point for integration).
All numbers are illustrative placeholders, not verified SafeNight predictions.
"""

import time

import streamlit as st
import streamlit.components.v1 as components

try:
    from shared import apply_theme, safenight_map, sos_bubble, current_mode
    from data_adapter import (HAZARD_TYPES, HAZARD_LABELS, WALK_KMH, START, END,
                              get_route_result, get_hazards, submit_hazard)
    from styles import palette
except ImportError:
    from ui.shared import apply_theme, safenight_map, sos_bubble, current_mode
    from ui.data_adapter import (HAZARD_TYPES, HAZARD_LABELS, WALK_KMH, START, END,
                                 get_route_result, get_hazards, submit_hazard)
    from ui.styles import palette

st.set_page_config(page_title="SafeNight", page_icon="🌙", layout="wide")

# ---- Header: title, demo mode, theme -----------------------------------------
with st.container(key="hdr"):
    h1, h2, h3 = st.columns([4, 1.5, 1.5])
with h1:
    st.markdown('<div class="sn-head"><span class="sn-title">SafeNight</span>'
                '<span class="sn-sub">Shortest walk vs lower estimated risk walk</span></div>',
                unsafe_allow_html=True)
with h2:
    if st.button("▶ Demo", key="demo_btn"):
        st.switch_page("pages/demo_mode.py")
apply_theme(slot=h3)
sos_bubble()

with st.sidebar:
    st.markdown("### Demo controls")
    demo_state = st.radio("Route data state", ["Normal", "Data limited", "No route found"], index=0)
    show_hazards = st.toggle("Show hazards on map", value=True)
    offline = st.toggle("Force offline map (test)", value=False,
                        help="Hides map tiles to preview the no-internet fallback.")
    st.caption("Placeholder values only, not verified predictions. These controls preview each state.")
STATE = {"Normal": "normal", "Data limited": "limited", "No route found": "no_route"}[demo_state]

st.session_state.setdefault("searched", True)
st.session_state.setdefault("src", "Koramangala 5th Block")
st.session_state.setdefault("dst", "Forum Mall")
st.session_state.setdefault("h_lat", 12.9345)
st.session_state.setdefault("h_lon", 77.6251)
hazards = get_hazards() if show_hazards else []

tab_plan, tab_report, tab_atlas, tab_guard = st.tabs(
    ["Plan route", "Report hazard", "Risk Atlas", "Guardian Mode"])

# ---- 1. Plan route: search + map + comparison cards in one view ---------------
with tab_plan:
    a, b, c2 = st.columns([3, 3, 1.3], vertical_alignment="bottom")
    source = a.text_input("From", key="src", placeholder="e.g. Koramangala 5th Block")
    dest = b.text_input("To", key="dst", placeholder="e.g. Forum Mall")
    with c2:
        find = st.button("Find routes", key="find")
    beta = st.slider("Route preference: Faster ↔ Lower estimated risk", 0.0, 5.0, 2.0, 0.5,
                     help="beta = 0 gives the shortest route. Higher beta weighs estimated risk more.")
    if find:
        if not source.strip() or not dest.strip():
            st.session_state["searched"] = False
            st.error("Enter both a start and a destination to compare routes.")
        else:
            with st.spinner("Finding routes..."):
                time.sleep(0.7)  # placeholder so the loading state is visible
            st.session_state["searched"] = True

    searched = st.session_state["searched"]
    route_result = get_route_result(STATE, source, dest) if searched else None
    safenight_map(mode="planner", routes=route_result, hazards=hazards, start=START, end=END,
                  beta=beta, beta_max=5.0, state=STATE, searched=searched, walk_kmh=WALK_KMH,
                  offline=offline, key="planner")

# ---- 2. Report hazard: tap map to set location --------------------------------
with tab_report:
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown("##### Tap the map to set the hazard location")
        pick = safenight_map(mode="picker", hazards=hazards, start=START, end=END, height=400,
                             pin={"lat": st.session_state["h_lat"], "lon": st.session_state["h_lon"]},
                             offline=offline, key="picker")
        if pick and pick.get("ts") != st.session_state.get("last_pick"):
            st.session_state["last_pick"] = pick["ts"]
            st.session_state["h_lat"] = round(pick["lat"], 5)
            st.session_state["h_lon"] = round(pick["lon"], 5)
    with right:
        with st.form("hazard_form", clear_on_submit=False):
            htype = st.selectbox("Category", HAZARD_TYPES, format_func=lambda k: HAZARD_LABELS[k])
            lc, lo = st.columns(2)
            lat = lc.number_input("Latitude", key="h_lat", format="%.5f")
            lon = lo.number_input("Longitude", key="h_lon", format="%.5f")
            desc = st.text_area("Description (optional)", max_chars=200,
                                placeholder="e.g. Lamp not working near the park entrance")
            submitted = st.form_submit_button("Submit report")
        if submitted:
            ok, msg = submit_hazard(lat, lon, htype, desc)
            (st.success if ok else st.error)(msg)
            if ok:
                st.caption("New reports are not treated as confirmed incidents.")
    rows = "".join(f"<tr><td>{h['label']}</td><td><span class='sn-pill'>{h['status']}</span></td>"
                   f"<td>{h['lat']:.4f}, {h['lon']:.4f}</td></tr>" for h in reversed(get_hazards()))
    st.markdown("##### Recent reports")
    st.markdown(f"<table class='sn-table'><tr><th>Category</th><th>Status</th><th>Location</th></tr>{rows}</table>",
                unsafe_allow_html=True)

# ---- 3. Risk Atlas: synthetic overlay ----------------------------------------
with tab_atlas:
    st.markdown('<div class="sn-note warn">Synthetic demonstration. These cells are made-up values to show the '
                'layout. They are not incident data and say nothing about real streets.</div>',
                unsafe_allow_html=True)
    st.markdown("")
    st.select_slider("Time of night", options=["8 pm", "10 pm", "12 am", "2 am", "4 am"], value="10 pm",
                     disabled=True, help="Enabled only when time-specific data exists.")
    st.caption("Time-of-night view is disabled: we don't have time-specific incident data.")
    safenight_map(mode="atlas", hazards=hazards, start=START, end=END, height=440,
                  atlas={"south": 12.9275, "north": 12.9395, "west": 77.6145, "east": 77.6295, "cols": 20, "rows": 12},
                  offline=offline, key="atlas")

# ---- 4. Guardian Mode: preview with explicit pause / stop --------------------
def _guardian_card(status, remaining, contact, running):
    p = palette(current_mode())
    color = {"active": p["teal"], "paused": p["coral"], "ended": p["muted"]}[status]
    label = {"active": "Sharing (preview)", "paused": "Paused", "ended": "Stopped"}[status]
    html = f"""
<div style="font-family:Inter,system-ui,sans-serif;color:{p['text']};background:{p['surface']};border:1px solid {color};
 border-radius:16px;padding:16px 18px;box-shadow:0 0 24px -8px {color}">
 <div style="display:flex;align-items:center;gap:10px"><span style="width:10px;height:10px;border-radius:50%;background:{color}"></span>
 <b style="font-size:16px">{label}</b></div>
 <div style="color:{p['muted']};font-size:13px;margin:6px 0 10px">Trusted contact: {contact or 'not set'} &middot; nothing is actually shared in this demo</div>
 <div id="t" style="font-size:34px;font-weight:700;font-family:Sora,Inter,sans-serif;font-variant-numeric:tabular-nums">--:--</div>
</div>
<script>
 var rem={int(remaining)}, run={str(running).lower()};
 function f(){{var m=Math.floor(rem/60),s=rem%60;document.getElementById('t').textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');}}
 f(); if(run){{var iv=setInterval(function(){{ if(document.hidden)return; rem=Math.max(0,rem-1); f(); if(rem===0)clearInterval(iv); }},1000);}}
</script>"""
    components.html(html, height=150)


with tab_guard:
    st.markdown('<div class="sn-note warn">Design preview. No location is shared and no contact is notified. '
                'The real feature would be opt-in, time-limited and easy to stop.</div>', unsafe_allow_html=True)
    st.markdown("")
    g = st.session_state.setdefault("g", {"status": "idle", "end": 0.0, "left": 0, "contact": ""})
    gl, gr = st.columns([1, 1], gap="large")
    with gl:
        contact = st.text_input("Trusted contact (name or number)", key="g_contact", placeholder="e.g. Amma")
        minutes = st.selectbox("Share for", [15, 30, 60], format_func=lambda m: f"{m} minutes", key="g_minutes")
        if g["status"] == "idle" or g["status"] == "ended":
            if st.button("Start sharing (preview)", key="g_start"):
                if not contact.strip():
                    st.error("Add a trusted contact first.")
                else:
                    g.update(status="active", end=time.time() + minutes * 60, contact=contact.strip())
                    st.rerun()
        else:
            b1, b2 = st.columns(2)
            if g["status"] == "active":
                if b1.button("Pause", key="g_pause"):
                    g.update(status="paused", left=max(0, int(g["end"] - time.time())))
                    st.rerun()
            else:
                if b1.button("Resume", key="g_resume"):
                    g.update(status="active", end=time.time() + g["left"])
                    st.rerun()
            if b2.button("Stop sharing", key="g_stop"):
                g.update(status="ended", left=0)
                st.rerun()
    with gr:
        if g["status"] == "active":
            rem = g["end"] - time.time()
            if rem <= 0:
                g.update(status="ended", left=0)
                _guardian_card("ended", 0, g["contact"], False)
            else:
                _guardian_card("active", rem, g["contact"], True)
        elif g["status"] == "paused":
            _guardian_card("paused", g["left"], g["contact"], False)
        elif g["status"] == "ended":
            _guardian_card("ended", 0, g["contact"], False)
        else:
            st.markdown('<div class="sn-empty"><h4>Not sharing</h4>Choose a contact and a time limit to preview.</div>',
                        unsafe_allow_html=True)
