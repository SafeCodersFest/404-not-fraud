import os
import sys
import random
import argparse
from typing import List, Tuple
import pandas as pd

# Listas ampliadas para generar nombres diversos
NOMBRES_PRIMARIOS = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Sofía", "Miguel", "Laura",
    "Diego", "Valentina", "Pedro", "Carmen", "Jorge", "Elena", "Roberto",
    "Patricia", "Fernando", "Isabel", "Antonio", "Lucía", "Javier", "Rosa",
    "Manuel", "Teresa", "Alejandro", "Cristina", "Francisco", "Mónica",
    "Andrés", "Beatriz", "Rafael", "Pilar", "Sergio", "Raquel", "Daniel",
    "Gloria", "Alberto", "Dolores", "Óscar", "Inés", "Raúl", "Silvia",
    "Enrique", "Amparo", "Pablo", "Nuria", "Rubén", "Eva", "Víctor", "Marta",
    "Jan", "José"  # Añadidos para casos específicos
]

NOMBRES_SECUNDARIOS = [
    "José", "Antonio", "Manuel", "Francisco", "Luis", "Carlos", "Miguel",
    "Juan", "Pedro", "Javier", "María", "Carmen", "Ana", "Rosa"
]

APELLIDOS = [
    "García", "González", "Rodríguez", "Fernández", "López", "Martínez",
    "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández",
    "Díaz", "Moreno", "Muñoz", "Álvarez", "Romero", "Alonso", "Gutiérrez",
    "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez",
    "Serrano", "Blanco", "Molina", "Morales", "Suárez", "Ortega", "Delgado",
    "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias", "Nuñez",
    "Medina", "Garrido", "Santos", "Castillo", "Cortés", "Lozano", "Méndez",
    "Pereira", "Silva", "Vargas"  # Añadidos para casos específicos
]

SPECIAL_CASES = {
    "high_risk": [
        ("Jan", "Pereira"),  # Alto riesgo
    ],
    "low_risk": [
        ("Juan José", "Pereira"),  # Bajo riesgo
        ("Antonio", "Pereira"),     # Bajo riesgo
    ]
}


def generate_full_name(use_compound: bool = False) -> Tuple[str, str]:
    """Genera nombre y apellido, con opción de nombres compuestos."""
    if use_compound and random.random() < 0.15:  # 15% nombres compuestos
        primer_nombre = random.choice(NOMBRES_PRIMARIOS)
        segundo_nombre = random.choice(NOMBRES_SECUNDARIOS)
        nombre = f"{primer_nombre} {segundo_nombre}"
    else:
        nombre = random.choice(NOMBRES_PRIMARIOS)
    
    apellido = random.choice(APELLIDOS)
    return nombre, apellido


def inject_special_cases(
    nombres: List[str],
    apellidos: List[str],
    high_risk_count: int = 50,
    low_risk_count: int = 30
) -> Tuple[List[str], List[str]]:
    """Inyecta casos especiales en las listas de nombres."""
    total_special = high_risk_count + low_risk_count * 2
    
    if len(nombres) < total_special:
        return nombres, apellidos
    
    # Inyectar casos de alto riesgo
    positions_high = random.sample(range(len(nombres)), high_risk_count)
    for pos in positions_high:
        nombres[pos] = SPECIAL_CASES["high_risk"][0][0]
        apellidos[pos] = SPECIAL_CASES["high_risk"][0][1]
    
    # Inyectar casos de bajo riesgo
    remaining_positions = [i for i in range(len(nombres)) if i not in positions_high]
    positions_low = random.sample(remaining_positions, min(low_risk_count * 2, len(remaining_positions)))
    
    for i, pos in enumerate(positions_low):
        case_index = i % 2  # Alternar entre los dos casos de bajo riesgo
        nombres[pos] = SPECIAL_CASES["low_risk"][case_index][0]
        apellidos[pos] = SPECIAL_CASES["low_risk"][case_index][1]
    
    return nombres, apellidos


def enrich_csv_with_names(
    input_path: str,
    output_path: str,
    seed: int = 42,
    inject_cases: bool = True,
    high_risk_count: int = 50,
    low_risk_count: int = 30
) -> None:
    """Enriquece CSV con columnas de nombre y apellido."""
    random.seed(seed)
    
    try:
        df = pd.read_csv(input_path, encoding="utf-8", low_memory=True)
    except Exception:
        df = pd.read_csv(input_path, encoding="ISO-8859-1", low_memory=True)
    
    # Generar nombres
    nombres = []
    apellidos = []
    for _ in range(len(df)):
        nombre, apellido = generate_full_name(use_compound=True)
        nombres.append(nombre)
        apellidos.append(apellido)
    
    # Inyectar casos especiales
    if inject_cases:
        nombres, apellidos = inject_special_cases(
            nombres, apellidos, high_risk_count, low_risk_count
        )
    
    # Si ya existen columnas Nombre/Apellido, reemplazarlas
    if "Nombre" in df.columns:
        df.drop(columns=["Nombre"], inplace=True)
    if "Apellido" in df.columns:
        df.drop(columns=["Apellido"], inplace=True)
    
    # Insertar al inicio
    df.insert(0, "Nombre", nombres)
    df.insert(1, "Apellido", apellidos)
    
    # Guardar
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    
    # Estadísticas
    print(f"✓ Archivo generado: {output_path}")
    print(f"  - Total filas: {len(df)}")
    print(f"  - Columnas: {len(df.columns)}")
    
    if inject_cases:
        jan_count = sum(1 for n, a in zip(nombres, apellidos) if n == "Jan" and a == "Pereira")
        juan_jose_count = sum(1 for n, a in zip(nombres, apellidos) if n == "Juan José" and a == "Pereira")
        antonio_count = sum(1 for n, a in zip(nombres, apellidos) if n == "Antonio" and a == "Pereira")
        print(f"  - Jan Pereira (alto riesgo): {jan_count}")
        print(f"  - Juan José Pereira (bajo riesgo): {juan_jose_count}")
        print(f"  - Antonio Pereira (bajo riesgo): {antonio_count}")


def process_directory(
    input_dir: str,
    output_dir: str,
    seed: int = 42,
    inject_cases: bool = True,
    high_risk_count: int = 50,
    low_risk_count: int = 30
) -> None:
    """Procesa todos los CSV en un directorio."""
    if not os.path.isdir(input_dir):
        print(f"Directorio no encontrado: {input_dir}", file=sys.stderr)
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]
    
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio.")
        return
    
    print(f"Procesando {len(csv_files)} archivos CSV...\n")
    
    for filename in csv_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        print(f"Procesando: {filename}")
        try:
            enrich_csv_with_names(
                input_path, output_path, seed, inject_cases,
                high_risk_count, low_risk_count
            )
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Enriquece CSV(s) con columnas Nombre y Apellido, inyectando casos especiales"
    )
    p.add_argument("--input", help="CSV de entrada (archivo único)")
    p.add_argument("--output", help="CSV de salida (archivo único)")
    p.add_argument("--input-dir", help="Directorio con múltiples CSV")
    p.add_argument("--output-dir", help="Directorio de salida para múltiples CSV")
    p.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
    p.add_argument("--no-inject", action="store_true", help="No inyectar casos especiales")
    p.add_argument("--high-risk-count", type=int, default=50, help="Cantidad de Jan Pereira a inyectar")
    p.add_argument("--low-risk-count", type=int, default=30, help="Cantidad de cada Pereira bajo riesgo")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    
    # Modo directorio
    if args.input_dir:
        if not args.output_dir:
            print("Error: --output-dir requerido cuando se usa --input-dir", file=sys.stderr)
            return 1
        process_directory(
            args.input_dir, args.output_dir, args.seed,
            not args.no_inject, args.high_risk_count, args.low_risk_count
        )
        return 0
    
    # Modo archivo único
    if not args.input or not args.output:
        print("Error: --input y --output requeridos en modo archivo único", file=sys.stderr)
        return 1
    
    if not os.path.isfile(args.input):
        print(f"Archivo no encontrado: {args.input}", file=sys.stderr)
        return 1
    
    enrich_csv_with_names(
        args.input, args.output, args.seed,
        not args.no_inject, args.high_risk_count, args.low_risk_count
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
