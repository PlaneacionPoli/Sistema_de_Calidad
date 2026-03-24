"""
pages/3_📖_Documentacion.py
---------------------------
Documentación técnica interna del proyecto.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import streamlit as st

st.markdown("""
<style>
  #MainMenu, footer { visibility: hidden; }
  .block-container { padding-top: 1.5rem; }
  code { font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📖 Documentación Técnica")
st.caption("Guía de mantenimiento y extensión del Dashboard SGC")
st.divider()

# ── Estructura ETL ────────────────────────────────────────────────────────────
st.markdown("## Módulo ETL (`src/etl/loader.py`)")

st.markdown("""
El módulo ETL es el corazón del proyecto. Se encarga de:

1. **Leer** el archivo `data/raw/Reporte_Calidad.xlsx` usando `pandas.read_excel`.
2. **Renombrar** columnas posicionales según el `COL_MAP` definido internamente.
3. **Limpiar** texto (strip, None normalization), fechas (coerce a NaT) y números.
4. **Propagar** valores jerárquicos vacíos (`ffill`) en las columnas `unidad`, `macro`, `proceso`, `sub`.
5. **Validar** que los estados OM y Doc sean valores conocidos.
6. **Devolver** un `pd.DataFrame` limpio con 15 columnas tipadas.

### Cómo actualizar el Excel fuente

Reemplace el archivo en `data/raw/Reporte_Calidad.xlsx` manteniendo la misma
estructura de hoja y columnas. Si Streamlit Cloud está activo, la caché se
invalida automáticamente tras 1 hora, o puede forzar la recarga con:
```python
st.cache_data.clear()
```
""")

with st.expander("Ver código completo de `load_data()`"):
    st.code("""
def load_data(path=DATA_PATH):
    raw = pd.read_excel(path, sheet_name=SHEET_NAME, header=HEADER_ROW, dtype=str)
    raw = raw.iloc[:, list(COL_MAP.keys())].copy()
    raw.columns = list(COL_MAP.values())

    # Limpieza texto
    for col in [c for c in raw.columns if c not in ("om_fecha","doc_fecha")]:
        raw[col] = raw[col].astype(str).str.strip().replace({"nan":None,"":None})

    # Fechas y números
    raw["om_fecha"]  = pd.to_datetime(raw["om_fecha"],  errors="coerce")
    raw["doc_fecha"] = pd.to_datetime(raw["doc_fecha"], errors="coerce")
    raw["om_num"]    = pd.to_numeric(raw["om_num"], errors="coerce").astype("Int64")

    # Forward-fill jerárquico
    raw[["unidad","macro","proceso","sub"]] = raw[["unidad","macro","proceso","sub"]].ffill()

    # Validar estados
    raw.loc[~raw["om_estado"].isin(ESTADO_OM_VALIDOS),   "om_estado"]  = None
    raw.loc[~raw["doc_estado"].isin(ESTADO_DOC_VALIDOS), "doc_estado"] = None

    return raw
""", language="python")

st.divider()

# ── Filtros en cascada ────────────────────────────────────────────────────────
st.markdown("## Filtros en Cascada (`src/utils/filters.py`)")

st.markdown("""
La función `get_cascade_options()` recalcula las opciones disponibles en cada
dropdown según lo que ya se haya seleccionado en los niveles superiores.

El flujo es:
```
Unidad ──► restringe ──► Macroproceso
                    ──► restringe ──► Proceso
                                ──► restringe ──► Subproceso
```

Esto evita que el usuario pueda seleccionar combinaciones que no existen en los datos.

La función `apply_filters()` toma el DataFrame completo y los cuatro valores seleccionados,
y devuelve el subconjunto filtrado que alimenta todos los componentes visuales.
""")

st.divider()

# ── Componentes ───────────────────────────────────────────────────────────────
st.markdown("## Componentes Visuales (`src/components/`)")

componentes = {
    "kpi_cards.py": "Renderiza las 4 métricas principales usando `st.metric`. Recibe el dict de KPIs calculados por `compute_kpis()`.",
    "sidebar.py": "Construye los 4 selectores en cascada dentro del sidebar. Devuelve un dict `{unidad, macro, proceso, sub}` con los valores seleccionados (None si no se eligió nada).",
    "om_table.py": "Tabla de OM con deduplicación, ordenamiento por urgencia y un `st.expander` por fila para mostrar la descripción completa.",
    "doc_table.py": "Tabla de documentos pendientes usando `st.dataframe` con colores condicionales por estado (Vencido = rojo, Próximo = naranja).",
    "ind_table.py": "Agrupa por subproceso y cuenta alertas de OM y documentos. Muestra tabla con `st.dataframe` con colores.",
    "charts.py": "Cuatro gráficas Plotly: barras horizontales de OM por unidad, dona de docs por estado, barras apiladas de alertas por macroproceso y barras de OM por fuente.",
}

for nombre, desc in componentes.items():
    with st.expander(f"📄 `{nombre}`"):
        st.markdown(desc)

st.divider()

# ── Cómo agregar una nueva gráfica ───────────────────────────────────────────
st.markdown("## Cómo Agregar una Nueva Gráfica")

st.code("""
# 1. En src/components/charts.py, agregue una nueva función:
def chart_mi_nueva_grafica(df: pd.DataFrame) -> go.Figure:
    # ... lógica plotly ...
    return fig

# 2. Expórtela en src/components/__init__.py:
from .charts import chart_mi_nueva_grafica

# 3. Úsela en app.py dentro del tab_charts:
with tab_charts:
    st.plotly_chart(chart_mi_nueva_grafica(df), use_container_width=True)
""", language="python")

st.divider()

# ── Cómo agregar una nueva página ────────────────────────────────────────────
st.markdown("## Cómo Agregar una Nueva Página")

st.markdown("""
Streamlit detecta automáticamente los archivos en la carpeta `pages/`.
La convención de nombre es:

```
pages/N_🔤_Nombre_Pagina.py
```

Donde `N` es el número de orden, el emoji es opcional y el nombre usa guiones bajos.
Cada archivo debe incluir `st.set_page_config()` al inicio.
""")

st.divider()

# ── FAQ ───────────────────────────────────────────────────────────────────────
st.markdown("## Preguntas Frecuentes")

with st.expander("¿Cómo forzar la recarga de los datos sin esperar la caché?"):
    st.markdown("""
En Streamlit Cloud, puede agregar un botón en el sidebar:
```python
if st.sidebar.button("🔄 Recargar datos"):
    st.cache_data.clear()
    st.rerun()
```
""")

with st.expander("¿Qué pasa si cambia la estructura del Excel?"):
    st.markdown("""
Actualice el diccionario `COL_MAP` en `src/etl/loader.py` mapeando el nuevo índice de columna
al nombre interno. Si cambia la fila de encabezado, ajuste la constante `HEADER_ROW`.
""")

with st.expander("¿Cómo desplegar en un servidor propio en lugar de Streamlit Cloud?"):
    st.markdown("""
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Para producción se recomienda usar `nginx` como reverse proxy
y `supervisor` o `systemd` para mantener el proceso activo.
""")
