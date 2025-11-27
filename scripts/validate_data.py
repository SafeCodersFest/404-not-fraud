import sys
import pandas as pd
import os

def main():
    datasets = []
    base_dir = "dataset_enriched"
    
    for filename in ["asegurados.csv", "siniestros.csv", "vehiculos.csv", "polizas.csv", "contrato_poliza.csv", "base_carvertical_ficticia.csv"]:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path, encoding="utf-8")
                datasets.append(df)
            except Exception as e:
                print(f"Error leyendo {filename}: {e}")
    
    if not datasets:
        print("No se encontraron datasets")
        return 1
    
    combined = pd.concat(datasets, axis=0, ignore_index=True, sort=False)
    
    # Generar full_name
    combined["full_name"] = (combined.get("Nombre", "") + " " + combined.get("Apellido", "")).str.strip().str.upper()
    
    # Contar casos especiales
    jan_count = len(combined[combined["full_name"] == "JAN PEREIRA"])
    juan_jose_count = len(combined[combined["full_name"].str.replace("  ", " ") == "JUAN JOSE PEREIRA"])
    antonio_count = len(combined[combined["full_name"] == "ANTONIO PEREIRA"])
    
    print("=== REPORTE DE VALIDACIÓN ===\n")
    print(f"Total registros combinados: {len(combined)}")
    print(f"Columnas únicas: {len(combined.columns)}")
    print(f"\nCasos especiales:")
    print(f"  - Jan Pereira (ALTO RIESGO):     {jan_count} registros")
    print(f"  - Juan José Pereira (SIN RIESGO): {juan_jose_count} registros")
    print(f"  - Antonio Pereira (SIN RIESGO):   {antonio_count} registros")
    
    # Top 10 nombres más frecuentes
    print(f"\nTop 10 nombres más frecuentes:")
    top_names = combined["full_name"].value_counts().head(10)
    for name, count in top_names.items():
        print(f"  {name}: {count}")
    
    # Verificar columnas clave
    print(f"\nColumnas presentes:")
    print(f"  - Nombre: {'Sí' if 'Nombre' in combined.columns else 'No'}")
    print(f"  - Apellido: {'Sí' if 'Apellido' in combined.columns else 'No'}")
    print(f"  - asegurado_id: {'Sí' if 'asegurado_id' in combined.columns else 'No'}")
    print(f"  - vehiculo_id: {'Sí' if 'vehiculo_id' in combined.columns else 'No'}")
    print(f"  - importe_estimada: {'Sí' if 'importe_estimada' in combined.columns else 'No'}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
