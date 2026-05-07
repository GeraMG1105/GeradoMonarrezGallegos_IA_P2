"""
Búsqueda Tabú (Tabu Search)

Es un algoritmo de búsqueda local metaheurística desarrollado por
Fred Glover en 1986. Utiliza una lista tabú (memoria a corto plazo)
para almacenar movimientos recientes y evitar ciclos, permitiendo
escapar de máximos locales al aceptar temporalmente soluciones peores.

Componentes clave:
  - Lista Tabú: memoriza los últimos movimientos para evitar repetirlos.
  - Criterio de Aspiración: ignora la lista tabú si se encuentra una
    solución mejor que la mejor conocida hasta el momento.
  - Vecindario: conjunto de soluciones alcanzables desde el estado actual.
  - Mejor Solución Global: la mejor solución encontrada en toda la búsqueda.

Ventajas sobre Hill Climbing:
  - Puede escapar de máximos locales.
  - Evita ciclos mediante la lista tabú.
  - Explora más ampliamente el espacio de búsqueda.
"""

# ==================================================
# Definición del grafo con costos
# Cada nodo tiene una lista de tuplas (vecino, costo)
# ==================================================
grafo = {
    'A': [('B', 2), ('C', 5)],       # A se conecta a B(costo 2) y C(costo 5)
    'B': [('A', 2), ('D', 3), ('E', 4)],  # B se conecta a A, D y E
    'C': [('A', 5), ('F', 2), ('G', 6)],  # C se conecta a A, F y G
    'D': [('B', 3), ('H', 1)],            # D se conecta a B y H
    'E': [('B', 4), ('H', 3), ('I', 2)],  # E se conecta a B, H e I
    'F': [('C', 2), ('I', 4), ('J', 3)],  # F se conecta a C, I y J
    'G': [('C', 6), ('J', 2)],            # G se conecta a C y J
    'H': [('D', 1), ('E', 3), ('K', 2)],  # H se conecta a D, E y K
    'I': [('E', 2), ('F', 4), ('K', 1)],  # I se conecta a E, F y K
    'J': [('F', 3), ('G', 2), ('K', 3)],  # J se conecta a F, G y K
    'K': []                               # K es el nodo objetivo
}

# ==================================================
# Heurística: estimación del costo al objetivo 'K'
# Mientras MENOR sea el valor, más cerca del objetivo
# ==================================================
heuristica = {
    'A': 8,   # Muy lejos del objetivo
    'B': 6,   # Lejos del objetivo
    'C': 7,   # Lejos del objetivo
    'D': 4,   # Distancia media
    'E': 3,   # Distancia media-baja
    'F': 4,   # Distancia media
    'G': 5,   # Distancia media-alta
    'H': 2,   # Cerca del objetivo
    'I': 1,   # Muy cerca del objetivo
    'J': 3,   # Distancia media-baja
    'K': 0    # Es el objetivo
}

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Función para obtener el valor heurístico de un nodo
def obtener_heuristica(nodo):
    return heuristica.get(nodo, float('inf'))

# ==================================================
# ALGORITMO DE BÚSQUEDA TABÚ
# ==================================================
def busqueda_tabu(inicio, objetivo, tam_lista_tabu=3, max_iteraciones=20):
    print("\n" + "="*55)
    print("         INICIANDO BÚSQUEDA TABÚ")
    print("="*55)
    print(f"Nodo Inicio       : '{inicio}'")
    print(f"Nodo Objetivo     : '{objetivo}'")
    print(f"Tamaño Lista Tabú : {tam_lista_tabu}")
    print(f"Máx. Iteraciones  : {max_iteraciones}")
    print("="*55 + "\n")

    nodo_actual       = inicio          # Estado actual
    mejor_nodo        = inicio          # Mejor solución global encontrada
    mejor_h           = obtener_heuristica(inicio)  # Mejor heurística global
    lista_tabu        = []              # Lista tabú (memoria a corto plazo)
    ruta              = [inicio]        # Ruta recorrida
    iteracion         = 0              # Contador de iteraciones

    while nodo_actual != objetivo and iteracion < max_iteraciones:
        iteracion += 1
        print(f"Iteración {iteracion}:")
        print(f"  Nodo actual  : '{nodo_actual}' | h(n) = {obtener_heuristica(nodo_actual)}")
        print(f"  Lista Tabú   : {lista_tabu}")

        vecinos = obtener_vecinos(nodo_actual)

        if not vecinos:
            print(f"  ✘ Sin vecinos disponibles. Búsqueda detenida.\n")
            break

        # Evaluar todos los vecinos disponibles
        print(f"  Evaluando vecinos:")
        mejor_candidato   = None
        mejor_h_candidato = float('inf')

        for vecino, costo in vecinos:
            h_vecino = obtener_heuristica(vecino)
            es_tabu  = vecino in lista_tabu

            # Criterio de Aspiración: ignorar tabú si es mejor que la mejor solución global
            criterio_aspiracion = h_vecino < mejor_h

            print(f"    Vecino '{vecino}': h(n)={h_vecino}, costo={costo}, "
                  f"Tabú={'Sí' if es_tabu else 'No'}, "
                  f"Aspiración={'Sí' if criterio_aspiracion else 'No'}")

            # Aceptar el vecino si no es tabú O si cumple criterio de aspiración
            if (not es_tabu or criterio_aspiracion) and h_vecino < mejor_h_candidato:
                mejor_h_candidato = h_vecino
                mejor_candidato   = vecino

        # Si no hay candidato válido, detener la búsqueda
        if mejor_candidato is None:
            print(f"  ✘ No hay candidatos válidos. Búsqueda detenida.\n")
            break

        # Actualizar la lista tabú
        lista_tabu.append(nodo_actual)
        if len(lista_tabu) > tam_lista_tabu:
            eliminado = lista_tabu.pop(0)  # Eliminar el movimiento más antiguo
            print(f"  Lista Tabú llena. Eliminando nodo más antiguo: '{eliminado}'")

        # Moverse al mejor candidato
        nodo_actual = mejor_candidato
        ruta.append(nodo_actual)
        print(f"  ✔ Moviéndose a '{nodo_actual}' con h(n) = {mejor_h_candidato}\n")

        # Actualizar la mejor solución global
        if mejor_h_candidato < mejor_h:
            mejor_h    = mejor_h_candidato
            mejor_nodo = nodo_actual
            print(f"  ★ Nueva mejor solución global: '{mejor_nodo}' con h(n) = {mejor_h}\n")

    # Resultado final
    print("="*55)
    if nodo_actual == objetivo:
        print(f"✔ Objetivo '{objetivo}' encontrado en {iteracion} iteraciones!")
    else:
        print(f"✘ Objetivo '{objetivo}' no alcanzado en {max_iteraciones} iteraciones.")
        print(f"  Mejor nodo alcanzado: '{mejor_nodo}' con h(n) = {mejor_h}")

    print(f"  RUTA RECORRIDA: {' -> '.join(ruta)}")
    print("="*55)
    return ruta

# ==================================================
# EJECUCIÓN PRINCIPAL
# ==================================================
if __name__ == "__main__":
    busqueda_tabu(
        inicio          = 'A',
        objetivo        = 'K',
        tam_lista_tabu  = 3,
        max_iteraciones = 20
    )
