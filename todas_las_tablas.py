import psycopg2
from datetime import datetime

# Parámetros de conexión
connection_params = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'GetaBook',
    'user': 'admin',
    'password': 'superSecure123!'
}

# Función para mostrar una tabla completa
def mostrar_tabla(cursor, nombre_tabla):
    print(f"\nContenido de la tabla {nombre_tabla}:")
    cursor.execute(f"SELECT * FROM {nombre_tabla}")
    registros = cursor.fetchall()
    for fila in registros:
        print(fila)

def insertar_usuario(cursor):
    print("\n--- Inserción de nuevo usuario ---")
    nombre = input("Nombre completo: ")
    identificacion = input("Identificación: ")
    tipo = input("Tipo de usuario: ")
    correo = input("Correo electrónico: ")
    fecha = input("Fecha de registro (YYYY-MM-DD): ")
    estado = input("Estado (activo/inactivo): ")

    mostrar_tabla(cursor, 'Usuarios')
    cursor.execute("""
        INSERT INTO Usuarios (nombre_completo, identificacion, tipo_usuario, correo, fecha_registro, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, identificacion, tipo, correo, fecha, estado))
    print("✅ Usuario insertado.")
    mostrar_tabla(cursor, 'Usuarios')

def borrar_usuario(cursor):
    print("\n--- Borrado de usuario ---")
    id_usuario = input("ID del usuario a eliminar: ")

    mostrar_tabla(cursor, 'Usuarios')
    try:
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        if cursor.rowcount == 0:
            print("⚠️ No se encontró el usuario.")
        else:
            print("✅ Usuario eliminado.")
    except psycopg2.errors.ForeignKeyViolation:
        print("❌ No se puede eliminar: hay registros relacionados.")
    mostrar_tabla(cursor, 'Usuarios')

def actualizar_usuario(cursor):
    print("\n--- Actualización de usuario ---")
    id_usuario = input("ID del usuario a actualizar: ")
    nuevo_correo = input("Nuevo correo electrónico: ")

    mostrar_tabla(cursor, 'Usuarios')
    cursor.execute("UPDATE Usuarios SET correo = %s WHERE id_usuario = %s", (nuevo_correo, id_usuario))
    if cursor.rowcount == 0:
        print("⚠️ No se encontró el usuario.")
    else:
        print("✅ Usuario actualizado.")
    mostrar_tabla(cursor, 'Usuarios')

def consultas_avanzadas(cursor):
    print("\n--- Consultas Avanzadas ---")

    print("\n1. Top 3 usuarios con más préstamos:")
    cursor.execute("""
        SELECT u.nombre_completo, COUNT(*) AS cantidad
        FROM Prestamo p
        JOIN Usuarios u ON p.id_usuario = u.id_usuario
        GROUP BY u.nombre_completo
        ORDER BY cantidad DESC
        LIMIT 3
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n2. Préstamos ordenados por fecha límite descendente:")
    cursor.execute("""
        SELECT id_prestamo, id_usuario, id_libro, fecha_limite
        FROM Prestamo
        ORDER BY fecha_limite DESC
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n3. Préstamos en enero y mayo:")
    cursor.execute("""
        SELECT * FROM Prestamo
        WHERE EXTRACT(MONTH FROM fecha_prestamo) IN (1, 5)
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n4. Mi consulta extra: usuarios con sanciones activas:")
    cursor.execute("""
        SELECT u.nombre_completo, s.motivo, s.fecha_inicio, s.fecha_fin
        FROM Sancion s
        JOIN Usuarios u ON s.id_usuario = u.id_usuario
        WHERE s.estado = 'activa'
    """)
    for fila in cursor.fetchall():
        print(fila)

def mostrar_todo(cursor):
    print("\n--- Todas las tablas ---")
    for tabla in ['Usuarios', 'Libro', 'Prestamo', 'Devolucion', 'Sancion']:
        mostrar_tabla(cursor, tabla)

def main():
    try:
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()

        while True:
            print("\n📚 MENÚ DE LA BIBLIOTECA")
            print("1. Ver todas las tablas")
            print("2. Insertar usuario")
            print("3. Borrar usuario")
            print("4. Actualizar usuario")
            print("5. Consultas avanzadas")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                mostrar_todo(cursor)
            elif opcion == '2':
                insertar_usuario(cursor)
            elif opcion == '3':
                borrar_usuario(cursor)
            elif opcion == '4':
                actualizar_usuario(cursor)
            elif opcion == '5':
                consultas_avanzadas(cursor)
            elif opcion == '6':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()