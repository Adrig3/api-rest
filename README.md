# Proyecto API REST - Sakila

**Autores:** Daniel Cobo y Adrià Gari

## Descripción

API REST mínima construida con Flask y SQLAlchemy que expone recursos sobre clientes (`customer`) y alquileres (`rental`) basados en la base de datos de ejemplo Sakila (MySQL).

El propósito es ofrecer endpoints para crear, leer, actualizar y eliminar clientes, así como gestionar alquileres (crear, listar, devolver).

## Estructura del proyecto

- `app.py` : aplicación Flask principal con todos los endpoints.
- `requirements.txt` : dependencias del proyecto.
- `archivos_bd/` : archivos de la base de datos de ejemplo Sakila (schema, datos y proyecto MySQL Workbench).

## Requisitos previos

- Python 3.8+ instalado.
- MySQL (servidor) instalado y accesible localmente.
- La base de datos `sakila` debe existir y estar poblada (ver sección siguiente).

## Preparar dependencias

1. Crear y activar un entorno virtual (recomendado):

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS / Linux
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:

```bash
python app.py
```

La aplicación arranca por defecto en `http://127.0.0.1:5000` con `debug=True`.

## Base de datos Sakila

La API usa la base de datos de ejemplo `sakila`. Debe estar creada y con los datos cargados en tu servidor MySQL local.

En `app.py` la configuración por defecto es:

```
mysql+pymysql://root:root@localhost/sakila
```

Si tus credenciales o host son distintas, edita `app.py` o configura la variable de entorno correspondiente antes de ejecutar.

Si no tienes la base de datos, en la carpeta `archivos_bd/` encontrarás:

- `sakila-schema.sql` : esquema de la base de datos.
- `sakila-data.sql` : datos de ejemplo.
- `sakila.mwb` : proyecto de MySQL Workbench.

Pasos para crearla e importarla (ejemplo con cliente `mysql`):

```bash
# conectarse al servidor MySQL con un usuario administrador
mysql -u root -p

# dentro del cliente MySQL crear la base de datos (si hace falta)
CREATE DATABASE sakila;
USE sakila;
EXIT;

# desde la terminal (Windows / Linux)
mysql -u root -p sakila < archivos_bd/sakila-schema.sql
mysql -u root -p sakila < archivos_bd/sakila-data.sql
```

Después de esto, la base de datos `sakila` debería estar disponible para que `app.py` la use.

## Endpoints disponibles

Todos los endpoints están bajo el prefijo `/api/v1/`.

- **Crear cliente**
  - Método: `POST`
  - Ruta: `/api/v1/customers`
  - Descripción: Crea un nuevo registro en la tabla `customer`.
  - Body (JSON) ejemplo:

```json
{
  "store_id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan@example.com",
  "address_id": 5,
  "active": 1
}
```

- Ejemplo curl:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/customers \
  -H "Content-Type: application/json" \
  -d "{\"store_id\":1,\"first_name\":\"Juan\",\"last_name\":\"Pérez\",\"email\":\"juan@example.com\",\"address_id\":5}"
```

- **Listar clientes**
  - Método: `GET`
  - Ruta: `/api/v1/customers`
  - Parámetros query opcionales:
    - `limit` (int): número máximo de registros a devolver (por defecto en el código: `700`).
    - `offset` (int): desplazamiento para paginación (por defecto `0`).
    - `first_name`, `last_name`, `email`: filtros parciales (LIKE).
  - Ejemplo:

```bash
curl "http://127.0.0.1:5000/api/v1/customers?limit=10&offset=0&first_name=Juan"
```

- **Obtener cliente por ID**
  - Método: `GET`
  - Ruta: `/api/v1/customers/<customer_id>`
  - Descripción: Devuelve los datos del cliente indicado.
  - Ejemplo:

```bash
curl http://127.0.0.1:5000/api/v1/customers/1
```

- **Actualizar cliente**
  - Método: `PUT`
  - Ruta: `/api/v1/customers/<customer_id>`
  - Body (JSON): campos a actualizar (se conservan los valores no proporcionados).
  - Ejemplo:

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/customers/1 \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"nuevo@example.com\"}"
```

- **Eliminar cliente**
  - Método: `DELETE`
  - Ruta: `/api/v1/customers/<customer_id>`
  - Ejemplo:

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/customers/1
```

- **Crear alquiler**
  - Método: `POST`
  - Ruta: `/api/v1/rentals`
  - Descripción: Inserta un registro en `rental`. Los campos requeridos en el body JSON son `inventory_id`, `customer_id` y `staff_id`.
  - Body (JSON) ejemplo:

```json
{
  "inventory_id": 12,
  "customer_id": 1,
  "staff_id": 1
}
```

- Ejemplo curl:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/rentals \
  -H "Content-Type: application/json" \
  -d "{\"inventory_id\":12,\"customer_id\":1,\"staff_id\":1}"
```

- **Obtener alquiler por ID**
  - Método: `GET`
  - Ruta: `/api/v1/rentals/<rental_id>`
  - Ejemplo:

```bash
curl http://127.0.0.1:5000/api/v1/rentals/1
```

- **Devolver alquiler**
  - Método: `PUT`
  - Ruta: `/api/v1/rentals/<rental_id>/return`
  - Descripción: Marca el `return_date` del alquiler con la fecha actual. Devuelve error si ya fue devuelto.
  - Ejemplo:

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/rentals/1/return
```

- **Listar alquileres de un cliente**
  - Método: `GET`
  - Ruta: `/api/v1/customers/<customer_id>/rentals`
  - Ejemplo:

```bash
curl http://127.0.0.1:5000/api/v1/customers/1/rentals
```

- **Listar alquileres (paginado)**
  - Método: `GET`
  - Ruta: `/api/v1/rentals`
  - Parámetros: `limit` (por defecto 50), `offset` (por defecto 0).
  - Ejemplo:

```bash
curl "http://127.0.0.1:5000/api/v1/rentals?limit=20&offset=0"
```
