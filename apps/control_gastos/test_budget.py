import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl import load_workbook

from apps.control_gastos.budget import (
    create_expense,
    export_excel,
    load_expenses,
    save_expenses,
    summarize,
)


class BudgetTests(unittest.TestCase):
    def test_create_expense_rejects_bad_date_and_amount(self):
        with self.assertRaises(ValueError):
            create_expense("31/12/2025", "Comida", "Almuerzo", "10")
        with self.assertRaises(ValueError):
            create_expense("2025-12-31", "Comida", "Almuerzo", "-1")

    def test_csv_round_trip_and_category_totals(self):
        first = create_expense("2025-01-03", "Comida", "Almuerzo", "12.50")
        second = create_expense("2025-01-04", "Comida", "Café", "3.25")
        third = create_expense("2025-01-05", "Transporte", "Bus", "2")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "gastos.csv"

            save_expenses(path, [first, second, third])
            loaded = load_expenses(path)
            total, categories = summarize(loaded)

        self.assertEqual(loaded[0].fecha, date(2025, 1, 3))
        self.assertEqual(total, Decimal("17.75"))
        self.assertEqual(categories["Comida"], Decimal("15.75"))

    def test_excel_export_contains_header_and_amount(self):
        expense = create_expense("2025-01-03", "Comida", "Almuerzo", "12.50")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reporte.xlsx"
            export_excel(path, [expense])

            sheet = load_workbook(path, data_only=True).active
            self.assertEqual(sheet["A1"].value, "Fecha")
            self.assertEqual(sheet["D2"].value, 12.5)


if __name__ == "__main__":
    unittest.main()
