# ✈️ Databricks Flights Reader

Una aplicación web desarrollada con FastAPI y Databricks SQL Warehouse que permite consultar, filtrar y visualizar en tiempo real un conjunto de datos sobre vuelos. La interfaz ofrece un panel interactivo con comboboxes alimentados dinámicamente desde el Data Lakehouse.

🚀 [Probar Aplicación en Vivo](httpsTU-APP-EN-RENDER.onrender.com) (Sustituye por tu URL de Render)

---

## 🛠️ Stack Tecnológico

 Backend [FastAPI](httpsfastapi.tiangolo.com) (Python)
 Base de Datos  Warehouse [Databricks Delta Lake](httpswww.databricks.com) mediante `databricks-sql-connector`
 Frontend HTML5, Jinja2 Templates, Tailwind CSS
 Servidor de Producción [Uvicorn](httpswww.uvicorn.org)
 Despliegue  Hosting [Render](httpsrender.com)

---

## 💡 Características Principales

1. Conexión SQL remota Ejecución de consultas `DISTINCT` y filtrado directo sobre la tabla `selectdata.vuelos_india.flights` en Databricks.
2. Comboboxes Dinámicos Las opciones de filtrado (Airline, Source, Destination) se leen automáticamente del Warehouse.
3. Filtros Combinados Construcción dinámica de la consulta SQL (`WHERE 1=1 AND ...`) según los parámetros seleccionados por el usuario.
4. Respuesta Rápida e Interfaz Responsiva Diseño limpio utilizando Tailwind CSS.

---

## 📊 Origen de los Datos

Los datos utilizados para este proyecto provienen del dataset público de vuelos de la India alojado en [Kaggle](httpswww.kaggle.com), el cual fue precargado y estructurado dentro de un esquema de Databricks Delta Lake.

---

## ⚙️ Configuración e Instalación Local

Si deseas ejecutar este proyecto de forma local, sigue estos pasos

### 1. Clonar el repositorio

```bash
git clone [httpsgithub.comTU_USUARIOdatabricks-fastapi-flights.git](httpsgithub.comTU_USUARIOdatabricks-fastapi-flights.git)
cd databricks-fastapi-flights
