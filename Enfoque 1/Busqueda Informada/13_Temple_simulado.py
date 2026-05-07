"""
Búsqueda de Temple Simulado (Simulated Annealing)

Algoritmo metaheurístico inspirado en el proceso físico del
recocido de metales. Acepta soluciones peores con una probabilidad
controlada por la temperatura, lo que le permite escapar de
óptimos locales. La temperatura disminuye gradualmente hasta
que el sistema se estabiliza en una solución cercana al óptimo.

Parámetros clave:
  - Temperatura inicial (T): alta al inicio, permite más exploración.
  - Tasa de enfriamiento (alpha): factor de reducción de temperatura.
  - Temperatura mínima: condición de parada del algoritmo.
  - Probabilidad de aceptación: e^(-delta/T) para soluciones peores.
"""

import math
import random

# ==================================================
# Definición del grafo con costos
# Cada nodo tiene una lista de tuplas (vecino, costo)
# ==================================================
grafo = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('D', 3), ('E', 6)],
    'C': [('A', 5), ('F', 2), ('G', 7)],
    'D': [('B', 3), ('H', 2)],
    'E': [('B', 6), ('H', 4), ('I', 3)],
    'F': [('C', 2), ('I', 5), ('J', 3)],
    'G': [('C', 7), ('J', 2)],
    'H': [('D', 2), ('E', 4), ('K', 1)],
    'I': [('E', 3), ('F', 5), ('K', 2)],
    'J': [('F', 3), ('G', 2), ('K', 4)],
    'K': []  # Nodo objetivo
}

# ==================================================
# Heurística: estimación del costo al objetivo 'K'
# Menor valor = más cerca del objetivo
# ==================================================
heuristica = {
    'A': 9,
    'B': 7,
    'C': 7,
    'D': 5,
    'E': 4,
    'F': 4,
    'G': 5,
    'H': 2,
    'I': 2,
    'J': 3,
    'K': 0
}

# Obtener vecinos de un nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Obtener valor heurístico de un nodo
def obtener_heuristica(nodo):
    return heuristica.get(nodo, float('inf'))

# ==================================================
# Probabilidad de aceptar una solución peor
# Formula: e^(-delta / T)
# ==================================================
def probabilidad_aceptacion(h_actual, h_nuevo, temperatura):
    delta = h_nuevo - h_actual  # Diferencia de costos
    if delta < 0:
        return 1.0  # Siempre aceptar si es mejor
    return math.exp(-delta / temperatura)  # Probabilidad decreciente

# ==================================================
# ALGORITMO DE TEMPLE SIMULADO
# ==================================================
def temple_simulado(inicio, objetivo,
                    temperatura_inicial=100.0,
                    tasa_enfriamiento=0.85,
                    temperatura_minima=0.1,
                    max_iteraciones=100):

    print("\n" + "="*55)
    print("      INICIANDO BÚSQUEDA DE TEMPLE SIMULADO")
    print("="*55)
    print(f"Nodo Inicio          : '{inicio}'")
    print(f"Nodo Objetivo        : '{objetivo}'")
    print(f"Temperatura Inicial  : {temperatura_inicial}")
    print(f"Tasa de Enfriamiento : {tasa_enfriamiento}")
    print(f"Temperatura Mínima   : {temperatura_minima}")
    print(f"Máx. Iteraciones     : {max_iteraciones}")
    print("="*55 + "\n")

    nodo_actual   = inicio           # Estado actual
    mejor_nodo    = inicio           # Mejor solución global
    mejor_h       = obtener_heuristica(inicio)  # Mejor heurística global
    temperatura   = temperatura_inicial          # Temperatura actual
    ruta          = [inicio]         # Ruta recorrida
    iteracion     = 0                # Contador de iteraciones

    while temperatura > temperatura_minima and iteracion < max_iteraciones:
        iteracion += 1

        print(f"Iteracion {iteracion} | Temperatura: {temperatura:.4f}")
        print(f"  Nodo actual : '{nodo_actual}' | h(n) = {obtener_heuristica(nodo_actual)}")

        # Si llegamos al objetivo, terminar
        if nodo_actual == objetivo:
            print(f"\n  Objetivo '{objetivo}' alcanzado!\n")
            break

        vecinos = obtener_vecinos(nodo_actual)

        # Si no hay vecinos, detener
        if not vecinos:
            print(f"  Sin vecinos disponibles. Deteniendo busqueda.\n")
            break

        # Elegir un vecino aleatorio
        vecino_elegido, costo_arista = random.choice(vecinos)
        h_vecino = obtener_heuristica(vecino_elegido)
        h_actual = obtener_heuristica(nodo_actual)

        # Calcular probabilidad de aceptacion
        prob = probabilidad_aceptacion(h_actual, h_vecino, temperatura)

        print(f"  Vecino elegido : '{vecino_elegido}' | h(n) = {h_vecino}")
        print(f"  Delta h        : {h_vecino - h_actual}")
        print(f"  Probabilidad   : {prob:.4f}")

        # Decidir si moverse al vecino
        if prob > random.random():
            nodo_actual = vecino_elegido
            ruta.append(nodo_actual)
            print(f"  Movimiento     : ACEPTADO -> '{nodo_actual}'")

            # Actualizar mejor solucion global
            if h_vecino < mejor_h:
                mejor_h    = h_vecino
                mejor_nodo = nodo_actual
                print(f"  Nueva mejor solucion global: '{mejor_nodo}' h(n) = {mejor_h}")
        else:
            print(f"  Movimiento     : RECHAZADO. Permanece en '{nodo_actual}'")

        # Reducir temperatura (enfriamiento)
        temperatura *= tasa_enfriamiento
        print()

    # Resultado final
    print("="*55)
    if nodo_actual == objetivo:
        print(f"Objetivo '{objetivo}' encontrado en {iteracion} iteraciones!")
    else:
        print(f"Objetivo '{objetivo}' no alcanzado.")
        print(f"Mejor nodo alcanzado : '{mejor_nodo}' con h(n) = {mejor_h}")

    print(f"Ruta recorrida : {' -> '.join(ruta)}")
    print(f"Temperatura final : {temperatura:.4f}")
    print("="*55)
    return ruta

# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":
    temple_simulado(
        inicio               = 'A',
        objetivo             = 'K',
        temperatura_inicial  = 100.0,
        tasa_enfriamiento    = 0.85,
        temperatura_minima   = 0.1,
        max_iteraciones      = 100
    )
