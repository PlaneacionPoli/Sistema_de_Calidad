"""
pages/2_📋_Ficha_Tecnica.py
---------------------------
Ficha técnica completa del proyecto SGC Dashboard.
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
  .ficha-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
  }
  .ficha-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8b949e;
    margin-bottom: 16px;
  }
  .tag {
    display: inline-block;
    background: rgba(30,144,255,0.1);
    color: #1e90ff;
    border: 1px solid rgba(30,144,255,0.3);
    padding: 3px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
  }
</style>
""", unsafe_allow_html=True)

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("# 📋 Ficha Técnica del Proyecto")
st.markdown("**Dashboard Ejecutivo de Gestión de Calidad · POLISIGS**")
st.divider()

# ── 1. Identificación ─────────────────────────────────────────────────────────
st.markdown("### 1. Identificación del Proyecto")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
| Campo | Detalle |
|---|---|
| **Nombre** | Dashboard Ejecutivo SGC |
| **Sistema** | POLISIGS |
| **Versión** | 1.0.0 |
| **Fecha de corte de datos** | Marzo 2026 |
| **Responsable técnico** | Área de Gestión de Calidad |
| **Tipo de proyecto** | Visualización y monitoreo de datos |
""")
with col2:
    st.markdown("""
| Campo | Detalle |
|---|---|
| **Institución** | Politécnico Grancolombiano |
| **Alcance** | Todos los procesos institucionales |
| **Fuente de datos** | KAWAK / Reporte_Calidad.xlsx |
| **Frecuencia de actualización** | Mensual |
| **Despliegue** | Streamlit Cloud |
| **Repositorio** | GitHub (rama `main`) |
""")

st.divider()

# ── 2. Objetivo ───────────────────────────────────────────────────────────────
st.markdown("### 2. Objetivo")
st.info(
    "Proveer una herramienta de visualización ejecutiva para el monitoreo en tiempo real "
    "de los pendientes críticos del Sistema Integrado de Aseguramiento y Gestión para la "
    "Sostenibilidad (POLISIGS), permitiendo identificar Órdenes de Mejora vencidas, "
    "documentos desactualizados y subprocesos sin indicadores gestionados.",
    icon="🎯",
)

st.divider()

# ── 3. Arquitectura del proyecto ──────────────────────────────────────────────
st.markdown("### 3. Arquitectura del Proyecto")

st.code("""
sgc_dashboard/
│
├── app.py                          # Punto de entrada principal (Streamlit)
│
├── pages/                          # Páginas adicionales del dashboard
│   ├── 2_📋_Ficha_Tecnica.py
│   └── 3_📖_Documentacion.py
│
├── src/                            # Código fuente del proyecto
│   ├── etl/
│   │   ├── __init__.py
│   │   └── loader.py               # Carga y transformación del Excel
│   ├── components/
│   │   ├── __init__.py
│   │   ├── kpi_cards.py            # KPIs animados
│   │   ├── sidebar.py              # Filtros en cascada
│   │   ├── om_table.py             # Tabla de OM con expander
│   │   ├── doc_table.py            # Tabla de documentos
│   │   ├── ind_table.py            # Tabla de indicadores
│   │   └── charts.py              # Gráficas Plotly
│   └── utils/
│       ├── __init__.py
│       ├── filters.py              # Lógica de filtrado en cascada
│       └── styling.py              # Helpers de estilo y formateo
│
├── data/
│   └── raw/
│       └── Reporte_Calidad.xlsx    # Archivo fuente (no versionado en Git)
│
├── docs/
│   ├── FICHA_TECNICA.md
│   └── diccionario_datos.md
│
├── .streamlit/
│   └── config.toml                 # Tema dark y configuración del servidor
│
├── requirements.txt                # Dependencias Python
├── .gitignore
└── README.md
""", language="text")

st.divider()

# ── 4. Stack tecnológico ──────────────────────────────────────────────────────
st.markdown("### 4. Stack Tecnológico")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🐍 Backend / ETL**")
    st.markdown("""
- Python 3.11+
- Pandas 2.2
- NumPy 1.26
- OpenPyXL 3.1
""")
with col2:
    st.markdown("**📊 Visualización**")
    st.markdown("""
- Streamlit 1.41
- Plotly 5.24
- HTML/CSS inline
""")
with col3:
    st.markdown("**☁️ Infraestructura**")
    st.markdown("""
- Streamlit Cloud (free tier)
- GitHub (source of truth)
- Git LFS (archivos xlsx)
""")

st.divider()

# ── 5. Diccionario de datos ───────────────────────────────────────────────────
st.markdown("### 5. Diccionario de Datos")
st.caption("Estructura del DataFrame resultante del proceso ETL.")

import pandas as pd

dic = pd.DataFrame([
    ("unidad",     "str",      "Unidad organizacional (ej. Rectoría, Vicerrectoría)"),
    ("macro",      "str",      "Macroproceso institucional (Estratégico, Misional, Apoyo, Evaluación)"),
    ("proceso",    "str",      "Nombre del proceso dentro del macroproceso"),
    ("sub",        "str",      "Subproceso específico"),
    ("om_num",     "Int64",    "Número de la Orden de Mejora (nullable integer)"),
    ("om_accion",  "str",      "Código de la acción asociada a la OM"),
    ("om_desc",    "str",      "Descripción completa del hallazgo u oportunidad de mejora"),
    ("om_fecha",   "datetime", "Fecha límite de cumplimiento de la OM"),
    ("om_estado",  "str",      "Estado: Vencido | Próximo a vencer | Vigente"),
    ("om_fuente",  "str",      "Fuente que originó la OM (Auditoría, Riesgos, Indicadores, etc.)"),
    ("doc_tipo",   "str",      "Tipo de documento (Procedimiento, Manual, Formato, Política, etc.)"),
    ("doc_nombre", "str",      "Nombre del documento que requiere actualización"),
    ("doc_accion", "str",      "Acción requerida sobre el documento (Actualizar, Crear)"),
    ("doc_fecha",  "datetime", "Fecha límite de actualización del documento"),
    ("doc_estado", "str",      "Estado del documento: Vencido | Próximo a vencer"),
], columns=["Campo", "Tipo", "Descripción"])

st.dataframe(dic, use_container_width=True, hide_index=True)

st.divider()

# ── 6. Reglas de negocio ──────────────────────────────────────────────────────
st.markdown("### 6. Reglas de Negocio y Criterios ETL")

st.markdown("""
| Regla | Descripción |
|---|---|
| **Deduplicación OM** | Se deduplicacion por la clave compuesta `(om_num, sub, om_fecha)` para evitar conteo doble de acciones múltiples sobre una misma OM |
| **Forward-fill jerárquico** | Las columnas `unidad`, `macro`, `proceso` y `sub` se propagan hacia abajo cuando están vacías (estructura de tabla anidada en Excel) |
| **Validación de estados** | Solo se reconocen `Vencido`, `Próximo a vencer` y `Vigente`; cualquier otro valor se trata como `None` |
| **Filtros en cascada** | Al seleccionar Unidad, los dropdowns de Macroproceso, Proceso y Subproceso se restringen a las opciones que existen en esa unidad |
| **Caché de datos** | El DataFrame se almacena en caché durante 1 hora (`ttl=3600`) para evitar relecturas del Excel en cada interacción |
| **Hoja fuente** | Se lee exclusivamente la hoja `Listado de procesos y subproces`, fila 4 como encabezado (índice 3) |
""")

st.divider()

# ── 7. KPIs definidos ─────────────────────────────────────────────────────────
st.markdown("### 7. KPIs del Dashboard")

st.markdown("""
| KPI | Fórmula |
|---|---|
| **OM Vencidas** | Count distinct `(om_num, sub, om_fecha)` donde `om_estado == 'Vencido'` |
| **Documentos Vencidos** | Count filas donde `doc_nombre IS NOT NULL AND doc_estado == 'Vencido'` |
| **Próximos a Vencer** | Count filas donde `om_estado == 'Próximo a vencer'` + `doc_estado == 'Próximo a vencer'` |
| **Subprocesos Afectados** | Count distinct `sub` donde existe al menos una alerta activa (OM o Doc) |
""")

st.divider()

# ── 8. Instrucciones de despliegue ────────────────────────────────────────────
st.markdown("### 8. Instrucciones de Despliegue en Streamlit Cloud")

st.markdown("""
**Paso 1 — Preparar el repositorio en GitHub**
```bash
git init
git add .
git commit -m "feat: initial SGC dashboard"
git remote add origin https://github.com/<usuario>/sgc_dashboard.git
git push -u origin main
```

**Paso 2 — Subir el archivo fuente** *(si no usa Git LFS)*
```bash
# El archivo xlsx se puede subir manualmente a GitHub
# o configurar Git LFS:
git lfs install
git lfs track "*.xlsx"
git add .gitattributes data/raw/Reporte_Calidad.xlsx
git commit -m "feat: add source data file"
git push
```

**Paso 3 — Conectar en Streamlit Cloud**
1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Hacer clic en **New app**
3. Seleccionar el repositorio y la rama `main`
4. Configurar **Main file path**: `app.py`
5. Hacer clic en **Deploy**

**Paso 4 — Actualizar datos**

Para actualizar el archivo fuente basta con reemplazar `data/raw/Reporte_Calidad.xlsx`
en el repositorio y hacer push. Streamlit Cloud detectará el cambio y recargará la app.
""")

st.divider()

# ── 9. Contacto ───────────────────────────────────────────────────────────────
st.markdown("### 9. Control de Versiones")

st.markdown("""
| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | Marzo 2026 | Versión inicial: KPIs, 3 tablas, 4 gráficas, filtros en cascada, ficha técnica |
""")
