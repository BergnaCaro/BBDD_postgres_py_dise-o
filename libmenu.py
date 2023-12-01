def menu(titulo,opciones):
    print("------------------")
    print(titulo)
    n=1
    for opcion in opciones:
        print(f"{n:3} {opcion}")
        n=n+1
    print("  0 Salir!")
    opcion=-1
    while opcion < 0 or opcion >= n:
        opcion = ingresoNum("Ingrese su Opcion:")
    return opcion

def ingreso(prompt,porDefecto = None):
    while True:
        try:
            opcion = input(prompt)
            if opcion != '':
                return opcion
            if porDefecto != None:
                return porDefecto
        except Exception as error:
            pass

def ingresoNum(prompt):
    while True:
        try:
            opcion = int(input(prompt))
            return opcion
        except Exception as error:
            pass

#ingreso numero opcional
def ingresoNumOpc(prompt,porDefecto = None):
    while True:
        try:
            opcion = input(prompt)
            if opcion == '' and porDefecto != None:
                return porDefecto
            else:
                opcion = int(opcion)
                return opcion
        except Exception as error:
            pass

def ingresoFloat(prompt):
    while True:
        try:
            opcion = float(input(prompt))
            return opcion
        except Exception as error:
            pass

#permite que el usuario ingrese S s N n
def ingresoSN(prompt):
    while True:
        try:
            opcion = input(prompt)
            if opcion == 's' or opcion == 'S' or opcion == 'n' or opcion == 'N':
                return opcion.upper()
        except Exception as error:
            pass

#agrega comillas simples sobre string != de NULL
def comillasSQL(texto):
    if texto == '':
        return 'NULL'
    elif texto == 'NULL':
        return texto
    else:
        textosql = "'" + texto + "'"
        return textosql
