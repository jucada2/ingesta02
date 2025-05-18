import boto3
import csv
import mysql.connector

# Configuración de la conexión S3
s3 = boto3.client('s3')
bucket_name = 'jucada-output-2'
file_name = 'data.csv'

# Configuración de la base de datos MySQL
db = mysql.connector.connect(
    host="172.31.95.13",
    port="8005",
    user="root",
    password="utec",
    database="bd_api_employees"
)

cursor = db.cursor()

# Realiza una consulta para obtener los datos de usuarios
cursor.execute("SELECT * FROM employees")

# Guardamos los datos en un archivo CSV
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([i[0] for i in cursor.description])  # Escribir encabezados
    writer.writerows(cursor.fetchall())  # Escribir los registros

# Carga el archivo CSV al bucket de S3
try:
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"File {file_name} uploaded successfully to {bucket_name}.")
except Exception as e:
    print(f"Error uploading file: {e}")

# Cierra la conexión de base de datos
cursor.close()
db.close()