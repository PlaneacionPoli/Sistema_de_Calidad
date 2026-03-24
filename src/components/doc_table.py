"""
components/doc_table.py
-----------------------
Tabla de documentos con pendientes (vencidos y próximos a vencer).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.styling import fmt_date, COLORS


def render_doc_table(df: pd.DataFrame) -> None:
    """Muestra la tabla de documentos pendientes."""
    doc_df = df[df["doc_nombre"].notna() & df["doc_estado"].notna()].copy()

    # Ordenar: Vencido primero
    estado_order = {"Vencido": 0, "Próximo a vencer": 1}
    doc_df["_orden"] = doc_df["doc_estado"].map(estado_order).fillna(2)
    doc_df = doc_df.sort_values(["_orden", "doc_fecha"]).drop(columns=["_orden"])

    if doc_df.empty:
        st.info("✅ No hay documentos con alertas para los filtros seleccionados.")
        return

    st.caption(f"Mostrando **{len(doc_df)}** registro(s)")

    # Preparar tabla para st.dataframe con colores
    display = doc_df[[
        "doc_estado", "unidad", "macro", "proceso", "sub",
        "doc_tipo", "doc_nombre", "doc_accion", "doc_fecha"
    ]].copy()

    display["doc_fecha"] = display["doc_fecha"].apply(fmt_date)
    display.columns = [
        "Estado", "Unidad", "Macroproceso", "Proceso", "Subproceso",
        "Tipo Doc.", "Nombre del Documento", "Tipo Acción", "Fecha Límite"
    ]

    def _color_row(row):
        color = COLORS["red"] if row["Estado"] == "Vencido" else COLORS["orange"]
        return [f"color: {color}" if col == "Estado" else "" for col in row.index]

    styled = display.style.apply(_color_row, axis=1)

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nombre del Documento": st.column_config.TextColumn(width="large"),
            "Proceso": st.column_config.TextColumn(width="medium"),
        },
    )
