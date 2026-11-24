import tempfile
import unittest
from pathlib import Path

from apps.biblioteca_json.library import (
    add_book,
    load_books,
    remove_book,
    save_books,
    search_books,
)


class LibraryTests(unittest.TestCase):
    def test_json_round_trip_and_search_are_case_insensitive(self):
        books = []
        added = add_book(books, "Cien años de soledad", "Gabriel García Márquez", 1967)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data" / "libros.json"
            save_books(path, books)
            loaded = load_books(path)

        self.assertEqual(loaded, [added])
        self.assertEqual(search_books(loaded, "GARCÍA"), [added])

    def test_remove_returns_false_when_id_is_missing(self):
        books = []
        add_book(books, "El libro", "Una autora", 2020)

        self.assertFalse(remove_book(books, "missing"))
        self.assertEqual(len(books), 1)

    def test_invalid_book_is_rejected(self):
        with self.assertRaises(ValueError):
            add_book([], "  ", "Autor", 2020)
        with self.assertRaises(ValueError):
            add_book([], "Título", "Autor", -1)

    def test_malformed_json_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "libros.json"
            path.write_text("{", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "dañado"):
                load_books(path)


if __name__ == "__main__":
    unittest.main()
