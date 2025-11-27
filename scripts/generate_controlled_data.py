"""
Script para generar datasets con perfiles de riesgo controlados.
Genera 3 perfiles distintos:
- Jan Pereira: Alto riesgo (muchos siniestros costosos, vehículos antiguos, etc.)
- Juan José Pereira: Bajo riesgo (pocos siniestros, bajo costo, vehículos nuevos)
- Antonio Pereira: Bajo riesgo (sin siniestros o muy pocos)
"""
import os
import sys
import random
from datetime import datetime, timedelta
import pandas as pd
import argparse

# Configuración
NOMBRES_GENERICOS = ["Juan", "María", "Carlos", "Ana", "Luis", "Sofía", "Miguel", "Laura"]
APELLIDOS_GENERICOS = ["García", "González", "Rodríguez", "López", "Martínez", "Sánchez"]

def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

def generate_nif():
    num = random.randint(10000000, 99999999)
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{num}{letters[num % 23]}"

def generate_matricula():
    return f"{random.randint(1000, 9999)}{''.join(random.choices('BCDFGHJKLMNPRSTVWXYZ', k=3))}"

def main(args):
    os.makedirs(args.output, exist_ok=True)
    
    # === ASEGURADOS ===
    asegurados = []
    id_counter = 1
    
    # Jan Pereira - Alto riesgo (100 personas)
    for i in range(100):
        asegurados.append({
            "id": id_counter,
            "nif": generate_nif(),
            "nombre": "Jan Pereira (perfil alto riesgo)",
            "tipo_persona": "FISICA",
            "Nombre": "Jan",
            "Apellido": "Pereira"
        })
        id_counter += 1
    
    # Juan José Pereira - Bajo riesgo (50 personas)
    for i in range(50):
        asegurados.append({
            "id": id_counter,
            "nif": generate_nif(),
            "nombre": "Juan José Pereira (perfil bajo riesgo)",
            "tipo_persona": "FISICA",
            "Nombre": "Juan José",
            "Apellido": "Pereira"
        })
        id_counter += 1
    
    # Antonio Pereira - Bajo riesgo (50 personas)
    for i in range(50):
        asegurados.append({
            "id": id_counter,
            "nif": generate_nif(),
            "nombre": "Antonio Pereira (perfil bajo riesgo)",
            "tipo_persona": "FISICA",
            "Nombre": "Antonio",
            "Apellido": "Pereira"
        })
        id_counter += 1
    
    # Resto genéricos (800 personas)
    for i in range(800):
        nombre = random.choice(NOMBRES_GENERICOS)
        apellido = random.choice(APELLIDOS_GENERICOS)
        asegurados.append({
            "id": id_counter,
            "nif": generate_nif(),
            "nombre": f"{nombre} {apellido}",
            "tipo_persona": "FISICA",
            "Nombre": nombre,
            "Apellido": apellido
        })
        id_counter += 1
    
    df_aseg = pd.DataFrame(asegurados)
    df_aseg.to_csv(os.path.join(args.output, "asegurados.csv"), index=False)
    print(f"✓ asegurados.csv: {len(df_aseg)} registros")
    
    # === VEHÍCULOS ===
    vehiculos = []
    for aseg in asegurados:
        id_aseg = aseg["id"]
        nombre = aseg["Nombre"]
        apellido = aseg["Apellido"]
        
        # Jan Pereira: vehículos antiguos
        if nombre == "Jan" and apellido == "Pereira":
            anio = random.randint(2008, 2014)
        # Juan José y Antonio: vehículos nuevos
        elif (nombre in ["Juan José", "Antonio"]) and apellido == "Pereira":
            anio = random.randint(2020, 2024)
        else:
            anio = random.randint(2015, 2023)
        
        vehiculos.append({
            "id": id_aseg,
            "matricula": generate_matricula(),
            "marca": random.choice(["Seat", "Volkswagen", "Ford", "Toyota", "Renault"]),
            "modelo": "Modelo",
            "anio_small": anio,
            "Nombre": nombre,
            "Apellido": apellido
        })
    
    df_veh = pd.DataFrame(vehiculos)
    df_veh.to_csv(os.path.join(args.output, "vehiculos.csv"), index=False)
    print(f"✓ vehiculos.csv: {len(df_veh)} registros")
    
    # === PÓLIZAS ===
    polizas = []
    for aseg in asegurados:
        id_aseg = aseg["id"]
        nombre = aseg["Nombre"]
        apellido = aseg["Apellido"]
        
        # Jan Pereira: más pólizas RC y canceladas
        if nombre == "Jan" and apellido == "Pereira":
            clase = "RC"
            estado = random.choice(["VIGENTE", "CANCELADA", "CANCELADA"])
        # Juan José y Antonio: TODO_RIESGO vigentes
        elif (nombre in ["Juan José", "Antonio"]) and apellido == "Pereira":
            clase = "TODO_RIESGO"
            estado = "VIGENTE"
        else:
            clase = random.choice(["RC", "TODO_RIESGO", "TERCEROS_AMPLIADO"])
            estado = random.choice(["VIGENTE", "VIGENTE", "CANCELADA"])
        
        polizas.append({
            "id": id_aseg,
            "numero_poliza": f"POL{str(id_aseg).zfill(6)}",
            "aseguradora_id": random.randint(1, 2),
            "clase_poliza": clase,
            "estado": estado,
            "Nombre": nombre,
            "Apellido": apellido
        })
    
    df_pol = pd.DataFrame(polizas)
    df_pol.to_csv(os.path.join(args.output, "polizas.csv"), index=False)
    print(f"✓ polizas.csv: {len(df_pol)} registros")
    
    # === SINIESTROS ===
    siniestros = []
    sin_id = 1
    
    for aseg in asegurados:
        id_aseg = aseg["id"]
        nombre = aseg["Nombre"]
        apellido = aseg["Apellido"]
        
        # Jan Pereira: muchos siniestros costosos
        if nombre == "Jan" and apellido == "Pereira":
            num_siniestros = random.randint(5, 10)
            for _ in range(num_siniestros):
                siniestros.append({
                    "id": sin_id,
                    "referencia": f"SIN{str(sin_id).zfill(6)}",
                    "poliza_id": id_aseg,
                    "vehiculo_id": id_aseg,
                    "asegurado_id": id_aseg,
                    "fecha_siniestro": random_date(2020, 2024),
                    "lugar": random.choice(["Madrid", "Barcelona", "Valencia"]),
                    "responsable": True,
                    "importe_estimada": round(random.uniform(3500, 8000), 2),
                    "estado": random.choice(["ABIERTA", "EN_TRAMITE"]),
                    "Nombre": nombre,
                    "Apellido": apellido
                })
                sin_id += 1
        
        # Juan José Pereira: pocos siniestros de bajo costo
        elif nombre == "Juan José" and apellido == "Pereira":
            if random.random() < 0.3:  # Solo 30% tienen siniestros
                siniestros.append({
                    "id": sin_id,
                    "referencia": f"SIN{str(sin_id).zfill(6)}",
                    "poliza_id": id_aseg,
                    "vehiculo_id": id_aseg,
                    "asegurado_id": id_aseg,
                    "fecha_siniestro": random_date(2022, 2024),
                    "lugar": random.choice(["Sevilla", "Málaga", "Granada"]),
                    "responsable": False,
                    "importe_estimada": round(random.uniform(300, 1000), 2),
                    "estado": "CERRADA",
                    "Nombre": nombre,
                    "Apellido": apellido
                })
                sin_id += 1
        
        # Antonio Pereira: casi sin siniestros
        elif nombre == "Antonio" and apellido == "Pereira":
            if random.random() < 0.1:  # Solo 10% tienen siniestros
                siniestros.append({
                    "id": sin_id,
                    "referencia": f"SIN{str(sin_id).zfill(6)}",
                    "poliza_id": id_aseg,
                    "vehiculo_id": id_aseg,
                    "asegurado_id": id_aseg,
                    "fecha_siniestro": random_date(2023, 2024),
                    "lugar": random.choice(["Bilbao", "Zaragoza"]),
                    "responsable": False,
                    "importe_estimada": round(random.uniform(200, 800), 2),
                    "estado": "CERRADA",
                    "Nombre": nombre,
                    "Apellido": apellido
                })
                sin_id += 1
        
        # Genéricos: distribución normal
        else:
            if random.random() < 0.4:  # 40% tienen siniestros
                for _ in range(random.randint(1, 3)):
                    siniestros.append({
                        "id": sin_id,
                        "referencia": f"SIN{str(sin_id).zfill(6)}",
                        "poliza_id": id_aseg,
                        "vehiculo_id": id_aseg,
                        "asegurado_id": id_aseg,
                        "fecha_siniestro": random_date(2020, 2024),
                        "lugar": random.choice(["Madrid", "Barcelona", "Valencia", "Sevilla"]),
                        "responsable": random.choice([True, False]),
                        "importe_estimada": round(random.uniform(500, 4000), 2),
                        "estado": random.choice(["ABIERTA", "EN_TRAMITE", "CERRADA", "CERRADA"]),
                        "Nombre": nombre,
                        "Apellido": apellido
                    })
                    sin_id += 1
    
    df_sin = pd.DataFrame(siniestros)
    df_sin.to_csv(os.path.join(args.output, "siniestros.csv"), index=False)
    print(f"✓ siniestros.csv: {len(df_sin)} registros")
    
    # === OTROS DATASETS ===
    df_aseguradoras = pd.DataFrame([
        {"id": 1, "codigo": "MAPFRE", "nombre": "Mapfre Seguros"},
        {"id": 2, "codigo": "ALLIANZ", "nombre": "Allianz España"}
    ])
    df_aseguradoras.to_csv(os.path.join(args.output, "aseguradoras.csv"), index=False)
    print(f"✓ aseguradoras.csv: 2 registros")
    
    print(f"\n=== RESUMEN ===")
    print(f"Total asegurados: {len(asegurados)}")
    print(f"  - Jan Pereira (alto riesgo): 100")
    print(f"  - Juan José Pereira (bajo riesgo): 50")
    print(f"  - Antonio Pereira (bajo riesgo): 50")
    print(f"  - Genéricos: 800")
    print(f"Total siniestros: {len(siniestros)}")
    print(f"  - Jan Pereira: {len([s for s in siniestros if s['Nombre'] == 'Jan'])}")
    print(f"  - Juan José Pereira: {len([s for s in siniestros if s['Nombre'] == 'Juan José'])}")
    print(f"  - Antonio Pereira: {len([s for s in siniestros if s['Nombre'] == 'Antonio' and s['Apellido'] == 'Pereira'])}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dataset_final", help="Directorio de salida")
    args = parser.parse_args()
    main(args)
