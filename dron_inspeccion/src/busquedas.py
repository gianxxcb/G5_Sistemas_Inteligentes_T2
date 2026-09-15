from collections import deque
from time import perf_counter
from resultados import ResultadoBusqueda
import heapq

def reconstruir_ruta(padres, meta):
    ruta = []
    actual = meta

    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()
    return ruta

def obtener_costo_camino(grafo, ruta):
    """Calcula el costo total real de una secuencia de nodos."""
    if not ruta or len(ruta) < 2:
        return 0
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo = grafo.obtener_costo_arista(ruta[i], ruta[i + 1])
        if costo is None:
            return float('inf')  # Arista inexistente
        costo_total += costo
    return costo_total

def crear_resultado(
    algoritmo, ruta, costo_total, orden_expansion, frontera_maxima,tiempo_ms):
    """
    Crea un resultado con el mismo formato para
    todos los algoritmos.
    """
    return {
        "algoritmo": algoritmo,
        "ruta": ruta,
        "pasos": len(ruta) - 1 if ruta else 0,
        "costo_total": costo_total,
        "nodos_expandidos": len(orden_expansion),
        "orden_expansion": orden_expansion,
        "frontera_maxima": frontera_maxima,
        "tiempo_ms": tiempo_ms,
    }


def bfs(grafo, inicio, meta):
    tiempo_inicio = perf_counter()

    frontera = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}
    costos = {inicio: 0}

    orden_expansion = []
    frontera_maxima = 1

    while frontera:
        actual = frontera.popleft()
        orden_expansion.append(actual)

        # Se considera que se encontró la solución.
        if actual == meta:
            ruta = reconstruir_ruta(padres, meta)
            tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

            return crear_resultado(
                "BFS",
                ruta,
                costos[meta],
                orden_expansion,
                frontera_maxima,
                tiempo_ms
            )

        # Recorre todos los vecinos del nodo actual.
        for vecino, costo_arista in grafo.obtener_vecinos(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                costos[vecino] = costos[actual] + costo_arista

                frontera.append(vecino)

        frontera_maxima = max(
            frontera_maxima,
            len(frontera)
        )

    # Caso en que no existe una ruta hacia la meta.
    tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

    return crear_resultado(
        "BFS",
        [],
        None,
        orden_expansion,
        frontera_maxima,
        tiempo_ms
    )


def dfs(grafo, inicio, meta):
    tiempo_inicio = perf_counter()

    frontera = [inicio]
    visitados = {inicio}
    padres = {inicio: None}
    costos = {inicio: 0}

    orden_expansion = []
    frontera_maxima = 1

    while frontera:
        actual = frontera.pop()
        orden_expansion.append(actual)

        # Se considera que se encontró la solución.
        if actual == meta:
            ruta = reconstruir_ruta(padres, meta)
            tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

            return crear_resultado(
                "DFS",
                ruta,
                costos[meta],
                orden_expansion,
                frontera_maxima,
                tiempo_ms
            )

        # reversed permite que DFS conserve el orden
        # original de los vecinos al sacarlos de la pila.
        for vecino, costo_arista in reversed(
            grafo.obtener_vecinos(actual)
        ):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                costos[vecino] = costos[actual] + costo_arista

                frontera.append(vecino)

        frontera_maxima = max(
            frontera_maxima,
            len(frontera)
        )

    # Caso en que no existe una ruta hacia la meta.
    tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

    return crear_resultado(
        "DFS",
        [],
        None,
        orden_expansion,
        frontera_maxima,
        tiempo_ms
    )

def greedy_best_first_search(grafo, heuristica, inicio, meta):
    tiempo_inicio = perf_counter()

    # 1. Inicialización de estructuras
    # La frontera es una Cola de Prioridad basada en tuplas (h(n), nodo)
    frontera = [(heuristica[inicio], inicio)]
    visitados = {inicio}
    padres = {inicio: None}
    costos = {inicio: 0}  # Acumulado real g(n) para reporte final

    orden_expansion = []
    frontera_maxima = 1

    # 2. Bucle principal de búsqueda
    while frontera:
        # 4. Extrae el nodo con el menor valor heurístico h(n)
        h_actual, actual = heapq.heappop(frontera)
        orden_expansion.append(actual)

        # 5. Evaluación de meta
        if actual == meta:
            ruta = reconstruir_ruta(padres, meta)
            tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

            return crear_resultado(
                "Greedy Best-First Search",
                ruta,
                costos[meta],
                orden_expansion,
                frontera_maxima,
                tiempo_ms
            )

        # 6 y 7. Expansión de vecinos (Función Sucesora)
        for vecino, costo_arista in grafo.obtener_vecinos(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                costos[vecino] = costos[actual] + costo_arista
                
                # Se inserta en la cola ordenado exclusivamente por h(n)
                heapq.heappush(frontera, (heuristica[vecino], vecino))

        frontera_maxima = max(frontera_maxima, len(frontera))

    # 3. Caso en que la frontera queda vacía sin encontrar la meta
    tiempo_ms = (perf_counter() - tiempo_inicio) * 1000
    return crear_resultado(
        "Greedy Best-First Search",
        [],
        None,
        orden_expansion,
        frontera_maxima,
        tiempo_ms
    )

def a_star(grafo, heuristica, inicio, meta):
    tiempo_inicio = perf_counter()

    # 1. Registro de costo real g(n) acumulado desde el inicio
    g_costos = {inicio: 0}
    
    # f(n) = g(n) + h(n)
    f_inicial = 0 + heuristica[inicio]
    
    # La frontera ordena tuplas (f_n, nodo) en el min-heap
    frontera = [(f_inicial, inicio)]
    
    padres = {inicio: None}
    visitados = set()
    
    orden_expansion = []
    frontera_maxima = 1

    # 2. Bucle principal de búsqueda
    while frontera:
        # 4. Recupera el nodo con el menor valor F = g(n) + h(n)
        f_actual, actual = heapq.heappop(frontera)

        # Evita re-expandir nodos previamente cerrados
        if actual in visitados:
            continue

        visitados.add(actual)
        orden_expansion.append(actual)

        # 5. Evaluación de meta
        if actual == meta:
            ruta = reconstruir_ruta(padres, meta)
            tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

            return crear_resultado(
                "A*",
                ruta,
                g_costos[meta],
                orden_expansion,
                frontera_maxima,
                tiempo_ms
            )

        # 6 y 7. Expansión de vecinos y cálculo de F = g(n) + h(n)
        for vecino, costo_arista in grafo.obtener_vecinos(actual):
            if vecino in visitados:
                continue

            # g(n) tentativo para el vecino a través del nodo actual
            g_tentativo = g_costos[actual] + costo_arista

            # 8. Reemplaza o añade si encontramos una ruta con menor costo real g(n)
            if g_tentativo < g_costos.get(vecino, float('inf')):
                padres[vecino] = actual
                g_costos[vecino] = g_tentativo
                f_vecino = g_tentativo + heuristica[vecino]
                
                heapq.heappush(frontera, (f_vecino, vecino))

        frontera_maxima = max(frontera_maxima, len(frontera))

    # 3. Caso sin solución
    tiempo_ms = (perf_counter() - tiempo_inicio) * 1000
    return crear_resultado(
        "A*",
        [],
        None,
        orden_expansion,
        frontera_maxima,
        tiempo_ms
    )

def uniform_cost_search(grafo, inicio, meta):
    tiempo_inicio = perf_counter()

    # 1. Inicialización
    # Frontera: cola de prioridad ordenada por costo acumulado g(n) -> (g(n), nodo)
    frontera = [(0, inicio)]
    visitados = set()
    padres = {inicio: None}
    costos = {inicio: 0}

    orden_expansion = []
    frontera_maxima = 1

    # 2. Bucle principal
    while frontera:
        g_actual, actual = heapq.heappop(frontera)

        # Si ya procesamos este nodo con un costo óptimo, lo ignoramos
        if actual in visitados:
            continue
            
        visitados.add(actual)
        orden_expansion.append(actual)

        # 3. Evaluación de meta
        if actual == meta:
            ruta = reconstruir_ruta(padres, meta) # Asume que esta función auxiliar ya existe
            tiempo_ms = (perf_counter() - tiempo_inicio) * 1000

            # USO DE LA DATACLASS
            return ResultadoBusqueda(
                algoritmo="UCS",
                ruta=ruta,
                costo_total=costos[meta],
                nodos_expandidos=len(orden_expansion),
                orden_expansion=orden_expansion,
                frontera_maxima=frontera_maxima,
                tiempo_ms=tiempo_ms
            )

        # 4. Exploración y relajación de vecinos
        for vecino, costo_arista in grafo.obtener_vecinos(actual):
            if vecino in visitados:
                continue
                
            nuevo_costo = g_actual + costo_arista

            # Si encontramos un camino más barato hacia el vecino
            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = actual
                heapq.heappush(frontera, (nuevo_costo, vecino))

        frontera_maxima = max(frontera_maxima, len(frontera))

    # 5. Caso sin solución
    tiempo_ms = (perf_counter() - tiempo_inicio) * 1000
    
    # USO DE LA DATACLASS (Ruta vacía)
    return ResultadoBusqueda(
        algoritmo="UCS",
        ruta=[],
        costo_total=0.0, 
        nodos_expandidos=len(orden_expansion),
        orden_expansion=orden_expansion,
        frontera_maxima=frontera_maxima,
        tiempo_ms=tiempo_ms
    )