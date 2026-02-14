#...variables
columnas= 8
filas= 8
gato="🐈"
raton="🐁"


#...bucle compacto
matriz= [["[]" for _ in range(columnas)] for _ in range(filas)]

def tablero_min(matriz):
    for fila in matriz:
        print(" ".join (fila))
        
tablero= tablero_min(matriz)
print(tablero)

#...colocar al gato y al raton


