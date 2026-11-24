# Consulta del clima

CLI que busca una ciudad con el servicio de geocodificación de Open-Meteo y presenta las condiciones meteorológicas actuales. No requiere una clave de API.

## Demo web

Prueba la [consulta web del clima](https://cdrrdev-crypto.github.io/portafolio/#clima) con cualquier ciudad. La demo llama a Open-Meteo desde el navegador; requiere Internet, no usa una API key y no envía datos a un servidor propio.

## Instalación

Desde la raíz del repositorio, activa tu entorno virtual e instala la dependencia:

```powershell
python -m pip install -r apps\clima_api\requirements.txt
```

## Uso

Ejecuta desde la raíz:

```powershell
python -m apps.clima_api.main "Buenos Aires"
```

Se muestran condición, temperatura, sensación térmica, humedad, viento y hora local. Si la ciudad no existe o la API falla, se informa el error y el proceso termina con código distinto de cero.

## Pruebas

```powershell
python -m unittest apps.clima_api.test_weather -v
```

Las solicitudes HTTP están simuladas en las pruebas; no se necesita Internet para ejecutarlas.
