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
            model.addConstr(x[e,t,s] <= h[e,s], f"Habilidades_${e}_${t}_${s}")
            model.addConstr(x[e,t,s] <= z[e], f"Contratado_${e}_${t}_${s}")
        
for e in E:
    for t in T:
        model.addConstr(quicksum(x[e,t,s] for s in S) <= 1, f"Una_sola_tarea_diaria_${e}_${t}")

for s in S:
    for t in T:
        model.addConstr(quicksum(x[e,t,s] for e in E) >= b[t,s], f"Empleados_requeridos_por_funcion_cada_dia_${t}_${s}")

for e in E:
    for s in S:
        model.addConstr(quicksum((x[e,tprima,s] + x[e,tprima + 1,s] + x[e,tprima + 2,s]+ x[e,tprima + 3,s]) 
                                 for tprima in range(0, len(T)-4, 3)) <= 3, f"No_3_dias_seguidos_${e}_${s}")
        
for e in E:
    model.addConstr(quicksum(x[e,t,s] for s in S for t in T) <= D*y[e], f"Limite_dias_normales_${e}")
    model.addConstr(quicksum(x[e,t,s] for s in S for t in T) >= M*z[e], f"Minimo_de_dias_con_contrato_${e}")


# Añadir función objetivo
model.setObjective(quicksum((c[e,t,s] * x[e,t,s]) for e in E for t in T for s in S) 
                   + quicksum((f[e] * y[e]) for e in E)
                   + quicksum((d[e] * z[e]) for e in E), GRB.MINIMIZE) 

model.update()
model.optimize()


# Añadir procesamiento de datos
if model.status == GRB.OPTIMAL:
    pass
    