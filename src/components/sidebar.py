"""
components/sidebar.py
---------------------
Renderiza el panel de filtros en cascada en el sidebar de Streamlit.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

from src.utils.filters import get_cascade_options


def render_sidebar(df: pd.DataFrame) -> dict[str, str | None]:
    """
    Dibuja los filtros en cascada en el sidebar.

    Returns
    -------
    dict con claves: unidad, macro, proceso, sub
    (valor None si no se seleccionó nada)
    """
    st.sidebar.markdown("## 🔍 Filtros")
    st.sidebar.markdown("---")

    # --- Unidad ---
    all_unidades = sorted(df["unidad"].dropna().unique().tolist())
    unidad_sel = st.sidebar.selectbox(
        "Unidad",
        options=["Todas"] + all_unidades,
        index=0,
        key="f_unidad",
    )
    unidad = None if unidad_sel == "Todas" else unidad_sel

    # --- Cascada ---
    opts = get_cascade_options(df, unidad, None, None)

    macro_sel = st.sidebar.selectbox(
        "Macroproceso",
        options=["Todos"] + opts["macros"],
        index=0,
        key="f_macro",
    )
    macro = None if macro_sel == "Todos" else macro_sel

    # Recalcular con macro ya elegida
    opts2 = get_cascade_options(df, unidad, macro, None)

    proceso_sel = st.sidebar.selectbox(
        "Proceso",
        options=["Todos"] + opts2["procesos"],
        index=0,
        key="f_proceso",
    )
    proceso = None if proceso_sel == "Todos" else proceso_sel

    # Recalcular con proceso elegido
    opts3 = get_cascade_options(df, unidad, macro, proceso)

    sub_sel = st.sidebar.selectbox(
        "Subproceso",
        options=["Todos"] + opts3["subs"],
        index=0,
        key="f_sub",
    )
    sub = None if sub_sel == "Todos" else sub_sel

    st.sidebar.markdown("---")
    if st.sidebar.button("✕ Limpiar filtros", use_container_width=True):
        st.rerun()

    # Info de versión
    st.sidebar.markdown("---")
    st.sidebar.caption("SGC Dashboard v1.0  \nPOLISIGS · 2025")

    return {
        "unidad":  unidad,
        "macro":   macro,
        "proceso": proceso,
        "sub":     sub,
    }
