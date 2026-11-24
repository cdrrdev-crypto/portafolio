# Biblioteca JSON

Catálogo de libros de consola con operaciones para agregar, listar, buscar y eliminar. Los registros persisten en un archivo JSON legible.

## Demo web

La [demo interactiva](https://cdrrdev-crypto.github.io/portafolio-python-jr/#biblioteca) permite buscar y agregar libros de ejemplo. Los cambios solo existen en la sesión del navegador; la aplicación Python descrita abajo sí guarda los datos en un archivo JSON.

## Instalación

Solo requiere Python 3.10 o superior y su biblioteca estándar.

## Uso

Desde la raíz del repositorio:

```powershell
python -m apps.biblioteca_json.main agregar --titulo "El principito" --autor "Antoine de Saint-Exupéry" --anio 1943
python -m apps.biblioteca_json.main listar
python -m apps.biblioteca_json.main buscar "principito"
python -m apps.biblioteca_json.main eliminar ID_DEL_LIBRO
```

El ID se muestra al agregar o listar un libro. El archivo predeterminado es `data/libros.json`; para usar otro, pasa `--archivo ruta.json` antes del subcomando.

## Pruebas

```powershell
python -m unittest apps.biblioteca_json.test_library -v
```
