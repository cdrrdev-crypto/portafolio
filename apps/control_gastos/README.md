# Control de gastos

Aplicación de consola para registrar gastos personales, calcular totales por categoría y exportar los registros a un libro Excel.

## Instalación

```powershell
python -m pip install -r apps\control_gastos\requirements.txt
```

## Uso

Desde la raíz del repositorio:

```powershell
python -m apps.control_gastos.main agregar --fecha 2025-04-15 --categoria Transporte --descripcion "Viaje en bus" --monto 2.50
python -m apps.control_gastos.main listar
python -m apps.control_gastos.main resumen
python -m apps.control_gastos.main exportar gastos.xlsx
```

Los datos se guardan en `data/gastos.csv`. Puedes elegir otra ubicación con `--archivo` antes del subcomando:

```powershell
python -m apps.control_gastos.main --archivo datos/mis_gastos.csv listar
```

Las fechas usan `AAAA-MM-DD`; los montos deben ser positivos. El CSV usa UTF-8 y el Excel se genera con una hoja llamada `Gastos`.

## Pruebas

```powershell
python -m unittest apps.control_gastos.test_budget -v
```
