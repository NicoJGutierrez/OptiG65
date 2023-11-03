import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum, Model
from Datos import h, b, c, f, d, D, M

model = Model()
T = range(25)
S = range(10)
E = range(37)

## Añadir las resrticciones

# Añadir función objetivo


model.update()
model.optimize()


# Añadir procesamiento de datos
if model.status == GRB.OPTIMAL:
    pass
    