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
    y[e] = model.addVar(lb=-1e10, ub=1e10, name=f"y_{e}")
    z[e] = model.addVar(vtype = GRB.BINARY, name=f"z_{e}")

## Añadir las resrticciones
for e in E:
    for s in S:
        for t in T:
            model.addConstr(x[e,t,s] <= h[e,s], f"Habilidades_${e}_${t}_${s}") # 1) Si no tienes la habilidad no te podemos usar
            model.addConstr(x[e,t,s] <= z[e], f"Contratado_${e}_${t}_${s}")
        
for e in E:
    for t in T:
        model.addConstr(quicksum(x[e,t,s] for s in S) <= 1, f"Una_sola_tarea_diaria_${e}_${t}") # 2) No más de una tarea por día
        pass

for s in S:
    for t in T:
        model.addConstr(quicksum(x[e,t,s] for e in E) >= b[t,s], f"Empleados_requeridos_por_funcion_cada_dia_${t}_${s}") # 3) Todas las tareas se cumplen todos los días
        pass

for e in E:
    for s in S:
        for t in range(len(T) - 3):
            model.addConstr(quicksum(x[e,tprima,s] for tprima in range(t, t+3)) <= 3, f"No_3_dias_seguidos_${e}_${t}_${s}") # 4) No más de 3 días seguidos trabajando
            #print(range(t,t+4))
        pass

for e in E:
    model.addConstr(quicksum(x[e,t,s] for s in S for t in T) <= D + y[e], f"Limite_dias_normales_${e}") # 5) Días trabajados = días normales + días extraordinarios
    model.addConstr(quicksum(x[e,t,s] for s in S for t in T) >= M * z[e], f"Minimo_de_dias_con_contrato_${e}") # 6) Debes trabajar mínimo M días si estás contratado


# Añadir función objetivo
model.setObjective((quicksum((c[e,t,s] * x[e,t,s]) for e in E for t in T for s in S) 
                   + quicksum((f[e] * y[e]) for e in E)
                   + quicksum((d[e] * z[e]) for e in E)), GRB.MINIMIZE) 

model.update()
model.optimize()


# Añadir procesamiento de datos
if model.status == GRB.OPTIMAL:
    # Imprimir semana de las personas a revisar:
    personas_a_revisar = [0, 5, 14]
    for e in E:
        if e in personas_a_revisar:
            lista_semana = []
            for t in T:
                funcion = -1
                for s in S:
                    if x[e,t,s].x >= 0.9:
                        funcion = s
                        #print(s)
                lista_semana.append(funcion)
            print(f"Lista_persona_{e} = {lista_semana}")
    
    # Lista de personas contratadas:
    lista_empleados = []
    for e in E:
        if z[e].x >= 0.9:
            lista_empleados.append(e)
    print(f"Empleados contratados: {lista_empleados}")
    