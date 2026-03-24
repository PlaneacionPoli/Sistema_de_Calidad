"""
utils/styling.py
----------------
Helpers de estilo para tablas y badges en Streamlit.
"""
from __future__ import annotations

import pandas as pd


# Paleta de colores base
COLORS = {
    "red":    "#ff4757",
    "orange": "#ffa502",
    "green":  "#2ed573",
    "blue":   "#1e90ff",
    "purple": "#a855f7",
    "muted":  "#8b949e",
}


def badge_html(text: str, color_key: str = "red") -> str:
    """Genera un badge HTML coloreado."""
    color = COLORS.get(color_key, COLORS["muted"])
    bg = color + "22"
    border = color + "55"
    return (
        f'<span style="background:{bg};color:{color};border:1px solid {border};'
        f'padding:2px 10px;border-radius:6px;font-size:12px;font-weight:700;'
        f'white-space:nowrap">{text}</span>'
    )


def estado_badge(estado: str | None) -> str:
    """Devuelve badge HTML según el estado."""
    if estado == "Vencido":
        return badge_html("Vencido", "red")
    if estado == "Próximo a vencer":
        return badge_html("Próximo", "orange")
    return "—"


def fmt_date(ts) -> str:
    """Formatea timestamp a dd/mm/yyyy."""
    if pd.isna(ts):
        return "—"
    return pd.Timestamp(ts).strftime("%d/%m/%Y")


def color_estado(val: str) -> str:
    """Para uso en df.style.applymap."""
    if val == "Vencido":
        return f"color: {COLORS['red']}; font-weight: 600"
    if val == "Próximo a vencer":
        return f"color: {COLORS['orange']}; font-weight: 600"
    return ""
