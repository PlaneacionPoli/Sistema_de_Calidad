"""
components/ind_table.py
-----------------------
Tabla de subprocesos con indicadores sin datos registrados.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.styling import COLORS


def render_ind_table(df: pd.DataFrame) -> None:
    """Muestra la tabla de indicadores por subproceso."""
    # Agrupar por subproceso
    groups = (
        df.groupby(["unidad", "macro", "proceso", "sub"], dropna=False)
        .agg(
            om_alerts=("om_num",    lambda s: s.notna().sum()),
            doc_alerts=("doc_nombre", lambda s: s.notna().sum()),
        )
        .reset_index()
    )
    groups["total"] = groups["om_alerts"] + groups["doc_alerts"]
    groups = groups.sort_values("total", ascending=False)

    if groups.empty:
        st.info("No hay subprocesos para los filtros seleccionados.")
        return

    st.caption(
        f"**{len(groups)}** subproceso(s) sin datos de indicadores registrados"
    )
    st.info(
        "ℹ️ Los indicadores de los subprocesos listados no tienen datos registrados. "
        "Se recomienda priorizar su carga y análisis en KAWAK para garantizar "
        "el seguimiento efectivo de la gestión.",
        icon="ℹ️",
    )

    display = groups[["unidad", "macro", "proceso", "sub", "om_alerts", "doc_alerts"]].copy()
    display.columns = ["Unidad", "Macroproceso", "Proceso", "Subproceso", "Alertas OM", "Alertas Doc."]

    def _color_alerts(val, col):
        if col == "Alertas OM" and val > 0:
            return f"color: {COLORS['red']}; font-weight: 600"
        if col == "Alertas Doc." and val > 0:
            return f"color: {COLORS['orange']}; font-weight: 600"
        return ""

    styled = display.style.apply(
        lambda col: [_color_alerts(v, col.name) for v in col], axis=0
    )

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Proceso":    st.column_config.TextColumn(width="medium"),
            "Subproceso": st.column_config.TextColumn(width="medium"),
        },
    )
