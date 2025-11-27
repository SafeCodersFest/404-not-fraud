import os
import sys
import random
import argparse
from datetime import datetime, timedelta
from typing import List
import pandas as pd

# Configuración para generar datos sintéticos
NOMBRES = ["Juan", "María", "Carlos", "Ana", "Luis", "Sofía", "Miguel", "Laura", "Diego", "Valentina", 
           "Pedro", "Carmen", "Jorge", "Elena", "Roberto", "Patricia", "Fernando", "Isabel", "Antonio", "Jan"]
APELLIDOS = ["García", "González", "Rodríguez", "Fernández", "López", "Martínez", "Sánchez", "Pérez", 
             "Gómez", "Pereira", "Silva", "Torres", "Castro", "Vargas"]
MARCAS = ["Seat", "Volkswagen", "Renault", "Peugeot", "Ford", "Toyota", "BMW", "Audi", "Kia", "Hyundai", 
          "Nissan", "Mazda", "Fiat", "Opel", "Citroen", "Honda"]
MODELOS = {
    "Seat": ["Ibiza", "Leon", "Arona", "Ateca"],
    "Volkswagen": ["Golf", "Polo", "Tiguan", "Passat"],
    "Renault": ["Clio", "Megane", "Captur", "Scenic"],
    "Ford": ["Focus", "Fiesta", "Kuga", "Mondeo"],
    "Toyota": ["Corolla", "Yaris", "RAV4", "C-HR"],
}
LUGARES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma", "Bilbao", "Alicante"]
CLASES_POLIZA = ["RC", "TODO_RIESGO", "TERCEROS_AMPLIADO"]
ESTADOS_SINIESTRO = ["ABIERTA", "EN_TRAMITE", "CERRADA"]
ESTADOS_POLIZA = ["VIGENTE", "CANCELADA", "EXPIRADA"]


def generate_nif() -> str:
    """Genera un NIF ficticio."""
    num = random.randint(10000000, 99999999)
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{num}{letters[num % 23]}"


def generate_matricula() -> str:
    """Genera una matrícula española ficticia."""
    nums = random.randint(1000, 9999)
    letters = "".join(random.choices("BCDFGHJKLMNPRSTVWXYZ", k=3))
    return f"{nums}{letters}"


def generate_vin() -> str:
    """Genera un VIN ficticio."""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=17))


def random_date(start_year: int = 2018, end_year: int = 2024) -> str:
    """Genera una fecha aleatoria."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def generate_asegurados(n: int = 500) -> pd.DataFrame:
    """Genera dataset de asegurados."""
    data = []
    for i in range(1, n + 1):
        nombre_completo = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
        data.append({
            "id": i,
            "nif": generate_nif(),
            "nombre": nombre_completo,
            "tipo_persona": "FISICA"
        })
    return pd.DataFrame(data)


def generate_vehiculos(n: int = 500) -> pd.DataFrame:
    """Genera dataset de vehículos."""
    data = []
    for i in range(1, n + 1):
        marca = random.choice(MARCAS)
        modelo = random.choice(MODELOS.get(marca, ["Modelo"]))
        data.append({
            "id": i,
            "matricula": generate_matricula(),
            "marca": marca,
            "modelo": modelo,
            "anio_small": random.randint(2010, 2024)
        })
    return pd.DataFrame(data)


def generate_polizas(n: int = 500) -> pd.DataFrame:
    """Genera dataset de pólizas."""
    data = []
    for i in range(1, n + 1):
        data.append({
            "id": i,
            "numero_poliza": f"POL{str(i).zfill(6)}",
            "aseguradora_id": random.randint(1, 2),
            "clase_poliza": random.choice(CLASES_POLIZA),
            "estado": random.choice(ESTADOS_POLIZA)
        })
    return pd.DataFrame(data)


def generate_siniestros(n: int = 800, max_asegurado: int = 500, max_vehiculo: int = 500, max_poliza: int = 500) -> pd.DataFrame:
    """Genera dataset de siniestros."""
    data = []
    for i in range(1, n + 1):
        data.append({
            "id": i,
            "referencia": f"SIN{str(i).zfill(6)}",
            "poliza_id": random.randint(1, max_poliza),
            "vehiculo_id": random.randint(1, max_vehiculo),
            "asegurado_id": random.randint(1, max_asegurado),
            "fecha_siniestro": random_date(2020, 2024),
            "lugar": random.choice(LUGARES),
            "responsable": random.choice([True, False]),
            "importe_estimada": round(random.uniform(300, 5000), 2),
            "estado": random.choice(ESTADOS_SINIESTRO)
        })
    return pd.DataFrame(data)


def generate_contrato_poliza(n: int = 500) -> pd.DataFrame:
    """Genera dataset de contratos de póliza."""
    data = []
    for i in range(1, n + 1):
        data.append({
            "id": i,
            "poliza_id": i,
            "asegurado_id": i,
            "vehiculo_id": i,
            "rol": "TITULAR"
        })
    return pd.DataFrame(data)


def generate_base_carvertical(n: int = 300) -> pd.DataFrame:
    """Genera dataset carvertical ficticio."""
    data = []
    tipos_incidente = ["Impacto frontal", "Daño menor", "Accidente grave", "Daño por granizo", None]
    gravedad = ["Leve", "Media", "Grave", None]
    partes = ["Capó", "Puertas", "Laterales", "Motor", "Parachoques", None]
    
    for i in range(n):
        tiene_dano = random.random() < 0.6
        data.append({
            "vin": generate_vin(),
            "marca": random.choice(MARCAS),
            "modelo": random.choice(["Modelo1", "Modelo2", "Modelo3"]),
            "año": random.randint(2010, 2024),
            "país_origen": random.choice(["España", "Alemania", "Francia", "Japón", "Italia"]),
            "color": random.choice(["Blanco", "Negro", "Gris", "Azul", "Rojo"]),
            "fecha_ultimo_dano": random_date(2015, 2024) if tiene_dano else None,
            "tipo_incidente": random.choice(tipos_incidente) if tiene_dano else None,
            "coste_estimado": round(random.uniform(500, 15000), 2) if tiene_dano else None,
            "gravedad": random.choice(gravedad) if tiene_dano else None,
            "partes_afectadas": random.choice(partes) if tiene_dano else None,
            "lectura_km": random.randint(5000, 200000),
            "fecha_ultimo_itv": random_date(2020, 2024),
            "resultado_itv": random.choice(["Favorable", "Desfavorable"]),
            "observaciones": random.choice(["Sin defectos", "Fugas leves de aceite", "Frenos OK", "Luces dañadas"])
        })
    return pd.DataFrame(data)


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Genera datasets sintéticos para pruebas")
    p.add_argument("--output-dir", default="dataset_synthetic", help="Directorio de salida")
    p.add_argument("--asegurados", type=int, default=500, help="Número de asegurados")
    p.add_argument("--siniestros", type=int, default=800, help="Número de siniestros")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Generando datasets sintéticos...")
    
    # Aseguradoras (fijo pequeño)
    df_aseg = pd.DataFrame([
        {"id": 1, "codigo": "MAPFRE", "nombre": "Mapfre Seguros"},
        {"id": 2, "codigo": "ALLIANZ", "nombre": "Allianz España"}
    ])
    df_aseg.to_csv(os.path.join(args.output_dir, "aseguradoras.csv"), index=False)
    print(f"✓ aseguradoras.csv: {len(df_aseg)} filas")
    
    # Asegurados
    df_aseg_p = generate_asegurados(args.asegurados)
    df_aseg_p.to_csv(os.path.join(args.output_dir, "asegurados.csv"), index=False)
    print(f"✓ asegurados.csv: {len(df_aseg_p)} filas")
    
    # Vehículos
    df_veh = generate_vehiculos(args.asegurados)
    df_veh.to_csv(os.path.join(args.output_dir, "vehiculos.csv"), index=False)
    print(f"✓ vehiculos.csv: {len(df_veh)} filas")
    
    # Pólizas
    df_pol = generate_polizas(args.asegurados)
    df_pol.to_csv(os.path.join(args.output_dir, "polizas.csv"), index=False)
    print(f"✓ polizas.csv: {len(df_pol)} filas")
    
    # Contratos
    df_cont = generate_contrato_poliza(args.asegurados)
    df_cont.to_csv(os.path.join(args.output_dir, "contrato_poliza.csv"), index=False)
    print(f"✓ contrato_poliza.csv: {len(df_cont)} filas")
    
    # Siniestros
    df_sin = generate_siniestros(args.siniestros, args.asegurados, args.asegurados, args.asegurados)
    df_sin.to_csv(os.path.join(args.output_dir, "siniestros.csv"), index=False)
    print(f"✓ siniestros.csv: {len(df_sin)} filas")
    
    # Base carvertical
    df_car = generate_base_carvertical(300)
    df_car.to_csv(os.path.join(args.output_dir, "base_carvertical_ficticia.csv"), index=False)
    print(f"✓ base_carvertical_ficticia.csv: {len(df_car)} filas")
    
    print(f"\nDatasets sintéticos generados en: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
