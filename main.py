import leerCSV as CSV
from gurobipy import Model, GRB, quicksum

print(CSV.leer_csv("Hola mundo"))

nodos = CSV.leer_csv()

# Generar el modelo
model = Model()

# Se instancian variables de decision

# Existe conexión directa entre 2 estaciones?
x = {}
for i in nodos:
    for j in nodos:
        if i != j: # Restricción de nodos no iguales
            x[i,j] = model.addVar(vtype = GRB.BINARY, name="x_({i[0]}, {j[0]})") # 0 tiene que ser el nombre de la ciudad
            # x = conexión

# Evitar ciclos de 2 nodos (los arcos son bidireccionales)
for i in nodos:
    for j in nodos:
        if i != j:
            model.addConstr(x[i, j] + x[j, i] <= 1, f"no_ciclo_{i}_{j}")

# Hay una estación en un nodo i?
y = {}
for i in nodos:
    y[i] = model.addVar(vtype = GRB.BINARY, name="y_({i[0]})") # y = estación


z = model.addVar(vtype = GRB.CONTINUOUS, name="z")

# Llamamos a update
# Restricciones
# Funcion Objetivo y optimizar el problema
# Manejo Soluciones
print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
# Holguras (0 significa que la restricción es activa)
print("\n"+"-"*9+" Restricciones Activas "+"-"*9)
