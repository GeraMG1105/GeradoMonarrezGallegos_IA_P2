"""
Búsqueda Bidireccional

La búsqueda bidireccional es un algoritmo eficiente de búsqueda no informada que intenta encontrar la solución iniciando simultáneamente desde dos extremos: el nodo inicial y el nodo objetivo. Este enfoque busca reducir el espacio de búsqueda al explorar juntos desde ambas direcciones, lo que puede llevar a un encuentro más rápido en comparación con la búsqueda unidireccional.

### Funcionamiento del Algoritmo:
1. **Inicialización**: Se crean dos fronteras, una comenzando en el nodo inicial y otra comenzando en el nodo objetivo. También se inicializan conjuntos de nodos visitados para ambas direcciones.
   
2. **Expansión**: El algoritmo alterna entre expandir nodos desde el inicio y el objetivo. En cada iteración, se exploran todos los nodos en la frontera actual para ver si alguno de ellos se ha encontrado en la frontera opuesta.

3. **Intersección**: Si durante la exploración se encuentra un nodo que ha sido visitado desde ambas direcciones, se indica que se ha encontrado un camino entre los nodos inicial y objetivo.

4. **Finalización**: El algoritmo termina si encuentra un camino que conecta ambos nodos o si no quedan más nodos por explorar en ambas fronteras.

### Implementación:
El siguiente código implementa la búsqueda bidireccional utilizando un grafo simplificado. Este grafo contiene nodos y conexiones que permiten al algoritmo demostrar su capacidad para encontrar un camino entre dos nodos específicos.

"""


from collections import deque

# Definición del grafo simplificado
grafo = {
    'A': ['B', 'C'],  # Nodo A se conecta a B y C
    'B': ['D', 'E'],  # Nodo B se conecta a D y E
    'C': ['F'],       # Nodo C se conecta a F
    'D': ['G'],       # Nodo D se conecta a G
    'E': ['H'],       # Nodo E se conecta a H
    'F': ['I'],       # Nodo F se conecta a I
    'G': ['J'],       # Nodo G se conecta a J
    'H': ['K'],       # Nodo H se conecta a K
    'I': ['L'],       # Nodo I se conecta a L
    'K': ['M'],       # Nodo K se conecta a M
}

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Implementación de la búsqueda bidireccional
def busqueda_bidireccional(inicio, objetivo):
    if inicio == objetivo:
        print(f"El nodo objetivo es el mismo que el nodo inicial: '{inicio}'.")
        return True

    frontera_inicio = deque([inicio])  # Cola para la búsqueda desde el inicio
    frontera_objetivo = deque([objetivo])  # Cola para la búsqueda desde el objetivo
    visitados_inicio = {inicio}  # Conjunto de nodos visitados desde el inicio
    visitados_objetivo = {objetivo}  # Conjunto de nodos visitados desde el objetivo

    print(f"Comenzando la búsqueda bidireccional desde '{inicio}' hacia '{objetivo}'.")

    while frontera_inicio and frontera_objetivo:
        # Expandir desde el inicio
        for _ in range(len(frontera_inicio)):
            nodo_actual = frontera_inicio.popleft()
            print(f"Explorando desde el inicio: {nodo_actual}")
            if nodo_actual in visitados_objetivo:  # Verificar intersección
                print(f"Ruta encontrada: {nodo_actual} (cruce entre inicio y objetivo)")
                return True
            for vecino in obtener_vecinos(nodo_actual):
                if vecino not in visitados_inicio:
                    visitados_inicio.add(vecino)
                    frontera_inicio.append(vecino)
                    print(f"Agregando '{vecino}' a la frontera desde inicio.")

        # Expandir desde el objetivo
        for _ in range(len(frontera_objetivo)):
            nodo_actual = frontera_objetivo.popleft()
            print(f"Explorando desde el objetivo: {nodo_actual}")
            if nodo_actual in visitados_inicio:  # Verificar intersección
                print(f"Ruta encontrada: {nodo_actual} (cruce entre objetivo y inicio)")
                return True
            for vecino in obtener_vecinos(nodo_actual):
                if vecino not in visitados_objetivo:
                    visitados_objetivo.add(vecino)
                    frontera_objetivo.append(vecino)
                    print(f"Agregando '{vecino}' a la frontera desde objetivo.")

    print(f"No se encontró ruta entre '{inicio}' y '{objetivo}'.")
    return False  # Si no se encuentra ruta

# Código para probar la búsqueda bidireccional
if __name__ == "__main__":
    objetivo = 'D'  # Nodo objetivo para la búsqueda
    busqueda_bidireccional('A', objetivo)
