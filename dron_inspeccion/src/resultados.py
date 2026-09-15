import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ResultadoBusqueda:
    algoritmo: str
    ruta: list[str]
    costo_total: float
    nodos_expandidos: int
    orden_expansion: list[str]
    frontera_maxima: int
    tiempo_ms: float

def guardar_resultados_csv(resultados, escenario_num):
    """Guarda una lista de objetos ResultadoBusqueda en un archivo CSV."""
    # Crear carpetas si no existen
    directorio = Path(f"salidas/experimento_{escenario_num}")
    directorio.mkdir(parents=True, exist_ok=True)
    
    archivo_salida = directorio / f"resultados_escenario_{escenario_num}.csv"
    
    with open(archivo_salida, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Algoritmo", "Costo Total", "Nodos Expandidos", 
            "Frontera Maxima", "Tiempo (ms)", "Ruta"
        ])
        
        for res in resultados:
            writer.writerow([
                res.algoritmo, 
                res.costo_total if res.costo_total is not None else "Sin solución",
                res.nodos_expandidos,
                res.frontera_maxima,
                round(res.tiempo_ms, 4),
                " -> ".join(res.ruta) if res.ruta else "Ninguna"
            ])