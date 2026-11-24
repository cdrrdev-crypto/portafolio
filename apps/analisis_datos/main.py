"""CLI para explorar y resumir las ventas de demostración."""

import argparse
from pathlib import Path

from .analysis import DEFAULT_DATA, load_sales, summarize_sales


def main() -> int:
    parser = argparse.ArgumentParser(description="Análisis exploratorio de ventas con pandas.")
    parser.add_argument(
        "--archivo",
        type=Path,
        default=DEFAULT_DATA,
        help="Ruta del CSV de ventas",
    )
    args = parser.parse_args()

    summary = summarize_sales(load_sales(args.archivo))
    print(f"Ingresos totales: ${summary['total_revenue']:,.2f}")
    print(f"Ventas: {summary['order_count']}")
    print(f"Unidades vendidas: {summary['units_sold']}")
    print(f"Ticket promedio: ${summary['average_order_value']:,.2f}")
    print("\nIngresos por categoría:")
    for category, amount in summary["revenue_by_category"].items():
        print(f"  {category}: ${amount:,.2f}")
    print("\nIngresos por mes:")
    for month, amount in summary["revenue_by_month"].items():
        print(f"  {month}: ${amount:,.2f}")
    print("\nProductos principales:")
    for product, amount in summary["top_products"].items():
        print(f"  {product}: ${amount:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
