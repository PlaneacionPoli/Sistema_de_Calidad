# Ficha Técnica — Dashboard Ejecutivo SGC / POLISIGS

---

## 1. Identificación del Proyecto

| Campo | Detalle |
|---|---|
| **Nombre del proyecto** | Dashboard Ejecutivo de Gestión de Calidad |
| **Sistema** | POLISIGS (Sistema Integrado de Aseguramiento y Gestión para la Sostenibilidad) |
| **Institución** | Politécnico Grancolombiano |
| **Versión** | 1.0.0 |
| **Fecha de corte de datos** | Marzo 2026 |
| **Responsable técnico** | Área de Gestión de Calidad |
| **Tipo de proyecto** | Ciencia de datos aplicada — Visualización y monitoreo |
| **Fuente de datos primaria** | KAWAK → exportación `Reporte_Calidad.xlsx` |
| **Frecuencia de actualización** | Mensual (o cuando se exporte un nuevo reporte) |
| **URL de despliegue** | Streamlit Cloud (share.streamlit.io) |

---

## 2. Objetivo

Proveer una herramienta de visualización ejecutiva para el monitoreo en tiempo real
de los pendientes críticos del Sistema Integrado POLISIGS, permitiendo identificar:

- **Órdenes de Mejora (OM)** vencidas o próximas a vencer
- **Documentos institucionales** que requieren actualización urgente
- **Subprocesos** sin indicadores gestionados en el sistema
- Distribución de alertas por unidad, macroproceso y fuente de identificación

---

## 3. Arquitectura del Proyecto

```
sgc_dashboard/
│
├── app.py                          # Punto de entrada principal (Streamlit)
│
├── pages/
│   ├── 2_📋_Ficha_Tecnica.py       # Esta ficha técnica (versión interactiva)
│   └── 3_📖_Documentacion.py       # Guía de mantenimiento
│
├── src/
│   ├── etl/
│   │   ├── __init__.py
│   │   └── loader.py               # Carga, limpieza y KPIs
│   ├── components/
│   │   ├── __init__.py
│   │   ├── kpi_cards.py
│   │   ├── sidebar.py
│   │   ├── om_table.py
│   │   ├── doc_table.py
│   │   ├── ind_table.py
│   │   └── charts.py
│   └── utils/
│       ├── __init__.py
│       ├── filters.py
│       └── styling.py
│
├── data/
│   └── raw/
│       └── Reporte_Calidad.xlsx    # Archivo fuente
│
├── docs/
│   ├── FICHA_TECNICA.md            # Este documento
│   └── diccionario_datos.md
│
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 4. Stack Tecnológico

| Capa | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.11+ |
| Framework UI | Streamlit | 1.41.1 |
| Manipulación de datos | Pandas | 2.2.3 |
| Lectura de Excel | OpenPyXL | 3.1.5 |
| Álgebra numérica | NumPy | 1.26.4 |
| Visualización | Plotly | 5.24.1 |
| Control de versiones | Git + GitHub | — |
| Despliegue | Streamlit Cloud | Free Tier |

---

## 5. Diccionario de Datos

### Hoja fuente: `Listado de procesos y subproces`

| # Col | Campo interno | Tipo | Descripción |
|---|---|---|---|
| 0 | `unidad` | str | Unidad organizacional |
| 1 | `macro` | str | Macroproceso institucional |
| 2 | `proceso` | str | Proceso dentro del macroproceso |
| 3 | `sub` | str | Subproceso específico |
| 4 | `om_num` | Int64 | Número de la Orden de Mejora |
| 5 | `om_accion` | str | Código de acción |
| 6 | `om_desc` | str | Descripción completa del hallazgo |
| 7 | `om_fecha` | datetime | Fecha límite de la OM |
| 8 | `om_estado` | str | Vencido \| Próximo a vencer \| Vigente |
| 9 | `om_fuente` | str | Fuente de identificación de la OM |
| 10 | `doc_tipo` | str | Tipo de documento |
| 11 | `doc_nombre` | str | Nombre del documento |
| 12 | `doc_accion` | str | Acción requerida (Actualizar \| Crear) |
| 13 | `doc_fecha` | datetime | Fecha límite del documento |
| 14 | `doc_estado` | str | Vencido \| Próximo a vencer |

---

## 6. Reglas de Negocio

| Regla | Descripción |
|---|---|
| **Deduplicación OM** | Clave compuesta `(om_num, sub, om_fecha)` para evitar doble conteo |
| **Forward-fill jerárquico** | `unidad`, `macro`, `proceso`, `sub` se propagan hacia abajo |
| **Validación de estados** | Valores fuera del catálogo se convierten a `None` |
| **Filtros en cascada** | Cada nivel de filtro restringe las opciones del siguiente |
| **Caché de datos** | TTL de 3600 segundos en `@st.cache_data` |
| **Hoja fuente** | Única hoja `Listado de procesos y subproces`, header en fila 4 (índice 3) |

---

## 7. KPIs Definidos

| KPI | Fórmula |
|---|---|
| **OM Vencidas** | `COUNT DISTINCT (om_num, sub, om_fecha) WHERE om_estado = 'Vencido'` |
| **Documentos Vencidos** | `COUNT rows WHERE doc_nombre IS NOT NULL AND doc_estado = 'Vencido'` |
| **Próximos a Vencer** | `COUNT (om_estado='Próximo a vencer') + COUNT (doc_estado='Próximo a vencer')` |
| **Subprocesos Afectados** | `COUNT DISTINCT sub WHERE om_estado IS NOT NULL OR doc_estado IS NOT NULL` |

---

## 8. Funcionalidades del Dashboard

| Funcionalidad | Descripción |
|---|---|
| KPI Cards | 4 métricas en tiempo real respondiendo a filtros |
| Filtros en cascada | Unidad → Macroproceso → Proceso → Subproceso |
| Tab OM Vencidas | Tabla deduplicada + descripción completa expandible por fila |
| Tab Documentos | Tabla coloreada por estado con todas las columnas relevantes |
| Tab Indicadores | Agrupación por subproceso con conteo de alertas |
| Tab Gráficas | 4 visualizaciones Plotly interactivas (hover, zoom, descarga PNG) |
| Ficha Técnica | Página dedicada dentro del mismo app |
| Documentación | Guía de mantenimiento y extensión |

---

## 9. Instrucciones de Despliegue

### Local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud

1. Repositorio en GitHub con `data/raw/Reporte_Calidad.xlsx` incluido.
2. [share.streamlit.io](https://share.streamlit.io) → New App.
3. Repo: `<usuario>/sgc_dashboard` | Branch: `main` | File: `app.py`.
4. Deploy → URL pública generada en ~2 minutos.

---

## 10. Control de Versiones

| Versión | Fecha | Responsable | Cambios |
|---|---|---|---|
| 1.0.0 | Marzo 2026 | Área SGC | Versión inicial del dashboard |
