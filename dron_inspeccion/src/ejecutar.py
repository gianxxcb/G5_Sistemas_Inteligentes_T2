import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from escenarios import crear_escenario_1, crear_escenario_2, POSICIONES_NODOS
from busquedas import bfs, dfs, uniform_cost_search, greedy_best_first_search, a_star
from visualizacion import dibujar_grafo
from resultados import guardar_resultados_csv

# Variables globales para el estado de la interfaz
escenario_actual = 1
algoritmo_seleccionado = 'BFS'

def iniciar_interfaz():
    # Configuración de ventana amplia 
    fig = plt.figure(figsize=(14, 8))
    fig.canvas.manager.set_window_title('Simulador de Dron de Inspección')

    # Área para el grafo (Ocupa el 75% derecho de la pantalla)
    ax_grafo = fig.add_axes([0.25, 0.05, 0.70, 0.85])

    # --- WIDGETS DE INTERFAZ (25% izquierdo) ---
    
    # Selector de Escenario
    ax_escenario = fig.add_axes([0.02, 0.75, 0.18, 0.15])
    ax_escenario.set_title('Escenario')
    radio_escenario = RadioButtons(ax_escenario, ('Escenario 1 (Base)', 'Escenario 2 (Clima)'))

    # Selector de Algoritmo
    ax_algoritmo = fig.add_axes([0.02, 0.45, 0.18, 0.25])
    ax_algoritmo.set_title('Método de Búsqueda')
    algoritmos_opciones = ('BFS', 'DFS', 'UCS', 'Greedy', 'A*')
    radio_algoritmo = RadioButtons(ax_algoritmo, algoritmos_opciones)

    # Botón de Ejecución
    ax_boton = fig.add_axes([0.02, 0.30, 0.18, 0.08])
    btn_ejecutar = Button(ax_boton, 'Ejecutar Búsqueda', color='lightgreen', hovercolor='palegreen')

    # Panel de texto para métricas
    ax_metricas = fig.add_axes([0.02, 0.05, 0.18, 0.20])
    ax_metricas.axis('off')
    texto_metricas = ax_metricas.text(0, 1, "Métricas aparecerán aquí...", 
                                      fontsize=9, verticalalignment='top')

    # Carga inicial del grafo sin ruta
    grafo, _, _, _ = crear_escenario_1()
    dibujar_grafo(ax_grafo, grafo, POSICIONES_NODOS, None, "Escenario 1: Sin resolver")

    # --- EVENTOS ---
    def actualizar_parametros(val):
        # Limpiar métricas al cambiar de opción
        texto_metricas.set_text("")
        fig.canvas.draw_idle()

    radio_escenario.on_clicked(actualizar_parametros)
    radio_algoritmo.on_clicked(actualizar_parametros)

    def ejecutar_busqueda(event):
        # 1. Obtener selecciones
        escenario_str = radio_escenario.value_selected
        algo_str = radio_algoritmo.value_selected
        
        # 2. Cargar el escenario correspondiente
        if "1" in escenario_str:
            grafo, heuristica, inicio, meta = crear_escenario_1()
            num_esc = 1
        else:
            grafo, heuristica, inicio, meta = crear_escenario_2()
            num_esc = 2

        # 3. Ejecutar algoritmo seleccionado
        if algo_str == 'BFS':
            resultado = bfs(grafo, inicio, meta)
        elif algo_str == 'DFS':
            resultado = dfs(grafo, inicio, meta)
        elif algo_str == 'UCS':
            resultado = uniform_cost_search(grafo, inicio, meta)
        elif algo_str == 'Greedy':
            resultado = greedy_best_first_search(grafo, heuristica, inicio, meta)
        elif algo_str == 'A*':
            resultado = a_star(grafo, heuristica, inicio, meta)

        # 4. Actualizar Visualización (Ruta roja)
        titulo = f"{algo_str} - Escenario {num_esc}"
        
        # NOTA: Asegúrate que resultado sea la Dataclass o accede como dict si tus compañeros aún no lo cambian.
        # Por ahora lo leo como diccionario basado en tu busquedas.py actual. 
        # CÁMBIALO a resultado.ruta, resultado.costo_total cuando implementen ResultadoBusqueda.
        ruta_encontrada = resultado["ruta"] if isinstance(resultado, dict) else resultado.ruta
        costo = resultado["costo_total"] if isinstance(resultado, dict) else resultado.costo_total
        nodos_exp = resultado["nodos_expandidos"] if isinstance(resultado, dict) else resultado.nodos_expandidos
        tiempo = resultado["tiempo_ms"] if isinstance(resultado, dict) else resultado.tiempo_ms
        
        dibujar_grafo(ax_grafo, grafo, POSICIONES_NODOS, ruta_encontrada, titulo)

        # 5. Mostrar métricas en pantalla
        metricas = (
            f"Ruta: {len(ruta_encontrada)} nodos\n"
            f"Costo Total: {costo}\n"
            f"Nodos Expandidos: {nodos_exp}\n"
            f"Tiempo: {tiempo:.2f} ms"
        )
        texto_metricas.set_text(metricas)
        
        fig.canvas.draw_idle()

    btn_ejecutar.on_clicked(ejecutar_busqueda)

    plt.show()

if __name__ == '__main__':
    iniciar_interfaz()