"""
Búsqueda de Ascensión de Colinas (Hill Climbing)

Es un algoritmo de búsqueda local e informada que se mueve
siempre hacia el vecino con el mejor valor heurístico, 
similar a escalar una colina buscando siempre la dirección
que suba más.

Características:
  - Solo considera el estado actual y sus vecinos inmediatos.
  - Es codicioso (Greedy): elige siempre el mejor vecino disponible.
  - No garantiza la solución óptima global.
  - Puede quedar atascado en:
      * Máximos locales: nodo mejor que sus vecinos pero no el óptimo global.
      * Mesetas: zona donde todos los vecinos tienen el mismo valor.
      * Crestas: secuencia de máximos locales difíciles de navegar.

Variantes:
  1. Hill Climbing Simple: se mueve al primer vecino mejor que el actual.
  2. Hill Climbing de Máxima Pendiente: evalúa todos los vecinos y elige el mejor.
  3. Hill Climbing Estocástico: elige aleatoriamente entre los mejores vecinos.

En este programa se implementan las tres variantes utilizando
el mismo grafo y heurística para comparar su comportamiento.
"""

import random

# ==================================================
# Definición del grafo
# Cada nodo tiene una lista de vecinos
# ==================================================
grafo = {
    'A': ['B', 'C'],        # A se conecta a B y C
    'B': ['D', 'E'],        # B se conecta a D y E
    'C': ['F', 'G'],        # C se conecta a F y G
    'D': ['H'],             # D se conecta a H
    'E': ['H', 'I'],        # E se conecta a H e I
    'F': ['I', 'J'],        # F se conecta a I y J
    'G': ['J'],             # G se conecta a J
    'H': ['K'],             # H se conecta a K
    'I': ['K', 'L'],        # I se conecta a K y L
    'J': ['L'],             # J se conecta a L
    'K': ['M'],             # K se conecta a M (objetivo)
    'L': ['M'],             # L se conecta a M (objetivo)
    'M': []                 # M es el nodo objetivo
}

# ==================================================
# Heurística: estimación de qué tan cerca está
# cada nodo del objetivo 'M'
# Mientras MENOR sea el valor, más cerca está del objetivo
# ==================================================
heuristica = {
    'A': 7,   # Muy lejos del objetivo
    'B': 6,   # Lejos del objetivo
    'C': 6,   # Lejos del objetivo
    'D': 5,   # Distancia media-alta
    'E': 4,   # Distancia media
    'F': 4,   # Distancia media
    'G': 5,   # Distancia media-alta
    'H': 3,   # Relativamente cerca
    'I': 2,   # Cerca del objetivo
    'J': 3,   # Relativamente cerca
    'K': 1,   # Muy cerca del objetivo
    'L': 1,   # Muy cerca del objetivo
    'M': 0    # Es el objetivo
}

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Función para obtener el valor heurístico de un nodo
def obtener_heuristica(nodo):
    return heuristica.get(nodo, float('inf'))

# ==================================================
# VARIANTE 1: Hill Climbing Simple
# Se mueve al PRIMER vecino que sea mejor que el actual
# ==================================================
def hill_climbing_simple(inicio, objetivo):
    print("\n" + "="*50)
    print("   HILL CLIMBING SIMPLE")
    print("="*50)
    print(f"Nodo Inicio: '{inicio}' | Nodo Objetivo: '{objetivo}'")
    print("Estrategia: moverse al PRIMER vecino mejor que el actual\n")

    nodo_actual = inicio
    ruta = [inicio]

    while nodo_actual != objetivo:
        print(f"Nodo actual: '{nodo_actual}' | h(n) = {obtener_heuristica(nodo_actual)}")
        vecinos = obtener_vecinos(nodo_actual)

        if not vecinos:
            print(f"  ✘ Sin vecinos disponibles. Búsqueda detenida en '{nodo_actual}'.")
            return None

        # Buscar el primer vecino mejor que el actual
        movimiento_realizado = False
        for vecino in vecinos:
            h_vecino = obtener_heuristica(vecino)
            print(f"  Evaluando vecino '{vecino}': h(n) = {h_vecino}")
            if h_vecino < obtener_heuristica(nodo_actual):
                print(f"  ✔ Mejor vecino encontrado: '{vecino}'. Moviéndose...")
                nodo_actual = vecino
                ruta.append(nodo_actual)
                movimiento_realizado = True
                break  # Se mueve al primer vecino mejor

        # Si no se encontró un vecino mejor, es un máximo local
        if not movimiento_realizado:
            print(f"  ✘ Máximo local alcanzado en '{nodo_actual}'. No hay vecinos mejores.")
            return None

    print(f"\n✔ Objetivo '{objetivo}' encontrado!")
    print(f"  RUTA RECORRIDA: {' -> '.join(ruta)}\n")
    return ruta

# ==================================================
# VARIANTE 2: Hill Climbing de Máxima Pendiente
# Evalúa TODOS los vecinos y elige el MEJOR
# ==================================================
def hill_climbing_maxima_pendiente(inicio, objetivo):
    print("\n" + "="*50)
    print("   HILL CLIMBING DE MÁXIMA PENDIENTE")
    print("="*50)
    print(f"Nodo Inicio: '{inicio}' | Nodo Objetivo: '{objetivo}'")
    print("Estrategia: evaluar TODOS los vecinos y elegir el MEJOR\n")

    nodo_actual = inicio
    ruta = [inicio]

    while nodo_actual != objetivo:
        print(f"Nodo actual: '{nodo_actual}' | h(n) = {obtener_heuristica(nodo_actual)}")
        vecinos = obtener_vecinos(nodo_actual)

        if not vecinos:
            print(f"  ✘ Sin vecinos disponibles. Búsqueda detenida en '{nodo_actual}'.")
            return None

        # Evaluar todos los vecinos y elegir el de menor heurística
        mejor_vecino = None
        mejor_h = obtener_heuristica(nodo_actual)

        for vecino in vecinos:
            h_vecino = obtener_heuristica(vecino)
            print(f"  Evaluando vecino '{vecino}': h(n) = {h_vecino}")
            if h_vecino < mejor_h:
                mejor_h = h_vecino
                mejor_vecino = vecino

        # Si no se encontró un vecino mejor, es un máximo local
        if mejor_vecino is None:
            print(f"  ✘ Máximo local alcanzado en '{nodo_actual}'. No hay vecinos mejores.")
            return None

        print(f"  ✔ Mejor vecino seleccionado: '{mejor_vecino}' con h(n) = {mejor_h}. Moviéndose...")
        nodo_actual = mejor_vecino
        ruta.append(nodo_actual)
        print()

    print(f"\n✔ Objetivo '{objetivo}' encontrado!")
    print(f"  RUTA RECORRIDA: {' -> '.join(ruta)}\n")
    return ruta

# ==================================================
# VARIANTE 3: Hill Climbing Estocástico
# Elige ALEATORIAMENTE entre los vecinos mejores
# ==================================================
def hill_climbing_estocastico(inicio, objetivo):
    print("\n" + "="*50)
    print("   HILL CLIMBING ESTOCÁSTICO")
    print("="*50)
    print(f"Nodo Inicio: '{inicio}' | Nodo Objetivo: '{objetivo}'")
    print("Estrategia: elegir ALEATORIAMENTE entre los mejores vecinos\n")

    nodo_actual = inicio
    ruta = [inicio]

    while nodo_actual != objetivo:
        print(f"Nodo actual: '{nodo_actual}' | h(n) = {obtener_heuristica(nodo_actual)}")
        vecinos = obtener_vecinos(nodo_actual)

        if not vecinos:
            print(f"  ✘ Sin vecinos disponibles. Búsqueda detenida en '{nodo_actual}'.")
            return None

        # Filtrar vecinos que sean mejores que el actual
        h_actual = obtener_heuristica(nodo_actual)
        mejores_vecinos = [v for v in vecinos if obtener_heuristica(v) < h_actual]

        print(f"  Vecinos disponibles: {vecinos}")
        print(f"  Vecinos mejores que el actual: {mejores_vecinos}")

        # Si no hay vecinos mejores, es un máximo local
        if not mejores_vecinos:
            print(f"  ✘ Máximo local alcanzado en '{nodo_actual}'. No hay vecinos mejores.")
            return None

        # Elegir aleatoriamente entre los mejores vecinos
        nodo_actual = random.choice(mejores_vecinos)
        ruta.append(nodo_actual)
        print(f"  ✔ Vecino elegido aleatoriamente: '{nodo_actual}'. Moviéndose...\n")

    print(f"\n✔ Objetivo '{objetivo}' encontrado!")
    print(f"  RUTA RECORRIDA: {' -> '.join(ruta)}\n")
    return ruta

# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================
if __name__ == "__main__":
    inicio = 'A'
    objetivo = 'M'

    # Ejecutar las tres variantes
    hill_climbing_simple(inicio, objetivo)
    hill_climbing_maxima_pendiente(inicio, objetivo)
    hill_climbing_estocastico(inicio, objetivo)
