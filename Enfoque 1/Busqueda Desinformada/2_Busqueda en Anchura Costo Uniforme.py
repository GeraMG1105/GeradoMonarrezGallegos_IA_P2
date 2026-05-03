import heapq

# Función para obtener los vecinos y sus costos
def obtener_vecinos_y_costos(nodo):
    # Definimos un grafo con costos, usando un diccionario anidado
    grafo_costos = {
        'A': {'B': 1, 'C': 4},  # Nodo A se conecta a B con costo 1 y a C con costo 4
        'B': {'D': 2, 'E': 5},  # Nodo B se conecta a D con costo 2 y a E con costo 5
        'C': {'F': 1},           # Nodo C se conecta a F con costo 1
        'D': {},                 # Nodo D no tiene vecinos
        'E': {'F': 2},           # Nodo E se conecta a F con costo 2
        'F': {}                  # Nodo F no tiene vecinos
    }
    # Devuelve una lista de tuplas (vecino, costo)
    return [(vecino, costo) for vecino, costo in grafo_costos.get(nodo, {}).items()]

# Implementación de la búsqueda en anchura de costo uniforme
def busqueda_costo_uniforme(inicio, objetivo):
    frontera = []  # Cola de prioridad para nodos a explorar
    heapq.heappush(frontera, (0, inicio, [inicio]))  # (costo acumulado, nodo, ruta)
    visitados = {}  # Diccionario para almacenar costos mínimos a cada nodo
    
    print(f"Comenzando la búsqueda en costo uniforme desde el nodo '{inicio}' hacia '{objetivo}'.")
    
    while frontera:  # Mientras haya nodos en la frontera
        costo_actual, nodo_actual, ruta_actual = heapq.heappop(frontera)  # Extraer el nodo con el costo más bajo
        print(f"Explorando el nodo: {nodo_actual} con costo acumulado: {costo_actual}")
        
        if nodo_actual == objetivo:  # Comprobar si es el nodo objetivo
            print(f"Nodo objetivo '{objetivo}' encontrado con un costo total de {costo_actual}.")
            print(f"Para llegar al objetivo se cruzó la ruta: {' -> '.join(ruta_actual)}")  # Ruta encontrada
            return True  # Se encontró el objetivo
        
        # Si el nodo no ha sido visitado o se encontró un costo menor
        if nodo_actual not in visitados or costo_actual < visitados[nodo_actual]:
            visitados[nodo_actual] = costo_actual  # Actualiza el costo mínimo
            # Añadir los vecinos a la cola de prioridad
            for vecino, costo in obtener_vecinos_y_costos(nodo_actual):
                nuevo_costo = costo_actual + costo  # Costo acumulado para el vecino
                print(f"Agregando el vecino '{vecino}' con costo acumulado: {nuevo_costo} a la frontera.")
                heapq.heappush(frontera, (nuevo_costo, vecino, ruta_actual + [vecino]))  # Agregar vecino con costo actualizado y nueva ruta
    
    print(f"No se encontró el nodo objetivo '{objetivo}'.")
    return False  # Si se sale del bucle, no se encontró el objetivo

# Código para probar la búsqueda de costo uniforme
if __name__ == "__main__":
    busqueda_costo_uniforme('A', 'F')  # Resultado esperado: True
