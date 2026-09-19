import networkx as nx

def construir_grafo_nx(grafo_adyacencia):
    """Convierte tu clase GrafoListaAdyacencia a un grafo de NetworkX."""
    G = nx.Graph()
    for origen in grafo_adyacencia.obtener_vertices():
        vecinos = grafo_adyacencia.obtener_vecinos(origen)
        for destino, costo in vecinos:
            G.add_edge(origen, destino, weight=costo)
    return G

def dibujar_grafo(ax, grafo_adyacencia, posiciones_3d, ruta=None, titulo="Mapa de Inspección"):
    """Dibuja el grafo, los costos y resalta la ruta encontrada."""
    ax.clear()
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    
    G = construir_grafo_nx(grafo_adyacencia)
    
    # Proyectar coordenadas 3D a 2D (x, y)
    posiciones_2d = {nodo: (coords[0], coords[1]) for nodo, coords in posiciones_3d.items()}
    
    # 1. Nodos un poco más pequeños para dar más espacio a las líneas (1000 en vez de 1500)
    nx.draw_networkx_nodes(G, posiciones_2d, ax=ax, node_color='#A0CBE2', node_size=1000)
    nx.draw_networkx_labels(G, posiciones_2d, ax=ax, font_size=7, font_weight='bold')
    
    # 2. Líneas base más gruesas y definidas (width=2.0)
    nx.draw_networkx_edges(G, posiciones_2d, ax=ax, edge_color='gray', width=2.0)
    
    # 3. Dibujar etiquetas de costos
    for (u, v, data) in G.edges(data=True):
        x = (posiciones_2d[u][0] + posiciones_2d[v][0]) / 2
        y = (posiciones_2d[u][1] + posiciones_2d[v][1]) / 2
        
        # Fondo blanco al texto para que no se mezcle con las líneas gruesas
        ax.text(x, y, str(data['weight']), size=8, color='black', 
                ha='center', va='center', 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    # 4. Resaltar la ruta con una línea roja mucho más visible (width=4.5)
    if ruta and len(ruta) > 0:
        edges_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_edges(G, posiciones_2d, edgelist=edges_ruta, edge_color='red', width=4.5, ax=ax)
        
        # Nodos de la ruta resaltados, ligeramente más grandes que los base
        nx.draw_networkx_nodes(G, posiciones_2d, nodelist=ruta, node_color='#76D7C4', node_size=1100, ax=ax)