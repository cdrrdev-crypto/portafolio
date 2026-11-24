import tempfile
import unittest
from pathlib import Path

from apps.analisis_datos.analysis import load_sales, summarize_sales


class SalesAnalysisTests(unittest.TestCase):
    def test_demo_csv_produces_metrics_and_ranked_categories(self):
        sales = load_sales()
        summary = summarize_sales(sales)

        self.assertGreater(summary["total_revenue"], 0)
        self.assertEqual(summary["order_count"], len(sales))
        category_values = list(summary["revenue_by_category"].values())
        self.assertEqual(category_values, sorted(category_values, reverse=True))

    def test_loader_discards_invalid_rows_and_reports_missing_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sales.csv"
            path.write_text(
                "venta_id,fecha,producto,categoria,region,unidades,precio_unitario\n"
                "1,2025-01-03,Cuaderno,Papelería,Norte,2,3.50\n"
                "2,fecha-invalida,Lápiz,Papelería,Norte,1,1.00\n"
                "3,2025-01-04,Regla,Papelería,Norte,0,2.00\n",
                encoding="utf-8",
            )

            sales = load_sales(path)

            self.assertEqual(len(sales), 1)
            self.assertEqual(sales.iloc[0]["ingresos"], 7.0)

            path.write_text("fecha,producto\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Faltan columnas"):
                load_sales(path)


if __name__ == "__main__":
    unittest.main()
