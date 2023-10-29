import leerCSV as CSV
from gurobipy import Model, GRB, quicksum

presupuesto = input("Elija un presupuesto para el proyecto (en miles de pesos)")

nodos = CSV.leer_csv("Datos.csv")
nodos[0][0] = '0'
# print(nodos)
# 0 = id, 1 = nombre, 2 = precio estación, 3 = población, 4...n = precio de armar un arco entre el nodo de id (i-2) y este.
# Los precios deben estar en miles de pesos
# IMPORTANTE: LOS COSTOS REPETIDOS DEBEN SER IGUALES A LOS ORIGINALES.

# Generar el modelo
model = Model()
# Se instancian variables de decision
model.setParam("TimeLimit", 300)
# Se determina un tiempo máximo para el algoritmo, en este caso, 5 minutos

# Existe conexión directa entre 2 estaciones?
x = {}
for i in nodos:
    for j in nodos:
        if i != j: # Restricción de nodos no iguales
            x[i[0],j[0]] = model.addVar(vtype = GRB.BINARY, name=f"x_{i[1]}_{j[1]}") # 1 tiene que ser el nombre de la ciudad
            # x = conexión

# Hay una estación en un nodo i?
y = {}
for i in nodos:
    y[i[0]] = model.addVar(vtype = GRB.BINARY, name= f"y_({i[1]})")


# Es i un nodo inicial? (los nodos desconectados son iniciales y hay uno solo conectado e inicial)
Ni = {}
for i in nodos:
    Ni[i[0]] = model.addVar(vtype = GRB.BINARY, name= f"Ni_({i[1]})")




# Llamamos a update
model.update()

# Restricciones:

# Sólo puede haber un camino entre 2 nodos que tienen estaciones
for i in nodos:
    for j in nodos:
        # Para que haya una conexión de i a j:
        model.addConstr((x[i[0], j[0]] <= y[i[0]]), f"ruta_{i[1]}_{j[1]}_estacion_{i[1]}") # Tiene que haber estación en i
        model.addConstr((x[i[0], j[0]] <= y[j[0]]), f"ruta_{i[1]}_{j[1]}_estacion_{j[1]}") # Tiene que haber estación en j

# Evitar ciclos de 2 nodos (los arcos no son bidireccionales)
for i in nodos:
    for j in nodos:
        if i != j:
            model.addConstr(x[i[0], j[0]] + x[j[0], i[0]] <= 1, f"no_ciclo_{i[1]}_{j[1]}")

# El costo total es menor al presupuesto
model.addConstr(
    (quicksum(x[i[0], j[0]] * (i[j[0] + 4])) for i, j in nodos if i != j) # Conexiones
    + (quicksum(y[i[0]]*i[2]) for i in nodos) # Estaciones
    <= presupuesto, f"Costos")
# Las conexiones no se generan dos veces por la restricción anterior


# Los nodos tienen máximo 1 antecesor y tienen 0 si no tienen estación
for i in nodos:
    model.addConstr((quicksum(x[j[0], i[0]]) for j in nodos if i != j) <= y[i[0]], f"Un_antecesor_{i[1]}")

# Los nodos con al menos 1 antecesor son todos los nodos no iniciales
for i in nodos:
    model.addConstr((quicksum(x[j[0], i[0]]) for j in nodos if i != j) >= (1 - Ni[i[0]]), f"not_Ni_tiene_antecesor_{i[1]}")

# El número de nodos iniciales es 1 + los nodos que no están conectados
model.addConstr((quicksum(Ni[i[0]]) for i in nodos) == 1 + ((quicksum(1 - y[i[0]])) for i in nodos), f"Nodo_sin_antecesor")

# Funcion Objetivo y optimizar el problema:

model.setObjective(quicksum((y[i[0]] * i[3]) for i in nodos), GRB.MAXIMIZE) 
#maximizar la suma de las estaciones puestas por la población en ellas

model.optimize()

# Todavía no sé como imprimir la solución
tiempo_ejecucion = model.Runtime
print(tiempo_ejecucion)
valor_objetivo = model.ObjVal
print(valor_objetivo)
print("banana")