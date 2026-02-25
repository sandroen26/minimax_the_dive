import random
import copy

# Las Variables
COLUMNAS = 5
FILAS = 5
pos_gato = (0, 0)
pos_raton = (4, 4)
pos_queso = (2, 2)
MAX_TURNOS = 30

# Tablero - Matriz 
#matriz = [["-" for _ in range(COLUMNAS)] for _ in range(FILAS)]

def mostrar_tablero(pos_gato, pos_raton, pos_queso):
    for i in range(FILAS):
        fila_str = ""
        for j in range(COLUMNAS):
            if (i, j) == pos_gato:
                fila_str += " 🐈 "   # Gato
            elif (i, j) == pos_raton:
                fila_str += " 🐁 "   # Ratón
            elif (i, j) == pos_queso:
                fila_str += " 🧀 "   # Queso
            else:
                fila_str += " [] "   # Celda vacía
        print(fila_str)
    print()

mostrar_tablero(pos_gato, pos_raton, pos_queso)

def movimientos_validos(pos, filas, columnas):
    fila, col = pos
    movimientos = []
    
    # 4 direcciones: arriba, abajo, izquierda, derecha
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
    for df, dc in deltas:
        nueva_fila = fila + df
        nueva_col = col + dc
        if 0 <= nueva_fila < filas and 0 <= nueva_col < columnas:
            movimientos.append((nueva_fila, nueva_col))
    
    return movimientos

#print("Movimientos del gato:", movimientos_validos(pos_gato, FILAS, COLUMNAS))
#print("Movimientos del ratón:", movimientos_validos(pos_raton, FILAS, COLUMNAS))

MAX_TURNOS = 30  # si el ratón sobrevive X turnos, gana!

def verificar_fin(pos_gato, pos_raton, pos_queso, turno):
    if pos_gato == pos_raton:
        print(f"😼 ¡El gato atrapó al ratón en el turno {turno}! Gato gana.")
        return True
    
    if pos_raton == pos_queso:
        print(f"🧀 ¡El ratón llegó al queso en el turno {turno}! Ratón gana.")
        return True
    
    if turno >= MAX_TURNOS:
        print(f"⏰ Se acabó el tiempo. El ratón sobrevivió {turno} turnos. ¡Empate!")
        return True
    
    return False

def mover_raton_aleatorio(pos_raton, filas, columnas):
    movimientos = movimientos_validos(pos_raton, filas, columnas)
    return random.choice(movimientos)

def jugar():
    pos_gato = (0, 0)
    pos_raton = (4, 4)
    pos_queso = (2, 2)
    turno = 0

    print("=== 🐱 LABERINTO DEL GATO Y EL RATÓN 🐭 ===\n")
    mostrar_tablero(pos_gato, pos_raton, pos_queso)

    while True:
        turno += 1
        print(f"--- Turno {turno} ---")

        # Por ahora el gato también se mueve al azar (lo haremos inteligente en paso 5)
        pos_gato = mover_raton_aleatorio(pos_gato, FILAS, COLUMNAS)

        # El ratón se mueve al azar
        pos_raton = mover_raton_aleatorio(pos_raton, FILAS, COLUMNAS)

        mostrar_tablero(pos_gato, pos_raton, pos_queso)

        if verificar_fin(pos_gato, pos_raton, pos_queso, turno):
            break

jugar()

def distancia(pos1, pos2):
    # Distancia Manhattan: cuántos pasos hay entre dos puntos
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def evaluar(pos_gato, pos_raton, pos_queso):
    dist_gato_raton = distancia(pos_gato, pos_raton)
    dist_raton_queso = distancia(pos_raton, pos_queso)
    
    # Positivo = bueno para el ratón, negativo = bueno para el gato
    return dist_gato_raton - dist_raton_queso

def minimax(pos_gato, pos_raton, pos_queso, profundidad, es_turno_gato, filas, columnas):
    
    # Casos base: fin del juego o profundidad máxima alcanzada
    if pos_gato == pos_raton:
        return -1000  # El gato atrapó al ratón → muy malo para el ratón
    if pos_raton == pos_queso:
        return 1000   # El ratón llegó al queso → muy bueno para el ratón
    if profundidad == 0:
        return evaluar(pos_gato, pos_raton, pos_queso)
    
    if es_turno_gato:
        # El gato MINIMIZA (quiere el valor más bajo)
        mejor = float('inf')
        for mov in movimientos_validos(pos_gato, filas, columnas):
            valor = minimax(mov, pos_raton, pos_queso, profundidad - 1, False, filas, columnas)
            mejor = min(mejor, valor)
        return mejor
    
    else:
        # El ratón MAXIMIZA (quiere el valor más alto)
        mejor = float('-inf')
        for mov in movimientos_validos(pos_raton, filas, columnas):
            valor = minimax(pos_gato, mov, pos_queso, profundidad - 1, True, filas, columnas)
            mejor = max(mejor, valor)
        return mejor
    
