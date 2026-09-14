class GrafoListaAdyacencia:
    # No dirigida
    def __init__(self):
        self._adyacencias = {}

    def agregar_vertice(self, vertice):
        if vertice in self._adyacencias:
            return False

        self._adyacencias[vertice] = []
        return True

    def agregar_arista(self, origen, destino, costo):
        if costo < 0:
            raise ValueError("El costo no puede ser negativo.")

        if origen not in self._adyacencias:
            self.agregar_vertice(origen)

        if destino not in self._adyacencias:
            self.agregar_vertice(destino)

        self._agregar_o_actualizar(origen, destino, costo)
        self._agregar_o_actualizar(destino, origen, costo)

    def _agregar_o_actualizar(self, origen, destino, costo):
        vecinos = self._adyacencias[origen]

        for indice, (vecino, _) in enumerate(vecinos):
            if vecino == destino:
                vecinos[indice] = (destino, costo)
                return

        vecinos.append((destino, costo))

    def eliminar_vertice(self, vertice):
        if vertice not in self._adyacencias:
            return False

        del self._adyacencias[vertice]

        for origen in self._adyacencias:
            self._adyacencias[origen] = [
                (destino, costo)
                for destino, costo in self._adyacencias[origen]
                if destino != vertice
            ]

        return True

    def eliminar_arista(self, origen, destino):
        if origen not in self._adyacencias:
            return False

        self._eliminar_arista_un_sentido(origen, destino)
        self._eliminar_arista_un_sentido(destino, origen)

        return True

    def _eliminar_arista_un_sentido(self, origen, destino):
        if origen not in self._adyacencias:
            return

        self._adyacencias[origen] = [
            (vecino, costo)
            for vecino, costo in self._adyacencias[origen]
            if vecino != destino
        ]

    def cambiar_costo_arista(self, origen, destino, nuevo_costo):
        if nuevo_costo < 0:
            raise ValueError("El costo no puede ser negativo.")

        if origen not in self._adyacencias or destino not in self._adyacencias:
            return False

        encontrada = False

        for indice, (vecino, _) in enumerate(self._adyacencias[origen]):
            if vecino == destino:
                self._adyacencias[origen][indice] = (
                    destino,
                    nuevo_costo
                )
                encontrada = True

        for indice, (vecino, _) in enumerate(self._adyacencias[destino]):
            if vecino == origen:
                self._adyacencias[destino][indice] = (
                    origen,
                    nuevo_costo
                )

        return encontrada

    def obtener_vecinos(self, vertice):
        return self._adyacencias.get(vertice, [])

    def obtener_vertices(self):
        return list(self._adyacencias.keys())

    def cantidad_vertices(self):
        return len(self._adyacencias)

    def cantidad_aristas(self):
        total = sum(
            len(vecinos)
            for vecinos in self._adyacencias.values()
        )
        return total // 2

    def mostrar_adyacencias(self):
        print("\n--- LISTA DE ADYACENCIA ---")

        for origen, vecinos in self._adyacencias.items():
            conexiones = ", ".join(
                f"{destino} ({costo})"
                for destino, costo in vecinos
            )
            print(f"{origen} -> {conexiones}")

    def obtener_costo_arista(self, origen, destino):
        """Retorna el costo de la arista directa si existe, o None si no."""
        if origen not in self._adyacencias:
            return None
        for vecino, costo in self._adyacencias[origen]:
            if vecino == destino:
                return costo
        return None