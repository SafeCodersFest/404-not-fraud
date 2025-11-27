# 404-not-fraud

Herramientas para exploración, perfilado y scoring de riesgo de fraude y siniestros.

## 1. Script de perfil y unificación

`scripts/data_loader.py`:
- Enumera todos los CSV en `dataset/`.
- Genera un perfil (tipos, faltantes, duplicados, muestra) por archivo.
- Unifica todos los CSV en un único dataset añadiendo la columna `__source_file`.
- Exporta el resultado en formato Parquet (o CSV) y guarda un reporte Markdown.

### Requisitos
Instalar dependencias:
```pwsh
python -m pip install -r requirements.txt
```

### Uso
```pwsh
python scripts/data_loader.py --dataset-dir dataset --output dataset/combined_dataset.parquet --export-format parquet --report reports/dataset_profile.md
```
Opcionales:
- `--max-profile-rows` (default 20000)
- `--export-format csv`

Ejemplo CSV:
```pwsh
python scripts/data_loader.py --export-format csv --output dataset/combined_dataset.csv
```

### Salidas
- `reports/dataset_profile.md`
- `dataset/combined_dataset.parquet` (o `.csv`)

## 2. Motor de reglas y scoring

`scripts/risk_scoring.py` aplica reglas definidas en `rules_engine.md` para asignar un puntaje de riesgo por fila y por nombre completo.

### Preparación: añadir nombres sintéticos
Si el dataset no tiene columnas de nombres, usar:
```pwsh
python scripts/add_names.py --input dataset/fraud_oracle.csv --output dataset/fraud_oracle_names.csv
```
Esto añade columnas `Nombre` y `Apellido` aleatorias.

### Archivo de reglas `rules_engine.md`
Tabla con columnas: `regla | score | descripcion`. Ejemplo:
```
| regla | score | descripcion |
| Age > 65 | 15 | Edad avanzada |
| duplicate(PolicyNumber) | 20 | Póliza repetida |
| full_name in ["JUAN PEREZ","MARIA GOMEZ"] | 25 | Watchlist |
```
Sintaxis soportada: comparaciones (`> < >= <= ==`), `in [..]`, `AND`, `||`, `duplicate(col)`, `high_cardinality(col)`, `col is not null`, `full_name in [...]`.

### Watchlist externa
Crear `watchlist.csv` con columnas `full_name,watchlist_score,reason`:
```csv
full_name,watchlist_score,reason
JUAN PEREZ,25,Múltiples reclamos sospechosos
MARIA GOMEZ,30,Fraude confirmado
```

### Uso del scoring
Ejecutar cálculo general:
```pwsh
python scripts/risk_scoring.py --dataset-dir dataset --rules rules_engine.md
```
Con watchlist:
```pwsh
python scripts/risk_scoring.py --dataset-dir dataset --rules rules_engine.md --watchlist watchlist.csv
```
Consulta de un nombre específico:
```pwsh
python scripts/risk_scoring.py --dataset-dir dataset --rules rules_engine.md --watchlist watchlist.csv --query-name "JUAN PEREZ"
```
Exportar resultados fila a CSV:
```pwsh
python scripts/risk_scoring.py --dataset-dir dataset --rules rules_engine.md --export results/risk_rows.csv --export-format csv
```

### Salida esperada (resumen)
- Número de reglas cargadas e ignoradas.
- Lista de activaciones: regla, score, count.
- Si `--query-name`: objeto con `risk_score`, `risk_level`, reglas activadas para ese nombre.

Ejemplo de salida para "JUAN PEREZ":
```
{'full_name': 'JUAN PEREZ', 'risk_score': 3267, 'risk_level': 'Crítico', 'records_count': 35}
```

### Escala sugerida
- 0-19: Bajo | 20-39: Medio | 40-59: Alto | 60+: Crítico

### Próximos pasos sugeridos
1. Ajustar reglas con métricas reales de fraude.
2. Añadir columnas de nombres si faltan para evaluación nominal.
3. Integrar un modelo supervisado y comparar vs heurística.

## 3. Generación de datos sintéticos

### Datos con perfiles controlados (RECOMENDADO)
`scripts/generate_controlled_data.py` genera datasets con 3 perfiles específicos:

```pwsh
python scripts/generate_controlled_data.py --output dataset_final
```

Perfiles generados:
- **Jan Pereira** (100 asegurados): Alto riesgo - muchos siniestros costosos, vehículos antiguos, en watchlist
- **Juan José Pereira** (50 asegurados): Bajo riesgo - pocos siniestros baratos, vehículos nuevos, NO en watchlist  
- **Antonio Pereira** (50 asegurados): Bajo riesgo - casi sin siniestros, vehículos nuevos, NO en watchlist
- **800 asegurados genéricos**: Distribución normal de riesgo

### Datos sintéticos aleatorios
Para pruebas generales:
```pwsh
python scripts/generate_synthetic_data.py --output dataset_synthetic --asegurados 1000 --siniestros 2000
```

### Enriquecimiento de datos existentes
Para añadir nombres a CSVs existentes:
```pwsh
python scripts/enrich_data.py --input-dir dataset --output-dir dataset_enriched --high-risk-count 100 --low-risk-count 50
```

## 4. Validación

Verificar estructura y distribución de datos:
```pwsh
python scripts/validate_data.py
```

## Resultados de Prueba

Ver `RESULTADOS.md` para análisis detallado de scores y comparaciones.

**Resumen de scores (dataset_final):**
- **Jan Pereira**: 97,196 puntos (CRÍTICO) - 739 siniestros, en watchlist
- **Juan José Pereira**: 3,750 puntos (mucho menor) - 16 siniestros, NO en watchlist
- **Antonio Pereira**: 3,750 puntos (mucho menor) - 4 siniestros, NO en watchlist

**Diferencia: Jan Pereira tiene 26x más score que Juan José/Antonio.**

---
Actualizado automáticamente el 27-11-2025.
