import psycopg2
from tabulate import tabulate

# Parámetros de conexión
connection_params = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'GetaBook',
    'user': 'admin',
    'password': 'superSecure123!'
}

# Mostrar tabla con formato
def mostrar_tabla(cursor, nombre_tabla):
    try:
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        print(f"\n📄 Contenido de la tabla '{nombre_tabla}':")
        print(tabulate(filas, headers=columnas, tablefmt='grid'))
    except Exception as e:
        print(f"⚠️ Error al mostrar la tabla {nombre_tabla}: {e}")

# Opción 1 - Ver todas las tablas
def mostrar_todo(cursor):
    for tabla in ['Usuarios', 'Libro', 'Prestamo', 'Devolucion', 'Sancion']:
        mostrar_tabla(cursor, tabla)

# Opción 2 - Insertar usuario
def insertar_usuario(cursor):
    print("\n📝 Insertar nuevo usuario:")
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
    print("✅ Usuario insertado con éxito.")
    mostrar_tabla(cursor, 'Usuarios')

# Opción 3 - Eliminar usuario
def borrar_usuario(cursor):
    id_usuario = input("\nID del usuario a eliminar: ")
    mostrar_tabla(cursor, 'Usuarios')
    try:
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        if cursor.rowcount == 0:
            print("⚠️ Usuario no encontrado.")
        else:
            print("✅ Usuario eliminado.")
    except psycopg2.errors.ForeignKeyViolation:
        print("❌ No se puede eliminar: el usuario tiene registros vinculados.")
    mostrar_tabla(cursor, 'Usuarios')

# Opción 4 - Actualizar usuario
def actualizar_usuario(cursor):
    id_usuario = input("\nID del usuario a actualizar: ")
    nuevo_correo = input("Nuevo correo electrónico: ")
    mostrar_tabla(cursor, 'Usuarios')
    cursor.execute("UPDATE Usuarios SET correo = %s WHERE id_usuario = %s", (nuevo_correo, id_usuario))
    if cursor.rowcount == 0:
        print("⚠️ No se encontró el usuario.")
    else:
        print("✅ Usuario actualizado.")
    mostrar_tabla(cursor, 'Usuarios')

# Opción 5 - Consultas avanzadas
def consultas_avanzadas(cursor):
    print("\n🔍 Top 3 usuarios con más préstamos:")
    cursor.execute("""
        SELECT u.nombre_completo, COUNT(*) AS cantidad
        FROM Prestamo p
        JOIN Usuarios u ON p.id_usuario = u.id_usuario
        GROUP BY u.nombre_completo
        ORDER BY cantidad DESC
        LIMIT 3
    """)
    print(tabulate(cursor.fetchall(), headers=["Usuario", "Cantidad"], tablefmt='grid'))

    print("\n📦 Préstamos ordenados por fecha límite descendente:")
    cursor.execute("""
        SELECT id_prestamo, id_usuario, id_libro, fecha_limite
        FROM Prestamo
        ORDER BY fecha_limite DESC
    """)
    print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt='grid'))

    print("\n🗓 Préstamos de enero y mayo 2025:")
    cursor.execute("""
        SELECT id_prestamo, fecha_prestamo
        FROM Prestamo
        WHERE EXTRACT(MONTH FROM fecha_prestamo) IN (1, 5)
          AND EXTRACT(YEAR FROM fecha_prestamo) = 2025
    """)
    print(tabulate(cursor.fetchall(), headers=["ID Préstamo", "Fecha"], tablefmt='grid'))

    print("\n🚨 Usuarios con sanciones activas:")
    cursor.execute("""
        SELECT u.nombre_completo, s.motivo, s.fecha_inicio, s.fecha_fin
        FROM Sancion s
        JOIN Usuarios u ON s.id_usuario = u.id_usuario
        WHERE s.estado = 'activa'
    """)
    print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt='grid'))

# Menú principal
def main():
    try:
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True
        cursor = conn.cursor()

        while True:
            print("\n📚 MENÚ PRINCIPAL")
            print("1. Ver todas las tablas")
            print("2. Insertar usuario")
            print("3. Eliminar usuario")
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
                print("👋 Gracias por el módulo estimada Emilia!")
                break
            else:
                print("❗ Opción inválida. Intente de nuevo.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Error de conexión o ejecución:", e)

if __name__ == "__main__":
    main()