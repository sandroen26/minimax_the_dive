# minimax_the_dive
juego del gato y el raton con minimax.

Implementación del algoritmo Minimax Proyecto Minimax: Gato vs. Ratón

¿De qué trata? El juego enfrenta a dos personajes con objetivos opuestos:

El Gato (G): Su objetivo es interceptar al ratón.

El Ratón (R): Su objetivo es evadir al gato la mayor cantidad de turnos posibles.

Lógica Principal Para dotar de "inteligencia" a los personajes, utilicé el algoritmo matemático Minimax.

Antes de dar un paso en la pantalla, el programa simula los posibles movimientos futuros en la memoria de la computadora. El Gato siempre elige el camino que minimiza la distancia hacia su objetivo, mientras que el Ratón elige el camino que maximiza su distancia para escapar.

Herramientas utilizadas Lenguaje: Python

Librerías: random y copy (incluidas por defecto en Python).

Estructuras: Uso de diccionarios para organizar los datos de la partida y matrices bidimensionales para el tablero.