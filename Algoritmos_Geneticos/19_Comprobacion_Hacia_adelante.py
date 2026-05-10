"""
Comprobacion Hacia Delante (Forward Checking)

Es una técnica utilizada en problemas de satisfaccion de restricciones
(CSP) que mejora la eficiencia del proceso de busqueda al eliminar valores
inconsistentes en los dominios de las variables antes de realizar
una asignación.

Los componentes principales son:
  - Variables: elementos a asignar.
  - Dominios: valores posibles para cada variable.
  - Restricciones: condiciones que deben cumplirse.

El objetivo es encontrar una asignacion completa y consistente
que satisface todas las restricciones.

Ejemplo implementado:
  Problema de Coloreo de Mapa de Australia.
"""

# ==================================================
# CLASE BASE: Problema CSP
# Define la estructura general de cualquier CSP
# ==================================================
class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones

    def es_consistente(self, variable, valor, asignacion):
        for (var1, var2), restriccion in self.restricciones.items():
            if var1 == variable and var2 in asignacion:
                if not restriccion(valor, asignacion[var2]):
                    return False
            if var2 == variable and var1 in asignacion:
                if not restriccion(asignacion[var1], valor):
                    return False
        return True

    def forward_checking(self, variable, valor, asignacion):
        """
        Realiza la comprobacion hacia delante al asignar
        un valor a una variable. Elimina valores inconsistentes
        en los dominios de otras variables relacionadas.
        """
        for (var1, var2), restriccion in self.restricciones.items():
            if var1 == variable and var2 not in asignacion:
                # Eliminar valores incompatibles en el dominio de var2
                for v in self.dominios[var2][:]:
                    if not restriccion(valor, v):
                        self.dominios[var2].remove(v)
            elif var2 == variable and var1 not in asignacion:
                # Eliminar valores incompatibles en el dominio de var1
                for v in self.dominios[var1][:]:
                    if not restriccion(v, valor):
                        self.dominios[var1].remove(v)

    def backtracking(self, asignacion={}):
        if len(asignacion) == len(self.variables):
            return asignacion

        sin_asignar = [v for v in self.variables if v not in asignacion]
        variable = sin_asignar[0]

        for valor in self.dominios[variable]:
            if self.es_consistente(variable, valor, asignacion):
                asignacion[variable] = valor
                # Guardar dominio original para restaurar después
                original_dominios = {var: self.dominios[var][:] for var in self.variables}

                # Realizar forward checking
                self.forward_checking(variable, valor, asignacion)

                # Comprobar si se puede continuar
                if all(len(self.dominios[var]) > 0 for var in sin_asignar[1:]):
                    resultado = self.backtracking(asignacion)
                    if resultado:
                        return resultado

                # Restaurar dominios si no hay solucion
                self.dominios = original_dominios
                del asignacion[variable]

        return None


# ==================================================
# PROBLEMA: Coloreo de Mapa de Australia
# ==================================================
def coloreo_mapa():
    print("\n" + "="*55)
    print("    PROBLEMA: COLOREO DE MAPA DE AUSTRALIA")
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
    csp = CSP(variables, dominios, restricciones)
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
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":
    # Problema: Coloreo de Mapa de Australia
    coloreo_mapa()
