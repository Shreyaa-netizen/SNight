"""Shared UI plumbing: theme state, CSS, and the custom map component."""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

try:
    from ui.styles import get_css, palette
except ImportError:  # launched as `streamlit run ui/frontend_demo.py`
    from styles import get_css, palette

_map = components.declare_component(
    "safenight_map", path=str(Path(__file__).parent / "components" / "safenight_map")
)


def current_mode() -> str:
    return "light" if st.session_state.get("light") else "dark"


def _flip_theme():
    st.session_state["light"] = not st.session_state.get("light", False)


def apply_theme(show_button: bool = True, slot=None):
    """Inject CSS for the current theme and (optionally) draw the theme button in `slot`."""
    st.session_state.setdefault("light", False)
    if show_button:
        target = slot if slot is not None else st
        label = "🌙 Dark" if st.session_state["light"] else "☀️ Light"
        target.button(label, on_click=_flip_theme, key="theme_btn")
    st.markdown(get_css(current_mode()), unsafe_allow_html=True)


def sos_bubble():
    # Opens the phone dialer where supported. It does not send any alert.
    st.markdown('<a class="sn-sos" href="tel:112" aria-label="Call emergency number 112">SOS 112</a>',
                unsafe_allow_html=True)


def safenight_map(**kwargs):
    """Render the map component with the active theme. Returns the component value (picker mode)."""
    theme = dict(palette(current_mode()), mode=current_mode())
    return _map(theme=theme, **kwargs)
