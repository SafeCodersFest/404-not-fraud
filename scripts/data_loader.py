import os
import sys
import csv
import argparse
import math
from typing import List, Dict, Any, Tuple

import pandas as pd

NA_VALUES = ["", "NA", "N/A", "null", "Null", "NONE", "None"]
DEFAULT_MAX_PROFILE_ROWS = 20000


def list_csv_files(dataset_dir: str) -> List[str]:
    files = []
    for entry in os.listdir(dataset_dir):
        if entry.lower().endswith(".csv"):
            files.append(os.path.join(dataset_dir, entry))
    return sorted(files)


def try_read_csv(path: str, nrows: int = None) -> pd.DataFrame:
    encodings = ["utf-8", "ISO-8859-1", "latin1", "cp1252"]
    last_error = None
    for enc in encodings:
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                na_values=NA_VALUES,
                low_memory=True,
                nrows=nrows,
                on_bad_lines='skip'
            )
            return df
        except Exception as e:  # noqa: BLE001
            last_error = e
    raise RuntimeError(f"No se pudo leer {path}: {last_error}")


def simplify_dtype(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "int"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    # Heurística fecha
    if series.dtype == object:
        sample = series.dropna().head(20).astype(str)
        date_like = 0
        for v in sample:
            v_strip = v.strip()
            if len(v_strip) >= 6 and any(sep in v_strip for sep in ["-", "/", ":"]):
                # Intento parseo
                try:
                    pd.to_datetime(v_strip, errors="raise")
                    date_like += 1
                except Exception:  # noqa: BLE001
                    pass
        if date_like >= max(3, len(sample) * 0.3):
            return "date"
        # Categórica vs texto libre
        nunique = series.nunique(dropna=True)
        total = len(series)
        if nunique <= 50 and (total == 0 or nunique / max(1, total) < 0.2):
            return "categorical"
        return "text"
    return str(series.dtype)


def detect_id_column(series: pd.Series) -> bool:
    if series.nunique(dropna=True) >= len(series) * 0.95 and series.nunique(dropna=True) > 50:
        return True
    return False


def profile_dataframe(df: pd.DataFrame, file_path: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {}
    info["file_name"] = os.path.basename(file_path)
    info["rows"] = len(df)
    info["columns"] = len(df.columns)
    info["memory_kb"] = math.ceil(df.memory_usage(deep=True).sum() / 1024)
    # Column details
    col_details = []
    for col in df.columns:
        ser = df[col]
        dtype_simple = simplify_dtype(ser)
        missing_pct = round(ser.isna().mean() * 100, 2)
        nunique = ser.nunique(dropna=True)
        is_id = detect_id_column(ser)
        col_details.append({
            "name": col,
            "dtype": dtype_simple,
            "missing_pct": missing_pct,
            "nunique": nunique,
            "is_id": is_id,
        })
    info["columns_detail"] = col_details
    # Duplicates
    try:
        info["duplicate_rows"] = int(df.duplicated().sum())
    except Exception:  # noqa: BLE001
        info["duplicate_rows"] = None
    # Sample head
    info["sample_head"] = df.head(5).to_dict(orient="records")
    return info


def build_report(profiles: List[Dict[str, Any]]) -> str:
    lines = ["# Perfil de Dataset", ""]
    lines.append("## Inventario")
    for p in profiles:
        lines.append(f"- {p['file_name']}: {p['rows']} filas, {p['columns']} columnas, {p['memory_kb']} KB")
    lines.append("")
    for p in profiles:
        lines.append(f"## {p['file_name']}")
        lines.append("### Columnas")
        lines.append("| Columna | Tipo | % Faltantes | Únicos | ID? |")
        lines.append("|---------|------|-------------|--------|-----|")
        for c in p["columns_detail"]:
            lines.append(f"| {c['name']} | {c['dtype']} | {c['missing_pct']} | {c['nunique']} | {('Sí' if c['is_id'] else 'No')} |")
        lines.append("")
        lines.append(f"Duplicados: {p['duplicate_rows']}")
        lines.append("")
        lines.append("### Muestra (primeras 5 filas)")
        if p["sample_head"]:
            header = p["sample_head"][0].keys()
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "|".join(["---" for _ in header]) + "|")
            for row in p["sample_head"]:
                lines.append("| " + " | ".join([str(row.get(h, "")) for h in header]) + " |")
        lines.append("")
    return "\n".join(lines)


def unify_datasets(file_paths: List[str], chunk_size: int = None) -> pd.DataFrame:
    frames = []
    for path in file_paths:
        df = try_read_csv(path)  # leer completo (simplificación)
        df["__source_file"] = os.path.basename(path)
        frames.append(df)
    unified = pd.concat(frames, axis=0, ignore_index=True, sort=False)
    return unified


def save_output(df: pd.DataFrame, output_path: str, export_format: str) -> None:
    if export_format == "parquet":
        df.to_parquet(output_path, index=False)
    elif export_format == "csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError(f"Formato no soportado: {export_format}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Perfil y unificación de CSVs del dataset")
    parser.add_argument("--dataset-dir", default="dataset", help="Directorio con archivos CSV")
    parser.add_argument("--max-profile-rows", type=int, default=DEFAULT_MAX_PROFILE_ROWS, help="Máximo de filas a cargar para perfilado si el archivo es grande")
    parser.add_argument("--output", default="dataset/combined_dataset.parquet", help="Ruta de salida para dataset unificado")
    parser.add_argument("--export-format", choices=["parquet", "csv"], default="parquet", help="Formato de salida unificado")
    parser.add_argument("--report", default="reports/dataset_profile.md", help="Ruta del reporte de perfil")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    if not os.path.isdir(args.dataset_dir):
        print(f"Directorio no encontrado: {args.dataset_dir}", file=sys.stderr)
        return 1
    csv_files = list_csv_files(args.dataset_dir)
    if not csv_files:
        print("No se encontraron archivos CSV.")
        return 0

    profiles = []
    for path in csv_files:
        # Perfilado parcial si grande
        total_rows = sum(1 for _ in open(path, "r", encoding="utf-8", errors="ignore")) - 1  # rest header
        if total_rows > args.max_profile_rows:
            df_profile = try_read_csv(path, nrows=args.max_profile_rows)
        else:
            df_profile = try_read_csv(path)
        profile = profile_dataframe(df_profile, path)
        profile["rows_total_file"] = total_rows
        profiles.append(profile)

    report_text = build_report(profiles)
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"Reporte generado: {args.report}")

    unified = unify_datasets(csv_files)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    save_output(unified, args.output, args.export_format)
    print(f"Dataset unificado guardado en: {args.output} ({len(unified)} filas, {len(unified.columns)} columnas)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
