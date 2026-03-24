# 📊 SGC Dashboard — POLISIGS

Dashboard ejecutivo para el monitoreo de pendientes críticos del **Sistema Integrado de Aseguramiento y Gestión para la Sostenibilidad (POLISIGS)** del Politécnico Grancolombiano.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 🚀 Inicio rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/<usuario>/sgc_dashboard.git
cd sgc_dashboard
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Colocar el archivo fuente
```
data/raw/Reporte_Calidad.xlsx
```

### 4. Ejecutar localmente
```bash
streamlit run app.py
```

---

## 📁 Estructura del proyecto

```
sgc_dashboard/
├── app.py                   # Punto de entrada Streamlit
├── pages/
│   ├── 2_📋_Ficha_Tecnica.py
│   └── 3_📖_Documentacion.py
├── src/
│   ├── etl/
│   │   └── loader.py        # Carga y limpieza del Excel
│   ├── components/
│   │   ├── kpi_cards.py
│   │   ├── sidebar.py       # Filtros en cascada
│   │   ├── om_table.py
│   │   ├── doc_table.py
│   │   ├── ind_table.py
│   │   └── charts.py        # Gráficas Plotly
│   └── utils/
│       ├── filters.py
│       └── styling.py
├── data/
│   └── raw/
│       └── Reporte_Calidad.xlsx
├── .streamlit/
│   └── config.toml
└── requirements.txt
```

---

## ☁️ Despliegue en Streamlit Cloud

1. Subir el repositorio a GitHub (incluir `data/raw/Reporte_Calidad.xlsx`).
2. Ir a [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Seleccionar repositorio, rama `main` y archivo principal `app.py`.
4. Clic en **Deploy** — listo en ~2 minutos.

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework UI | Streamlit 1.41 |
| ETL / Datos | Pandas 2.2 + OpenPyXL |
| Visualización | Plotly 5.24 |
| Despliegue | Streamlit Cloud |

---

## 📋 Funcionalidades

- ✅ **4 KPIs** animados: OM Vencidas, Docs Vencidos, Próximos a Vencer, Subprocesos Afectados
- ✅ **Filtros en cascada**: Unidad → Macroproceso → Proceso → Subproceso
- ✅ **Tab OM Vencidas**: tabla deduplicada con descripción completa expandible
- ✅ **Tab Documentos**: tabla con colores por estado de vencimiento
- ✅ **Tab Indicadores**: subprocesos sin datos con conteo de alertas
- ✅ **Tab Gráficas**: 4 visualizaciones Plotly interactivas
- ✅ **Ficha Técnica**: documentación completa dentro del mismo app
- ✅ **Caché de 1 hora** para rendimiento óptimo

---

## 🔄 Actualización de datos

Para actualizar los datos, reemplace `data/raw/Reporte_Calidad.xlsx` con el nuevo
reporte exportado de KAWAK y haga `git push`. La caché se invalida automáticamente.
