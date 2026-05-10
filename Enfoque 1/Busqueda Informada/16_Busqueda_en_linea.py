"""
Busqueda Online (Online Search)

A diferencia de los algoritmos offline, el agente no conoce
el grafo completo de antemano. Descubre nodos y conexiones
conforme los visita, actuando y explorando al mismo tiempo.

Algoritmos implementados:
  1. DFS Online: explora en profundidad sin mapa previo,
     con capacidad de backtracking cuando no hay salida.
  2. LRTA* (Learning Real-Time A*): aprende y actualiza
     heuristicas mientras explora el entorno desconocido.

Diferencia clave con busqueda offline:
  - Offline: planifica toda la ruta antes de moverse.
  - Online: descubre el grafo mientras actua en el.

Aplicaciones reales:
  - Robots navegando en espacios desconocidos.
  - Agentes en videojuegos con mapas ocultos.
  - Sistemas de navegacion en tiempo real.
"""

import random

# ==================================================
# Grafo OCULTO para el agente
# El agente NO conoce esta estructura al inicio.
# La va descubriendo nodo por nodo al visitarlos.
# ==================================================
grafo_oculto = {
    'A': [('B', 2), ('C', 4)],
    'B': [('A', 2), ('D', 3), ('E', 5)],
    'C': [('A', 4), ('E', 2), ('F', 6)],
    'D': [('B', 3), ('G', 4)],
    'E': [('B', 5), ('C', 2), ('G', 3), ('H', 4)],
    'F': [('C', 6), ('H', 1)],
    'G': [('D', 4), ('E', 3), ('I', 2)],
    'H': [('E', 4), ('F', 1), ('I', 2)],
    'I': []  # Nodo objetivo
}

# ==================================================
# Heuristica OCULTA
# El agente tampoco conoce estos valores al inicio.
# En LRTA* los va aprendiendo y actualizando.
# ==================================================
heuristica_oculta = {
    'A': 8,
    'B': 6,
    'C': 6,
    'D': 4,
    'E': 3,
    'F': 4,
    'G': 2,
    'H': 2,
    'I': 0
}

INICIO   = 'A'
OBJETIVO = 'I'

# ==================================================
# Simulador del entorno
# Representa lo que el agente puede "percibir"
# al llegar a un nodo: sus vecinos y costos.
# ==================================================
class EntornoDesconocido:
    def __init__(self, grafo, heuristica):
        self.grafo      = grafo
        self.heuristica = heuristica

    # El agente percibe los vecinos al llegar al nodo
    def percibir_vecinos(self, nodo):
        return self.grafo.get(nodo, [])

    # El agente percibe la heuristica inicial del nodo
    def percibir_heuristica(self, nodo):
        return self.heuristica.get(nodo, float('inf'))

    # Verificar si el nodo es el objetivo
    def es_objetivo(self, nodo):
        return nodo == OBJETIVO


# ==================================================
# ALGORITMO 1: DFS Online
# Explora en profundidad sin conocer el grafo.
# Usa backtracking cuando no hay vecinos nuevos.
# ==================================================
def dfs_online(entorno, inicio, objetivo, max_pasos=50):
    print("\n" + "="*55)
    print("            DFS ONLINE")
    print("="*55)
    print(f"Nodo Inicio   : '{inicio}'")
    print(f"Nodo Objetivo : '{objetivo}'")
    print("="*55 + "\n")

    nodo_actual  = inicio
    visitados    = set()          # Nodos ya explorados
    pila_retorno = []             # Pila para backtracking
    ruta         = [inicio]       # Ruta recorrida
    pasos        = 0
    # Mapa aprendido: vecinos descubiertos por nodo
    mapa_aprendido = {}

    while pasos < max_pasos:
        pasos += 1
        print(f"Paso {pasos} | Nodo actual: '{nodo_actual}'")

        # Marcar como visitado
        visitados.add(nodo_actual)

        # Verificar si es el objetivo
        if entorno.es_objetivo(nodo_actual):
            print(f"\n  Objetivo '{objetivo}' encontrado!")
            print(f"  Ruta recorrida : {' -> '.join(ruta)}")
            print(f"  Pasos totales  : {pasos}\n")
            return ruta

        # Percibir vecinos del nodo actual (descubrimiento)
        vecinos_percibidos = entorno.percibir_vecinos(nodo_actual)
        mapa_aprendido[nodo_actual] = vecinos_percibidos

        print(f"  Vecinos descubiertos : {[v for v, _ in vecinos_percibidos]}")

        # Filtrar vecinos no visitados
        vecinos_nuevos = [v for v, _ in vecinos_percibidos
                         if v not in visitados]

        print(f"  Vecinos no visitados : {vecinos_nuevos}")

        if vecinos_nuevos:
            # Moverse al primer vecino no visitado
            siguiente = vecinos_nuevos[0]
            pila_retorno.append(nodo_actual)  # Guardar para backtracking
            nodo_actual = siguiente
            ruta.append(nodo_actual)
            print(f"  Movimiento : avanzar a '{nodo_actual}'\n")
        elif pila_retorno:
            # Backtracking: regresar al nodo anterior
            nodo_actual = pila_retorno.pop()
            ruta.append(nodo_actual)
            print(f"  Movimiento : backtrack a '{nodo_actual}'\n")
        else:
            # Sin opciones ni retorno posible
            print(f"  Sin opciones disponibles. Deteniendo busqueda.\n")
            break

    print("="*55)
    print(f"Objetivo '{objetivo}' no alcanzado en {max_pasos} pasos.")
    print(f"Mapa aprendido : {list(mapa_aprendido.keys())}")
    print("="*55)
    return ruta


# ==================================================
# ALGORITMO 2: LRTA* (Learning Real-Time A*)
# Aprende y actualiza heuristicas mientras explora.
# En cada paso elige el vecino con menor f(n) = c + h
# y actualiza la heuristica del nodo actual.
# ==================================================
def lrta_estrella(entorno, inicio, objetivo, max_pasos=50):
    print("\n" + "="*55)
    print("     LRTA* (Learning Real-Time A*)")
    print("="*55)
    print(f"Nodo Inicio   : '{inicio}'")
    print(f"Nodo Objetivo : '{objetivo}'")
    print("="*55 + "\n")

    nodo_actual      = inicio
    # Tabla de heuristicas aprendidas (se actualiza durante la busqueda)
    heuristicas_aprendidas = {}
    ruta             = [inicio]
    pasos            = 0

    while pasos < max_pasos:
        pasos += 1
        print(f"Paso {pasos} | Nodo actual: '{nodo_actual}'")

        # Verificar si es el objetivo
        if entorno.es_objetivo(nodo_actual):
            print(f"\n  Objetivo '{objetivo}' encontrado!")
            print(f"  Ruta recorrida     : {' -> '.join(ruta)}")
            print(f"  Pasos totales      : {pasos}")
            print(f"  Heuristicas aprendidas: {heuristicas_aprendidas}\n")
            return ruta

        # Percibir vecinos del nodo actual
        vecinos = entorno.percibir_vecinos(nodo_actual)

        if not vecinos:
            print(f"  Sin vecinos. Deteniendo busqueda.\n")
            break

        # Inicializar heuristica del nodo si no la conoce aun
        if nodo_actual not in heuristicas_aprendidas:
            heuristicas_aprendidas[nodo_actual] = entorno.percibir_heuristica(nodo_actual)

        print(f"  h aprendida actual : {heuristicas_aprendidas[nodo_actual]}")
        print(f"  Vecinos percibidos : {[v for v, _ in vecinos]}")

        # Calcular f(n) = costo_arista + h(vecino) para cada vecino
        evaluaciones = []
        for vecino, costo in vecinos:
            if vecino not in heuristicas_aprendidas:
                heuristicas_aprendidas[vecino] = entorno.percibir_heuristica(vecino)
            f = costo + heuristicas_aprendidas[vecino]
            evaluaciones.append((vecino, costo, f))
            print(f"    '{vecino}' : c={costo} + h={heuristicas_aprendidas[vecino]} = f={f}")

        # Elegir el vecino con menor f(n)
        mejor_vecino, mejor_costo, mejor_f = min(evaluaciones, key=lambda x: x[2])

        # Actualizar heuristica del nodo actual (regla de aprendizaje LRTA*)
        # h(actual) = max(h(actual), mejor_f)
        h_anterior = heuristicas_aprendidas[nodo_actual]
        heuristicas_aprendidas[nodo_actual] = max(h_anterior, mejor_f)

        print(f"  Actualizacion h('{nodo_actual}') : {h_anterior} -> {heuristicas_aprendidas[nodo_actual]}")
        print(f"  Movimiento : avanzar a '{mejor_vecino}'\n")

        # Moverse al mejor vecino
        nodo_actual = mejor_vecino
        ruta.append(nodo_actual)

    print("="*55)
    print(f"Objetivo '{objetivo}' no alcanzado en {max_pasos} pasos.")
    print(f"Heuristicas aprendidas : {heuristicas_aprendidas}")
    print("="*55)
    return ruta


# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":

    # Crear el entorno desconocido para el agente
    entorno = EntornoDesconocido(grafo_oculto, heuristica_oculta)

    # Ejecutar DFS Online
    dfs_online(
        entorno   = entorno,
        inicio    = INICIO,
        objetivo  = OBJETIVO,
        max_pasos = 50
    )

    # Ejecutar LRTA*
    lrta_estrella(
        entorno   = entorno,
        inicio    = INICIO,
        objetivo  = OBJETIVO,
        max_pasos = 50
    )
