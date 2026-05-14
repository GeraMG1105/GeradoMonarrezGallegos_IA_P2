"""
Teoria de la Utilidad: Funcion de Utilidad

Formalizada por Von Neumann y Morgenstern (1944).
Un agente racional asigna un valor numerico (utilidad)
a cada resultado posible y elige la accion que maximiza
la utilidad esperada (MEU: Maximum Expected Utility).

Componentes:
  - Funcion de Utilidad U(x): mapea resultados a valores.
  - Utilidad Esperada EU(a): promedio ponderado de utilidades.
  - Principio MEU: elegir accion* = argmax EU(accion).

Actitudes ante el riesgo:
  - Neutral : U(x) = x          (lineal)
  - Averso  : U(x) = sqrt(x)    (concava)
  - Amante  : U(x) = x^2        (convexa)

Ejemplos implementados:
  1. Comparacion de actitudes ante el riesgo.
  2. Agente tomando decisiones con MEU.
  3. Problema clasico: dilema de la loteria.
"""

import math

# ==================================================
# FUNCIONES DE UTILIDAD
# Representan distintas actitudes ante el riesgo
# ==================================================

def utilidad_neutral(x):
    """
    Agente neutral al riesgo.
    U(x) = x  (lineal)
    Indiferente entre resultado seguro e incierto
    si tienen el mismo valor esperado.
    """
    return x

def utilidad_averso(x):
    """
    Agente averso al riesgo.
    U(x) = sqrt(x)  (concava)
    Prefiere resultado seguro aunque el incierto
    tenga mayor valor esperado.
    """
    if x < 0:
        return -math.sqrt(abs(x))
    return math.sqrt(x)

def utilidad_amante(x):
    """
    Agente amante del riesgo.
    U(x) = x^2  (convexa)
    Prefiere apostar aunque el resultado seguro
    tenga mayor valor esperado.
    """
    return x ** 2

# ==================================================
# CALCULO DE UTILIDAD ESPERADA
# EU(accion) = Σ P(resultado | accion) * U(resultado)
# ==================================================
def utilidad_esperada(loteria, funcion_utilidad):
    """
    Calcula la utilidad esperada de una loteria.

    loteria          : lista de (probabilidad, resultado)
    funcion_utilidad : funcion U(x) a aplicar
    """
    eu = 0.0
    for probabilidad, resultado in loteria:
        eu += probabilidad * funcion_utilidad(resultado)
    return eu

# ==================================================
# AGENTE RACIONAL: Principio MEU
# Elige la accion con mayor utilidad esperada
# ==================================================
def agente_meu(acciones, funcion_utilidad):
    """
    Implementa el Principio de Maxima Utilidad Esperada.
    Elige la accion que maximiza EU(accion).

    acciones         : diccionario {nombre_accion: loteria}
    funcion_utilidad : funcion U(x) del agente
    """
    print("\n  Evaluando acciones disponibles:")
    print(f"  {'Accion':<25} {'EU':>10}")
    print(f"  {'-'*35}")

    mejor_accion = None
    mejor_eu     = float('-inf')

    for nombre, loteria in acciones.items():
        eu = utilidad_esperada(loteria, funcion_utilidad)
        print(f"  {nombre:<25} {eu:>10.4f}")
        if eu > mejor_eu:
            mejor_eu     = eu
            mejor_accion = nombre

    print(f"  {'-'*35}")
    print(f"  Mejor accion : '{mejor_accion}' con EU = {mejor_eu:.4f}")
    return mejor_accion, mejor_eu


# ==================================================
# EJEMPLO 1: Comparacion de Actitudes ante el Riesgo
# Dos opciones: resultado seguro vs loteria incierta
# ==================================================
def ejemplo_actitudes_riesgo():
    print("\n" + "="*55)
    print("  EJEMPLO 1: ACTITUDES ANTE EL RIESGO")
    print("="*55)

    # Opcion A: resultado seguro de 50
    opcion_segura = [(1.0, 50)]

    # Opcion B: loteria con 50% de ganar 100 y 50% de ganar 0
    opcion_loteria = [(0.5, 100), (0.5, 0)]

    # Valor esperado monetario (igual para ambas = 50)
    ve_segura  = sum(p * r for p, r in opcion_segura)
    ve_loteria = sum(p * r for p, r in opcion_loteria)

    print(f"\n  Opcion Segura  : resultado fijo de 50")
    print(f"  Opcion Loteria : 50% ganar 100 | 50% ganar 0")
    print(f"\n  Valor Esperado Monetario:")
    print(f"    Opcion Segura  : {ve_segura}")
    print(f"    Opcion Loteria : {ve_loteria}")
    print(f"  (Ambas tienen el mismo valor esperado = 50)\n")

    funciones = {
        'Neutral al Riesgo  [U(x) = x]      ': utilidad_neutral,
        'Averso al Riesgo   [U(x) = sqrt(x)]': utilidad_averso,
        'Amante del Riesgo  [U(x) = x^2]    ': utilidad_amante
    }

    print(f"  {'Tipo de Agente':<42} {'U(Segura)':>10} {'U(Loteria)':>11} {'Prefiere':>10}")
    print(f"  {'-'*75}")

    for nombre, fn in funciones.items():
        eu_segura  = utilidad_esperada(opcion_segura,  fn)
        eu_loteria = utilidad_esperada(opcion_loteria, fn)
        prefiere   = "Segura" if eu_segura >= eu_loteria else "Loteria"
        print(f"  {nombre:<42} {eu_segura:>10.4f} {eu_loteria:>11.4f} {prefiere:>10}")

    print("="*55)


# ==================================================
# EJEMPLO 2: Agente Tomando Decisiones con MEU
# Un agente decide entre varias inversiones
# ==================================================
def ejemplo_decision_inversion():
    print("\n" + "="*55)
    print("  EJEMPLO 2: DECISION DE INVERSION")
    print("="*55)
    print("\n  Un agente debe elegir entre tres inversiones.")
    print("  Cada inversion tiene distintos resultados posibles")
    print("  con sus respectivas probabilidades.\n")

    # Acciones disponibles con sus loterias
    # Formato: {nombre: [(probabilidad, ganancia), ...]}
    acciones = {
        'Inversion Conservadora': [
            (0.9, 80),    # 90% de ganar 80
            (0.1, 20)     # 10% de ganar 20
        ],
        'Inversion Moderada    ': [
            (0.6, 120),   # 60% de ganar 120
            (0.3, 50),    # 30% de ganar 50
            (0.1, -10)    # 10% de perder 10
        ],
        'Inversion Agresiva    ': [
            (0.4, 200),   # 40% de ganar 200
            (0.3, 80),    # 30% de ganar 80
            (0.3, -50)    # 30% de perder 50
        ]
    }

    # Mostrar loterias
    for nombre, loteria in acciones.items():
        print(f"  {nombre}:")
        for prob, resultado in loteria:
            signo = "+" if resultado >= 0 else ""
            print(f"    P={prob:.1f} -> {signo}{resultado}")
        ve = sum(p * r for p, r in loteria)
        print(f"    Valor Esperado Monetario = {ve:.1f}\n")

    # Evaluar con distintos tipos de agente
    tipos = [
        ('Agente Neutral al Riesgo ', utilidad_neutral),
        ('Agente Averso al Riesgo  ', utilidad_averso),
        ('Agente Amante del Riesgo ', utilidad_amante)
    ]

    for nombre_tipo, fn in tipos:
        print(f"\n  --- {nombre_tipo} ---")
        agente_meu(acciones, fn)

    print("\n" + "="*55)


# ==================================================
# EJEMPLO 3: Dilema Clasico de la Loteria
# Paradoja de Allais: muestra limitaciones del MEU
# ==================================================
def ejemplo_dilema_loteria():
    print("\n" + "="*55)
    print("  EJEMPLO 3: DILEMA DE LA LOTERIA")
    print("="*55)
    print("\n  Situacion: un agente debe elegir entre dos opciones")
    print("  en dos escenarios distintos.\n")

    # Escenario A
    print("  ESCENARIO A:")
    opcion_a1 = [(1.00, 100)]                          # 100% ganar 100
    opcion_a2 = [(0.89, 100), (0.10, 500), (0.01, 0)] # loteria mixta

    eu_a1_neutral = utilidad_esperada(opcion_a1, utilidad_neutral)
    eu_a2_neutral = utilidad_esperada(opcion_a2, utilidad_neutral)
    eu_a1_averso  = utilidad_esperada(opcion_a1, utilidad_averso)
    eu_a2_averso  = utilidad_esperada(opcion_a2, utilidad_averso)

    print(f"    Opcion A1: 100% ganar 100")
    print(f"    Opcion A2: 89% ganar 100 | 10% ganar 500 | 1% ganar 0")
    print(f"\n    {'Agente':<25} {'EU(A1)':>8} {'EU(A2)':>8} {'Elige':>8}")
    print(f"    {'-'*50}")
    for nombre, eu1, eu2 in [
        ('Neutral al Riesgo', eu_a1_neutral, eu_a2_neutral),
        ('Averso al Riesgo ', eu_a1_averso,  eu_a2_averso)
    ]:
        elige = "A1" if eu1 >= eu2 else "A2"
        print(f"    {nombre:<25} {eu1:>8.3f} {eu2:>8.3f} {elige:>8}")

    # Escenario B
    print(f"\n  ESCENARIO B:")
    opcion_b1 = [(0.11, 100), (0.89, 0)]              # loteria baja
    opcion_b2 = [(0.10, 500), (0.90, 0)]              # loteria alta

    eu_b1_neutral = utilidad_esperada(opcion_b1, utilidad_neutral)
    eu_b2_neutral = utilidad_esperada(opcion_b2, utilidad_neutral)
    eu_b1_averso  = utilidad_esperada(opcion_b1, utilidad_averso)
    eu_b2_averso  = utilidad_esperada(opcion_b2, utilidad_averso)

    print(f"    Opcion B1: 11% ganar 100 | 89% ganar 0")
    print(f"    Opcion B2: 10% ganar 500 | 90% ganar 0")
    print(f"\n    {'Agente':<25} {'EU(B1)':>8} {'EU(B2)':>8} {'Elige':>8}")
    print(f"    {'-'*50}")
    for nombre, eu1, eu2 in [
        ('Neutral al Riesgo', eu_b1_neutral, eu_b2_neutral),
        ('Averso al Riesgo ', eu_b1_averso,  eu_b2_averso)
    ]:
        elige = "B1" if eu1 >= eu2 else "B2"
        print(f"    {nombre:<25} {eu1:>8.3f} {eu2:>8.3f} {elige:>8}")

    print("\n" + "="*55)


# ==================================================
# EJECUCION PRINCIPAL
# ==================================================
if __name__ == "__main__":

    # Ejemplo 1: Comparacion de actitudes ante el riesgo
    ejemplo_actitudes_riesgo()

    # Ejemplo 2: Agente tomando decisiones de inversion
    ejemplo_decision_inversion()

    # Ejemplo 3: Dilema clasico de la loteria
    ejemplo_dilema_loteria()
