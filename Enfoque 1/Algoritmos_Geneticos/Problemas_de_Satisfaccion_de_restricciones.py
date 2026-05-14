"""
Problemas de Satisfaccion de Restricciones (CSP)

Un CSP se define por tres elementos:
  - Variables: elementos a los que se asigna un valor.
  - Dominios: valores posibles para cada variable.
  - Restricciones: condiciones que deben cumplirse.

El objetivo es encontrar una asignacion completa y consistente,
es decir, que todas las variables tengan valor y todas las
restricciones se cumplan.

Problemas implementados:
  1. Coloreo de Mapa de Australia: asignar colores a regiones
     de forma que regiones adyacentes tengan colores distintos.
  2. N-Reinas: colocar N reinas en un tablero NxN sin que
     ninguna se ataque entre si.

Metodo de resolucion:
  Backtracking simple con verificacion de consistencia.
  (Los algoritmos avanzados como Forward Checking y
   Backjumping se cubren en los temas 18 al 23.)
"""

# ==================================================
# CLASE BASE: Problema CSP
# Define la estructura general de cualquier CSP
# ==================================================
class CSP:
    def __init__(self, variables, dominios, restricciones):
        """
        variables     : lista de variables del problema
        dominios      : diccionario {variable: [valores posibles]}
        restricciones : diccionario {(var1, var2): funcion_restriccion}
        """
        self.variables     = variables
        self.dominios      = dominios
        self.restricciones = restricciones

    def es_consistente(self, variable, valor, asignacion):
        """
        Verifica si asignar 'valor' a 'variable' es consistente
        con la asignacion actual, revisando todas las restricciones
        que involucran a esa variable.
        """
        for (var1, var2), restriccion in self.restricciones.items():
            # Revisar restricciones donde participa la variable actual
            if var1 == variable and var2 in asignacion:
                if not restriccion(valor, asignacion[var2]):
                    return False
            if var2 == variable and var1 in asignacion:
                if not restriccion(asignacion[var1], valor):
                    return False
        return True

    def backtracking(self, asignacion={}):
        """
        Algoritmo de backtracking simple para resolver el CSP.
        Asigna valores a variables una por una, verificando
        consistencia en cada paso. Si hay conflicto, retrocede.
        """
        # Si todas las variables tienen valor, solucion encontrada
        if len(asignacion) == len(self.variables):
            return asignacion

        # Elegir la siguiente variable sin asignar
        sin_asignar = [v for v in self.variables if v not in asignacion]
        variable    = sin_asignar[0]

        # Probar cada valor del dominio de la variable
        for valor in self.dominios[variable]:
            if self.es_consistente(variable, valor, asignacion):
                # Asignar el valor y continuar
                asignacion[variable] = valor
                resultado = self.backtracking(asignacion)
                if resultado:
                    return resultado
                # Si no funciono, deshacer la asignacion (backtrack)
                del asignacion[variable]

        return None  # No se encontro solucion


# ==================================================
# PROBLEMA 1: Coloreo de Mapa de Australia
# Variables : regiones de Australia
# Dominio   : colores disponibles
# Restriccion: regiones adyacentes deben tener distinto color
# ==================================================
def coloreo_mapa():
    print("\n" + "="*55)
    print("    PROBLEMA 1: COLOREO DE MAPA DE AUSTRALIA")
    print("="*55)

    # Variables: regiones de Australia
    variables = [
        'WA',   # Western Australia
        'NT',   # Northern Territory
        'SA',   # South Australia
        'Q',    # Queensland
        'NSW',  # New South Wales
        'V',    # Victoria
        'T'     # Tasmania
    ]

    # Dominio: tres colores disponibles para todas las regiones
    dominios = {v: ['Rojo', 'Verde', 'Azul'] for v in variables}

    # Restricciones: pares de regiones adyacentes deben tener distinto color
    adyacencias = [
        ('WA', 'NT'),
        ('WA', 'SA'),
        ('NT', 'SA'),
        ('NT', 'Q'),
        ('SA', 'Q'),
        ('SA', 'NSW'),
        ('SA', 'V'),
        ('Q',  'NSW'),
        ('NSW','V')
    ]

    # Funcion de restriccion: los dos valores deben ser distintos
    restricciones = {par: (lambda a, b: a != b) for par in adyacencias}

    print(f"Variables    : {variables}")
    print(f"Dominio      : ['Rojo', 'Verde', 'Azul']")
    print(f"Adyacencias  : {len(adyacencias)} pares de regiones")
    print("\nResolviendo...\n")

    # Crear y resolver el CSP
    csp      = CSP(variables, dominios, restricciones)
    solucion = csp.backtracking({})

    if solucion:
        print("Solucion encontrada:")
        for region, color in solucion.items():
            print(f"  {region:5} -> {color}")
    else:
        print("No se encontro solucion.")

    print("="*55)
    return solucion


# ==================================================
# PROBLEMA 2: N-Reinas
# Variables : filas del tablero (una reina por fila)
# Dominio   : columnas posibles (1 a N)
# Restriccion: ninguna reina se ataca entre si
# ==================================================
def n_reinas(n=6):
    print(f"\n" + "="*55)
    print(f"    PROBLEMA 2: {n}-REINAS")
    print("="*55)

    # Variables: una por cada fila del tablero
    variables = [f'Fila{i}' for i in range(1, n + 1)]

    # Dominio: cualquier columna del tablero
    dominios  = {v: list(range(1, n + 1)) for v in variables}

    # Funcion de restriccion entre dos reinas
    # Parametros: col1, col2 = columnas; fila1, fila2 = filas
    def no_se_atacan(col1, col2, fila1, fila2):
        # No pueden estar en la misma columna
        if col1 == col2:
            return False
        # No pueden estar en la misma diagonal
        if abs(col1 - col2) == abs(fila1 - fila2):
            return False
        return True

    # Crear restricciones para cada par de filas
    restricciones = {}
    filas = list(range(1, n + 1))
    for i in range(len(filas)):
        for j in range(i + 1, len(filas)):
            f1 = filas[i]
            f2 = filas[j]
            var1 = f'Fila{f1}'
            var2 = f'Fila{f2}'
            # Capturar f1 y f2 correctamente con valores por defecto
            restricciones[(var1, var2)] = (
                lambda c1, c2, r1=f1, r2=f2: no_se_atacan(c1, c2, r1, r2)
            )

    print(f"Tablero      : {n}x{n}")
    print(f"Variables    : {variables}")
    print(f"Dominio      : columnas 1 a {n}")
    print(f"Restricciones: {len(restricciones)} pares de reinas")
    print("\nResolviendo...\n")

    # Crear y resolver el CSP
    csp      = CSP(variables, dominios, restricciones)
    solucion = csp.backtracking({})

    if solucion:
        print("Solucion encontrada:")
        for fila, col in solucion.items():
            print(f"  {fila} -> Columna {col}")

        # Visualizar el tablero
        print(f"\nTablero {n}x{n}:")
        print("  " + " ".join(str(c) for c in range(1, n + 1)))
        for i in range(1, n + 1):
            fila_key = f'Fila{i}'
            col_reina = solucion[fila_key]
            fila_str  = ""
            for c in range(1, n + 1):
                if c == col_reina:
                    fila_str += "Q "
                else:
                    fila_str += ". "
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

    # Problema 2: N-Reinas (tablero 6x6)
    n_reinas(n=6)
