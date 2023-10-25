import leerCSV as CSV
from gurobipy import Model, GRB, quicksum

print(CSV.leer_csv("Hola mundo"))

nodos = CSV.leer_csv()
# 0 = id, 1 = nombre, 2 = precio estación, 3...n = precio de armar un arco entre el nodo de id (i-2) y este.

# Generar el modelo
model = Model()

# Se instancian variables de decision

# Existe conexión directa entre 2 estaciones?
x = {}
for i in nodos:
    for j in nodos:
        if i != j: # Restricción de nodos no iguales
            x[i,j] = model.addVar(vtype = GRB.BINARY, name=f"x_{i[1]}_{j[1]}") # 0 tiene que ser el nombre de la ciudad
            # x = conexión

# Hay una estación en un nodo i?
y = {}
for i in nodos:
    y[i] = model.addVar(vtype = GRB.BINARY, name= f"y_({i[1]})")

# Número de estaciones que tengo en el sistema (tiene que estar sobre el número de estaciones que tengo construídas)
N = model.addVar(vtype = GRB.CONTINUOUS, name="N_estaciones")

# Número de nodos que puedo visitar desde cada nodo
V = {}
for i in nodos:
    V[i] = model.addVar(vtype = GRB.CONTINUOUS, name=f"Visitas_{i[1]}")

# Llamamos a update


# Restricciones
# Evitar ciclos de 2 nodos (los arcos son bidireccionales)
for i in nodos:
    for j in nodos:
        if i != j:
            model.addConstr(x[i, j] + x[j, i] <= 1, f"no_ciclo_{i[1]}_{j[1]}")


# Funcion Objetivo y optimizar el problema:

# Falta la función objetivo
model.optimize()

# Todavía no sé como imprimir la solución