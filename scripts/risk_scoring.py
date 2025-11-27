import os
import re
import sys
import argparse
from typing import List, Dict, Any, Tuple
import pandas as pd

RULE_TABLE_PATTERN = re.compile(r"^\|.*\|$")

SCORE_BUCKETS = [
    (60, "Crítico"),
    (40, "Alto"),
    (20, "Medio"),
    (0, "Bajo"),
]

NAME_COLUMNS_CANDIDATES = [
    ("Nombre", "Apellido"),
    ("first_name", "last_name"),
    ("FirstName", "LastName"),
]


def load_unified(dataset_dir: str) -> pd.DataFrame:
    files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.lower().endswith(".csv")]
    frames = []
    errors = []
    for path in files:
        try:
            df = pd.read_csv(path, encoding="utf-8", low_memory=True, on_bad_lines='skip')
        except Exception as e1:
            try:
                df = pd.read_csv(path, encoding="ISO-8859-1", low_memory=True, on_bad_lines='skip')
            except Exception as e2:
                errors.append(f"{os.path.basename(path)}: {e2}")
                continue
        if df.empty:
            errors.append(f"{os.path.basename(path)}: archivo vacío")
            continue
        df["__source_file"] = os.path.basename(path)
        frames.append(df)
    if errors:
        print(f"Advertencias al cargar archivos ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
    if not frames:
        raise SystemExit("No se encontraron CSVs válidos en dataset.")
    return pd.concat(frames, axis=0, ignore_index=True, sort=False)


def load_watchlist(watchlist_path: str) -> Dict[str, int]:
    if not os.path.isfile(watchlist_path):
        return {}
    try:
        df = pd.read_csv(watchlist_path, encoding="utf-8")
    except Exception:
        df = pd.read_csv(watchlist_path, encoding="ISO-8859-1")
    if "full_name" not in df.columns or "watchlist_score" not in df.columns:
        return {}
    result = {}
    for _, row in df.iterrows():
        name_norm = normalize_name(str(row["full_name"]))
        score = int(row["watchlist_score"])
        result[name_norm] = score
    return result


def parse_rules(rules_path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(rules_path):
        raise FileNotFoundError(f"No existe archivo de reglas: {rules_path}")
    rules: List[Dict[str, Any]] = []
    with open(rules_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Detect table lines starting with |
    header_found = False
    for line in lines:
        line_strip = line.strip()
        if not line_strip.startswith("|"):
            continue
        cells = [c.strip() for c in line_strip.split("|")[1:-1]]  # remove outer empties
        if not header_found:
            header_found = True
            continue  # skip header
        if len(cells) < 2:
            continue
        regla = cells[0]
        score_raw = cells[1]
        descripcion = cells[2] if len(cells) > 2 else ""
        try:
            score = int(score_raw)
        except ValueError:
            continue
        rules.append({"expr": regla, "score": score, "desc": descripcion})
    return rules


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().upper())


def find_name_columns(df: pd.DataFrame) -> Tuple[str, str]:
    for a, b in NAME_COLUMNS_CANDIDATES:
        if a in df.columns and b in df.columns:
            return a, b
    # Try single column full name
    for col in df.columns:
        if col.lower() in ("full_name", "nombre_apellido", "name"):
            return col, None
    return None, None


def bucket_score(score: int) -> str:
    for threshold, label in SCORE_BUCKETS:
        if score >= threshold:
            return label
    return "Bajo"

# --- Rule evaluation helpers ---

def eval_duplicate(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series([False] * len(df))
    return df[col].duplicated(keep=False)


def eval_high_cardinality(df: pd.DataFrame, col: str) -> bool:
    if col not in df.columns:
        return False
    nunique = df[col].nunique(dropna=True)
    total = len(df)
    if total == 0:
        return False
    return (nunique / total) > 0.95 and total > 100


def build_full_name_series(df: pd.DataFrame, name_cols: Tuple[str, str]) -> pd.Series:
    a, b = name_cols
    if a and b:
        return (df[a].fillna("") + " " + df[b].fillna(""))
    if a and not b:
        return df[a].fillna("")
    return pd.Series(["" for _ in range(len(df))])


def apply_rule(df: pd.DataFrame, rule: Dict[str, Any], full_name_series: pd.Series) -> pd.Series:
    expr = rule["expr"]
    # duplicate(col)
    m = re.match(r"duplicate\(([^)]+)\)", expr)
    if m:
        col = m.group(1).strip()
        return eval_duplicate(df, col)
    # high_cardinality(col)
    m = re.match(r"high_cardinality\(([^)]+)\)", expr)
    if m:
        col = m.group(1).strip()
        val = eval_high_cardinality(df, col)
        return pd.Series([val] * len(df))
    # full_name in [...]
    m = re.match(r"full_name in \[(.*)\]", expr)
    if m:
        raw_list = m.group(1)
        # split by comma not inside quotes
        names = [normalize_name(n.strip().strip('"').strip("'")) for n in raw_list.split(",")]
        return full_name_series.apply(lambda x: normalize_name(x) in names)
    # Presence check: col is not null
    m = re.match(r"([A-Za-z0-9_]+) is not null", expr)
    if m:
        col = m.group(1)
        if col not in df.columns:
            return pd.Series([False] * len(df))
        return df[col].notna()
    # Binary logical with AND
    if " AND " in expr:
        parts = expr.split(" AND ")
        series_list = [apply_rule(df, {"expr": p, "score": rule["score"], "desc": rule.get("desc", "")}, full_name_series) for p in parts]
        out = series_list[0]
        for s in series_list[1:]:
            out = out & s
        return out
    # OR logical with ||
    if "||" in expr:
        parts = [p.strip() for p in expr.split("||")] 
        series_list = [apply_rule(df, {"expr": p, "score": rule["score"], "desc": rule.get("desc", "")}, full_name_series) for p in parts]
        out = series_list[0]
        for s in series_list[1:]:
            out = out | s
        return out
    # column in [..]
    m = re.match(r"([A-Za-z0-9_]+) in \[(.*)\]", expr)
    if m:
        col = m.group(1)
        if col not in df.columns:
            return pd.Series([False] * len(df))
        raw_list = m.group(2)
        values = [v.strip().strip('"').strip("'") for v in raw_list.split(",")]
        return df[col].astype(str).isin(values)
    # Comparisons: col > value, >=, <, <=, ==
    m = re.match(r"([A-Za-z0-9_]+)\s*(==|>=|<=|>|<)\s*(.+)", expr)
    if m:
        col, op, val_raw = m.groups()
        if col not in df.columns:
            return pd.Series([False] * len(df))
        val_raw = val_raw.strip().strip('"').strip("'")
        series = df[col]
        # try numeric
        try:
            val_num = float(val_raw)
            series_num = pd.to_numeric(series, errors="coerce")
            if op == ">":
                return series_num > val_num
            if op == ">=":
                return series_num >= val_num
            if op == "<":
                return series_num < val_num
            if op == "<=":
                return series_num <= val_num
            if op == "==":
                return series_num == val_num
        except ValueError:
            # treat as string
            ser_str = series.astype(str)
            if op == "==":
                return ser_str == val_raw
            # other ops on string not supported
            return pd.Series([False] * len(df))
    # Fallback no match
    return pd.Series([False] * len(df))


def compute_scores(df: pd.DataFrame, rules: List[Dict[str, Any]], watchlist: Dict[str, int] = None) -> Dict[str, Any]:
    if watchlist is None:
        watchlist = {}
    name_cols = find_name_columns(df)
    full_name_series = build_full_name_series(df, name_cols).fillna("")
    activated_records: Dict[str, List[Dict[str, Any]]] = {}
    rule_activations = []
    total_score_series = pd.Series([0] * len(df), dtype=int)
    ignored_rules = []

    for rule in rules:
        try:
            mask = apply_rule(df, rule, full_name_series)
        except Exception as e:  # noqa: BLE001
            ignored_rules.append({"expr": rule["expr"], "error": str(e)})
            continue
        if mask.any():
            total_score_series = total_score_series + (mask.astype(int) * rule["score"])
            rule_activations.append({"expr": rule["expr"], "score": rule["score"], "count": int(mask.sum())})
    
    # Apply watchlist scores
    if watchlist and name_cols[0]:
        watchlist_scores = full_name_series.apply(lambda x: watchlist.get(normalize_name(x), 0))
        watchlist_match_count = (watchlist_scores > 0).sum()
        if watchlist_match_count > 0:
            total_score_series = total_score_series + watchlist_scores
            rule_activations.append({"expr": "watchlist_match", "score": "variable", "count": int(watchlist_match_count)})
    
    df_result = df.copy()
    df_result["__risk_score"] = total_score_series
    df_result["__risk_level"] = total_score_series.apply(bucket_score)

    # Aggregate per full name if name columns exist
    if name_cols[0]:
        norm_names = full_name_series.apply(normalize_name)
        df_result["__full_name"] = norm_names
        agg = df_result.groupby("__full_name")["__risk_score"].sum().reset_index().rename(columns={"__risk_score": "risk_score", "__full_name": "full_name"})
        agg["risk_level"] = agg["risk_score"].apply(bucket_score)
    else:
        agg = pd.DataFrame(columns=["full_name", "risk_score", "risk_level"])  # empty

    return {
        "row_scores": df_result,
        "name_scores": agg,
        "activations": rule_activations,
        "ignored": ignored_rules,
        "name_columns": name_cols,
    }


def query_name(result: Dict[str, Any], name: str) -> Dict[str, Any]:
    norm_query = normalize_name(name)
    name_scores = result["name_scores"]
    if name_scores.empty:
        return {"error": "No hay columnas de nombre en el dataset unificado."}
    match_row = name_scores[name_scores["full_name"] == norm_query]
    if match_row.empty:
        return {"full_name": name, "risk_score": 0, "risk_level": "Bajo", "rules": []}
    # Determine which rules triggered for this name
    row_scores = result["row_scores"]
    if "__full_name" not in row_scores.columns:
        return {"full_name": name, "risk_score": int(match_row.iloc[0]["risk_score"]), "risk_level": match_row.iloc[0]["risk_level"], "rules": []}
    triggered_rows = row_scores[(row_scores["__risk_score"] > 0) & (row_scores["__full_name"] == norm_query)]
    active_rules = []
    for act in result["activations"]:
        expr = act["expr"]
        score = act["score"]
        active_rules.append({"expr": expr, "score": score})
    return {
        "full_name": name,
        "risk_score": int(match_row.iloc[0]["risk_score"]),
        "risk_level": match_row.iloc[0]["risk_level"],
        "rules": active_rules,
        "records_count": len(triggered_rows)
    }


def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Motor de scoring de riesgo por reglas")
    p.add_argument("--dataset-dir", default="dataset", help="Directorio de CSVs")
    p.add_argument("--rules", default="rules_engine.md", help="Archivo markdown de reglas")
    p.add_argument("--watchlist", default=None, help="Archivo CSV watchlist (full_name, watchlist_score, reason)")
    p.add_argument("--query-name", default=None, help="Nombre completo a consultar (opcional)")
    p.add_argument("--export", default=None, help="Ruta para exportar resultados row_scores en CSV/Parquet")
    p.add_argument("--export-format", choices=["csv", "parquet"], default="csv")
    return p.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    df = load_unified(args.dataset_dir)
    rules = parse_rules(args.rules)
    watchlist = load_watchlist(args.watchlist) if args.watchlist else {}
    if watchlist:
        print(f"Watchlist cargada: {len(watchlist)} nombres")
    result = compute_scores(df, rules, watchlist)

    print(f"Reglas cargadas: {len(rules)} | Ignoradas: {len(result['ignored'])}")
    for ir in result["ignored"]:
        print(f"[IGNORADA] {ir['expr']} -> {ir['error']}")

    # Activaciones resumen
    print("Activaciones:")
    for act in result["activations"]:
        print(f" - {act['expr']} (+{act['score']}) count={act['count']}")

    if args.query_name:
        qres = query_name(result, args.query_name)
        print("\nConsulta nombre:")
        print(qres)

    if args.export:
        row_scores = result["row_scores"]
        if args.export_format == "csv":
            row_scores.to_csv(args.export, index=False)
        else:
            row_scores.to_parquet(args.export, index=False)
        print(f"Resultados exportados a {args.export}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
