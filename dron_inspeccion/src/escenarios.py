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

def distancia_3d(u, v, posiciones):
    """Calcula la distancia euclidiana 3D real entre dos nodos conectados."""
    x1, y1, z1 = posiciones[u]
    x2, y2, z2 = posiciones[v]
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2), 2)

def generar_heuristica_euclidiana(posiciones, meta):
    """Calcula h(n) como la distancia euclidiana 3D admisible y consistente hacia la meta."""
    x_m, y_m, z_m = posiciones[meta]
    return {
        nodo: round(math.sqrt((x - x_m)**2 + (y - y_m)**2 + (z - z_m)**2), 2)
        for nodo, (x, y, z) in posiciones.items()
    }

def crear_escenario_1():
    grafo = GrafoListaAdyacencia()
    
    # Definición de adyacencias
    conexiones = [
        ("EstacionCarga", "TanqueNorte"),
        ("EstacionCarga", "TorreAlta"),
        ("EstacionCarga", "Almacen"),
        ("TanqueNorte", "TanqueSur"),
        ("TanqueNorte", "TuberiaNorte"),
        ("TanqueSur", "TuberiaSur"),
        ("TanqueSur", "AreaProduccion1"),
        ("TorreAlta", "PuntoInspeccionFinal"),
        ("TorreAlta", "TorreEste"),
        ("TorreEste", "Subestacion"),
        ("TuberiaNorte", "Subestacion"),
        ("TuberiaNorte", "AreaProduccion1"),
        ("TuberiaSur", "Almacen"),
        ("TuberiaSur", "AreaProduccion2"),
        ("Almacen", "AreaProduccion2"),
        ("Subestacion", "PuntoInspeccion1"),
        ("AreaProduccion1", "PuntoInspeccion1"),
        ("AreaProduccion2", "PuntoInspeccion2"),
        ("PuntoInspeccion1", "PuntoInspeccionFinal"),
        ("PuntoInspeccion2", "PuntoInspeccionFinal"),
        ("PuntoInspeccion1", "PuntoInspeccion2")
    ]
    
    # Asigna a cada arista su distancia física real 3D
    for origen, destino in conexiones:
        costo = distancia_3d(origen, destino, POSICIONES_NODOS)
        grafo.agregar_arista(origen, destino, costo)

    inicio = "EstacionCarga"
    meta = "PuntoInspeccionFinal"
    heuristica = generar_heuristica_euclidiana(POSICIONES_NODOS, meta)

    return grafo, heuristica, inicio, meta

def crear_escenario_2():
    grafo, _, inicio, meta = crear_escenario_1()
    
    # Penalizaciones adicionales sobre el costo base por viento u obstáculos
    costo_base_1 = distancia_3d("Almacen", "AreaProduccion2", POSICIONES_NODOS)
    costo_base_2 = distancia_3d("PuntoInspeccion2", "PuntoInspeccionFinal", POSICIONES_NODOS)
    
    grafo.cambiar_costo_arista("Almacen", "AreaProduccion2", round(costo_base_1 + 10.0, 2))
    grafo.cambiar_costo_arista("PuntoInspeccion2", "PuntoInspeccionFinal", round(costo_base_2 + 9.0, 2))
    
    heuristica = generar_heuristica_euclidiana(POSICIONES_NODOS, meta)

    return grafo, heuristica, inicio, meta