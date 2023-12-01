import psycopg2
from libpg import *
from libmenu import *
from datetime import date

conn = None
opcion = -1
conn = conectar("postgres","postgreAndrea","localhost","5432","TP_4_Bergna_Andrea_G1")
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
                    razon_social = input("*Razon Social:")
                    saldo_deudor = ingresoFloat("*Saldo Deudor:")
                    cuit = ingresoNum("*CUIT:")
                    calle = input("*Calle:")
                    calle_numero = ingresoNum("*Numero:")
                    piso = ingresoNumOpc("Piso:",'NULL')
                    depto = comillasSQL(ingreso("Depto (letra):",'NULL'))
                    contacto = comillasSQL(ingreso("Contacto:",'NULL'))
                    mostrar(conn,"select nombre as provincia, numero as zona,costo from pc order by nombre asc,numero asc")
                    nombre = ingreso("*Provincia:")
                    nro = ingresoNum("*Zona:")
                    mostrar(conn,"select cpostal, nombre from localidad order by cpostal asc")
                    cp = ingresoNum("*Codigo Postal:")
                    mayorista = ingresoSN("*Es Mayorista? (S/N):")
                    descuento = 0.0
                    if mayorista == 'S':
                        descuento = ingresoFloat("*% Descuento Mayorista:")
                    telefono = ingresoNumOpc("Telefono:",'NULL')
                    sn = ingresoSN("Ingreso este Cliente? (S/N)")
                    if sn == 'S':
                        #insert cliente
                        sql1 = f"insert into cliente(codigo,razon_social,saldo_deudor,cuit,calle,calle_numero,piso,depto,contacto,nombre,nro,cp) "
                        sql2 = f"values({codigo},'{razon_social}',{saldo_deudor},{cuit},'{calle}',{numero},{piso},{depto},{contacto},'{nombre}',{nro},{cp})"
                        sql = sql1+sql2
                        ejecutar(conn,sql)
                        if mayorista == 'S':
                            sql = f"insert into mayorista(codigo,dto) values({codigo},{descuento})"
                            ejecutar(conn,sql)
                        if mayorista == 'N':
                            sql = f"insert into minorista(codigo) values({codigo})"
                            ejecutar(conn,sql)
                        if telefono != 'NULL':
                            sql = f"insert into telefono(numero,codigo) values({telefono},{codigo})"
                            ejecutar(conn,sql)
                else:
                    print(f"El cliente {codigo} ya existe!")

            elif opcli == 2:
                mostrar(conn,"select codigo, razon_social, saldo_deudor, cuit, nombre as provincia, numero as zona, codigo_postal as cp from cliente order by codigo asc")
                codigo = ingresoNum("*Codigo:")
                sql=f"select codigo, razon_social, saldo_deudor, cuit, nombre as provincia, numero as zona, codigo_postal as cp from cliente where codigo = {codigo}"
                if mostrar(conn,sql):
                    sql=f"select numero,fecha,monto_ambos from factura where codigo = {codigo} order by numero asc"
                    tuplas,cols = consultar(conn,sql)
                    if tuplas:
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
                mostrar(conn,"select codigo, razon_social, saldo_deudor, cuit, nombre as provincia, numero as zona, codigo_postal as cp from cliente order by codigo asc")
    elif opcion == 2:
        opfac = -1
        while opfac != 0:
            opfac = menu("MENU FACTURACION",["Facturar","Terminar Factura"])
            if opfac == 1:
                codigo = 'NULL'
                envio = 'N'
                if ingresoSN("Factura a Consumidor Final? (S/N)") == 'N':
                    mostrar(conn,"select codigo, razon_social, saldo_deudor, cuit, nombre as provincia, numeroro as zona, codigo_postal as cp from cliente order by codigo asc")
                    codigo = ingresoNum("*Codigo Cliente:")
                    sql=f"select codigo, razon_social, saldo_deudor, cuit, nombre as provincia, numero as zona, codigo_postal as cp from cliente where codigo = {codigo}"
                    if not mostrar(conn,sql):
                        print(f"El cliente {codigo} no existe!")
                        continue
                    envio = ingresoSN("Factura con Envio? (S/N)")
                    if envio == 'S':
                        print('Costo del Envio:')
                        mostrar(conn,f"select p.costo_envio from prov_zona as p inner join cliente as c on c.nombre = p.nombre and c.numero = p.numero where c.codigo = {codigo}")
                fecha = date.today()
                tuplas,cols = consultar(conn,"select coalesce(max(numero)+1,1) as nuevo_nro from factura")
                if tuplas:
                    tupla = tuplas[0]
                    numero = tupla[0]
                    print(f"Nuevo numero de factura: {numero}")
                    sql1=f"insert into factura(numero,fecha,monto_gravado,monto_no_gravado,codigo,envio,pagada,terminada,total_pagado) "
                    sql2=             f"values({numero},'{fecha}',0,0,{codigo},'{envio}','N','N',0) "
                    sql=sql1+sql2
                    if ejecutar(conn,sql):
                        print(f"Cabecera de Factura {numero} dada de alta Ok!")
                        sigofacturando=True
                        while sigofacturando:
                            print('Comenzamos a ingresar los productos de la factura:')
                            continuo = True
                            while continuo:
                                mostrar(conn,"select codigo, descripcion, stock, gravado_s_n, precio_sugerido as precio from producto order by codigo asc")
                                codigo_producto = ingresoNum("*Codigo Producto:")
                                tuplas_prod,pcols = consultar(conn,f"select codigo, descripcion, stock, gravado_s_n, precio_sugerido as precio from producto where codigo = {codigo_producto}")
                                if not tuplas_prod:
                                    print(f"El Producto {codigo_producto} no existe!")
                                    continue
                                tupla_prod = tuplas_prod[0]
                                precio = ingresoFloat("*Precio Producto:")
                                while precio < tupla_prod[4]:
                                    print(f"El precio no puede ser menor a $ {tupla_prod[4]}")
                                    precio = ingresoFloat("*Precio Producto:")
                                cantidad = ingresoNum("*Cantidad:")
                                while cantidad <= 0:
                                    cantidad = ingresoNum("*Cantidad:")
                                # ATENCION: en la BD compuesta.subtotal = cantidad * precio es una columna calculada
                                sql = f"insert into compuesta(numero,codigo,precio,cantidad) values({numero},{codigo_producto},{precio},{cantidad})"
                                if not ejecutar(conn,sql):
                                    print('Error en facturacion de este producto!')
                                if ingresoSN("Continua facturando productos? (S/N)") == 'N':
                                    continuo = False
                            #luego de cargar todos los productos de la factura, actualizo la cabecera
                            sql = f"select count(*) as cnt, sum(c.subtotal) as gravado from compuesta as c inner join producto as p on c.codigo = p.codigo where c.numero = {numero} and p.gravado = 'S' "
                            tuplas_gravado,gcols = consultar(conn,sql)
                            gravado=0.0
                            if tuplas_gravado:
                                tupla_gravado = tuplas_gravado[0]
                                if tupla_gravado[0] > 0:
                                    gravado=tupla_gravado[1]
                            sql = f"select count(*) as cnt, sum(c.subtotal) as monto_no_gravado from compuesta as c inner join producto as p on c.codigo = p.codigo where c.numero = {numero} and p.gravado = 'N' "
                            tuplas_nogravado,ngcols = consultar(conn,sql)
                            nogravado=0.0
                            if tuplas_nogravado:
                                tupla_nogravado = tuplas_nogravado[0]
                                if tupla_nogravado[0] > 0:
                                    nogravado=tupla_nogravado[1]
                            if gravado == 0.0 and nogravado == 0.0:
                                print('El total gravado y no gravado es cero! esto no es posible! no hay productos facturados!')
                                continue
                            else:
                                sigofacturando=False
                                # ATENCION: en la BD factura.monto = gravado + nogravado es una columna calculada
                                sql = f"update factura set monto_gravado = {gravado}, monto_no_gravado = {nogravado} where numero = {numero}"
                                if not ejecutar(conn,sql):
                                    print(f"Error en la actualizacion de la cabecera de factura {numero}")
                        #muestro datos de la factura y su detalle
                        sql=f"select numero,fecha,monto,gravado,nogravado,codigo as cliente,conenvio as envio,pagada,terminada from factura where numero = {numero}"
                        mostrar(conn,sql)
                        sql=f"select c.codigo,p.descripcion,c.cantidad,c.precio,c.subtotal from compuesta as c inner join producto as p on c.codigo = p.codigo where c.numero = {numero}"
                        mostrar(conn,sql)
                        input('Facturacion Completa!, Presine ENTER para continuar')
                    else:
                        print(f"Error en dar de alta Factura {numero}")
                else:
                    print('Error obteniendo el nuevo numero de factura, reintente!')
            elif opfac == 2:
                sql=f"select numero,fecha,monto,gravado,nogravado,codigo as cliente,envio as envio,pagada from factura where terminada = 'N'"
                mostrar(conn,sql)
                numero = ingresoNum("*Numero Factura:")
                sql=f"select numero,fecha,monto_ambos,monto_gravado,monto_no_gravado,codigo as cliente,envio as envio,pagada from factura where terminada = 'N' and numero = {numero}"
                tuplas,cols = consultar(conn,sql)
                if tuplas:
                    tupla = tuplas[0]
                    fecha = tupla[cols['fecha']].strftime("%d/%m/%Y")
                    if ingresoSN(f"Termino la Factura {numero} {fecha}? (S/N)") == 'S':
                        #Actualizo cliente si la factura tiene cliente asociado
                        if tupla[cols['cliente']] != None:
                            sql=f"update cliente set saldo_deudor = saldo_deudor + {tupla[cols['saldo_deudor']]} where codigo = {tupla[cols['cliente']]}"
                            if not ejecutar(conn,sql):
                                print(f"Error al actualizar el saldo deudor del cliente {tupla[cols['cliente']]}")
                        #Actualizo stock de productos
                        tuplas_com,ccols = consultar(conn,f"select codigo,cantidad from compuesta where numero = {numero}")
                        if tuplas_com:
                            for tupla_com in tuplas_com:
                                sql=f"update producto set stock = stock - {tupla_com[ccols['cantidad']]} where codigo = {tupla_com[ccols['codigo']]}"
                                if not ejecutar(conn,sql):
                                    print(f"Error al actualizar el stock del producto {tupla_com[ccols['codigo']]}")
                        #Actualizo Factura
                        sql=f"update factura set terminada = 'S' where numero = {numero}"
                        if not ejecutar(conn,sql):
                            print(f"Error al intentar terminar la factura {numero}")
                        else:
                            input(f"Factua {numero} terminada Ok!, presione ENTER")
                else:
                    print(f"Error, Factura {numero} no Terminada no existe!")
    elif opcion == 3:
        sql=f"select numero, to_char(fecha::date) as fecha, monto_ambos, monto_gravado, monto_no_gravado, codigo as cliente, envio as envio, total_pagado from factura where pagada ='N' and terminada = 'S' and total_pagado < importe"
        mostrar(conn,sql)
        numero= ingresoNum("*Número Factura:")
        sql= f'select numero, fecha, monto_ambos, monto_gravado_monto_no_gravado, codigo as cliente, envio as envio, total_pagado from factura where numero = {numero}'
        tuplas, cols= consultar (conn, sql)
        if tuplas:
            tupla = tuplas[0]
            fecha_fac= tupla[cols['fecha']]
            saldo_deudor= tupla[cols['importe']] - tupla[cols['total_pagado']]
            if ingresoSN(f"Ingresa el pago de la Factura {numero} del {fecha_fac} con saldo deudor $ {saldo_deudor}? (S/N) == 'S'"):
                fecha= date.today()
                importe= 0
                while importe <= 0 or importe > saldo_deudor:
                    importe =ingresoFloat(f'Total Pagado (<=${saldo_deudor}):')
                sql= f"insert into pago(numero, fecha, importe) values ({numero}, {fecha}, {importe})"
                if not ejecutar(conn, sql):
                    print(f'Error de ingreso de Pago en la Factura {numero}')
                if tupla[cols['cliente']] !=None:
                    sql= f"update cliente set saldo_deudor = saldo_deudor - {importe} where codigo ={tupla[cols['cliente']]}"
                    if not ejecutar(conn,sql):
                        print(f'Error al actualizar el saldo deudor del cliente {numero}')
                if importe < saldo_deudor:
                    sql= f'update factura set total_pagado =total_pagado + {importe} where numero = {numero}'
                else:
                    sql= f"update factura set total_pagado = importe , pagada ='S' where numero {numero}"
                if not ejecutar(conn, sql):
                    print(f"Error al actualizar  el saldo deudor de la factura {numero}")
        else:
            print (f'Error!, la Factura {numero} no terminada, NO EXISTE')
            

        pass
desconectar(conn)

exit(0)

# Bergna Andrea tp 5 ej 7
# Reutilice el Código que nos compartió profe y le fui adaptando con mis columnas del TP 4
# Aún no decubro bien que le ocurre a la librería psycopg porque en el uno de los archivos me lee bien pero en este me da el error de busqueda
# Tuve que hacer cambio de extensión de Python 
# Espero su devolución profe