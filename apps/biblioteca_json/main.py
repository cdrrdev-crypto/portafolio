"""CLI para mantener un catálogo personal de libros."""

import argparse
from pathlib import Path

from .library import add_book, load_books, remove_book, save_books, search_books

DEFAULT_JSON = Path("data") / "libros.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Catálogo de libros en un archivo JSON.")
    parser.add_argument("--archivo", type=Path, default=DEFAULT_JSON, help="Ruta del JSON de datos")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("agregar", help="Agregar un libro")
    add.add_argument("--titulo", required=True)
    add.add_argument("--autor", required=True)
    add.add_argument("--anio", type=int, required=True)
    commands.add_parser("listar", help="Listar todos los libros")
    search = commands.add_parser("buscar", help="Buscar por título o autor")
    search.add_argument("consulta")
    delete = commands.add_parser("eliminar", help="Eliminar un libro por su ID")
    delete.add_argument("id")
    args = parser.parse_args()

    books = load_books(args.archivo)
    if args.command == "agregar":
        book = add_book(books, args.titulo, args.autor, args.anio)
        save_books(args.archivo, books)
        print(f"Libro agregado [{book.id}]: {book.titulo} — {book.autor} ({book.anio})")
    elif args.command == "listar":
        for book in books:
            print(f"[{book.id}] {book.titulo} — {book.autor} ({book.anio})")
        if not books:
            print("El catálogo está vacío.")
    elif args.command == "buscar":
        matches = search_books(books, args.consulta)
        for book in matches:
            print(f"[{book.id}] {book.titulo} — {book.autor} ({book.anio})")
        if not matches:
            print("No se encontraron libros.")
    elif args.command == "eliminar":
        if not remove_book(books, args.id):
            print(f"No existe un libro con el ID {args.id}.")
            return 1
        save_books(args.archivo, books)
        print("Libro eliminado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
