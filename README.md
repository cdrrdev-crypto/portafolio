# Portafolio Python Junior

Tres aplicaciones pequeñas para mostrar fundamentos de Python, organización en módulos, manejo de datos, consumo de APIs, pruebas automatizadas y control de versiones.

## Aplicaciones

| Proyecto | Qué demuestra | Documentación |
|---|---|---|
| [Consulta del clima](apps/clima_api/README.md) | API REST con `requests`, validación y manejo de errores | [apps/clima_api/README.md](apps/clima_api/README.md) |
| [Control de gastos](apps/control_gastos/README.md) | CSV, cálculos con `Decimal` y exportación Excel | [apps/control_gastos/README.md](apps/control_gastos/README.md) |
| [Biblioteca JSON](apps/biblioteca_json/README.md) | Funciones, estructuras de datos y persistencia JSON | [apps/biblioteca_json/README.md](apps/biblioteca_json/README.md) |

## Requisitos

- Python 3.10 o superior
- `pip`
- Conexión a Internet para consultar el clima

Cada aplicación es independiente y tiene sus propias dependencias. Desde la raíz:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r apps\clima_api\requirements.txt
python -m pip install -r apps\control_gastos\requirements.txt
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
```

Los archivos de datos se guardan por defecto en una carpeta `data/` relativa al directorio desde el que ejecutas el comando; no se versionan. Consulta el README de cada proyecto para más comandos y formatos.

## Pruebas

Instala las dependencias de las aplicaciones y ejecuta:

```powershell
python -m unittest discover -s apps -t . -v
```

Las pruebas usan datos temporales y no llaman a la API real.

## Tecnologías

Python, `requests`, `openpyxl`, `csv`, `json`, `unittest`, Git y GitHub.
