# Análisis de ventas

Análisis exploratorio de un conjunto de ventas ficticio con `pandas`. La aplicación limpia fechas y números, descarta filas inválidas y calcula ingresos, unidades vendidas, ticket promedio y agrupaciones por mes, categoría y producto.

## Instalación y uso

Desde la raíz del repositorio:

```powershell
python -m pip install -r apps\analisis_datos\requirements.txt
python -m apps.analisis_datos.main
```

Para analizar otro CSV con las mismas columnas:

```powershell
python -m apps.analisis_datos.main --archivo ruta\ventas.csv
```

El conjunto de datos de ejemplo está en `docs/data/ventas.csv`; contiene datos sintéticos, no información de clientes reales. La misma fuente alimenta el dashboard web.

## Pruebas

```powershell
python -m unittest apps.analisis_datos.test_analysis -v
```

## Demo web

El [dashboard interactivo de ventas](https://cdrrdev-crypto.github.io/portafolio/#analisis) permite filtrar por categoría y región. La demo web es estática y no ejecuta Python en el servidor.
