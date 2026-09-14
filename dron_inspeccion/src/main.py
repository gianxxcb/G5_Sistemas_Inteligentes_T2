from escenarios import crear_escenario_1, crear_escenario_2
from busquedas import a_star, greedy_best_first_search, bfs, dfs

# 1. Cargas el mapa y la heurística del experimento 1
grafo, heuristica, inicio, meta = crear_escenario_1()

# 2. Ejecutas el algoritmo A*
resultado_astar = a_star(grafo, heuristica, inicio, meta)
resultado_greedy = greedy_best_first_search(grafo, heuristica, inicio, meta)

# 3. Imprimes la respuesta en consola
print("=== RESULTADO A* (Escenario 1) ===")
print("Ruta optimizada :", " -> ".join(resultado_astar["ruta"]))
print("Costo de batería:", resultado_astar["costo_total"])
print("Nodos explorados:", resultado_astar["nodos_expandidos"])
print("Tiempo (ms)     :", resultado_astar["tiempo_ms"])

print("\n=== RESULTADO GREEDY BEST FIRST SEARCH (Escenario 1) ===")
print("Ruta optimizada :", " -> ".join(resultado_greedy["ruta"]))
print("Costo de batería:", resultado_greedy["costo_total"])
print("Nodos explorados:", resultado_greedy["nodos_expandidos"])
print("Tiempo (ms)     :", resultado_greedy["tiempo_ms"])