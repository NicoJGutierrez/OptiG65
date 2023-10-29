import leerCSV as CSV
from gurobipy import Model, GRB, quicksum
from itertools import combinations

presupuesto = 3000
#input("Elija un presupuesto para el proyecto (en millones de pesos)")

# constante arbitrariamente grande:
ctte = 9999

nodos = CSV.leer_csv("Datos.csv")
nodos[0][0] = '0'

for i in nodos:
    i[0] = int(i[0])
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
FLOW = {}
for i in nodos:
    for j in nodos:
        if i != j: # Restricción de nodos no iguales
            x[i[0],j[0]] = model.addVar(vtype = GRB.BINARY, name=f"x_{i[1]}_{j[1]}") # 1 tiene que ser el nombre de la ciudad
            # x = conexión
            # flujo:
            FLOW[i[0],j[0]] = model.addVar(vtype = GRB.CONTINUOUS, name= f"FLOW_{i[1]}_{j[1]}")

# Hay una estación en un nodo i?
y = {}
for i in nodos:
    y[i[0]] = model.addVar(vtype = GRB.BINARY, name= f"y_({i[1]})")


# Es i un nodo inicial? (los nodos desconectados son iniciales y hay uno solo conectado e inicial)
Ni = {}
for i in nodos:
    Ni[i[0]] = model.addVar(vtype = GRB.BINARY, name= f"Ni_({i[1]})")

# Costo de conexiones de i:
Cx = {}
for i in nodos:
    Cx[i[0]] = model.addVar(vtype = GRB.CONTINUOUS, name= f"Cx_({i[1]})")
    #(quicksum(x[i[0], j[0]] * (i[(int(j[0]) + 4)])) for j in nodos if i != j)

# Costo de todas las conexiones:
CAx = model.addVar(vtype = GRB.CONTINUOUS, name= f"CAx")
#(quicksum(Cx[i[0]]) for i in nodos)

# Costo de todas las estaciones:
CAy = model.addVar(vtype = GRB.CONTINUOUS, name= f"CAy")
#(quicksum(y[i[0]]) for i in nodos)

# Cantidad de estaciones no conectadas:
NCS = model.addVar(vtype = GRB.CONTINUOUS, name= f"NCS")


# Llamamos a update
model.update()

# Restricciones:

# Sólo puede haber un camino entre 2 nodos que tienen estaciones
for i in nodos:
    for j in nodos:
        if i != j:
            #print(f"i[0]: {i[0]}, j[0]: {j[0]}")
            # Para que haya una conexión de i a j:
            model.addConstr((x[i[0], j[0]] <= y[i[0]]), f"ruta_{i[1]}_{j[1]}_estacion_{i[1]}") # Tiene que haber estación en i
            model.addConstr((x[i[0], j[0]] <= y[j[0]]), f"ruta_{i[1]}_{j[1]}_estacion_{j[1]}") # Tiene que haber estación en j

# Evitar ciclos de 2 nodos (los arcos no son bidireccionales)
for i in nodos:
    for j in nodos:
        if i != j:
            model.addConstr(x[i[0], j[0]] + x[j[0], i[0]] <= 1, f"no_ciclo_{i[1]}_{j[1]}")

# El costo de todas las conexiones de una estación es la suma de todos esos costos
for i in nodos:
    model.addConstr(quicksum(x[i[0], j[0]] * (i[(int(j[0]) + 4)])for j in nodos if i != j) == Cx[i[0]], f"Rest Cx")

# El costo de todas las conexiones de todas las estaciones es la suma de esos costos
model.addConstr(quicksum(Cx[i[0]] for i in nodos) == CAx, f"Rest CAx")

# El costo de todas las estaciones es la suma de esos costos
model.addConstr(quicksum(y[i[0]]*i[2] for i in nodos) == CAy, f"Rest CAy")

# El costo total es menor al presupuesto
model.addConstr(CAx <= presupuesto - CAy, f"Rest Costos")
# Las conexiones no se generan dos veces por la restricción anterior


# Las estaciones no conectadas son las estaciones que no están construídas
model.addConstr(NCS == quicksum(1 - y[i[0]] for i in nodos), f"Rest NCS")

# Los nodos tienen máximo 1 antecesor y tienen 0 si no tienen estación
for i in nodos:
    model.addConstr(quicksum(x[j[0], i[0]] for j in nodos if i != j) <= y[i[0]], f"Un_antecesor_{i[1]}")

# Los nodos con al menos 1 antecesor son todos los nodos no iniciales
for i in nodos:
    model.addConstr(quicksum(x[j[0], i[0]] for j in nodos if i != j) >= (1 - Ni[i[0]]), f"not_Ni_tiene_antecesor_{i[1]}")

# El número de nodos iniciales es 1 + los nodos que no están conectados
model.addConstr(quicksum(Ni[i[0]] for i in nodos) == 1 + NCS, f"Nodo_sin_antecesor")

# ===================
# SIN CICLOS
# ===================

# Flujo solo a receptor válido
for i in nodos:
    for j in nodos:
        if j != i:
            model.addConstr(FLOW[i[0], j[0]] <= ctte * x[i[0],j[0]], f"Flujo_solo_a_receptor_${i[1]}_${j[1]}")
            model.addConstr(0 <= FLOW[i[0], j[0]], f"Flujo_no_negativo_${i[1]}_${j[1]}")



for i in nodos:
    if i[0] != 0:
        # Demanda en la red
        model.addConstr(quicksum(FLOW[j[0], i[0]] for j in nodos if i != j) - y[i[0]] == quicksum(FLOW[i[0], j[0]] for j in nodos if i != j), f"Nodo_receptor_${i[1]}")
    else:
        # Oferta en la red
        model.addConstr(quicksum(FLOW[i[0], j[0]] for j in nodos if i != j) == quicksum(y[i[0]] for i in nodos) - 1, f"Nodo_inicial")

# El nodo sin antecesores pero con sucesores tiene capacidad = número de nodos -1

# El resto de los nodos que tienen un antecesor tienen capacidad = -1

# Los nodos no conectados tienen capacidad = 0

# ===================

# Funcion Objetivo y optimizar el problema:
model.setObjective(quicksum((y[i[0]] * i[3]) for i in nodos), GRB.MAXIMIZE) 
#maximizar la suma de las estaciones puestas por la población en ellas

model.optimize()

# Todavía no sé como imprimir la solución

# Imprimir solución

q = "======================================================"

# Print the values of x[i,j]
print(f"{q}\nConexiones:\n{q}")
k = 0
for i in nodos:
    for j in nodos:
        if i != j:
            if x[i[0],j[0]].x >= 0.5:
                k += 1
                print(f"{k}) Conex {i[1]} con {j[1]} ({x[i[0],j[0]].x})")
            if FLOW[i[0],j[0]].x >= 0.5:
                pass
                print(f"Flujo {i[1]} con {j[1]} = {FLOW[i[0],j[0]].x}")

# Print the values of y[i]
print(f"{q}\nEstaciones:\n{q}")
k = 0
for i in nodos:
    if y[i[0]].x >= 0.5:
        k += 1
        print(f"{k}) Estación en {i[1]} ({y[i[0]].x})")

print(f"{q}")


tiempo_ejecucion = model.Runtime
print(tiempo_ejecucion)
valor_objetivo = model.ObjVal
print(valor_objetivo)