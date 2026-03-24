"""
components/om_table.py
----------------------
Tabla de Órdenes de Mejora con deduplicación y expansor de descripción.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.utils.styling import fmt_date, COLORS


def render_om_table(df: pd.DataFrame) -> None:
    """
    Muestra la tabla de OM vencidas y próximas a vencer.
    Deduplica por (om_num, sub, om_fecha).
    Cada fila tiene un expander con la descripción completa.
    """
    # Filtrar solo filas con OM
    om_df = df[df["om_num"].notna() & df["om_estado"].notna()].copy()

    # Deduplicar
    om_df = om_df.drop_duplicates(subset=["om_num", "sub", "om_fecha"])

    # Ordenar: Vencido primero, luego por fecha
    estado_order = {"Vencido": 0, "Próximo a vencer": 1}
    om_df["_orden"] = om_df["om_estado"].map(estado_order).fillna(2)
    om_df = om_df.sort_values(["_orden", "om_fecha"]).drop(columns=["_orden"])

    if om_df.empty:
        st.info("✅ No hay OM con alertas para los filtros seleccionados.")
        return

    st.caption(f"Mostrando **{len(om_df)}** registro(s)")

    # Encabezados
    header = st.columns([1, 1.2, 2, 2, 2, 1.5, 1.5])
    for col, label in zip(header, ["OM #", "Estado", "Subproceso", "Proceso", "Fuente", "Vencimiento", "Descripción"]):
        col.markdown(f"**{label}**")
    st.divider()

    for _, row in om_df.iterrows():
        cols = st.columns([1, 1.2, 2, 2, 2, 1.5, 1.5])

        # OM #
        cols[0].markdown(
            f'<span style="color:{COLORS["red"]};font-weight:700;'
            f'background:rgba(255,71,87,0.1);padding:2px 8px;border-radius:5px">'
            f'OM {row["om_num"]}</span>',
            unsafe_allow_html=True,
        )

        # Estado
        color = COLORS["red"] if row["om_estado"] == "Vencido" else COLORS["orange"]
        cols[1].markdown(
            f'<span style="color:{color};font-weight:600">{row["om_estado"]}</span>',
            unsafe_allow_html=True,
        )

        cols[2].markdown(f"**{row['sub']}**" if row["sub"] else "—")
        cols[3].write(row["proceso"] or "—")

        # Fuente
        if row["om_fuente"]:
            cols[4].markdown(
                f'<span style="background:rgba(46,213,115,0.1);color:{COLORS["green"]};'
                f'border:1px solid rgba(46,213,115,0.2);padding:2px 8px;border-radius:4px;'
                f'font-size:12px">{row["om_fuente"]}</span>',
                unsafe_allow_html=True,
            )
        else:
            cols[4].write("—")

        # Fecha
        date_color = COLORS["red"] if row["om_estado"] == "Vencido" else COLORS["orange"]
        cols[5].markdown(
            f'<span style="color:{date_color};font-weight:500">{fmt_date(row["om_fecha"])}</span>',
            unsafe_allow_html=True,
        )

        # Descripción: truncada + expander
        desc = row["om_desc"] or ""
        if desc:
            short = desc[:90] + "…" if len(desc) > 90 else desc
            with cols[6].expander(short[:40] + "…" if len(short) > 40 else short):
                st.markdown(f"**Descripción completa:**\n\n{desc}")
        else:
            cols[6].write("—")

        st.divider()
