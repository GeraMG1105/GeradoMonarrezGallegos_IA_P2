
graph = {
    """
    Este módulo implementa una búsqueda informada utilizando el algoritmo Greedy Best-First Search.

    Las heurísticas en la búsqueda informada son funciones de estimación que guían el algoritmo hacia el objetivo
    sin explorar todas las posibilidades, reduciendo el espacio de búsqueda. En este caso, la heurística estima la
    distancia restante hasta el nodo objetivo 'G', proporcionando una aproximación de costo para priorizar nodos
    prometedores.

    En el código, la heurística se representa como un diccionario 'heuristic' donde cada clave es un nodo y su valor
    es la estimación heurística (por ejemplo, "A": 5 indica que desde A se estima un costo de 5 para llegar a G).
    Esta heurística se utiliza en la función greedy_best_first para ordenar la frontera (frontier) por el valor
    heurístico más bajo, asegurando que se explore primero el nodo con la mejor estimación.
    """
    "A": [("B", 1), ("C", 4)],
    "B": [("D", 2), ("E", 5)],
    "C": [("E", 1)],
    "D": [("G", 5)],
    "E": [("G", 2)],
    "G": []
}

# Heurística simple: estima la distancia restante hasta el objetivo G
heuristic = {
    "A": 5,
    "B": 3,
    "C": 2,
    "D": 2,
    "E": 1,
    "G": 0
}

def greedy_best_first(start, goal):
    frontier = [(heuristic[start], start, [start])]
    visited = set()

    while frontier:
        _, node, path = frontier.pop(0)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                frontier.append((heuristic[neighbor], neighbor, path + [neighbor]))
        frontier.sort(key=lambda item: item[0])

    return None

if __name__ == "__main__":
    resultado = greedy_best_first("A", "G")
    print("Camino encontrado:", resultado)
    print("La heurística guía la búsqueda hacia el objetivo usando estimaciones simples.")