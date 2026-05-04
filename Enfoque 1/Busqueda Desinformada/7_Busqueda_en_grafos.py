#La búsqueda en grafos se refiere a las técnicas que se utilizan para explorar o encontrar una solución en una estructura de datos
#  representada como un grafo. Un grafo es una colección de nodos (o vértices) conectados por aristas (o enlaces). Los nodos pueden 
# representar cualquier entidad (como ciudades, personas, o recursos), y las aristas representan la conexión o relación entre estas 
# entidades.

from collections import deque

# Definición del grafo
grafo = {
    'A': ['B', 'C'],  # Nodo A se conecta a B y C
    'B': ['D', 'E'],  # Nodo B se conecta a D y E
    'C': ['F'],       # Nodo C se conecta a F
    'D': ['G'],       # Nodo D se conecta a G
    'E': ['H'],       # Nodo E se conecta a H
    'F': ['I'],       # Nodo F se conecta a I
    'G': [],          # Nodo G no tiene vecinos
    'H': [],          # Nodo H no tiene vecinos
    'I': []           # Nodo I no tiene vecinos
}

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])

# Implementación de la Búsqueda en Anchura (BFS)
def busqueda_en_anchura(inicio, objetivo):
    frontera = deque([inicio])  # Cola para los nodos a explorar
    visitados = {inicio}         # Conjunto para nodos visitados

    print(f"Comenzando la Búsqueda en Anchura desde '{inicio}' hacia '{objetivo}'.")

    while frontera:
        nodo_actual = frontera.popleft()  # Extraer el nodo del frente de la cola
        print(f"Explorando el nodo: {nodo_actual}")
        
        if nodo_actual == objetivo:  # Comprobar si es el nodo objetivo
            print(f"Nodo objetivo '{objetivo}' encontrado.")
            return True
        
        # Explorar vecinos del nodo actual
        for vecino in obtener_vecinos(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)  # Marcar como visitado
                frontera.append(vecino)  # Agregar vecino a la cola
                print(f"Agregando '{vecino}' a la frontera.")
    
    print(f"No se encontró el nodo objetivo '{objetivo}'.")
    return False  # Si se sale del bucle, no se encontró el objetivo

# Implementación de la Búsqueda en Profundidad (DFS)
def busqueda_en_profundidad(nodo_actual, objetivo, visitados=set()):
    print(f"Explorando el nodo: {nodo_actual} en Búsqueda en Profundidad")
    
    if nodo_actual == objetivo:
        print(f"Nodo objetivo '{objetivo}' encontrado.")
        return True

    visitados.add(nodo_actual)  # Marca el nodo como visitado
    
    for vecino in obtener_vecinos(nodo_actual):
        if vecino not in visitados:
            if busqueda_en_profundidad(vecino, objetivo, visitados):
                return True
            
    return False  # Si no se encuentra el objetivo

# Código para probar ambas búsquedas
if __name__ == "__main__":
    objetivo = 'I'  # Puedes cambiar el objetivo a cualquier nodo en la base de datos
    print("Ejecutando Búsqueda en Anchura...")
    busqueda_en_anchura('A', objetivo)
    
    print("\nEjecutando Búsqueda en Profundidad...")
    busqueda_en_profundidad('A', objetivo)
