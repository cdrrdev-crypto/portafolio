"""Carga, limpieza y resumen de los datos de ventas del portafolio."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = (
    "venta_id",
    "fecha",
    "producto",
    "categoria",
    "region",
    "unidades",
    "precio_unitario",
)
DEFAULT_DATA = Path(__file__).resolve().parents[2] / "docs" / "data" / "ventas.csv"


def load_sales(path: Path = DEFAULT_DATA) -> pd.DataFrame:
    """Carga las ventas, descarta filas incompletas y calcula ingresos."""
    sales = pd.read_csv(path)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(sales.columns))
    if missing_columns:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_columns)}.")

    sales = sales.loc[:, REQUIRED_COLUMNS].copy()
    sales["fecha"] = pd.to_datetime(sales["fecha"], errors="coerce")
    sales["unidades"] = pd.to_numeric(sales["unidades"], errors="coerce")
    sales["precio_unitario"] = pd.to_numeric(sales["precio_unitario"], errors="coerce")

    text_columns = ("venta_id", "producto", "categoria", "region")
    for column in text_columns:
        sales[column] = sales[column].astype("string").str.strip()

    valid_rows = (
        sales["fecha"].notna()
        & sales["unidades"].notna()
        & sales["precio_unitario"].notna()
        & (sales["unidades"] > 0)
        & (sales["precio_unitario"] >= 0)
    )
    for column in text_columns:
        valid_rows &= sales[column].notna() & sales[column].ne("")
    sales = sales.loc[valid_rows].copy()
    if sales.empty:
        raise ValueError("El archivo no contiene filas de ventas válidas.")

    sales["ingresos"] = sales["unidades"] * sales["precio_unitario"]
    sales["mes"] = sales["fecha"].dt.strftime("%Y-%m")
    return sales


def summarize_sales(sales: pd.DataFrame) -> dict[str, object]:
    """Calcula métricas y agrupaciones básicas para el conjunto de ventas."""
    if sales.empty:
        raise ValueError("No se pueden resumir ventas sin filas.")

    revenue_by_category = sales.groupby("categoria")["ingresos"].sum().sort_values(
        ascending=False
    )
    revenue_by_month = sales.groupby("mes")["ingresos"].sum().sort_index()
    revenue_by_product = sales.groupby("producto")["ingresos"].sum().sort_values(
        ascending=False
    )
    total_revenue = float(sales["ingresos"].sum())
    order_count = int(sales["venta_id"].nunique())

    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "units_sold": int(sales["unidades"].sum()),
        "average_order_value": total_revenue / order_count if order_count else 0.0,
        "revenue_by_category": revenue_by_category.to_dict(),
        "revenue_by_month": revenue_by_month.to_dict(),
        "top_products": revenue_by_product.head(5).to_dict(),
    }
