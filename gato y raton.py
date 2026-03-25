import random
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURACIÓN ---
SIZE = 10
TURNOS_MAXIMOS = 1
# Importante: El ratón DEBE moverse, eliminamos el (0,0) de los movimientos
MOVIMIENTOS = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

def obtener_distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def obtener_jugadas_legales(pos):
    jugadas = []
    for dx, dy in MOVIMIENTOS:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            jugadas.append((nx, ny))
    random.shuffle(jugadas) # Rompe el empate de decisiones
    return jugadas

def minimax(gato, raton, profundidad, es_turno_raton):
    distancia = obtener_distancia(gato, raton)
    
    if distancia == 0: 
        return -100 
    
    if profundidad == 0:
        # Añadimos un pequeño bono por estar lejos de las esquinas
        # Esto evita que se quede "atrapado" solo por lógica
        bono_centro = (SIZE // 2) - abs(raton[0] - SIZE // 2) - abs(raton[1] - SIZE // 2)
        return distancia + (bono_centro * 0.1)

    if es_turno_raton:
        mejor_valor = float('-inf')
        for nueva_pos in obtener_jugadas_legales(raton):
            valor = minimax(gato, nueva_pos, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        peor_valor = float('inf')
        for nueva_pos in obtener_jugadas_legales(gato):
            valor = minimax(nueva_pos, raton, profundidad - 1, True)
            peor_valor = min(peor_valor, valor)
        return peor_valor

def dibujar_tablero(gato, raton, mensaje=""):
    print("\n" * 2 + mensaje)
    for y in range(SIZE):
        fila = ""
        for x in range(SIZE):
            if (x, y) == gato: fila += "🐈 "
            elif (x, y) == raton: fila += "🐭 "
            else: fila += ".  "
        print(fila)

def jugar():
    gato = (0, 0)
    raton = (SIZE-1, SIZE-1)
    
    for turno in range(1, TURNOS_MAXIMOS + 1):
        # --- TURNO DEL RATÓN ---
        if turno <= 1:
            # Fase 1: El ratón es tonto (Movimiento aleatorio)
            proximo_raton = random.choice(obtener_jugadas_legales(raton))
            msg = f"Turno {turno}: El Ratón está confundido (Mov. Aleatorio)..."
        else:
            # Fase 2: Despierta el genio (Minimax)
            posibles = obtener_jugadas_legales(raton)
            mejor_puntuacion = float('-inf')
            proximo_raton = raton
            for mov in posibles:
                puntuacion = minimax(gato, mov, profundidad=4, es_turno_raton=False)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    proximo_raton = mov
            msg = f"Turno {turno}: ¡El Ratón ha despertado su genio!"

        raton = proximo_raton
        dibujar_tablero(gato, raton, msg)
        
        if gato == raton:
            print("¡EL GATO ATRAPÓ AL RATÓN!")
            return

        time.sleep(0.5)

        # --- TURNO DEL GATO ---es tonto (Movimiento aleatorio)
 
        posibles_gato = obtener_jugadas_legales(gato)
        mejor_puntuacion = float('inf')
        proximo_gato = gato

        for mov in posibles_gato:
            puntuacion = minimax(mov, raton, profundidad=4, es_turno_raton=True)
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                proximo_gato = mov
        
        gato = proximo_gato
        dibujar_tablero(gato, raton, "El Gato está calculando su salto...")

        if gato == raton:
            print("¡GAME OVER: El gato ha cenado!")
            return

        time.sleep(0.5)

    print("\n¡EL RATÓN ESCAPÓ! La científica cyborg está decepcionada del gato.")

jugar()