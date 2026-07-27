import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from databricks import sql

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(title="Databricks Flights Reader")
templates = Jinja2Templates(directory="templates")

NOMBRE_TABLA = "selectdata.vuelos_india.flights"

def obtener_conexion():
    """Crea la conexión a Databricks usando las variables de entorno."""
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")

    if not server_hostname or not http_path or not access_token:
        raise ValueError("Faltan variables de entorno en el archivo .env")

    return sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    )

def obtener_opciones_filtros():
    """Consulta los valores únicos para llenar los comboboxes."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                # Obtener valores únicos para la columna airline
                cursor.execute(f"SELECT DISTINCT airline FROM {NOMBRE_TABLA} WHERE airline IS NOT NULL ORDER BY airline")
                airlines = [row[0] for row in cursor.fetchall()]

                # Obtener valores únicos para la columna Source
                cursor.execute(f"SELECT DISTINCT Source FROM {NOMBRE_TABLA} WHERE Source IS NOT NULL ORDER BY Source")
                sources = [row[0] for row in cursor.fetchall()]

                # Obtener valores únicos para la columna Destination
                cursor.execute(f"SELECT DISTINCT Destination FROM {NOMBRE_TABLA} WHERE Destination IS NOT NULL ORDER BY Destination")
                destinations = [row[0] for row in cursor.fetchall()]

                return airlines, sources, destinations
    except Exception as e:
        print(f"⚠️ Error al cargar opciones de filtros: {e}")
        return [], [], []

def consultar_vuelos_filtrados(airline: str = None, source: str = None, destination: str = None, limit: int = 100):
    """Aplica los filtros opcionales sobre la tabla en Databricks."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {NOMBRE_TABLA} WHERE 1=1"
            
            # Construcción dinámica del WHERE según las selecciones
            if airline:
                query += f" AND airline = '{airline}'"
            if source:
                query += f" AND Source = '{source}'"
            if destination:
                query += f" AND Destination = '{destination}'"

            query += f" LIMIT {limit}"

            cursor.execute(query)

            columnas = [column[0] for column in cursor.description]
            registros_raw = cursor.fetchall()
            registros = [list(fila) for fila in registros_raw]

            return columnas, registros

@app.get("/", response_class=HTMLResponse)
async def inicio(
    request: Request,
    airline: str = Query(None),
    source: str = Query(None),
    destination: str = Query(None)
):
    try:
        # 1. Obtener valores únicos para los comboboxes
        opciones_airlines, opciones_sources, opciones_destinations = obtener_opciones_filtros()

        # 2. Consultar registros aplicando los filtros si el usuario seleccionó alguno
        columnas, registros = consultar_vuelos_filtrados(
            airline=airline, 
            source=source, 
            destination=destination
        )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "columnas": columnas,
                "registros": registros,
                "opciones_airlines": opciones_airlines,
                "opciones_sources": opciones_sources,
                "opciones_destinations": opciones_destinations,
                "selected_airline": airline,
                "selected_source": source,
                "selected_destination": destination,
                "error": None
            }
        )
    except Exception as e:
        print(f"\n❌ Error capturado en el servidor: {e}\n")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "columnas": [],
                "registros": [],
                "opciones_airlines": [],
                "opciones_sources": [],
                "opciones_destinations": [],
                "selected_airline": None,
                "selected_source": None,
                "selected_destination": None,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)