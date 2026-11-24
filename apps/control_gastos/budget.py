"""Lógica de registro, resumen y exportación de gastos."""

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from openpyxl import Workbook

CSV_FIELDS = ("fecha", "categoria", "descripcion", "monto")


@dataclass(frozen=True)
class Expense:
    fecha: date
    categoria: str
    descripcion: str
    monto: Decimal


def create_expense(fecha: str, categoria: str, descripcion: str, monto: str) -> Expense:
    """Valida entradas de usuario y crea un gasto."""
    try:
        parsed_date = date.fromisoformat(fecha)
    except ValueError as error:
        raise ValueError("La fecha debe tener formato AAAA-MM-DD.") from error

    categoria = categoria.strip()
    descripcion = descripcion.strip()
    if not categoria or not descripcion:
        raise ValueError("La categoría y la descripción son obligatorias.")
    try:
        amount = Decimal(monto)
    except InvalidOperation as error:
        raise ValueError("El monto debe ser un número válido.") from error
    if not amount.is_finite() or amount <= 0:
        raise ValueError("El monto debe ser mayor que cero.")
    return Expense(parsed_date, categoria, descripcion, amount.quantize(Decimal("0.01")))


def load_expenses(path: Path) -> list[Expense]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != list(CSV_FIELDS):
            raise ValueError(f"El archivo CSV debe contener las columnas: {', '.join(CSV_FIELDS)}.")
        return [
            create_expense(row["fecha"], row["categoria"], row["descripcion"], row["monto"])
            for row in reader
        ]


def save_expenses(path: Path, expenses: list[Expense]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    "fecha": expense.fecha.isoformat(),
                    "categoria": expense.categoria,
                    "descripcion": expense.descripcion,
                    "monto": f"{expense.monto:.2f}",
                }
            )


def summarize(expenses: list[Expense]) -> tuple[Decimal, dict[str, Decimal]]:
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for expense in expenses:
        totals[expense.categoria] += expense.monto
    return sum(totals.values(), Decimal("0.00")), dict(sorted(totals.items()))


def export_excel(path: Path, expenses: list[Expense]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Gastos"
    sheet.append(["Fecha", "Categoría", "Descripción", "Monto"])
    for expense in expenses:
        sheet.append(
            [
                expense.fecha.isoformat(),
                expense.categoria,
                expense.descripcion,
                float(expense.monto),
            ]
        )
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
