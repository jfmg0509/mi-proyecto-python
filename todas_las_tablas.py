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

    tablas = ['Libros', 'Usuarios', 'Prestamos', 'Sanciones', 'Historial']

    # Ejecutar el SELECT
    for tabla in tablas:
        print(f"\n📄 Contenido de la tabla: {tabla}")
        cursor.execute(f"SELECT * FROM {tabla}")
        registros = cursor.fetchall()

        if registros:
            for fila in registros:
                print(fila)
        else:
            print(" (sin registros)")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar la conexión
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()