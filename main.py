import leerCSV as CSV
from gurobipy import Model, GRB, quicksum
from optimizar import optimizar

nodos = CSV.leer_csv("Datos.csv")
nodos[0][0] = '0'

presupuesto = int(input("Elija un presupuesto para el proyecto (en millones de pesos)"))
# print("Elija una localidad de la cual iniciar la construcción de la red:")
# for i in nodos:
#     print(f"{i[0]}) {i[1]}")
# indice_nodo_inicial = int(input())
#input("Elija un presupuesto para el proyecto (en millones de pesos)")

# constante arbitrariamente grande:
ctte = 9999

for i in nodos:
    i[0] = int(i[0])
# print(nodos)
# 0 = id, 1 = nombre, 2 = precio estación, 3 = población, 4...n = precio de armar un arco entre el nodo de id (i-2) y este.
# Los precios deben estar en miles de pesos
# IMPORTANTE: LOS COSTOS REPETIDOS DEBEN SER IGUALES A LOS ORIGINALES.

val = 0
for i in range(len(nodos)):
    nval, nx, ny = optimizar(nodos, presupuesto, i)
    if nval > val:
        val = nval
        x = nx
        y = ny

# Imprimir solución

q = "======================================================"

# Print the values of x[i,j]
print(f"{q}\nConexiones:\n{q}")
for i in x:
    print(i)

# Print the values of y[i]
print(f"{q}\nEstaciones:\n{q}")
for i in y:
    print(i)

print(f"{q}")

print(f"Cantidad de gente movida con este sistema: {val}")