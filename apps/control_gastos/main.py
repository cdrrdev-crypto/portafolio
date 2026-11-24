"""CLI para registrar gastos, consultar totales y exportar a Excel."""

import argparse
from decimal import Decimal
from pathlib import Path

from .budget import create_expense, export_excel, load_expenses, save_expenses, summarize

DEFAULT_CSV = Path("data") / "gastos.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description="Control de gastos personales en CSV y Excel.")
    parser.add_argument("--archivo", type=Path, default=DEFAULT_CSV, help="Ruta del CSV de datos")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("agregar", help="Registrar un gasto")
    add.add_argument("--fecha", required=True, help="Fecha AAAA-MM-DD")
    add.add_argument("--categoria", required=True)
    add.add_argument("--descripcion", required=True)
    add.add_argument("--monto", required=True)
    commands.add_parser("listar", help="Mostrar los gastos registrados")
    commands.add_parser("resumen", help="Mostrar totales por categoría")
    export = commands.add_parser("exportar", help="Exportar los datos a un archivo Excel")
    export.add_argument("destino", type=Path, help="Ruta del archivo .xlsx")
    args = parser.parse_args()

    expenses = load_expenses(args.archivo)
    if args.command == "agregar":
        expense = create_expense(args.fecha, args.categoria, args.descripcion, args.monto)
        expenses.append(expense)
        save_expenses(args.archivo, expenses)
        print(f"Gasto guardado: {expense.categoria} - {expense.monto:.2f}")
    elif args.command == "listar":
        if not expenses:
            print("Aún no hay gastos registrados.")
        for expense in expenses:
            print(
                f"{expense.fecha.isoformat()} | {expense.categoria} | "
                f"{expense.descripcion} | {expense.monto:.2f}"
            )
    elif args.command == "resumen":
        total, by_category = summarize(expenses)
        print(f"Total: {total:.2f}")
        for category, amount in by_category.items():
            print(f"  {category}: {amount:.2f}")
    else:
        export_excel(args.destino, expenses)
        print(f"Excel exportado: {args.destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
