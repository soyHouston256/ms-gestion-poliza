from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
import mysql.connector
from mysql.connector import Error
import schemas

app = FastAPI(
    title="ms-gestion-poliza",
    description="API para gestión de pólizas y productos de seguros",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Endpoints para verificación de salud del servicio"
        },
        {
            "name": "productos",
            "description": "Operaciones relacionadas con productos de seguros"
        },
        {
            "name": "polizas",
            "description": "Operaciones relacionadas con pólizas de seguros"
        }
    ]
)

origins = ['*'] # Permite que el Api Rest se consuma desde cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

host_name = os.getenv("MYSQL_HOST", "localhost") # IPv4 privada de "MV Bases de Datos"
port_number = os.getenv("MYSQL_PORT", "3306")
user_name = os.getenv("MYSQL_USER", "root")
password_db = os.getenv("MYSQL_PASSWORD", "root")
database_name = os.getenv("MYSQL_DATABASE", "db_poliza")

# Get echo test for load balancer's health check
@app.get("/health", tags=["health"])
def get_echo_test():
    return {"data": None, "success": True, "errorMessage": None }

# Get all polizas
@app.get("/productos", tags=["productos"])
def get_productos():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )

        cursor = mydb.cursor()
        cursor.execute("SELECT id, nombre, codigo, descripcion, categoria, modalidad FROM policy_types")
        result = cursor.fetchall()
        cursor.close()
        mydb.close()

        print(f"Result from database: {result}")  # Debug print

        productos = []
        if result:
            for row in result:
                print(f"Processing row: {row}")  # Debug print
                producto_dict = {
                    "id": row[0],
                    "nombre": row[1],
                    "codigo": row[2],
                    "descripcion": row[3],
                    "categoria": row[4],
                    "modalidad": row[5]
                }
                producto_out = schemas.ProductoOut(**producto_dict)
                productos.append(producto_out.dict())

        print(f"Final productos: {productos}")  # Debug print
        return {"data": productos, "success": True, "errorMessage": None }

    except Error as e:
        # Catch database-related errors
        return {"data": None, "success": False, "errorMessage": f"MySQL Error: {e}"}

    except Exception as e:
        # Catch any other errors
        return {"data": None, "success": False, "errorMessage": f"Unexpected error: {str(e)}"}

# Get an poliza by persona ID
@app.get("/producto/{codigo}", tags=["productos"])
def get_producto(codigo: str):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM policy_types WHERE codigo = %s", (codigo,))
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        
        productos = []
        if result:
            for row in result:
                producto_dict = {
                    "id": row[0],
                    "nombre": row[1],
                    "codigo": row[2],
                    "descripcion": row[3],
                    "categoria": row[4],
                    "modalidad": row[5]
                }
                producto = schemas.ProductoOut(**producto_dict)
                productos.append(producto.dict())
            
            return {"data": productos, "success": True, "errorMessage": None }
        else:
            return {"data": None, "success": False, "errorMessage": "Producto no encontrado"}
    except Error as e:
        return {"data": None, "success": False, "errorMessage": f"MySQL Error: {e}"}
    except Exception as e:
        return {"data": None, "success": False, "errorMessage": f"Unexpected error: {str(e)}"}

# Get polizas by persona ID
@app.get("/polizas/{codigo_persona}", tags=["polizas"])
def get_polizas_by_persona(codigo_persona: int):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM polizas WHERE codigo_persona = %s", (codigo_persona,))
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        
        polizas = []
        if result:
            for row in result:
                poliza_dict = {
                    "codigo_poliza": row[0],
                    "codigo_persona": row[1],
                    "numero_poliza": row[2],
                    "producto_codigo": row[3],
                    "producto_nombre": row[4],
                    "producto_descripcion": row[5],
                    "producto_categoria": row[6]
                }
                # Crear un objeto policy_types para el producto
                producto_dict = {
                    "id": 0,  # No tenemos ID del producto en esta tabla
                    "codigo": row[3],  # Ahora sí tenemos el código del producto
                    "nombre": row[4],
                    "descripcion": row[5],
                    "categoria": row[6],
                    "modalidad": "Ambas"  # Valor por defecto
                }
                producto = schemas.policy_types(**producto_dict)
                
                poliza_dict["producto"] = producto
                poliza_out = schemas.policies(**poliza_dict)
                polizas.append(poliza_out.dict())
            
            return {"data": polizas, "success": True, "errorMessage": None }
        else:
            return {"data": None, "success": False, "errorMessage": "Polizas no encontradas"}
    except Error as e:
        return {"data": None, "success": False, "errorMessage": f"MySQL Error: {e}"}
    except Exception as e:
        return {"data": None, "success": False, "errorMessage": f"Unexpected error: {str(e)}"}
