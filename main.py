import leerCSV as CSV
from gurobipy import Model, GRB, quicksum

print(CSV.leer_csv("Hola mundo"))

nodos = CSV.leer_csv()

# Generar el modelo
model = Model()

# Se instancian variables de decision

#Existe conexión directa entre 2 estaciones?
for i in nodos:
    for j in nodos:
        if i != j: # Restricción de nodos no iguales
            x = model.addVar(vtype = GRB.BINARY, name="x_({i[0]}, {j[0]})") # 0 tiene que ser el nombre de la ciudad

# Llamamos a update
# Restricciones
# Funcion Objetivo y optimizar el problema
# Manejo Soluciones
print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
# Holguras (0 significa que la restricción es activa)
print("\n"+"-"*9+" Restricciones Activas "+"-"*9)
