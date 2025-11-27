import os
import sys
import random
import argparse
import pandas as pd

NOMBRES = [
    "JUAN", "MARIA", "CARLOS", "ANA", "LUIS", "SOFIA", "MIGUEL", "LAURA", 
    "DIEGO", "VALENTINA", "PEDRO", "CARMEN", "JORGE", "ELENA", "ROBERTO",
    "PATRICIA", "FERNANDO", "ISABEL", "ANTONIO", "LUCIA"
]

APELLIDOS = [
    "PEREZ", "GOMEZ", "RODRIGUEZ", "MARTINEZ", "FERNANDEZ", "LOPEZ", "TORRES",
    "GARCIA", "SANCHEZ", "RUIZ", "MORALES", "DIAZ", "CASTRO", "VARGAS", "ROMERO",
    "HERRERA", "SILVA", "MENDEZ", "JIMENEZ", "ALVAREZ"
]


def add_names_to_csv(input_path: str, output_path: str, seed: int = 42) -> None:
    random.seed(seed)
    df = pd.read_csv(input_path, encoding="utf-8", low_memory=True)
    
    first_names = [random.choice(NOMBRES) for _ in range(len(df))]
    last_names = [random.choice(APELLIDOS) for _ in range(len(df))]
    
    df.insert(0, "Nombre", first_names)
    df.insert(1, "Apellido", last_names)
    
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Archivo generado: {output_path} ({len(df)} filas, {len(df.columns)} columnas)")


def parse_args(argv):
    p = argparse.ArgumentParser(description="Añadir columnas Nombre y Apellido sintéticos a CSV")
    p.add_argument("--input", required=True, help="CSV de entrada")
    p.add_argument("--output", required=True, help="CSV de salida con columnas nombre/apellido")
    p.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
    return p.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    if not os.path.isfile(args.input):
        print(f"Archivo no encontrado: {args.input}", file=sys.stderr)
        return 1
    add_names_to_csv(args.input, args.output, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
