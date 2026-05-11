"""
Busqueda Local: Minimos-Conflictos (Min-Conflicts)

Algoritmo de busqueda local para resolver CSPs propuesto por
Steven Minton en 1992. A diferencia del backtracking, parte de
una asignacion completa (posiblemente invalida) y la repara
iterativamente eligiendo el valor que minimiza conflictos.

Componentes:
  - Asignacion inicial: valores aleatorios para todas las variables.
  - Seleccion: elegir una variable en conflicto aleatoriamente.
  - Reparacion: asignar el valor que minimiza conflictos.
  - Condicion de parada: sin conflictos o maximo de iteraciones.

Problemas implementados:
  1. Coloreo de Mapa de Australia.
  2. N-Reinas: problema clasico de colocacion de reinas.
"""

import random

# ==================================================
# CLASE BASE: CSP con Minimos-Conflictos
# ==================================================
class CSPMinConflictos:
    def __init__(self, variables, dominios, restricciones):
        """
        variables     : lista de variables del problema.
        dominios      : diccionario {variable: [valores posibles]}.
        restricciones : diccionario {(var1, var2): funcion_restriccion}.
        """
        self.variables     = variables
        self.dominios      = dominios
        self.restricciones = restricciones

    # ==================================================
    # Contar cuantos conflictos genera una asignacion
    # de 'valor' a 'variable' dado el estado actual
    # ==================================================
    def contar_conflictos(self, variable, valor, asignacion):
        conflictos = 0
        for (var1, var2), restriccion in self.restricciones.items():
            if var1 == variable and var2 in asignacion:
                if not restriccion(valor, asignacion[var2]):
                    conflictos += 1
            if var2 == variable and var1 in asignacion:
                if not restriccion(asignacion[var1], valor):
                    conflictos += 1
        return conflictos

    # ==================================================
    # Obtener todas las variables que tienen conflictos
    # en la asignacion actual
    # ==================================================
    def variables_en_conflicto(self, asignacion):
        en_conflicto = []
        for variable in self.variables:
            if variable in asignacion:
                valor = asignacion[variable]
                if self.contar_conflictos(variable, valor, asignacion) > 0:
                    en_conflicto.append(variable)
        return en_conflicto

    # ==================================================
    # ALGORITMO PRINCIPAL: Minimos-Conflictos
    # ==================================================
    def min_conflictos(self, max_iteraciones=1000):
        print("\n" + "="*55)
        print("     ALGORITMO: MINIMOS-CONFLICTOS")
        print("="*55)
        print(f"Variables        : {self.variables}")
        print(f"Max Iteraciones  : {max_iteraciones}")
        print("="*55 + "\n")

        # PASO 1: Asignacion inicial aleatoria completa
        asignacion = {}
        for variable in self.variables:
            asignacion[variable] = random.choice(self.dominios[variable])

        print(f"Asignacion inicial:")
        for var, val in asignacion.items():
            conflictos = self.contar_conflictos(var, val, asignacion)
            print(f"  {var:5} = {val:8} | conflictos: {conflictos}")
        print()

        # PASO 2: Reparar conflictos iterativamente
        for iteracion in range(1, max_iteraciones + 1):

            # Obtener variables en conflicto
            en_conflicto = self.variables_en_conflicto(asignacion)

            # Si no hay conflictos, solucion encontrada
            if not en_conflicto:
                print(f"Solucion encontrada en iteracion {iteracion - 1}!\n")
                return asignacion

            # Elegir una variable en conflicto aleatoriamente
            variable = random.choice(en_conflicto)

            # Calcular conflictos para cada valor del dominio
            conflictos_por_valor = {}
            for valor in self.dominios[variable]:
                conflictos_por_valor[valor] = self.contar_conflictos(
                    variable, valor, asignacion
                )

            # Elegir el valor con menor numero de conflictos
            min_conflictos = min(conflictos_por_valor.values())
            mejores_valores = [
                v for v, c in conflictos_por_valor.items()
                if c == min_conflictos
            ]
            nuevo_valor = random.choice(mejores_valores)

            # Mostrar progreso cada 10 iteraciones
            if iteracion % 10 == 0 or iteracion <= 5:
                total_conflictos = sum(
                    self.contar_conflictos(v, asignacion[v], asignacion)
                    for v in self.variables
                ) // 2
                print(f"Iteracion {iteracion:4} | Variable: '{variable}' | "
                      f"{asignacion[variable]} -> {nuevo_valor} | "
                      f"Conflictos totales: {total_conflictos}")

            # Actualizar asignacion
            asignacion[variable] = nuevo_valor

        print(f"\nNo se encontro solucion en {max_iteraciones} iteraciones.")
        return None


# ==================================================
# PROBLEMA 1: Coloreo de Mapa de Australia
# ==================================================
def coloreo_mapa():
    print("\n" + "="*55)
    print("   PROBLEMA 1: COLOREO DE MAPA DE AUSTRALIA")
    print("="*55)

    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    dominios  = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}

    adyacencias = [
        ('WA', 'NT'), ('WA', 'SA'),
        ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'),  ('SA', 'NSW'),
        ('SA', 'V'),  ('Q',  'NSW'),
        ('NSW','V')
    ]
    restricciones = {par: (lambda a, b: a != b) for par in adyacencias}

    csp      = CSPMinConflictos(variables, dominios, restricciones)
    solucion = csp.min_conflictos(max_iteraciones=1000)

    if solucion:
        print("\nSolucion final:")
        for region, color in solucion.items():
            print(f"  {region:5} -> {color}")
    else:
        print("No se encontro solucion.")

    print("="*55)
    return solucion


# ==================================================
# PROBLEMA 2: N-Reinas con Minimos-Conflictos
# Variables : una por cada fila del tablero
# Dominio   : columnas posibles (1 a N)
# Restriccion: ninguna reina se ataca entre si
# ==================================================
def n_reinas(n=8):
    print(f"\n" + "="*55)
    print(f"   PROBLEMA 2: {n}-REINAS CON MINIMOS-CONFLICTOS")
    print("="*55)

    variables = [f'Fila{i}' for i in range(1, n + 1)]
    dominios  = {v: list(range(1, n + 1)) for v in variables}

    def no_se_atacan(col1, col2, fila1, fila2):
        if col1 == col2:
            return False
        if abs(col1 - col2) == abs(fila1 - fila2):
            return False
        return True

    restricciones = {}
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            var1 = f'Fila{i}'
            var2 = f'Fila{j}'
            restricciones[(var1, var2)] = (
                lambda c1, c2, r1=i, r2=j: no_se_atacan(c1, c2, r1, r2)
            )

    print(f"Tablero : {n}x{n}")

    csp      = CSPMinConflictos(variables, dominios, restricciones)
    solucion = csp.min_conflictos(max_iteraciones=1000)

    if solucion:
        print("\nSolucion final:")
        for fila, col in solucion.items():
            print(f"  {fila} -> Columna {col}")

        # Visualizar tablero
        print(f"\nTablero {n}x{n}:")
        print("  " + " ".join(str(c) for c in range(1, n + 1)))
        for i in range(1, n + 1):
            col_reina = solucion[f'Fila{i}']
            fila_str  = ""
            for c in range(1, n + 1):
                fila_str += "Q " if c == col_reina else ". "
            print(f"{i} {fila_str}")
    else:
        print("No se encontro solucion.")

    print("="*55)
    return solucion


# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":

    # Problema 1: Coloreo de Mapa de Australia
    coloreo_mapa()

    # Problema 2: N-Reinas (tablero 8x8)
    n_reinas(n=8)
