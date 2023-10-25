def leer_csv(archivo):  #Colocar dirección de excel en comillas
    import csv
    salida = ""
    with open(archivo, newline="") as carpeta:
        datos = csv.reader(carpeta, delimiter=",")
        salida = list(datos)
    
    return salida