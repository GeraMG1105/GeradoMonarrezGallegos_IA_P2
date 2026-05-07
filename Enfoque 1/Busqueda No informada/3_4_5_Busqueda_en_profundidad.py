# Definimos un grafo más complejo como un diccionario
grafo = {
    'A': ['B', 'C'],  # Nodo A se conecta a B y C
    'B': ['D', 'E'],  # Nodo B se conecta a D y E
    'C': ['F', 'G'],  # Nodo C se conecta a F y G
    'D': ['H'],       # Nodo D se conecta a H
    'E': ['I', 'J'],  # Nodo E se conecta a I y J
    'F': ['K'],       # Nodo F se conecta a K
    'G': ['L'],       # Nodo G se conecta a L
    'H': ['M'],       # Nodo H se conecta a M
    'I': ['N'],       # Nodo I se conecta a N
    'J': ['O'],       # Nodo J se conecta a O
    'K': ['P'],       # Nodo K se conecta a P
    'L': ['Q', 'R'],  # Nodo L se conecta a Q y R
    'M': [],          # Nodo M no tiene vecinos
    'N': [],          # Nodo N no tiene vecinos
    'O': [],          # Nodo O no tiene vecinos
    'P': [],          # Nodo P no tiene vecinos
    'Q': [],          # Nodo Q no tiene vecinos
    'R': []           # Nodo R no tiene vecinos
}

# Función para obtener los vecinos de cada nodo
def obtener_vecinos(nodo):
    return grafo.get(nodo, [])  # Devuelve la lista de vecinos o vacío si el nodo no existe

# 1. Búsqueda en Profundidad
def busqueda_en_profundidad(nodo_actual, objetivo, visitados=set()):
    print(f"Explorando el nodo: {nodo_actual} en Búsqueda en Profundidad")
    if nodo_actual == objetivo:
        print(f"Nodo objetivo '{objetivo}' encontrado en Búsqueda en Profundidad.")
        return True
    visitados.add(nodo_actual)  # Marca el nodo como visitado
    for vecino in obtener_vecinos(nodo_actual):
        if vecino not in visitados:
            if busqueda_en_profundidad(vecino, objetivo, visitados):
                return True
    return False

# 2. Búsqueda en Profundidad Limitada
def busqueda_en_profundidad_limitada(nodo_actual, objetivo, profundidad_maxima, profundidad=0):
    print(f"Explorando el nodo: {nodo_actual} con profundidad {profundidad} en Búsqueda en Profundidad Limitada")
    if profundidad > profundidad_maxima:
        print(f"Alcanzada profundidad máxima en nodo '{nodo_actual}'.")
        return False  # Excede la profundidad máxima
    if nodo_actual == objetivo:
        print(f"Nodo objetivo '{objetivo}' encontrado en Búsqueda en Profundidad Limitada.")
        return True
    for vecino in obtener_vecinos(nodo_actual):
        if busqueda_en_profundidad_limitada(vecino, objetivo, profundidad_maxima, profundidad + 1):
            return True
    return False

# 3. Búsqueda en Profundidad Iterativa
def busqueda_en_profundidad_iterativa(inicio, objetivo):
    profundidad = 0
    while True:
        print(f"Iniciando búsqueda en profundidad iterativa con profundidad máxima: {profundidad}")
        if busqueda_en_profundidad_limitada(inicio, objetivo, profundidad):
            return True  # Se encontró el objetivo
        profundidad += 1  # Aumentar la profundidad para la siguiente iteración

# Código para probar las búsquedas
if __name__ == "__main__":
    objetivo = 'M'  # Puedes cambiar el objetivo a cualquier nodo en la base de datos
    print("Ejecutando Búsqueda en Profundidad...")
    busqueda_en_profundidad('A', objetivo)
    
    print("\nEjecutando Búsqueda en Profundidad Limitada (profundidad máxima = 3)...")
    busqueda_en_profundidad_limitada('A', objetivo, 3)
    
    print("\nEjecutando Búsqueda en Profundidad Iterativa...")
    busqueda_en_profundidad_iterativa('A', objetivo)
