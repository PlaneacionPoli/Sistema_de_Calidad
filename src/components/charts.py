"""
components/charts.py
--------------------
Visualizaciones Plotly para el dashboard SGC.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.utils.styling import COLORS

# Layout base reutilizable
_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e6edf3", family="DM Sans, sans-serif"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)


def chart_om_por_unidad(df: pd.DataFrame) -> go.Figure:
    """Barras: OM vencidas por unidad."""
    seen: set = set()
    rows = []
    for _, r in df[df["om_estado"] == "Vencido"].iterrows():
        key = (r["om_num"], r["sub"], r["om_fecha"])
        if key not in seen:
            seen.add(key)
            rows.append(r)

    if not rows:
        return _empty_fig("Sin datos de OM vencidas")

    agg = (
        pd.DataFrame(rows)
        .groupby("unidad")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x=agg["count"],
        y=agg["unidad"],
        orientation="h",
        marker_color=COLORS["red"],
        marker_opacity=0.85,
        text=agg["count"],
        textposition="outside",
    ))
    fig.update_layout(
        **_BASE_LAYOUT,
        title="OM Vencidas por Unidad",
        xaxis=dict(showgrid=True, gridcolor="#30363d"),
        yaxis=dict(showgrid=False),
        height=300,
    )
    return fig


def chart_docs_por_estado(df: pd.DataFrame) -> go.Figure:
    """Dona: documentos por estado."""
    doc_df = df[df["doc_nombre"].notna() & df["doc_estado"].notna()]
    if doc_df.empty:
        return _empty_fig("Sin datos de documentos")

    counts = doc_df["doc_estado"].value_counts()
    colors = [
        COLORS["red"] if s == "Vencido" else COLORS["orange"]
        for s in counts.index
    ]

    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.55,
        marker_colors=colors,
        textinfo="label+percent",
        textfont_size=12,
    ))
    fig.update_layout(
        **_BASE_LAYOUT,
        title="Documentos por Estado",
        height=300,
        showlegend=False,
    )
    return fig


def chart_alertas_por_macro(df: pd.DataFrame) -> go.Figure:
    """Barras apiladas: alertas OM y Doc por macroproceso."""
    om_counts  = df[df["om_estado"].notna()].groupby("macro")["om_num"].count()
    doc_counts = df[df["doc_estado"].notna()].groupby("macro")["doc_nombre"].count()

    macros = sorted(set(om_counts.index) | set(doc_counts.index))
    if not macros:
        return _empty_fig("Sin datos")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Alertas OM",
        x=macros,
        y=[om_counts.get(m, 0) for m in macros],
        marker_color=COLORS["red"],
        opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        name="Alertas Doc.",
        x=macros,
        y=[doc_counts.get(m, 0) for m in macros],
        marker_color=COLORS["orange"],
        opacity=0.85,
    ))
    fig.update_layout(
        **_BASE_LAYOUT,
        title="Alertas por Macroproceso",
        barmode="stack",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#30363d"),
        height=320,
    )
    return fig


def chart_fuentes_om(df: pd.DataFrame) -> go.Figure:
    """Barras horizontales: OM por fuente de auditoría."""
    om_df = df[df["om_fuente"].notna() & df["om_estado"].notna()]
    if om_df.empty:
        return _empty_fig("Sin datos")

    counts = om_df["om_fuente"].value_counts().sort_values()
    fig = go.Figure(go.Bar(
        x=counts.values,
        y=counts.index,
        orientation="h",
        marker_color=COLORS["green"],
        marker_opacity=0.85,
        text=counts.values,
        textposition="outside",
    ))
    fig.update_layout(
        **_BASE_LAYOUT,
        title="OM por Fuente de Identificación",
        xaxis=dict(showgrid=True, gridcolor="#30363d"),
        yaxis=dict(showgrid=False),
        height=300,
    )
    return fig


def _empty_fig(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        **_BASE_LAYOUT,
        annotations=[dict(text=msg, showarrow=False, font=dict(color=COLORS["muted"], size=14))],
        height=250,
    )
    return fig
