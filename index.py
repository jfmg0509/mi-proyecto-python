import psycopg2

# Configura los datos de conexión a tu contenedor Docker
connection_params = {
    'host': 'localhost',        # o el nombre del servicio Docker si usas docker-compose
    'port': 5432,               # Puerto expuesto por tu contenedor
    'dbname': 'GetaBook',   # Reemplaza con el nombre de tu base de datos
    'user': 'admin',       # Usuario de la base de datos
    'password': 'superSecure123!' # Contraseña de la base de datos
}

try:
    # Establecer la conexión
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Ejecutar el SELECT
    cursor.execute("SELECT * FROM libros")

    # Obtener resultados
    rows = cursor.fetchall()

    # Imprimir los resultados
    for row in rows:
        print(row)

except Exception as e:
    print(f"Error al conectar o consultar la base de datos: {e}")

finally:
    # Cerrar la conexión
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()