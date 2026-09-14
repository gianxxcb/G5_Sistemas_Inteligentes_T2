import math
from grafo import GrafoListaAdyacencia

# Coordenadas espaciales 3D (x, y, z) de la infraestructura industrial
POSICIONES_NODOS = {
    "EstacionCarga": (15, 15, 0),
    "TanqueNorte": (18, 14, 5),
    "TanqueSur": (20, 18, 8),
    "TorreAlta": (25, 23, 14),
    "TorreEste": (23, 20, 12),
    "TuberiaNorte": (22, 15, 6),
    "TuberiaSur": (20, 22, 10),
    "Almacen": (20, 22, 9),
    "Subestacion": (25, 17, 8),
    "AreaProduccion1": (25, 16, 8),
    "AreaProduccion2": (24, 22, 12),
    "PuntoInspeccion1": (27, 19, 9),
    "PuntoInspeccion2": (26, 21, 11),
    "PuntoInspeccionFinal": (30, 20, 10)
}

def generar_heuristica_euclidiana(posiciones, meta):
    """Calcula h(n) como la distancia euclidiana 3D admisible hacia la meta."""
    x_m, y_m, z_m = posiciones[meta]
    return {
        nodo: math.sqrt((x - x_m)**2 + (y - y_m)**2 + (z - z_m)**2)
        for nodo, (x, y, z) in posiciones.items()
    }

def crear_escenario_1():
    grafo = GrafoListaAdyacencia()
    
    # Aristas del escenario base
    grafo.agregar_arista("EstacionCarga", "TanqueNorte", 4)
    grafo.agregar_arista("EstacionCarga", "TorreAlta", 12)
    grafo.agregar_arista("EstacionCarga", "Almacen", 5)
    grafo.agregar_arista("TanqueNorte", "TanqueSur", 3)
    grafo.agregar_arista("TanqueNorte", "TuberiaNorte", 4)
    grafo.agregar_arista("TanqueSur", "TuberiaSur", 5)
    grafo.agregar_arista("TanqueSur", "AreaProduccion1", 4)
    grafo.agregar_arista("TorreAlta", "PuntoInspeccionFinal", 13)
    grafo.agregar_arista("TorreAlta", "TorreEste", 7)
    grafo.agregar_arista("TorreEste", "Subestacion", 5)
    grafo.agregar_arista("TuberiaNorte", "Subestacion", 4)
    grafo.agregar_arista("TuberiaNorte", "AreaProduccion1", 5)
    grafo.agregar_arista("TuberiaSur", "Almacen", 4)
    grafo.agregar_arista("TuberiaSur", "AreaProduccion2", 4)
    grafo.agregar_arista("Almacen", "AreaProduccion2", 3)
    grafo.agregar_arista("Subestacion", "PuntoInspeccion1", 3)
    grafo.agregar_arista("AreaProduccion1", "PuntoInspeccion1", 3)
    grafo.agregar_arista("AreaProduccion2", "PuntoInspeccion2", 3)
    grafo.agregar_arista("PuntoInspeccion1", "PuntoInspeccionFinal", 4)
    grafo.agregar_arista("PuntoInspeccion2", "PuntoInspeccionFinal", 5)
    grafo.agregar_arista("PuntoInspeccion1", "PuntoInspeccion2", 4)

    inicio = "EstacionCarga"
    meta = "PuntoInspeccionFinal"
    heuristica = generar_heuristica_euclidiana(POSICIONES_NODOS, meta)

    return grafo, heuristica, inicio, meta

def crear_escenario_2():
    grafo, _, inicio, meta = crear_escenario_1()
    
    # Alteraciones de costos por obstáculos y viento
    grafo.cambiar_costo_arista("Almacen", "AreaProduccion2", 10)
    grafo.cambiar_costo_arista("PuntoInspeccion2", "PuntoInspeccionFinal", 9)
    
    heuristica = generar_heuristica_euclidiana(POSICIONES_NODOS, meta)

    return grafo, heuristica, inicio, meta