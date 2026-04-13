# Fuel Stations API

API REST desarrollada en **Python con FastAPI** para la búsqueda de estaciones de combustible utilizando la API inspeccionada de **Bencina en Línea**.

## Objetivo

Permitir la búsqueda de estaciones de combustible en base a coordenadas geográficas y distintos criterios de búsqueda:

* Estación más cercana por producto
* Estación más cercana con menor precio
* Estación más cercana con tienda
* Estación más cercana con tienda y menor precio

---

## Tecnologías utilizadas

* Python 3.11
* FastAPI
* Uvicorn
* Requests
* Swagger UI

---

## Estructura del proyecto

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
│   │   └── response.py
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
├── requirements.txt
└── README.md
```

---

## Instalación

Clonar repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd fuel-stations-api
```

Crear entorno virtual:

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

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Endpoint principal

### Buscar estación

```http
GET /api/stations/search
```

### Parámetros

| Parámetro | Tipo   | Requerido | Descripción                  |
| --------- | ------ | --------- | ---------------------------- |
| lat       | float  | Sí        | Latitud                      |
| lng       | float  | Sí        | Longitud                     |
| product   | string | Sí        | 93, 95, 97, diesel, kerosene |
| nearest   | bool   | No        | Buscar más cercana           |
| store     | bool   | No        | Filtrar con tienda           |
| cheapest  | bool   | No        | Filtrar menor precio         |

---

## Ejemplos de uso

### 1. Estación más cercana

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true
```

---

### 2. Más cercana con menor precio

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&cheapest=true
```

---

### 3. Más cercana con tienda

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&store=true
```

---

### 4. Más cercana con tienda y menor precio

```text
/api/stations/search?lat=-33.4463&lng=-70.6427&product=93&nearest=true&store=true&cheapest=true
```

---

## Respuesta ejemplo

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

## Fuente de datos

La API utiliza datos obtenidos mediante inspección de la página:

```text
https://www.bencinaenlinea.cl/#/busqueda_estaciones
```

Endpoint inspeccionado:

```text
https://api.bencinaenlinea.cl/api/estacion_ciudadano/{id}
```

---

## Autor

Pedro Ignacio Basualto Leon 
