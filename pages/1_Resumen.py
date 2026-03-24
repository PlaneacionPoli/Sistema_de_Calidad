"""
pages/1_Resumen.py
------------------
Dashboard principal SGC — cargado vía st.navigation desde app.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import streamlit as st

from src.etl.loader import load_data, compute_kpis
from src.utils.filters import apply_filters
from src.components.kpi_cards import render_kpi_cards
from src.components.sidebar import render_sidebar
from src.components.om_table import render_om_table
from src.components.doc_table import render_doc_table
from src.components.ind_table import render_ind_table
from src.components.charts import (
    chart_om_por_unidad,
    chart_docs_por_estado,
    chart_alertas_por_macro,
    chart_fuentes_om,
)

# ─────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu, footer { visibility: hidden; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  [data-testid="metric-container"] {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 12px;
      padding: 16px 20px;
  }
  [data-testid="metric-container"] label { color: #8b949e !important; font-size: 12px; }
  [data-testid="stMetricValue"] { color: #e6edf3 !important; }
  [data-baseweb="tab-list"] { gap: 4px; background: #161b22; border-radius: 12px; padding: 4px; }
  [data-baseweb="tab"] { border-radius: 8px; padding: 8px 20px; color: #8b949e !important; }
  [aria-selected="true"] { background: #1e2530 !important; color: #e6edf3 !important; }
  hr { border-color: #30363d !important; margin: 0.4rem 0; }
  [data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Carga de datos con caché
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner="Cargando datos…")
def get_data():
    return load_data()


df_raw = get_data()

# ─────────────────────────────────────────────
# Sidebar con filtros en cascada
# ─────────────────────────────────────────────
filtros = render_sidebar(df_raw)
df = apply_filters(df_raw, **filtros)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
col_title, col_badge = st.columns([6, 1])
with col_title:
    st.markdown("## 📊 Sistema de Gestión de Calidad")
    st.caption("Dashboard Ejecutivo · POLISIGS · Monitoreo de pendientes críticos")
with col_badge:
    st.markdown(
        '<div style="text-align:right;padding-top:12px">'
        '<span style="background:rgba(255,71,87,0.1);color:#ff4757;border:1px solid rgba(255,71,87,0.3);'
        'padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700">⚠ ALERTA ACTIVA</span>'
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
kpis = compute_kpis(df)
render_kpi_cards(kpis)

st.markdown("---")

# ─────────────────────────────────────────────
# Tabs principales
# ─────────────────────────────────────────────
tab_om, tab_doc, tab_ind, tab_charts = st.tabs([
    "🚨 OM Vencidas",
    "📄 Documentos Pendientes",
    "📊 Indicadores",
    "📈 Gráficas",
])

with tab_om:
    st.markdown("### Órdenes de Mejora — Vencidas y Próximas a Vencer")
    st.caption("Expanda cada fila para ver la descripción completa de la OM.")
    render_om_table(df)

with tab_doc:
    st.markdown("### Documentos con Pendientes de Actualización")
    render_doc_table(df)

with tab_ind:
    st.markdown("### Subprocesos con Indicadores Sin Gestión")
    render_ind_table(df)

with tab_charts:
    st.markdown("### Análisis Visual")

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.plotly_chart(chart_om_por_unidad(df),    use_container_width=True)
    with row1_c2:
        st.plotly_chart(chart_docs_por_estado(df),  use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.plotly_chart(chart_alertas_por_macro(df), use_container_width=True)
    with row2_c2:
        st.plotly_chart(chart_fuentes_om(df),        use_container_width=True)
