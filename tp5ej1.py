import psycopg2
conexion=None
try:
    # Connecto a una base de datos existente
    conexion = psycopg2.connect(user="postgres",password="postgres",host="localhost",port="5432",database="tp4ej1")
    # Creo un cursor para hacer operaciones sobre la base de datos conectada
    cursor = conexion.cursor()
    # Imprimo deatos de la conexion con el servidor
    print("Informacion Servidor PostgreSQL:")
    print(conexion.get_dsn_parameters(), "\n")
    # Ejecuto una consulta SQL
    cursor.execute("SELECT version();")
    # Obtengo el resultado de la consulta SQL
    record = cursor.fetchone()
    print("Ud esta conectado a: ", record, "\n")

except Exception as error:
    print("Error conectando con PostgreSQL:",error)

finally:
    if (conexion):
        cursor.close()
        conexion.close()
        print("Conexion con PostgreSQL cerrada")