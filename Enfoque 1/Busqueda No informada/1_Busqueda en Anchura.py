from collections import deque

# La búsqueda en anchura es un algoritmo de búsqueda no informada que explora todos los nodos a un nivel de profundidad antes de avanzar 
# al siguiente nivel. Utiliza una estructura de datos tipo cola (FIFO) para realizar la exploración. Debido a su enfoque sistemático,
#  es especialmente útil para encontrar la ruta más corta en un grafo no ponderado, donde todos los nodos son igualmente accesibles.

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    # Definimos un grafo sencillamente como un diccionario
    grafo = {
        'A': ['B', 'C'],  # Nodo A se conecta con B y C
        'B': ['D', 'E'],  # Nodo B se conecta con D y E
        'C': ['F'],       # Nodo C se conecta con F
        'D': [],          # Nodo D no tiene vecinos
        'E': ['F'],       # Nodo E se conecta con F
        'F': []           # Nodo F no tiene vecinos
    }
    return grafo.get(nodo, [])  # Devuelve la lista de vecinos o vacío si el nodo no existe

# Implementación de la búsqueda en anchura
def busqueda_en_anchura(inicio, objetivo):
    frontera = deque([inicio])  # Cola para los nodos a explorar
    visitados = set()            # Conjunto para almacenar nodos visitados
    
    print(f"Comenzando la búsqueda en anchura desde el nodo '{inicio}' hacia '{objetivo}'.")
    
    while frontera:  # Mientras haya nodos en la frontera
        nodo_actual = frontera.popleft()  # Extraer el nodo del frente de la cola
        print(f"Explorando el nodo: {nodo_actual}")
        
        if nodo_actual == objetivo:  # Comprobar si es el nodo objetivo
            print(f"Nodo objetivo '{objetivo}' encontrado.")
            return True               # Se encontró el objetivo
        
        visitados.add(nodo_actual)   # Marcar el nodo como visitado
        # Explorar vecinos del nodo actual
        for vecino in obtener_vecinos(nodo_actual):
            # Agregar vecino a la cola si no ha sido visitado
            if vecino not in visitados and vecino not in frontera:
                print(f"Agregando el vecino '{vecino}' a la frontera.")
                frontera.append(vecino)
    
    print(f"No se encontró el nodo objetivo '{objetivo}'.")
    return False  # Si se sale del bucle, no se encontró el objetivo

# Código para probar la búsqueda
if __name__ == "__main__":
    busqueda_en_anchura('A', 'F')  # Resultado esperado: True
