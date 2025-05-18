import pandas as pd
import pymysql
import boto3

# --- CONFIGURACIÓN ---

MYSQL_CONFIG = {
    'host': '172.31.95.13',
    'user': 'root',
    'password': 'admin',
    'database': 'bd_api_employees',
    'port': 8005  # cambia si tu puerto es distinto
}

SQL_QUERY = "SELECT * FROM employees"
ficheroUpload = "data.csv"
nombreBucket = "jucada-output-2"


# --- CONEXIÓN A MYSQL Y EXPORTACIÓN A CSV ---

connection = None  # Asegura que esté definida

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    df = pd.read_sql(SQL_QUERY, connection)
    df.to_csv(ficheroUpload, index=False)
    print(f"{ficheroUpload} generado con éxito.")
except Exception as e:
    print("Error al consultar MySQL o guardar CSV:", e)
finally:
    if connection:
        connection.close()

# SUBIR A S3
try:
    s3 = boto3.client('s3')
    s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)
    print("Ingesta completada en S3")
except Exception as e:
    print("Error al subir a S3:", e)
