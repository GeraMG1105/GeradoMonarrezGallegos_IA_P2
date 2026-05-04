"""
Búsqueda A* y AO*

A* es un algoritmo de búsqueda informada que encuentra el camino más
corto entre un nodo inicial y un nodo objetivo utilizando una función
de evaluación f(n) = g(n) + h(n), donde:
  - g(n): costo acumulado desde el inicio hasta el nodo actual.
  - h(n): heurística que estima el costo desde el nodo actual al objetivo.

A* garantiza encontrar la solución óptima siempre que la heurística
sea admisible (nunca sobreestime el costo real).

AO* es una extensión de A* para grafos AND-OR, donde:
  - Nodos OR: basta con resolver UNO de sus subproblemas.
  - Nodos AND: se deben resolver TODOS sus subproblemas.
AO* es útil en planificación de tareas complejas y sistemas expertos
donde los problemas tienen subproblemas dependientes entre sí.
"""

import heapq

# ==================================================
# Definición del grafo con costos para A*
# Cada nodo tiene una lista de tuplas (vecino, costo)
# ==================================================
grafo_a_estrella = {
    'A': [('B', 1), ('C', 4)],  # A se conecta a B(costo 1) y C(costo 4)
    'B': [('D', 2), ('E', 5)],  # B se conecta a D(costo 2) y E(costo 5)
    'C': [('F', 3)],            # C se conecta a F(costo 3)
    'D': [('G', 1)],            # D se conecta a G(costo 1)
    'E': [('G', 2)],            # E se conecta a G(costo 2)
    'F': [('G', 2)],            # F se conecta a G(costo 2)
    'G': []                     # G es el nodo objetivo
}

# ==================================================
# Heurística para A* (estimación de costo al objetivo 'G')
# Estos valores son estimaciones predefinidas
# ==================================================
heuristica = {
    'A': 6,  # Estimación desde A hasta G
    'B': 4,  # Estimación desde B hasta G
    'C': 4,  # Estimación desde C hasta G
    'D': 2,  # Estimación desde D hasta G
    'E': 2,  # Estimación desde E hasta G
    'F': 2,  # Estimación desde F hasta G
    'G': 0   # El objetivo tiene costo 0
}

# ==================================================
# Definición del grafo AND-OR para AO*
# Cada nodo tiene una lista de subproblemas
# Los subproblemas pueden ser AND (todos) u OR (uno)
# ==================================================
grafo_ao_estrella = {
    'A': {'tipo': 'OR',  'hijos': [('B', 1), ('C', 4)]},   # OR: basta con resolver B o C
    'B': {'tipo': 'AND', 'hijos': [('D', 2), ('E', 3)]},   # AND: hay que resolver D y E
    'C': {'tipo': 'OR',  'hijos': [('F', 2)]},             # OR: basta con resolver F
    'D': {'tipo': 'OR',  'hijos': []},                     # Nodo hoja (sin hijos)
    'E': {'tipo': 'OR',  'hijos': []},                     # Nodo hoja (sin hijos)
    'F': {'tipo': 'OR',  'hijos': [('G', 1)]},             # OR: basta con resolver G
    'G': {'tipo': 'OR',  'hijos': []}                      # Nodo objetivo (sin hijos)
}

# Heurística para AO*
heuristica_ao = {
    'A': 5,
    'B': 3,
    'C': 3,
    'D': 1,
    'E': 1,
    'F': 2,
    'G': 0
}

# ==================================================
# ALGORITMO A*
# ==================================================
def busqueda_a_estrella(inicio, objetivo):
    print("\n" + "="*50)
    print("   INICIANDO BÚSQUEDA A*")
    print("="*50)
    print(f"Nodo Inicio: '{inicio}' | Nodo Objetivo: '{objetivo}'")
    print(f"Fórmula de evaluación: f(n) = g(n) + h(n)\n")

    # Cola de prioridad: (f(n), g(n), nodo_actual, ruta)
    frontera = []
    heapq.heappush(frontera, (heuristica[inicio], 0, inicio, [inicio]))
    visitados = {}  # Almacena el menor costo g(n) por nodo

    while frontera:
        f_actual, g_actual, nodo_actual, ruta = heapq.heappop(frontera)

        print(f"Explorando nodo: '{nodo_actual}'")
        print(f"  g(n) = {g_actual} | h(n) = {heuristica[nodo_actual]} | f(n) = {f_actual}")

        # Si llegamos al objetivo, mostramos la ruta
        if nodo_actual == objetivo:
            print(f"\n✔ Objetivo '{objetivo}' encontrado!")
            print(f"  Costo total: {g_actual}")
            print(f"  PARA LLEGAR AL OBJETIVO SE CRUZÓ: {' -> '.join(ruta)}\n")
            return ruta

        # Si ya visitamos con menor costo, saltamos
        if nodo_actual in visitados and visitados[nodo_actual] <= g_actual:
            print(f"  Nodo '{nodo_actual}' ya visitado con menor costo. Saltando...\n")
            continue

        visitados[nodo_actual] = g_actual  # Registrar costo mínimo

        # Expandir vecinos
        for vecino, costo in grafo_a_estrella.get(nodo_actual, []):
            g_nuevo = g_actual + costo
            f_nuevo = g_nuevo + heuristica[vecino]
            print(f"  Vecino '{vecino}': g={g_nuevo}, h={heuristica[vecino]}, f={f_nuevo}")
            heapq.heappush(frontera, (f_nuevo, g_nuevo, vecino, ruta + [vecino]))

        print()

    print(f"✘ No se encontró ruta hacia '{objetivo}'.")
    return None

# ==================================================
# ALGORITMO AO*
# ==================================================
def busqueda_ao_estrella(nodo, visitados=None):
    if visitados is None:
        visitados = {}

    # Si ya fue resuelto, retornar su costo
    if nodo in visitados:
        return visitados[nodo]

    print(f"\nExplorando nodo: '{nodo}' (Tipo: {grafo_ao_estrella[nodo]['tipo']})")

    hijos = grafo_ao_estrella[nodo]['hijos']
    tipo = grafo_ao_estrella[nodo]['tipo']

    # Si es un nodo hoja (sin hijos), retornar heurística
    if not hijos:
        print(f"  Nodo hoja '{nodo}' alcanzado. Costo heurístico: {heuristica_ao[nodo]}")
        visitados[nodo] = heuristica_ao[nodo]
        return heuristica_ao[nodo]

    costos = []

    for hijo, costo_arista in hijos:
        print(f"  Evaluando hijo '{hijo}' con costo de arista: {costo_arista}")
        costo_hijo = busqueda_ao_estrella(hijo, visitados)
        costo_total = costo_arista + costo_hijo
        costos.append((costo_total, hijo))
        print(f"  Costo total para '{hijo}': {costo_total}")

    # Nodo OR: elegir el hijo de menor costo
    if tipo == 'OR':
        mejor_costo, mejor_hijo = min(costos, key=lambda x: x[0])
        print(f"  Nodo OR '{nodo}': Mejor hijo '{mejor_hijo}' con costo {mejor_costo}")
        visitados[nodo] = mejor_costo
        return mejor_costo

    # Nodo AND: sumar todos los costos de los hijos
    if tipo == 'AND':
        costo_and = sum(c for c, _ in costos)
        print(f"  Nodo AND '{nodo}': Suma de costos de hijos = {costo_and}")
        visitados[nodo] = costo_and
        return costo_and

# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================
if __name__ == "__main__":
    
    # --- Ejecutar A* ---
    busqueda_a_estrella('A', 'G')

    # --- Ejecutar AO* ---
    print("\n" + "="*50)
    print("   INICIANDO BÚSQUEDA AO*")
    print("="*50)
    print("Nodo Inicio: 'A' | Nodo Objetivo: 'G'")
    print("Nodos OR: se resuelve el hijo de MENOR costo")
    print("Nodos AND: se deben resolver TODOS los hijos\n")
    
    visitados_ao = {}
    costo_final = busqueda_ao_estrella('A', visitados_ao)
    
    print("\n" + "="*50)
    print(f"✔ Costo óptimo encontrado por AO*: {costo_final}")
    print("Costos calculados por nodo:")
    for nodo, costo in visitados_ao.items():
        print(f"  Nodo '{nodo}': Costo = {costo}")
    print("="*50)
