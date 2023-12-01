import psycopg2
from libpg import *
from libmenu import *

conn = None
opcion = -1
conn = conectar("postgres","postgres","localhost","5432","tp4ej1")
while opcion != 0:
    opcion = menu("MENU PRINCIPAL",["Clientes","Facturas", "Pagos"])
    if opcion == 1:
        opcli = -1
        while opcli != 0:
            opcli = menu("MENU CLIENTES",["Agregar Nuevo Cliente","Borrar Cliente","Mostrar Clientes"])
            if opcli == 1:
                codigo = ingresoNum("*Codigo:")
                sql=f"select codigo from cliente where codigo = {codigo}"
                tuplas,cols = consultar(conn,sql)
                if not (tuplas):
                    razon = input("*Razon Social:")
                    saldo = ingresoFloat("*Saldo Deudor:")
                    cuit = ingresoNum("*CUIT:")
                    calle = input("*Calle:")
                    numero = ingresoNum("*Numero:")
                    piso = ingresoNumOpc("Piso:",'NULL')
                    depto = comillasSQL(ingreso("Depto (letra):",'NULL'))
                    contacto = comillasSQL(ingreso("Contacto:",'NULL'))
                    mostrar(conn,"select nombre as provincia, numero as zona,costo from pc order by nombre asc,numero asc")
                    nombre = ingreso("*Provincia:")
                    nro = ingresoNum("*Zona:")
                    mostrar(conn,"select cpostal, nombre from localidad order by cpostal asc")
                    cpostal = ingresoNum("*Codigo Postal:")
                    mayo = ingresoSN("*Es Mayorista? (S/N):")
                    dto = 0.0
                    if mayo == 'S':
                        dto = ingresoFloat("*% Descuento Mayorista:")
                    telefono = ingresoNumOpc("Telefono:",'NULL')
                    sn = ingresoSN("Ingreso este Cliente? (S/N)")
                    if sn == 'S':
                        #insert cliente
                        sql1 = f"insert into cliente(codigo,razon,saldo,cuit,calle,numero,piso,depto,contacto,nombre,nro,cpostal) "
                        sql2 = f"values({codigo},'{razon}',{saldo},{cuit},'{calle}',{numero},{piso},{depto},{contacto},'{nombre}',{nro},{cpostal})"
                        sql = sql1+sql2
                        ejecutar(conn,sql)
                        if mayo == 'S':
                            sql = f"insert into mayorista(codigo,dto) values({codigo},{dto})"
                            ejecutar(conn,sql)
                        if mayo == 'N':
                            sql = f"insert into minorista(codigo) values({codigo})"
                            ejecutar(conn,sql)
                        if telefono != 'NULL':
                            sql = f"insert into telefono(numero,codigo) values({telefono},{codigo})"
                            ejecutar(conn,sql)
                else:
                    print(f"El cliente {codigo} ya existe!")

            elif opcli == 2:
                mostrar(conn,"select codigo, razon, saldo, cuit, nombre as prov, nro as zona, cpostal as cod_postal from cliente order by codigo asc")
                codigo = ingresoNum("*Codigo:")
                sql=f"select codigo, razon, saldo, cuit, nombre as prov, nro as zona, cpostal as cod_postal from cliente where codigo = {codigo}"
                if mostrar(conn,sql):
                    sql=f"select numero,fecha,monto from factura where codigo = {codigo} order by numero asc"
                    tuplas,cols = consultar(conn,sql)
                    if (tuplas):
                        print(f"El cliente {codigo} tiene",len(tuplas)," facturas!")
                        for tupla in tuplas:
                            print(f"Numero: {tupla[0]} Fecha: {tupla[1]} $ {tupla[2]}")
                    else:
                        print('El cliente no tiene facturas asociadas')
                        sn = ingresoSN("Borro a este Cliente? (S/N)")
                        if sn == 'S':
                            sql=f"delete from minorista where codigo = {codigo}"
                            ejecutar(conn,sql)
                            sql=f"delete from mayorista where codigo = {codigo}"
                            ejecutar(conn,sql)
                            sql=f"delete from telefono where codigo = {codigo}"
                            ejecutar(conn,sql)
                            sql=f"delete from cliente where codigo = {codigo}"
                            ejecutar(conn,sql)
                else:
                    print(f"El cliente {codigo} no existe!")
            elif opcli == 3:
                mostrar(conn,"select codigo, razon, saldo, cuit, nombre as prov, nro as zona, cpostal as cod_postal from cliente order by codigo asc")
    elif opcion == 2:
        # sql = "SELECT * from localidad"
        # tuplas,cols = consultar(conn,sql)
        # if (tuplas):
        #     print("Resultado Consulta:",len(tuplas)," tuplas!")
        #     for tupla in tuplas:
        #         print(f"Codigo Postal: {tupla[0]} Localidad: {tupla[1]}")
        # else:
        #     print(f"La Consulta: {sql} no dio ningun resultado!")
        pass
    elif opcion == 3:
        # postal = ingresoNum("Codigo Postal:")
        # localidad = input("Localidad:")
        # sql = f"insert into localidad(cpostal,nombre) values({postal},'{localidad}')"
        # ejecutar(conn,sql)
        pass
desconectar(conn)

exit(0)