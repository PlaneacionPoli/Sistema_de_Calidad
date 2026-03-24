"""
utils/filters.py
----------------
Lógica de filtrado en cascada para los selectores del sidebar.
"""
from __future__ import annotations

import pandas as pd


def get_cascade_options(
    df: pd.DataFrame,
    unidad: str | None,
    macro: str | None,
    proceso: str | None,
) -> dict[str, list[str]]:
    """
    Dado el estado actual de los tres filtros superiores, devuelve
    las opciones válidas para cada nivel.

    Returns
    -------
    dict con claves: 'unidades', 'macros', 'procesos', 'subs'
    """
    mask_u = df["unidad"] == unidad if unidad else pd.Series(True, index=df.index)
    mask_m = df["macro"]  == macro  if macro   else pd.Series(True, index=df.index)
    mask_p = df["proceso"] == proceso if proceso else pd.Series(True, index=df.index)

    unidades = sorted(df["unidad"].dropna().unique().tolist())
    macros   = sorted(df.loc[mask_u, "macro"].dropna().unique().tolist())
    procesos = sorted(df.loc[mask_u & mask_m, "proceso"].dropna().unique().tolist())
    subs     = sorted(df.loc[mask_u & mask_m & mask_p, "sub"].dropna().unique().tolist())

    return {
        "unidades": unidades,
        "macros":   macros,
        "procesos": procesos,
        "subs":     subs,
    }


def apply_filters(
    df: pd.DataFrame,
    unidad:  str | None = None,
    macro:   str | None = None,
    proceso: str | None = None,
    sub:     str | None = None,
) -> pd.DataFrame:
    """Filtra el DataFrame según los criterios seleccionados."""
    mask = pd.Series(True, index=df.index)
    if unidad:  mask &= df["unidad"]  == unidad
    if macro:   mask &= df["macro"]   == macro
    if proceso: mask &= df["proceso"] == proceso
    if sub:     mask &= df["sub"]     == sub
    return df[mask].copy()
