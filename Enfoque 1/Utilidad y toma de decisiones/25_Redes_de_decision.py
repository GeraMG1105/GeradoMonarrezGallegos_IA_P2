"""
Redes de Decision (Decision Networks / Influence Diagrams)

Extension de las Redes Bayesianas que incorpora nodos de
decision y nodos de utilidad para modelar problemas de toma
de decisiones bajo incertidumbre.

Componentes:
  - Nodo de Azar    : variable aleatoria con probabilidad.
  - Nodo de Decision: accion que el agente puede elegir.
  - Nodo de Utilidad: valor numerico a maximizar.

Algoritmo de evaluacion:
  1. Fijar evidencia observada.
  2. Para cada accion, calcular EU(accion).
  3. Elegir accion* = argmax EU(accion).

Problemas implementados:
  1. Decision de llevar paraguas (clasico).
  2. Decision de inversion con estado del mercado.
"""

# ==================================================
# CLASE: Nodo de Azar
# Variable aleatoria con distribucion de probabilidad
# ==================================================
class NodoAzar:
    def __init__(self, nombre, valores, probabilidades):
        """
        nombre          : nombre del nodo.
        valores         : lista de valores posibles.
        probabilidades  : dict {valor: P(valor)} o
                          dict {(valor, padre): P(valor|padre)}
        """
        self.nombre         = nombre
        self.valores        = valores
        self.probabilidades = probabilidades

    def probabilidad(self, valor, evidencia=None):
        """
        Retorna P(valor) o P(valor | evidencia).
        """
        if evidencia:
            clave = (valor, evidencia)
            return self.probabilidades.get(clave, 0.0)
        return self.probabilidades.get(valor, 0.0)


# ==================================================
# CLASE: Nodo de Decision
# Accion que el agente puede elegir
# ==================================================
class NodoDecision:
    def __init__(self, nombre, acciones):
        """
        nombre   : nombre del nodo de decision.
        acciones : lista de acciones posibles.
        """
        self.nombre   = nombre
        self.acciones = acciones


# ==================================================
# CLASE: Nodo de Utilidad
# Valor numerico asociado a combinaciones de estados
# ==================================================
class NodoUtilidad:
    def __init__(self, nombre, utilidades):
        """
        nombre      : nombre del nodo de utilidad.
        utilidades  : dict {(accion, estado): utilidad}
        """
        self.nombre     = nombre
        self.utilidades = utilidades

    def obtener_utilidad(self, accion, estado):
        """
        Retorna U(accion, estado).
        """
        return self.utilidades.get((accion, estado), 0.0)


# ==================================================
# CLASE: Red de Decision
# Integra nodos de azar, decision y utilidad
# ==================================================
class RedDecision:
    def __init__(self, nombre):
        self.nombre    = nombre
        self.azares    = {}   # {nombre: NodoAzar}
        self.decisiones= {}   # {nombre: NodoDecision}
        self.utilidades= {}   # {nombre: NodoUtilidad}

    def agregar_azar(self, nodo):
        self.azares[nodo.nombre] = nodo

    def agregar_decision(self, nodo):
        self.decisiones[nodo.nombre] = nodo

    def agregar_utilidad(self, nodo):
        self.utilidades[nodo.nombre] = nodo

    def calcular_eu(self, nodo_decision, nodo_azar,
                    nodo_utilidad, evidencia=None):
        """
        Calcula la Utilidad Esperada para cada accion.

        EU(accion) = Σ P(estado | evidencia) * U(accion, estado)

        nodo_decision : nombre del nodo de decision.
        nodo_azar     : nombre del nodo de azar relevante.
        nodo_utilidad : nombre del nodo de utilidad.
        evidencia     : valor observado del nodo de azar padre
                        (si existe dependencia condicional).
        """
        decision  = self.decisiones[nodo_decision]
        azar      = self.azares[nodo_azar]
        utilidad  = self.utilidades[nodo_utilidad]

        resultados = {}

        for accion in decision.acciones:
            eu = 0.0
            for estado in azar.valores:
                # P(estado | evidencia)
                prob = azar.probabilidad(estado, evidencia)
                # U(accion, estado)
                u    = utilidad.obtener_utilidad(accion, estado)
                eu  += prob * u
            resultados[accion] = eu

        return resultados

    def mejor_accion(self, resultados_eu):
        """
        Retorna la accion con mayor utilidad esperada.
        """
        return max(resultados_eu, key=resultados_eu.get)

    def mostrar_estructura(self):
        """
        Muestra la estructura de la red de decision.
        """
        print(f"\n  Estructura de la Red: '{self.nombre}'")
        print(f"  {'─'*45}")
        print(f"  Nodos de Azar     : {list(self.azares.keys())}")
        print(f"  Nodos de Decision : {list(self.decisiones.keys())}")
        print(f"  Nodos de Utilidad : {list(self.utilidades.keys())}")
        print(f"  {'─'*45}")


# ==================================================
# PROBLEMA 1: Decision de Llevar Paraguas
# Clasico problema de decision bajo incertidumbre.
#
# Estructura:
#   [Pronostico] --> (Clima) --> <Utilidad>
#                       ^
#                  [Paraguas]---> <Utilidad>
#
# Nodo Azar    : Clima {Lluvia, Sol}
# Nodo Decision: Paraguas {Llevar, No Llevar}
# Nodo Utilidad: U(paraguas, clima)
# ==================================================
def problema_paraguas():
    print("\n" + "="*55)
    print("   PROBLEMA 1: DECISION DE LLEVAR PARAGUAS")
    print("="*55)

    # --- Nodo de Azar: Clima ---
    # P(Lluvia) = 0.4, P(Sol) = 0.6
    clima = NodoAzar(
        nombre         = 'Clima',
        valores        = ['Lluvia', 'Sol'],
        probabilidades = {
            'Lluvia': 0.4,
            'Sol'   : 0.6
        }
    )

    # --- Nodo de Decision: Paraguas ---
    paraguas = NodoDecision(
        nombre   = 'Paraguas',
        acciones = ['Llevar', 'No Llevar']
    )

    # --- Nodo de Utilidad: U(accion, clima) ---
    # Llevar paraguas con lluvia    : +70 (protegido)
    # Llevar paraguas con sol       : +20 (incomodo pero seguro)
    # No llevar paraguas con lluvia : -30 (mojado)
    # No llevar paraguas con sol    : +100 (comodo y libre)
    utilidad = NodoUtilidad(
        nombre     = 'Utilidad Paraguas',
        utilidades = {
            ('Llevar',    'Lluvia'): 70,
            ('Llevar',    'Sol')   : 20,
            ('No Llevar', 'Lluvia'): -30,
            ('No Llevar', 'Sol')   : 100
        }
    )

    # --- Construir la Red de Decision ---
    red = RedDecision('Red Paraguas')
    red.agregar_azar(clima)
    red.agregar_decision(paraguas)
    red.agregar_utilidad(utilidad)
    red.mostrar_estructura()

    # --- Mostrar probabilidades y utilidades ---
    print(f"\n  Probabilidades del Clima:")
    for estado in clima.valores:
        print(f"    P({estado}) = {clima.probabilidad(estado)}")

    print(f"\n  Tabla de Utilidades U(accion, clima):")
    print(f"  {'Accion':<15} {'Clima':<10} {'Utilidad':>10}")
    print(f"  {'-'*35}")
    for (accion, estado), u in utilidad.utilidades.items():
        print(f"  {accion:<15} {estado:<10} {u:>10}")

    # --- Calcular Utilidad Esperada ---
    print(f"\n  Calculando EU(accion):")
    print(f"  EU(accion) = Σ P(clima) * U(accion, clima)\n")

    resultados = red.calcular_eu('Paraguas', 'Clima', 'Utilidad Paraguas')

    for accion, eu in resultados.items():
        print(f"  EU({accion:<12}) = {eu:.2f}")

    mejor = red.mejor_accion(resultados)
    print(f"\n  Decision optima : '{mejor}'")
    print(f"  EU optima       : {resultados[mejor]:.2f}")
    print("="*55)


# ==================================================
# PROBLEMA 2: Decision de Inversion con Pronostico
# El agente puede consultar un pronostico del mercado
# antes de decidir su inversion.
#
# Estructura:
#   [Pronostico] --> (Mercado) --> <Utilidad>
#                       ^
#                  [Inversion] --> <Utilidad>
#
# Nodo Azar    : Mercado {Alza, Baja}
# Nodo Azar    : Pronostico {Positivo, Negativo} | Mercado
# Nodo Decision: Inversion {Acciones, Bonos, Efectivo}
# Nodo Utilidad: U(inversion, mercado)
# ==================================================
def problema_inversion():
    print("\n" + "="*55)
    print("   PROBLEMA 2: DECISION DE INVERSION")
    print("="*55)

    # --- Nodo de Azar: Estado del Mercado ---
    # P(Alza) = 0.55, P(Baja) = 0.45
    mercado = NodoAzar(
        nombre         = 'Mercado',
        valores        = ['Alza', 'Baja'],
        probabilidades = {
            'Alza': 0.55,
            'Baja': 0.45
        }
    )

    # --- Nodo de Azar: Pronostico del Mercado ---
    # P(Positivo | Alza) = 0.80, P(Negativo | Alza) = 0.20
    # P(Positivo | Baja) = 0.30, P(Negativo | Baja) = 0.70
    pronostico = NodoAzar(
        nombre         = 'Pronostico',
        valores        = ['Positivo', 'Negativo'],
        probabilidades = {
            ('Positivo', 'Alza'): 0.80,
            ('Negativo', 'Alza'): 0.20,
            ('Positivo', 'Baja'): 0.30,
            ('Negativo', 'Baja'): 0.70
        }
    )

    # --- Nodo de Decision: Tipo de Inversion ---
    inversion = NodoDecision(
        nombre   = 'Inversion',
        acciones = ['Acciones', 'Bonos', 'Efectivo']
    )

    # --- Nodo de Utilidad: U(inversion, mercado) ---
    utilidad = NodoUtilidad(
        nombre     = 'Utilidad Inversion',
        utilidades = {
            ('Acciones', 'Alza'): 200,
            ('Acciones', 'Baja'): -100,
            ('Bonos',    'Alza'): 80,
            ('Bonos',    'Baja'): 40,
            ('Efectivo', 'Alza'): 30,
            ('Efectivo', 'Baja'): 30
        }
    )

    # --- Construir la Red de Decision ---
    red = RedDecision('Red Inversion')
    red.agregar_azar(mercado)
    red.agregar_azar(pronostico)
    red.agregar_decision(inversion)
    red.agregar_utilidad(utilidad)
    red.mostrar_estructura()

    # --- Mostrar tabla de utilidades ---
    print(f"\n  Tabla de Utilidades U(inversion, mercado):")
    print(f"  {'Inversion':<12} {'Mercado':<10} {'Utilidad':>10}")
    print(f"  {'-'*35}")
    for (accion, estado), u in utilidad.utilidades.items():
        print(f"  {accion:<12} {estado:<10} {u:>10}")

    # --- CASO A: Sin pronostico (decision a priori) ---
    print(f"\n  CASO A: Sin pronostico (probabilidades a priori)")
    print(f"  P(Alza) = 0.55 | P(Baja) = 0.45\n")

    resultados_sin = red.calcular_eu(
        'Inversion', 'Mercado', 'Utilidad Inversion'
    )
    for accion, eu in resultados_sin.items():
        print(f"  EU({accion:<10}) = {eu:.2f}")

    mejor_sin = red.mejor_accion(resultados_sin)
    print(f"\n  Decision optima (sin pronostico) : '{mejor_sin}'")
    print(f"  EU optima                        : {resultados_sin[mejor_sin]:.2f}")

    # --- CASO B: Con pronostico Positivo ---
    print(f"\n  CASO B: Pronostico POSITIVO recibido")

    # P(Alza | Positivo) usando Bayes
    # P(Pos|Alza)*P(Alza) / P(Pos)
    p_pos_alza = 0.80 * 0.55
    p_pos_baja = 0.30 * 0.45
    p_pos      = p_pos_alza + p_pos_baja
    p_alza_pos = p_pos_alza / p_pos
    p_baja_pos = p_pos_baja / p_pos

    print(f"  P(Alza | Positivo) = {p_alza_pos:.4f}")
    print(f"  P(Baja | Positivo) = {p_baja_pos:.4f}\n")

    mercado_pos = NodoAzar(
        nombre         = 'Mercado|Positivo',
        valores        = ['Alza', 'Baja'],
        probabilidades = {'Alza': p_alza_pos, 'Baja': p_baja_pos}
    )
    red.agregar_azar(mercado_pos)

    resultados_pos = red.calcular_eu(
        'Inversion', 'Mercado|Positivo', 'Utilidad Inversion'
    )
    for accion, eu in resultados_pos.items():
        print(f"  EU({accion:<10}) = {eu:.2f}")

    mejor_pos = red.mejor_accion(resultados_pos)
    print(f"\n  Decision optima (pronostico positivo) : '{mejor_pos}'")
    print(f"  EU optima                             : {resultados_pos[mejor_pos]:.2f}")

    # --- CASO C: Con pronostico Negativo ---
    print(f"\n  CASO C: Pronostico NEGATIVO recibido")

    p_neg_alza = 0.20 * 0.55
    p_neg_baja = 0.70 * 0.45
    p_neg      = p_neg_alza + p_neg_baja
    p_alza_neg = p_neg_alza / p_neg
    p_baja_neg = p_neg_baja / p_neg

    print(f"  P(Alza | Negativo) = {p_alza_neg:.4f}")
    print(f"  P(Baja | Negativo) = {p_baja_neg:.4f}\n")

    mercado_neg = NodoAzar(
        nombre         = 'Mercado|Negativo',
        valores        = ['Alza', 'Baja'],
        probabilidades = {'Alza': p_alza_neg, 'Baja': p_baja_neg}
    )
    red.agregar_azar(mercado_neg)

    resultados_neg = red.calcular_eu(
        'Inversion', 'Mercado|Negativo', 'Utilidad Inversion'
    )
    for accion, eu in resultados_neg.items():
        print(f"  EU({accion:<10}) = {eu:.2f}")

    mejor_neg = red.mejor_accion(resultados_neg)
    print(f"\n  Decision optima (pronostico negativo) : '{mejor_neg}'")
    print(f"  EU optima                             : {resultados_neg[mejor_neg]:.2f}")

    # --- Resumen comparativo ---
    print(f"\n  RESUMEN COMPARATIVO:")
    print(f"  {'Escenario':<35} {'Mejor Accion':<12} {'EU':>8}")
    print(f"  {'-'*55}")
    print(f"  {'Sin pronostico':<35} {mejor_sin:<12} {resultados_sin[mejor_sin]:>8.2f}")
    print(f"  {'Con pronostico Positivo':<35} {mejor_pos:<12} {resultados_pos[mejor_pos]:>8.2f}")
    print(f"  {'Con pronostico Negativo':<35} {mejor_neg:<12} {resultados_neg[mejor_neg]:>8.2f}")
    print("="*55)


# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":

    # Problema 1: Decision de llevar paraguas
    problema_paraguas()

    # Problema 2: Decision de inversion con pronostico
    problema_inversion()
