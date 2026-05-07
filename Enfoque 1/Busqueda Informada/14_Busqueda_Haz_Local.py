"""
Búsqueda de Haz Local (Local Beam Search)

Algoritmo de búsqueda local que mantiene k estados simultáneos.
En cada iteración genera todos los sucesores de los k estados
actuales y selecciona los k mejores para continuar la búsqueda.

Diferencia clave con Hill Climbing:
  - Hill Climbing mantiene 1 estado.
  - Haz Local mantiene k estados simultáneos que comparten
    información entre sí, lo que permite mejor exploración.

Variantes implementadas:
  1. Haz Local Simple: selecciona siempre los k mejores sucesores.
  2. Haz Local Estocástico: selecciona k sucesores con probabilidad
     proporcional a su calidad, reduciendo riesgo de concentración.

Parámetros:
  - k: numero de estados a mantener simultaneamente.
  - max_iteraciones: limite de iteraciones para evitar ciclos infinitos.
"""

import random

# ==================================================
# Definicion del grafo con costos
# Cada nodo tiene una lista de tuplas (vecino, costo)
# ==================================================
grafo = {
    'A': [('B', 2), ('C', 4)],
    'B': [('A', 2), ('D', 3), ('E', 5)],
    'C': [('A', 4), ('F', 2), ('G', 6)],
    'D': [('B', 3), ('H', 2), ('I', 4)],
    'E': [('B', 5), ('H', 3), ('I', 2)],
    'F': [('C', 2), ('I', 4), ('J', 3)],
    'G': [('C', 6), ('J', 2), ('K', 5)],
    'H': [('D', 2), ('E', 3), ('L', 1)],
    'I': [('D', 4), ('E', 2), ('F', 4), ('L', 2)],
    'J': [('F', 3), ('G', 2), ('L', 3)],
    'K': [('G', 5), ('L', 1)],
    'L': []  # Nodo objetivo
}

# ==================================================
# Heuristica: estimacion del costo al objetivo 'L'
# Menor valor = mas cerca del objetivo
# ==================================================
heuristica = {
    'A': 10,
    'B': 8,
    'C': 8,
    'D': 6,
    'E': 5,
    'F': 5,
    'G': 6,
    'H': 2,
    'I': 2,
    'J': 3,
    'K': 2,
    'L': 0
}

# Obtener vecinos de un nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Obtener valor heuristico de un nodo
def obtener_heuristica(nodo):
    return heuristica.get(nodo, float('inf'))

# ==================================================
# Generar todos los sucesores de una lista de estados
# Retorna lista de nodos vecinos sin repetir
# ==================================================
def generar_sucesores(estados):
    sucesores = []
    for estado in estados:
        for vecino, _ in obtener_vecinos(estado):
            if vecino not in sucesores:
                sucesores.append(vecino)
    return sucesores

# ==================================================
# VARIANTE 1: Haz Local Simple
# Mantiene los k mejores estados en cada iteracion
# ==================================================
def haz_local_simple(inicio, objetivo, k=3, max_iteraciones=20):
    print("\n" + "="*55)
    print("         HAZ LOCAL SIMPLE")
    print("="*55)
    print(f"Nodo Inicio      : '{inicio}'")
    print(f"Nodo Objetivo    : '{objetivo}'")
    print(f"k estados        : {k}")
    print(f"Max. Iteraciones : {max_iteraciones}")
    print("="*55 + "\n")

    # Inicializar con k copias del estado inicial
    estados_actuales = [inicio] * k
    iteracion = 0

    while iteracion < max_iteraciones:
        iteracion += 1
        print(f"Iteracion {iteracion}:")
        print(f"  Estados actuales : {estados_actuales}")

        # Verificar si alguno de los estados es el objetivo
        for estado in estados_actuales:
            if estado == objetivo:
                print(f"\n  Objetivo '{objetivo}' encontrado!")
                print(f"  Estados finales : {estados_actuales}\n")
                return estados_actuales

        # Generar todos los sucesores de los k estados
        sucesores = generar_sucesores(estados_actuales)
        print(f"  Sucesores generados : {sucesores}")

        if not sucesores:
            print(f"  Sin sucesores disponibles. Deteniendo busqueda.")
            break

        # Ordenar sucesores por heuristica (menor es mejor)
        sucesores_ordenados = sorted(sucesores, key=obtener_heuristica)
        print(f"  Sucesores ordenados por h(n):")
        for s in sucesores_ordenados:
            print(f"    '{s}' -> h(n) = {obtener_heuristica(s)}")

        # Seleccionar los k mejores sucesores
        estados_actuales = sucesores_ordenados[:k]
        print(f"  k mejores seleccionados : {estados_actuales}\n")

    print("="*55)
    print(f"Objetivo '{objetivo}' no alcanzado en {max_iteraciones} iteraciones.")
    mejor = min(estados_actuales, key=obtener_heuristica)
    print(f"Mejor estado alcanzado : '{mejor}' con h(n) = {obtener_heuristica(mejor)}")
    print("="*55)
    return estados_actuales

# ==================================================
# VARIANTE 2: Haz Local Estocastico
# Selecciona k sucesores con probabilidad proporcional
# a su calidad, reduciendo riesgo de concentracion
# ==================================================
def haz_local_estocastico(inicio, objetivo, k=3, max_iteraciones=20):
    print("\n" + "="*55)
    print("      HAZ LOCAL ESTOCASTICO")
    print("="*55)
    print(f"Nodo Inicio      : '{inicio}'")
    print(f"Nodo Objetivo    : '{objetivo}'")
    print(f"k estados        : {k}")
    print(f"Max. Iteraciones : {max_iteraciones}")
    print("="*55 + "\n")

    # Inicializar con k copias del estado inicial
    estados_actuales = [inicio] * k
    iteracion = 0

    while iteracion < max_iteraciones:
        iteracion += 1
        print(f"Iteracion {iteracion}:")
        print(f"  Estados actuales : {estados_actuales}")

        # Verificar si alguno de los estados es el objetivo
        for estado in estados_actuales:
            if estado == objetivo:
                print(f"\n  Objetivo '{objetivo}' encontrado!")
                print(f"  Estados finales : {estados_actuales}\n")
                return estados_actuales

        # Generar todos los sucesores de los k estados
        sucesores = generar_sucesores(estados_actuales)
        print(f"  Sucesores generados : {sucesores}")

        if not sucesores:
            print(f"  Sin sucesores disponibles. Deteniendo busqueda.")
            break

        # Calcular pesos inversamente proporcionales a la heuristica
        # Menor heuristica = mayor probabilidad de ser seleccionado
        pesos = []
        for s in sucesores:
            h = obtener_heuristica(s)
            # Evitar division por cero si h = 0 (objetivo)
            peso = 1.0 / (h + 0.1)
            pesos.append(peso)

        print(f"  Pesos de seleccion:")
        for s, p in zip(sucesores, pesos):
            print(f"    '{s}' -> h(n) = {obtener_heuristica(s)}, peso = {p:.4f}")

        # Seleccionar k estados con probabilidad proporcional al peso
        k_real = min(k, len(sucesores))
        estados_actuales = random.choices(sucesores, weights=pesos, k=k_real)
        print(f"  k estados seleccionados estocasticamente : {estados_actuales}\n")

    print("="*55)
    print(f"Objetivo '{objetivo}' no alcanzado en {max_iteraciones} iteraciones.")
    mejor = min(estados_actuales, key=obtener_heuristica)
    print(f"Mejor estado alcanzado : '{mejor}' con h(n) = {obtener_heuristica(mejor)}")
    print("="*55)
    return estados_actuales

# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":

    # Ejecutar Haz Local Simple
    haz_local_simple(
        inicio          = 'A',
        objetivo        = 'L',
        k               = 3,
        max_iteraciones = 20
    )

    # Ejecutar Haz Local Estocastico
    haz_local_estocastico(
        inicio          = 'A',
        objetivo        = 'L',
        k               = 3,
        max_iteraciones = 20
    )
