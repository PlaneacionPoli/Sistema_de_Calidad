"""
app.py  –  Router principal SGC / POLISIGS
==========================================
Punto de entrada para Streamlit Cloud.
Define la navegación con etiquetas personalizadas via st.navigation().
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

st.set_page_config(
    page_title="Dashboard SGC · POLISIGS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation([
    st.Page("pages/1_Resumen.py",        title="Resumen",        icon="📊"),
    st.Page("pages/2_Ficha_Tecnica.py",  title="Ficha Técnica",  icon="📋"),
    st.Page("pages/3_Documentacion.py",  title="Documentación",  icon="📖"),
])
pg.run()
