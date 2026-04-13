# Fuel Stations API

API REST desarrollada en **Python con FastAPI** para la búsqueda de estaciones de combustible utilizando la API inspeccionada de **Bencina en Línea**.

---

## Objetivo

Permitir la búsqueda de estaciones de combustible en base a coordenadas geográficas y distintos criterios de búsqueda.

### Casos implementados

- Estación más cercana por producto
- Estación más cercana con menor precio por producto
- Soporte para filtrado por disponibilidad de tienda

---

## Tecnologías utilizadas

- Python 3.11
- FastAPI
- Uvicorn
- Requests
- Pytest
- Swagger UI

---

## Arquitectura del proyecto

```text
fuel-stations-api/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── stations.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   ├── response.py
│   │   └── station.py
│   │
│   ├── schemas/
│   │   └── station_schema.py
│   │
│   ├── services/
│   │   ├── bencina_client.py
│   │   ├── distance_service.py
│   │   └── search_service.py
│   │
│   ├── utils/
│   │   └── helpers.py
│   │
│   └── main.py
│
├── test/
│   └── test_search_service.py
│
├── conftest.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Opibl/fuel-stations-api.git
cd fuel-stations-api
```

Crear entorno virtual.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecutar proyecto

```bash
uvicorn app.main:app --reload
```

Servidor disponible en:

```text
http://127.0.0.1:8000
```

La API puede probarse localmente desde Swagger en:

```text
http://127.0.0.1:8000/docs
```

Desde esta interfaz es posible probar directamente el endpoint:

```http
GET /api/stations/search
```

ingresando los parámetros requeridos (`lat`, `lng`, `product`, `nearest`, `store`, `cheapest`).

---

## Ejecutar tests

Se incorporó una prueba unitaria básica para validar la lógica de distancia geográfica.

```bash
pytest
```

Resultado esperado:

```text
1 passed
```

---

## Endpoint principal

### Buscar estación

```http
GET /api/stations/search
```

---

## Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|----------|------|-----------|-------------|
| lat | float | Sí | Latitud |
| lng | float | Sí | Longitud |
| product | string | Sí | 93, 95, 97, diesel, kerosene |
| nearest | bool | No | Buscar estación más cercana |
| store | bool | No | Filtrar estaciones con tienda |
| cheapest | bool | No | Buscar estación con menor precio |

---

## Ejemplos de uso

### Estación más cercana

```text
/api/stations/search?lat=-33.0364&lng=-71.6296&product=93&nearest=true
```

### Estación más cercana con menor precio

```text
/api/stations/search?lat=-33.0364&lng=-71.6296&product=93&nearest=true&cheapest=true
```

### Estación con filtro de tienda

```text
/api/stations/search?lat=-33.0364&lng=-71.6296&product=93&nearest=true&store=true
```

---

## Respuesta de ejemplo

```json
{
  "success": true,
  "data": {
    "id": "1572",
    "compania": "SHELL",
    "direccion": "BRASIL 154",
    "comuna": "Santiago Centro",
    "region": "Metropolitana de Santiago",
    "latitud": -33.44241788189269,
    "longitud": -70.66533923149109,
    "distancia_lineal": 0.81,
    "precio": 1515,
    "tiene_tienda": true,
    "tienda": {
      "codigo": null,
      "nombre": "Tienda de conveniencia",
      "tipo": "Conveniencia"
    }
  }
}
```

---

## Manejo de errores

La API implementa manejo de errores y excepciones utilizando:

- `HTTPException`
- `StationNotFoundException`

Se retornan respuestas HTTP informativas para errores de búsqueda o parámetros inválidos.

---

## Fuente de datos

La API utiliza datos obtenidos mediante inspección de la página oficial:

```text
https://www.bencinaenlinea.cl/#/busqueda_estaciones
```

### Endpoints inspeccionados

Detalle por estación:

```text
https://api.bencinaenlinea.cl/api/estacion_ciudadano/{id}
```

Listado masivo de estaciones:

```text
https://api.bencinaenlinea.cl/api/busqueda_estacion_filtro
```

---

## Nota sobre la implementación

Durante la inspección de red se identificó el endpoint público utilizado por la plataforma para obtener el **listado masivo de estaciones**.

La solución utiliza este endpoint como fuente principal de datos y posteriormente aplica:

- filtrado por producto
- cálculo de distancia lineal (Haversine)
- selección por menor precio
- filtrado por disponibilidad de tienda

Esto permitió optimizar la estrategia inicial basada en consulta por identificadores individuales, mejorando escalabilidad, rendimiento y cobertura geográfica a nivel nacional.

---

## Normalización de datos

La estructura de respuesta entregada por la API fuente presenta diferencias respecto al formato solicitado en la prueba técnica.

Por este motivo se implementó una capa de normalización para exponer un formato consistente orientado al consumo REST.

Se normalizan especialmente:

- coordenadas con coma decimal
- precios nulos o inconsistentes
- campos opcionales
- información de tienda
- nombre de compañía

---

## Autor

Pedro Ignacio Basualto León