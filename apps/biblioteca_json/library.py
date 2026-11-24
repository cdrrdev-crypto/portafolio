"""Catálogo de libros con almacenamiento local en JSON."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class Book:
    id: str
    titulo: str
    autor: str
    anio: int


def load_books(path: Path) -> list[Book]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"El archivo JSON está dañado: {path}") from error
    if not isinstance(data, list):
        raise ValueError("El contenido JSON debe ser una lista de libros.")
    try:
        return [Book(**item) for item in data]
    except (TypeError, KeyError) as error:
        raise ValueError("El archivo JSON contiene un libro con formato inválido.") from error


def save_books(path: Path, books: list[Book]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(book) for book in books], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def add_book(books: list[Book], titulo: str, autor: str, anio: int) -> Book:
    titulo, autor = titulo.strip(), autor.strip()
    if not titulo or not autor:
        raise ValueError("El título y el autor son obligatorios.")
    if anio < 0:
        raise ValueError("El año no puede ser negativo.")
    book = Book(uuid4().hex[:8], titulo, autor, anio)
    books.append(book)
    return book


def search_books(books: list[Book], query: str) -> list[Book]:
    query = query.strip().casefold()
    if not query:
        return []
    return [
        book
        for book in books
        if query in book.titulo.casefold() or query in book.autor.casefold()
    ]


def remove_book(books: list[Book], book_id: str) -> bool:
    for index, book in enumerate(books):
        if book.id == book_id:
            del books[index]
            return True
    return False
