"""
components/kpi_cards.py
-----------------------
Renderiza los 4 KPI cards superiores del dashboard.
"""
from __future__ import annotations

import streamlit as st


def render_kpi_cards(kpis: dict) -> None:
    """
    Muestra cuatro métricas principales en columnas.

    Parameters
    ----------
    kpis : dict con claves om_vencidas, doc_vencidos, proximos, sub_afectados
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🔴 OM Vencidas",
            value=kpis["om_vencidas"],
            help="Órdenes de Mejora con estado Vencido (únicas por OM + subproceso + fecha)",
        )
    with col2:
        st.metric(
            label="🟠 Documentos Vencidos",
            value=kpis["doc_vencidos"],
            help="Documentos con fecha de vencimiento superada",
        )
    with col3:
        st.metric(
            label="🔵 Próximos a Vencer",
            value=kpis["proximos"],
            help="OM y documentos con estado 'Próximo a vencer'",
        )
    with col4:
        st.metric(
            label="🟣 Subprocesos Afectados",
            value=kpis["sub_afectados"],
            help="Subprocesos con al menos una alerta activa",
        )
