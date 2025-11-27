# Motor de reglas de riesgo de fraude / siniestros

Formato de la tabla: cada fila define una regla. La columna `regla` es una expresión simple evaluada sobre cada registro del dataset unificado. La columna `score` es el puntaje (entero) que se suma si la regla se cumple para ese registro.

Sintaxis soportada (lado `regla`):
- Comparaciones numéricas: `Age > 60`, `DriverRating <= 2`
- Igualdad textual exacta: `PolicyType == "Sport - Collision"`
- Contención en lista: `Make in ["Honda","Ford"]`
- Presencia de valor (no nulo): `PoliceReportFiled is not null`
- Duplicados por columna: `duplicate(PolicyNumber)`
- Cardinalidad alta de columna: `high_cardinality(PolicyNumber)`
- Combinación AND: `Age > 50 AND Make == "Ford"`
- Combinación OR (usa ||): `AccidentArea == "Rural" || Age > 65`
- Watchlist de nombres completos: `full_name in ["JUAN PEREZ","MARIA GOMEZ"]` (concatena `Nombre`+`Apellido` o `first_name`+`last_name` si existen)
- **Watchlist externa**: usar el argumento `--watchlist watchlist.csv` para cargar nombres con scores personalizados desde archivo externo (columnas: full_name, watchlist_score, reason)

Reglas que hacen referencia a columnas inexistentes se ignoran y se registran en el reporte.

Tabla de reglas inicial (editar según necesidades):

| regla | score | descripcion |
|-------|-------|-------------|
| Age > 65 | 15 | Edad avanzada aumenta riesgo potencial |
| DriverRating <= 2 | 10 | Conductor con baja calificación |
| PolicyType == "Sport - Collision" | 8 | Tipo de póliza con mayor frecuencia de fraude histórico |
| Make in ["Honda","Ford"] | 5 | Marcas con mayor incidencia estadística (ejemplo) |
| AccidentArea == "Urban" AND Age < 25 | 12 | Jóvenes en zonas urbanas |
| duplicate(PolicyNumber) | 20 | Número de póliza repetido |
| PastNumberOfClaims == "more than 30" | 18 | Historial extremo de reclamos |
| Days_Policy_Claim == "more than 30" | 7 | Reclamo tardío |
| PoliceReportFiled == "No" AND WitnessPresent == "No" | 10 | Sin validación externa |
| high_cardinality(PolicyNumber) | 4 | Posible intento de ofuscación si demasiado único |
| full_name in ["JUAN PEREZ","MARIA GOMEZ"] | 25 | Nombres en lista de vigilancia |
| Age == 0 | 30 | Edad inválida declarada |
| VehiclePrice == "more than 69000" AND AgeOfVehicle == "new" | 14 | Vehículo nuevo muy caro |

Notas:
- `duplicate(col)` suma score si existe >0 duplicados del valor de esa columna para el registro.
- `high_cardinality(col)` suma si la proporción de valores únicos de col > 0.95 y número de filas > 100.
- Para listas usar comillas dobles en valores con espacios.
- Scores se acumulan; luego se normaliza opcionalmente.

Escala sugerida final:
- 0-19: Bajo
- 20-39: Medio
- 40-59: Alto
- 60+: Crítico

Agregue nuevas filas manteniendo el formato de la tabla.
