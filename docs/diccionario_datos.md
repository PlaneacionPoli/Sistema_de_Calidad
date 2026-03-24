# Diccionario de Datos — Reporte_Calidad.xlsx

## Hoja: `Listado de procesos y subproces`

**Fila de encabezado:** 4 (índice 3 en pandas)  
**Registros totales:** ~120 filas (varía según exportación de KAWAK)

---

## Campos de Jerarquía Organizacional

| Campo | Nombre en Excel | Tipo | Valores posibles | Notas |
|---|---|---|---|---|
| `unidad` | UNIDAD | str | Rectoría, Vicerrectoría Académica, Vicerrectoría Administrativa y Financiera, Vicerrectoría de Crecimiento, Vicerrectoría del Estudiante | Forward-fill en ETL |
| `macro` | MACROPROCESO | str | Estratégico, Misional, Apoyo, Evaluación y mejora | Forward-fill en ETL |
| `proceso` | PROCESO | str | Nombre del proceso | Forward-fill en ETL |
| `sub` | SUBPROCESO | str | Nombre del subproceso | Llave mínima del análisis |

---

## Campos de Órdenes de Mejora (OM)

| Campo | Nombre en Excel | Tipo | Valores posibles | Notas |
|---|---|---|---|---|
| `om_num` | OM # | Int64 nullable | Número entero (ej. 418, 449) | Múltiples acciones pueden tener la misma OM |
| `om_accion` | Número de Acción | str | Código numérico (ej. "1663") | Una OM puede tener N acciones |
| `om_desc` | Descripción | str | Texto libre | Descripción completa del hallazgo. Puede superar los 1000 caracteres |
| `om_fecha` | Fecha de Vencimiento OM | datetime | Fecha ISO | NaT si no aplica |
| `om_estado` | Estado OM | str | Vencido, Próximo a vencer, Vigente | Solo estos 3 valores son válidos |
| `om_fuente` | Fuente | str | Auditoría de Tercera Parte, Auditoría Interna - Gestión, Actividades de Seguimiento y Control, Gestión del Cambio, Riesgos, Indicadores, Contexto Institucional DOFA | Origen de la identificación de la OM |

---

## Campos de Documentos

| Campo | Nombre en Excel | Tipo | Valores posibles | Notas |
|---|---|---|---|---|
| `doc_tipo` | Tipo de documento | str | Procedimiento, Manual, Formatos, Instructivo, Política, Caracterización, Reglamento | Tipo dentro del sistema documental |
| `doc_nombre` | Nombre del documento | str | Texto libre | Nombre oficial del documento en KAWAK |
| `doc_accion` | Tipo de Acción | str | Actualizar, Crear | Acción requerida sobre el documento |
| `doc_fecha` | Fecha de vencimiento doc | datetime | Fecha ISO | NaT si no aplica |
| `doc_estado` | Estado doc | str | Vencido, Próximo a vencer | Estado respecto a la fecha de vencimiento |

---

## Campos de Indicadores

> Los campos de indicadores (columnas 15–20) están actualmente vacíos en el reporte.
> Todos los subprocesos se listan en la pestaña "Indicadores" como **sin datos registrados**.

---

## Notas de Calidad de Datos

1. **Celdas fusionadas en Excel:** La tabla usa celdas fusionadas en las columnas jerárquicas. El ETL aplica `ffill()` para propagarlas correctamente.
2. **Múltiples acciones por OM:** Una misma OM puede aparecer en múltiples filas (una por acción). Para el KPI de "OM Vencidas" se deduplica por `(om_num, sub, om_fecha)`.
3. **Filas vacías:** Existen filas donde solo está definida la jerarquía pero sin OM ni documentos. Estas se mantienen para el conteo de subprocesos en el tab de Indicadores.
4. **Proceso con espacios:** El campo `proceso` puede contener espacios trailing. El ETL aplica `.str.strip()`.
