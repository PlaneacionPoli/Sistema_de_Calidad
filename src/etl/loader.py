"""
etl/loader.py
-------------
Carga y transforma el archivo fuente Reporte_Calidad.xlsx
en un DataFrame limpio y estructurado para el dashboard.

Columnas esperadas en la hoja 'Listado de procesos y subproces':
  0: UNIDAD
  1: MACROPROCESO
  2: PROCESO
  3: SUBPROCESO
  4: OM #
  5: Número de Acción
  6: Descripción
  7: Fecha de Vencimiento OM
  8: Estado OM
  9: Fuente
 10: Tipo de documento
 11: Nombre del documento
 12: Tipo de Acción
 13: Fecha de vencimiento doc
 14: Estado doc
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
SHEET_NAME = "Listado de procesos y subproces"
HEADER_ROW = 3          # fila 4 en Excel (0-indexado)
DATA_PATH = Path(__file__).parents[2] / "data" / "raw" / "Reporte Calidad.xlsx"

COL_MAP = {
    0:  "unidad",
    1:  "macro",
    2:  "proceso",
    3:  "sub",
    4:  "om_num",
    5:  "om_accion",
    6:  "om_desc",
    7:  "om_fecha",
    8:  "om_estado",
    9:  "om_fuente",
    10: "doc_tipo",
    11: "doc_nombre",
    12: "doc_accion",
    13: "doc_fecha",
    14: "doc_estado",
}

ESTADO_OM_VALIDOS  = {"Vencido", "Próximo a vencer", "Vigente"}
ESTADO_DOC_VALIDOS = {"Vencido", "Próximo a vencer", "Vigente"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _clean_str(series: pd.Series) -> pd.Series:
    """Quita espacios, normaliza None/NaN a None."""
    return series.astype(str).str.strip().replace({"nan": None, "None": None, "": None})


def _clean_date(series: pd.Series) -> pd.Series:
    """Convierte a datetime, fuerza errores a NaT."""
    return pd.to_datetime(series, errors="coerce")


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------
def load_data(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """
    Lee el Excel, aplica limpieza y devuelve un DataFrame.

    Parameters
    ----------
    path : Path | str
        Ruta al archivo xlsx. Por defecto apunta a data/raw/Reporte_Calidad.xlsx.

    Returns
    -------
    pd.DataFrame con columnas definidas en COL_MAP.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo fuente: {path}")

    logger.info("Cargando datos desde %s", path)

    raw = pd.read_excel(
        path,
        sheet_name=SHEET_NAME,
        header=HEADER_ROW,
        dtype=str,
    )

    # Seleccionar solo las columnas definidas en COL_MAP
    cols_idx = list(COL_MAP.keys())
    raw = raw.iloc[:, cols_idx].copy()
    raw.columns = list(COL_MAP.values())

    # ---------- Limpieza de texto ----------
    str_cols = [c for c in raw.columns if c not in ("om_fecha", "doc_fecha")]
    for col in str_cols:
        raw[col] = _clean_str(raw[col])

    # ---------- Limpieza de fechas ----------
    raw["om_fecha"]  = _clean_date(raw["om_fecha"])
    raw["doc_fecha"] = _clean_date(raw["doc_fecha"])

    # ---------- Tipos numéricos ----------
    raw["om_num"] = pd.to_numeric(raw["om_num"], errors="coerce").astype("Int64")

    # ---------- Filtrar filas completamente vacías ----------
    key_cols = ["unidad", "sub"]
    raw = raw.dropna(subset=key_cols, how="all")

    # ---------- Forward-fill jerárquico (unidad, macro, proceso, sub) ----------
    hier_cols = ["unidad", "macro", "proceso", "sub"]
    raw[hier_cols] = raw[hier_cols].ffill()

    # ---------- Proceso: quitar espacios residuales ----------
    raw["proceso"] = raw["proceso"].str.strip()

    # ---------- Validar estados conocidos ----------
    raw.loc[~raw["om_estado"].isin(ESTADO_OM_VALIDOS),   "om_estado"]  = None
    raw.loc[~raw["doc_estado"].isin(ESTADO_DOC_VALIDOS), "doc_estado"] = None

    logger.info("Datos cargados: %d filas, %d columnas", len(raw), len(raw.columns))
    return raw


# ---------------------------------------------------------------------------
# KPIs derivados
# ---------------------------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    """Calcula los KPIs principales sobre el DataFrame filtrado."""
    seen: set = set()
    om_vencidas = 0
    for _, r in df[df["om_estado"] == "Vencido"].iterrows():
        key = (r["om_num"], r["sub"], r["om_fecha"])
        if key not in seen:
            seen.add(key)
            om_vencidas += 1

    doc_vencidos  = df[df["doc_estado"] == "Vencido"]["doc_nombre"].notna().sum()
    proximos      = (
        (df["om_estado"]  == "Próximo a vencer").sum() +
        (df["doc_estado"] == "Próximo a vencer").sum()
    )
    sub_afectados = df[
        df["om_estado"].notna() | df["doc_estado"].notna()
    ]["sub"].nunique()

    return {
        "om_vencidas":    int(om_vencidas),
        "doc_vencidos":   int(doc_vencidos),
        "proximos":       int(proximos),
        "sub_afectados":  int(sub_afectados),
    }
