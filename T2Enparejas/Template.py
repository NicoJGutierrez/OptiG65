import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum, Model
from Datos import h, b, c, f, d, D, M

model = Model()
T = range(25)
S = range(10)
E = range(37)

## Añadir las resrticciones
for e in E:
    for s in S:
        model.addConstr(quicksum(FLOW[j[0], i[0]] for j in nodos if i != j) - y[i[0]] == quicksum(FLOW[i[0], j[0]] for j in nodos if i != j), f"Nodo_receptor_${i[1]}")

# Añadir función objetivo
model.setObjective(quicksum((y[i[0]] * i[3]) for i in nodos), GRB.MAXIMIZE) 

model.update()
model.optimize()


# Añadir procesamiento de datos
if model.status == GRB.OPTIMAL:
    pass
    