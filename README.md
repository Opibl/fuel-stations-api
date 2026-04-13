# Fuel Stations API

API REST desarrollada en **Python con FastAPI** para la búsqueda de estaciones de combustible utilizando la API inspeccionada de **Bencina en Línea**.

---

## Objetivo

Permitir la búsqueda de estaciones de combustible en base a coordenadas geográficas y distintos criterios de búsqueda.

### Casos implementados

* Estación más cercana por producto
* Estación más cercana con menor precio por producto
* Estación más cercana con tienda por producto
* Estación más cercana con tienda y menor precio por producto

---

## Tecnologías utilizadas

* Python 3.11
* FastAPI
* Uvicorn
* Requests
* Pytest
* Swagger UI

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

Documentación Swagger:

```text
http://127.0.0.1:8000/docs
```

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

| Parámetro | Tipo   | Requerido | Descripción                      |
| --------- | ------ | --------- | -------------------------------- |
| lat       | float  | Sí        | Latitud                          |
| lng       | float  | Sí        | Longitud                         |
| product   | string | Sí        | 93, 95, 97, diesel, kerosene     |
| nearest   | bool   | No        | Buscar estación más cercana      |
| store     | bool   | No        | Filtrar estaciones con tienda    |
| cheapest  | bool   | No        | Buscar estación con menor precio |

---

## Ejemplos de uso

### 1. Estación más cercana

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true
```

### 2. Estación más cercana con menor precio

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&cheapest=true
```

### 3. Estación más cercana con tienda

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&store=true
```

### 4. Estación más cercana con tienda y menor precio

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&store=true&cheapest=true
```

---

## Respuesta de ejemplo

```json
{
  "success": true,
  "data": {
    "id": "1556",
    "compania": "Sin marca",
    "direccion": "Avenida Matta 665",
    "comuna": "Santiago Centro",
    "region": "Metropolitana de Santiago",
    "latitud": -33.4578,
    "longitud": -70.6423,
    "distancia_lineal": 1.29,
    "precio": 1241,
    "tiene_tienda": true,
    "tienda": {
      "codigo": 4,
      "nombre": "Tienda de conveniencia",
      "tipo": "Conveniencia"
    }
  }
}
```

---

## Manejo de errores

La API implementa manejo de errores y excepciones utilizando:

* `HTTPException`
* `StationNotFoundException`

Se retornan respuestas HTTP informativas para errores de búsqueda o parámetros inválidos.

---

## Fuente de datos

La API utiliza datos obtenidos mediante inspección de la página:

```text
https://www.bencinaenlinea.cl/#/busqueda_estaciones
```

Endpoint inspeccionado:

```text
https://api.bencinaenlinea.cl/api/estacion_ciudadano/{id}
```

## Nota sobre la obtención del listado

Durante la inspección de la página oficial de **Bencina en Línea**, se identificó el endpoint público utilizado para consultar el detalle de una estación por identificador:

```http
GET /api/estacion_ciudadano/{id}
```

Sin embargo, no fue posible identificar un endpoint público de listado masivo de estaciones por zona o coordenadas mediante inspección de red.

Por este motivo, la solución implementa una estrategia de consulta dinámica basada en identificadores reales observados desde la página, aplicando posteriormente la lógica de filtrado por producto, distancia, menor precio y disponibilidad de tienda.

Esta decisión permite mantener el uso de la API inspeccionada solicitada en la prueba técnica, replicando el comportamiento observado desde la página web.

---

## Nota sobre la estructura de datos

La prueba técnica incluye un ejemplo de respuesta JSON como referencia.

Durante la implementación, se utilizó la **API real inspeccionada desde Bencina en Línea**, obtenida directamente desde la página oficial mediante inspección de red.

La estructura de la respuesta real presenta algunas diferencias respecto al ejemplo entregado en la prueba, por lo que se realizó una **normalización de datos** para exponer un formato limpio, consistente y orientado al consumo del endpoint:

```http
GET /api/stations/search
```

De esta forma se mantiene toda la información relevante solicitada:

* compañía
* dirección
* comuna
* región
* coordenadas
* precio
* tienda
* distancia lineal

Esta decisión se tomó para asegurar una respuesta REST consistente, limpia y fácil de consumir desde clientes externos.

---

## Autor

Pedro Ignacio Basualto León
