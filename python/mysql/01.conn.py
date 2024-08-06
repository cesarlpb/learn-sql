# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

def leer_env():
    """Se considera que el .env está en la misma carpeta"""
    with open(".env") as f:
        lineas = f.read().splitlines()
    ENV={}
    for linea in lineas:
        key, value = linea.split('=')
        ENV[key]=value
    return ENV

def connect_to_mysql():
    try:
        ENV = leer_env()
        # Establece la conexión con MySQL
        connection = mysql.connector.connect(
            host=ENV['DB_HOST'],
            port=ENV['DB_PORT'],
            database=ENV['DB_NAME'],
            user=ENV['DB_USER'],
            password=ENV['DB_PASS']
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Conectado a MySQL Server versión {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Conectado a la base de datos: {record}")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    connect_to_mysql()
