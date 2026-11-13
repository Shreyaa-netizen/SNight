"""SafeNight UI styles (Aurora AI-Native theme, dark + light).

Presentation only: colours, fonts, spacing, card/button styles.
No routing math, no database code.
Dark is the default (also set in .streamlit/config.toml). Light is a CSS override.
"""

# ---- Brand tokens (match the Figma design system) --------------------------
MIDNIGHT = "#0A0F1F"
INDIGO = "#4F46E5"
CYAN = "#22D3EE"
MAGENTA = "#E879F9"
MIST = "#E5E7EB"

FONT_HEADING = "Sora"
FONT_BODY = "Inter"

THEMES = {
    "dark": dict(
        bg=MIDNIGHT, surface="#121936", input="#0F1530", text=MIST, muted="#A3AAC2",
        border="#2A3566", teal="#2DD4BF", magenta=MAGENTA, coral="#FB923C", cyan=CYAN,
        indigo=INDIGO, indigo_hover="#6366F1", bar="#1E2750", glow1="rgba(79,70,229,.28)",
        glow2="rgba(34,211,238,.12)", note="rgba(34,211,238,.08)", warn="rgba(251,146,60,.10)",
    ),
    "light": dict(
        bg="#F4F6FB", surface="#FFFFFF", input="#FFFFFF", text="#0A0F1F", muted="#4B5563",
        border="#CBD2E1", teal="#0D9488", magenta="#C026D3", coral="#EA580C", cyan="#0891B2",
        indigo=INDIGO, indigo_hover="#4338CA", bar="#E5E7EB", glow1="rgba(79,70,229,.12)",
        glow2="rgba(34,211,238,.10)", note="rgba(8,145,178,.08)", warn="rgba(234,88,12,.08)",
    ),
}


def palette(mode: str) -> dict:
    return THEMES["light" if mode == "light" else "dark"]


def get_css(mode: str = "dark") -> str:
    """Full stylesheet for st.markdown(unsafe_allow_html=True)."""
    t = palette(mode)
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700&display=swap');

:root {{
  --bg:{t['bg']}; --surface:{t['surface']}; --input:{t['input']}; --text:{t['text']}; --muted:{t['muted']};
  --border:{t['border']}; --teal:{t['teal']}; --magenta:{t['magenta']}; --coral:{t['coral']};
  --cyan:{t['cyan']}; --indigo:{t['indigo']}; --indigo-hover:{t['indigo_hover']}; --bar:{t['bar']};
}}

/* ---------- Base: force every Streamlit layer onto our theme ---------- */
.stApp, [data-testid="stAppViewContainer"] {{
  background: radial-gradient(900px 260px at 50% -80px, {t['glow1']}, transparent 70%), var(--bg) !important;
  color: var(--text);
}}
[data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stHeader"] {{ background: transparent !important; }}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {{ background: var(--surface) !important; }}
.stApp, .stApp p, .stApp label, .stApp li, .stApp span, .stApp div {{ font-family: '{FONT_BODY}', system-ui, sans-serif; }}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{ font-family: '{FONT_HEADING}', system-ui, sans-serif !important; color: var(--text) !important; letter-spacing: -0.01em; }}
.stApp p, .stApp label, .stApp li, [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
[data-testid="stToggle"] p, [data-testid="stSidebar"] p {{ color: var(--text) !important; }}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p, small {{ color: var(--muted) !important; }}
.block-container {{ padding-top: 3.4rem; padding-bottom: 7rem; max-width: 1200px; }}

/* ---------- Inputs (text, number, textarea, select) ---------- */
.stTextInput input, .stNumberInput input, .stTextArea textarea {{
  background: var(--input) !important; color: var(--text) !important; border-radius: 12px !important;
  border: 1px solid var(--border) !important; -webkit-text-fill-color: var(--text) !important;
}}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{ color: var(--muted) !important; opacity: .8; -webkit-text-fill-color: var(--muted) !important; }}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{ border-color: var(--cyan) !important; box-shadow: 0 0 0 1px var(--cyan) !important; }}
[data-testid="stNumberInput"] > div > div, [data-testid="stNumberInputContainer"] {{ background: var(--input) !important; border-radius: 12px !important; }}
[data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {{ background: var(--input) !important; color: var(--text) !important; }}
[data-testid="stNumberInputStepUp"] svg, [data-testid="stNumberInputStepDown"] svg {{ fill: var(--text) !important; color: var(--text) !important; }}
div[data-baseweb="select"] span, div[data-baseweb="select"] div {{ color: var(--text) !important; }}
div[data-baseweb="select"] svg {{ fill: var(--text) !important; }}
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li, div[data-baseweb="menu"] {{ background: var(--surface) !important; color: var(--text) !important; }}
div[data-baseweb="popover"] li:hover {{ background: var(--bar) !important; }}
[data-testid="stForm"] {{ border: 1px solid var(--border) !important; border-radius: 16px; background: var(--surface); padding: 18px; }}


/* Selectbox (Streamlit 1.67 structure) */
[data-testid="stSelectbox"] [role="group"] {{ background: var(--input) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }}
[data-testid="stSelectbox"] input, [data-testid="stSelectbox"] [role="combobox"] {{ color: var(--text) !important; -webkit-text-fill-color: var(--text) !important; }}
[data-testid="stSelectbox"] svg, [data-testid="stSelectbox"] button {{ color: var(--text) !important; fill: var(--text) !important; }}
[role="listbox"], [role="listbox"] [role="option"], ul[role="listbox"] li {{ background: var(--surface) !important; color: var(--text) !important; }}
[role="listbox"] [role="option"]:hover, [role="option"][aria-selected="true"] {{ background: var(--bar) !important; }}
/* Radio: unselected circle follows the theme */
[role="radiogroup"] label:has(input:not(:checked)) > div:first-of-type > div:first-child {{ background: var(--input) !important; border-color: var(--border) !important; }}
[role="radiogroup"] label:has(input:not(:checked)) > div:first-of-type > div:first-child > div {{ background: var(--input) !important; }}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid var(--border); }}
.stTabs [data-baseweb="tab"] {{ min-height: 46px; padding: 0 16px; border-radius: 10px 10px 0 0; }}
.stTabs [data-baseweb="tab"] p {{ color: var(--muted) !important; font-weight: 500; }}
.stTabs [aria-selected="true"] {{ background: rgba(79,70,229,.16); }}
.stTabs [aria-selected="true"] p {{ color: var(--text) !important; font-weight: 600; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: var(--cyan) !important; box-shadow: 0 0 10px var(--cyan); }}

/* ---------- Buttons: default / hover / pressed / focus / disabled ---------- */
.stButton > button, .stFormSubmitButton > button {{
  background: var(--indigo) !important; color: #fff !important; border: 1px solid var(--indigo) !important;
  border-radius: 12px; min-height: 48px; font-weight: 600; width: 100%; transition: background .15s ease, transform .05s ease, box-shadow .2s ease;
  box-shadow: 0 0 20px -6px rgba(79,70,229,.75);
}}
.stButton > button p, .stFormSubmitButton > button p {{ color: #fff !important; }}
.stButton > button:hover, .stFormSubmitButton > button:hover {{ background: var(--indigo-hover) !important; border-color: var(--indigo-hover) !important; }}
.stButton > button:active, .stFormSubmitButton > button:active {{ transform: scale(.98); }}
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible {{ outline: 3px solid var(--cyan); outline-offset: 2px; }}
.stButton > button:disabled {{ background: var(--bar) !important; border-color: var(--border) !important; }}
.stButton > button:disabled p {{ color: var(--muted) !important; }}
.st-key-theme_btn .stButton > button, .st-key-g_stop .stButton > button {{ background: transparent !important; color: var(--text) !important; border: 1px solid var(--border) !important; }}
.st-key-theme_btn .stButton > button p, .st-key-g_stop .stButton > button p {{ color: var(--text) !important; }}

iframe {{ border: 0 !important; color-scheme: normal; }}
/* ---------- Components ---------- */
.sn-head {{ padding-top: 6px; line-height: 1.2; }}
.sn-title {{ font-family: '{FONT_HEADING}', system-ui, sans-serif; font-weight: 700; font-size: 1.7rem; margin: 0; color: var(--text); }}
.sn-sub {{ color: var(--muted); margin: 0 0 0 14px; font-size: .92rem; }}
.sn-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 16px 18px; height: 100%; }}
.sn-card.lower {{ border: 2px solid var(--teal); }}
.sn-card h4 {{ margin: 0 0 4px 0; font-size: 1.08rem; }}
.sn-tag {{ color: var(--muted); font-size: .84rem; margin-bottom: 10px; }}
.sn-stat {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-top: 1px solid var(--border); font-size: .96rem; color: var(--text); }}
.sn-stat b {{ font-family: '{FONT_HEADING}', system-ui, sans-serif; font-weight: 600; }}
.sn-bar {{ height: 8px; border-radius: 99px; background: var(--bar); overflow: hidden; margin-top: 4px; }}
.sn-bar > span {{ display: block; height: 100%; border-radius: 99px; }}
.sn-legend {{ display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: .9rem; margin: 8px 0 2px 0; color: var(--text); }}
.sn-legend .item {{ display: flex; align-items: center; gap: 8px; }}
.sn-legend .swatch {{ width: 36px; height: 0; border-top: 6px solid var(--teal); }}
.sn-legend .swatch.thin {{ border-top: 3px solid var(--magenta); }}
.sn-legend .hazard {{ width: 12px; height: 12px; border-radius: 3px; background: var(--coral); transform: rotate(45deg); }}
.sn-badge {{ display: inline-block; padding: 2px 10px; border-radius: 99px; font-size: .8rem; font-weight: 600; border: 1px solid var(--coral); color: var(--coral); }}
.sn-note {{ border-left: 4px solid var(--cyan); background: {t['note']}; padding: 12px 14px; border-radius: 8px; font-size: .94rem; color: var(--text); }}
.sn-note.warn {{ border-left-color: var(--coral); background: {t['warn']}; }}
.sn-empty {{ border: 1px dashed var(--border); border-radius: 16px; padding: 28px 18px; text-align: center; color: var(--muted); }}
.sn-table {{ width: 100%; border-collapse: collapse; font-size: .92rem; color: var(--text); }}
.sn-table th {{ text-align: left; color: var(--muted); font-weight: 600; padding: 8px 10px; border-bottom: 1px solid var(--border); }}
.sn-table td {{ padding: 9px 10px; border-bottom: 1px solid var(--border); }}
.sn-pill {{ padding: 2px 10px; border-radius: 99px; border: 1px solid var(--border); font-size: .8rem; }}

/* ---------- SOS floating bubble (a tel: link only, sends nothing) ---------- */
.sn-sos {{
  position: fixed; right: 18px; bottom: 18px; z-index: 99999; background: #DC2626; color: #fff !important;
  text-decoration: none !important; font-family: '{FONT_HEADING}', system-ui, sans-serif; font-weight: 700; letter-spacing: .02em;
  padding: 14px 22px; border-radius: 99px; min-height: 48px; display: flex; align-items: center;
  box-shadow: 0 6px 20px rgba(220,38,38,.45);
}}
.sn-sos:hover {{ background: #EF4444; }}
.sn-sos:focus-visible {{ outline: 3px solid var(--cyan); outline-offset: 3px; }}


/* Streamlit icon font must not be overridden by our text font */
.stApp [data-testid="stIconMaterial"], .stApp span[class*="material"] {{ font-family: 'Material Symbols Rounded', 'Material Icons' !important; }}
/* Header row stays on one line, even on phones */
.st-key-hdr [data-testid="stHorizontalBlock"] {{ flex-wrap: nowrap !important; gap: .5rem !important; align-items: center; }}
.st-key-hdr [data-testid="stColumn"] {{ min-width: 0 !important; width: auto !important; flex: 0 0 auto !important; }}
.st-key-hdr [data-testid="stColumn"]:first-child {{ flex: 1 1 auto !important; }}
.st-key-hdr .stButton > button {{ min-height: 42px; padding: 0 14px; white-space: nowrap; width: auto; }}

/* ---------- Mobile ---------- */
@media (max-width: 640px) {{
  .block-container {{ padding-left: .9rem; padding-right: .9rem; padding-top: 3.6rem; }}
  .sn-title {{ font-size: 1.45rem; }}
  .sn-sub {{ display: none; }}
  [data-testid="stVerticalBlock"] {{ gap: .55rem !important; }}
  .stTextInput label, .stSlider label {{ margin-bottom: 0 !important; }}
  html, body, .stApp {{ overflow-x: hidden; }}
  .sn-sos {{ right: 12px; bottom: 12px; }}
  .stTabs [data-baseweb="tab"] {{ padding: 0 10px; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
"""
