import psycopg2
import libpg
import libmenu
from libpg import *
from libmenu import *

conn = None
opcion = -1
while opcion != 0:
    opcion = menu("MENU PRINCIPAL",["Conectar","Consultar", "Ejecutar","Desconectar"])
    if opcion == 1:
        conn = conectar("postgres","postgres","localhost","5432","tp4ej1")
    elif opcion == 2:
        sql = "SELECT * from localidad"
        tuplas,cols = consultar(conn,sql)
        if (tuplas):
            print("Resultado Consulta:",len(tuplas)," tuplas!")
            columnas = [desc for desc in cols]
            for tupla in tuplas:
                print(f"Codigo Postal: {tupla[0]} Localidad: {tupla[1]}")
                #uso los nombres de columnas de la base de datos
                #print(f"{columnas[0]}:{tupla[0]} {columnas[1]}:{tupla[1]}")
        else:
            print(f"La Consulta: {sql} no dio ningun resultado!")
    elif opcion == 3:
        postal = ingresoNum("Codigo Postal:")
        localidad = input("Localidad:")
        sql = f"insert into localidad(cpostal,nombre) values({postal},'{localidad}')"
        ejecutar(conn,sql)
    else:
        desconectar(conn)

exit(0)