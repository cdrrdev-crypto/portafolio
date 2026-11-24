# Portafolio Python Junior

Portafolio de proyectos para mostrar fundamentos de Python, análisis de datos, consumo de APIs, pruebas automatizadas y control de versiones.

## Portafolio web

La [interfaz web](https://cdrrdev-crypto.github.io/portafolio-python-jr/) reúne demos interactivas de todos los proyectos y un dashboard de análisis de ventas. Está construida como un sitio estático, sin backend, claves privadas ni servicios de pago. Los datos que se agregan en las demos viven solo en la sesión del navegador; el proyecto de clima consulta Open-Meteo y requiere Internet.

El sitio usa GitHub Pages, incluido sin costo para repositorios públicos. En **Settings > Pages**, selecciona **Deploy from a branch**, la rama `main` y la carpeta `/docs`, y guarda. Después de configurarlo, cada push a `main` actualiza el sitio. El enlace anterior estará disponible cuando termine la primera publicación.

## Aplicaciones

| Proyecto | Qué demuestra | Documentación y demo |
|---|---|---|
| [Análisis de ventas](apps/analisis_datos/README.md) | Limpieza, métricas y agrupaciones con `pandas` | [Documentación](apps/analisis_datos/README.md) · [Dashboard](https://cdrrdev-crypto.github.io/portafolio-python-jr/#analisis) |
| [Consulta del clima](apps/clima_api/README.md) | API REST con `requests`, validación y manejo de errores | [Documentación](apps/clima_api/README.md) · [Demo](https://cdrrdev-crypto.github.io/portafolio-python-jr/#clima) |
| [Control de gastos](apps/control_gastos/README.md) | CSV, cálculos con `Decimal` y exportación Excel | [Documentación](apps/control_gastos/README.md) · [Demo](https://cdrrdev-crypto.github.io/portafolio-python-jr/#gastos) |
| [Biblioteca JSON](apps/biblioteca_json/README.md) | Funciones, estructuras de datos y persistencia JSON | [Documentación](apps/biblioteca_json/README.md) · [Demo](https://cdrrdev-crypto.github.io/portafolio-python-jr/#biblioteca) |

## Requisitos

- Python 3.10 o superior
- `pip`
- Conexión a Internet para consultar el clima
- `pandas` para el análisis de ventas

Cada aplicación es independiente y tiene sus propias dependencias. Instala las necesarias desde la raíz:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r apps\clima_api\requirements.txt
python -m pip install -r apps\control_gastos\requirements.txt
python -m pip install -r apps\analisis_datos\requirements.txt
```

La aplicación de biblioteca usa únicamente la biblioteca estándar.

## Ejecutar

Desde la raíz del repositorio:

```powershell
python -m apps.clima_api.main Madrid
python -m apps.control_gastos.main agregar --fecha 2025-04-15 --categoria Comida --descripcion Almuerzo --monto 12.50
python -m apps.control_gastos.main resumen
python -m apps.control_gastos.main exportar reporte.xlsx
python -m apps.biblioteca_json.main agregar --titulo "El principito" --autor "Antoine de Saint-Exupéry" --anio 1943
python -m apps.biblioteca_json.main listar
python -m apps.analisis_datos.main
```

Los datos creados por las aplicaciones de consola se guardan por defecto en una carpeta `data/` relativa al directorio desde el que ejecutas el comando y no se versionan. El conjunto sintético del dashboard sí está versionado en `docs/data/ventas.csv`.

## Ejecutar en GitHub Codespaces

El repositorio incluye una configuración de Codespaces que instala Python y las dependencias de las aplicaciones al crear el entorno.

1. Abre el repositorio en GitHub y selecciona **Code > Codespaces > Create codespace on main**.
2. Cuando se abra VS Code en el navegador, abre una terminal y ejecuta cualquiera de los comandos de la sección anterior.

Por ejemplo:

```bash
python -m apps.clima_api.main Madrid
python -m apps.control_gastos.main resumen
python -m apps.biblioteca_json.main listar
python -m apps.analisis_datos.main
```

La consulta del clima necesita conexión a Internet. Codespaces requiere que la función esté disponible en la cuenta y puede estar sujeta a cuotas de uso; no es necesario para visitar las demos de GitHub Pages.

## Pruebas

Instala las dependencias de las aplicaciones y ejecuta:

```powershell
python -m pip install -r apps\clima_api\requirements.txt
python -m pip install -r apps\control_gastos\requirements.txt
python -m pip install -r apps\analisis_datos\requirements.txt
python -m unittest discover -s apps -t . -v
```

Las pruebas usan datos temporales y no llaman a la API real.

## Tecnologías

Python, `pandas`, `requests`, `openpyxl`, `csv`, `json`, `unittest`, HTML, CSS, JavaScript, Git y GitHub Pages.
