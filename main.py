import leerCSV as CSV
from gurobipy import Model, GRB, quicksum

print(CSV.leer_csv("Hola mundo"))

presupuesto = input("Elija un presupuesto para el proyecto (en miles de pesos)")

nodos = CSV.leer_csv()
# 0 = id, 1 = nombre, 2 = precio estación, 3 = población, 4...n = precio de armar un arco entre el nodo de id (i-2) y este.
# Los precios deben estar en miles de pesos
# IMPORTANTE: LOS COSTOS REPETIDOS DEBEN SER 0.

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

# El costo total es menor al presupuesto
model.addConstr(
    (quicksum(x[i, j] * (i[j[0] + 4])) for i, j in nodos if i != j) # Conexiones
    + (quicksum(y[i]*i[2]) for i in nodos) # Estaciones
    <= presupuesto, f"Costos")
# Las conexiones no se generan dos veces porque se asume que las conexiones repetidas valen 0
# y aparece aplicada la restricción de que no generen loops


# Se cumple que de un nodo conectado puedo tirar una señal igual a los nodos conectados menos uno
# y esa señal va a ser demandada por todos los demás nodos.


# Funcion Objetivo y optimizar el problema:

model.setObjective(quicksum((y[i] * i[3]) for i in nodos), GRB.MAXIMIZE) 
#maximizar la suma de las estaciones puestas por la población en ellas

# Falta la función objetivo
model.optimize()

# Todavía no sé como imprimir la solución