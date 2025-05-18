import pandas as pd
import pymysql
import boto3

# --- CONFIGURACIÓN ---

# Datos de conexión a MySQL
MYSQL_CONFIG = {
    'host': '172.31.95.13',
    'user': 'root',
    'password': 'admin',
    'database': 'bd_api_employees',
    'port': 3306  # cambia si tu puerto es distinto
}

# Consulta que quieres ejecutar
SQL_QUERY = "SELECT * FROM 	employees"

# Nombre del archivo CSV
CSV_FILENAME = "data.csv"

# Datos de S3
BUCKET_NAME = "gcr-output-01"
S3_KEY = CSV_FILENAME  # nombre del archivo en S3

# --- CONEXIÓN A MySQL Y EXPORTACIÓN ---

# Conexión a la base de datos
connection = pymysql.connect(**MYSQL_CONFIG)
df = pd.read_sql(SQL_QUERY, connection)
connection.close()

# Guardar como CSV
df.to_csv(CSV_FILENAME, index=False)
print(f"{CSV_FILENAME} generado con éxito.")

# --- SUBIDA A S3 ---

s3 = boto3.client('s3')
s3.upload_file(CSV_FILENAME, BUCKET_NAME, S3_KEY)

print("Ingesta completada")
