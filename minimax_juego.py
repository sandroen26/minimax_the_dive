#!/usr/bin/env python3
"""🐈 Gato vs Ratón 🐁 - Minimax Compacto (150 líneas)"""
import os, time

# VARIABLES GLOBALES
filas, columnas = 5, 5
matriz = []
pos_gato = {"f": 0, "c": 0}
pos_raton = {"f": 4, "c": 4}
pos_queso = {"f": 0, "c": 4}
profundidad = 3
nodos, podas = 0, 0

# FUNCIONES BÁSICAS
def limpiar(): os.system('cls' if os.name == 'nt' else 'clear')

def crear_tablero():
    global matriz
    matriz = [[None] * columnas for _ in range(filas)]
    matriz[pos_gato["f"]][pos_gato["c"]] = 'G'
    matriz[pos_raton["f"]][pos_raton["c"]] = 'R'
    matriz[pos_queso["f"]][pos_queso["c"]] = 'Q'

def dibujar():
    limpiar()
    print("🐈 GATO vs RATÓN 🐁 | Nodos:", nodos, "| Podas:", podas)
    print("  " + " ".join(str(i) for i in range(columnas)))
    for i, fila in enumerate(matriz):
        print(f"{i} " + " ".join("🐈" if c == 'G' else "🐁" if c == 'R' else "🧀" if c == 'Q' else "▢" for c in fila))
    print()

def distancia(p1, p2): return abs(p1["f"] - p2["f"]) + abs(p1["c"] - p2["c"])

def movimientos_validos(pos):
    movs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            nf, nc = pos["f"] + i, pos["c"] + j
            if 0 <= nf < filas and 0 <= nc < columnas:
                if matriz[nf][nc] is None or matriz[nf][nc] == 'Q':
                    movs.append({"f": nf, "c": nc})
    return movs

# FUNCIÓN HEURÍSTICA - Evalúa qué tan buena es una posición para el gato
def evaluar(pg, pr):
    if pr == pos_queso: return -1000  # Ratón gana (malo para gato)
    if pg == pr: return 1000           # Gato gana (bueno para gato)
    return distancia(pg, pr) * 10 - distancia(pr, pos_queso) * 20

# MINIMAX CON PODA ALFA-BETA - Algoritmo de decisión para juegos
def minimax(pg, pr, prof, maximizando, alfa=-float('inf'), beta=float('inf')):
    global nodos, podas
    nodos += 1
    if prof == 0 or pg == pr or pr == pos_queso: return evaluar(pg, pr)
    
    if maximizando:  # Turno del gato - MAXIMIZA el puntaje
        mejor = -float('inf')
        for mov in movimientos_validos(pg):
            valor = minimax(mov, pr, prof - 1, False, alfa, beta)
            mejor = max(mejor, valor)
            alfa = max(alfa, valor)
            if beta <= alfa:  # PODA BETA
                podas += 1
                break
        return mejor
    else:  # Turno del ratón - MINIMIZA el puntaje
        mejor = float('inf')
        for mov in movimientos_validos(pr):
            valor = minimax(pg, mov, prof - 1, True, alfa, beta)
            mejor = min(mejor, valor)
            beta = min(beta, valor)
            if beta <= alfa:  # PODA ALFA
                podas += 1
                break
        return mejor

# MOVIMIENTOS
def mover(pos, nueva, pieza):
    matriz[pos["f"]][pos["c"]] = None
    pos["f"], pos["c"] = nueva["f"], nueva["c"]
    matriz[pos["f"]][pos["c"]] = pieza

def mover_ia():
    global nodos, podas
    nodos, podas = 0, 0
    movs = movimientos_validos(pos_gato)
    mejor_mov, mejor_val = None, -float('inf')
    for mov in movs:
        val = minimax(mov, pos_raton, profundidad - 1, False)
        if val > mejor_val: mejor_val, mejor_mov = val, mov
    if mejor_mov: mover(pos_gato, mejor_mov, 'G')

def verificar_fin():
    if pos_raton == pos_queso: return "🎉 ¡GANASTE! Llegaste al queso 🧀"
    if pos_gato == pos_raton: return "😿 PERDISTE! El gato te atrapó"
    if not movimientos_validos(pos_raton): return "😿 PERDISTE! Estás bloqueado"
    return None

# JUEGO PRINCIPAL
def jugar():
    crear_tablero()
    while True:
        dibujar()
        fin = verificar_fin()
        if fin:
            print(fin)
            break
        
        # Turno del ratón
        print("🐁 Tu turno:")
        movs = movimientos_validos(pos_raton)
        for i, m in enumerate(movs):
            print(f"  {i+1}. Fila {m['f']}, Columna {m['c']}")
        
        try:
            opcion = int(input("Elige movimiento: ")) - 1
            if 0 <= opcion < len(movs):
                mover(pos_raton, movs[opcion], 'R')
            else:
                print("❌ Opción inválida")
                continue
        except:
            print("❌ Error")
            continue
        
        fin = verificar_fin()
        if fin:
            dibujar()
            print(fin)
            break
        
        # Turno del gato
        print("\n🐈 Turno del gato...")
        time.sleep(0.5)
        mover_ia()

if __name__ == "__main__": jugar()
