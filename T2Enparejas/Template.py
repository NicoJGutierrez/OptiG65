import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum, Model
from Datos import h, b, c, f, d, D, M

model = Model()
T = range(25)
S = range(10)
E = range(37)

## Añadir las variables
x = {}
y = {}
z = {}
# Se asigna el empleado (e) a una función (s) el día (t)?
for e in E:
    for t in T:
        for s in S:
            x[e,t,s] = model.addVar(vtype = GRB.BINARY, name=f"x_{e}_{t}_{s}")
    y[e] = model.addVar(vtype = GRB.BINARY, name=f"y_{e}")
    z[e] = model.addVar(vtype = GRB.BINARY, name=f"z_{e}")

## Añadir las resrticciones
for e in E:
    for s in S:
        for t in T:
            model.addConstr(x[e,t,s] - y[i[0]] <= h[e,s], f"Nodo_receptor_${i[1]}")

# Añadir función objetivo
model.setObjective(quicksum((c[e,t,s] * x[e,t,s]) for e in E for t in T for s in S) 
                   + quicksum((f[e] * y[e]) for e in E)
                   + quicksum((d[e] * z[e]) for e in E), GRB.MINIMIZE) 

model.update()
model.optimize()


# Añadir procesamiento de datos
if model.status == GRB.OPTIMAL:
    pass
    