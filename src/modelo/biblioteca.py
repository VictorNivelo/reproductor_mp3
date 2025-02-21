from modelo.cancion import Cancion
from typing import List, Dict
from pathlib import Path


class Biblioteca:
    canciones: List[Cancion]
    por_titulo: Dict[str, Cancion]
    por_artista: Dict[str, List[Cancion]]
    por_album: Dict[str, List[Cancion]]
    me_gusta: List[Cancion]
    favoritos: List[Cancion]

    # Agregar una canción a la biblioteca
    def agregar_cancion(self, ruta: Path) -> Cancion:
        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        cancion = Cancion.desde_archivo(ruta)
        # Agregar a las colecciones
        self.canciones.append(cancion)
        self.por_titulo[cancion.titulo] = cancion
        # Agregar a artistas
        if cancion.artista not in self.por_artista:
            self.por_artista[cancion.artista] = []
        self.por_artista[cancion.artista].append(cancion)
        # Agregar a álbumes
        if cancion.album not in self.por_album:
            self.por_album[cancion.album] = []
        self.por_album[cancion.album].append(cancion)
        return cancion

    # Agregar todas las canciones de un directorio
    def agregar_directorio(self, ruta: Path) -> List[Cancion]:
        if not ruta.is_dir():
            raise NotADirectoryError(f"No es un directorio: {ruta}")
        canciones_agregadas = []
        formatos = (".mp3", ".wav", ".flac", ".m4a", ".ogg")
        for archivo in ruta.rglob("*"):
            if archivo.suffix.lower() in formatos:
                try:
                    cancion = self.agregar_cancion(archivo)
                    canciones_agregadas.append(cancion)
                except Exception as e:
                    print(f"Error al agregar {archivo}: {e}")
        return canciones_agregadas

    # Eliminar una canción de la biblioteca
    def eliminar_cancion(self, cancion: Cancion) -> bool:
        try:
            # Eliminar de la lista principal
            self.canciones.remove(cancion)
            # Eliminar del diccionario por título
            if cancion.titulo_cancion in self.por_titulo:
                del self.por_titulo[cancion.titulo_cancion]
            # Eliminar de la lista de artistas
            if cancion.artista in self.por_artista:
                self.por_artista[cancion.artista].remove(cancion)
                if not self.por_artista[cancion.artista]:  # Si la lista queda vacía
                    del self.por_artista[cancion.artista]
            # Eliminar de la lista de álbumes
            if cancion.album in self.por_album:
                self.por_album[cancion.album].remove(cancion)
                if not self.por_album[cancion.album]:  # Si la lista queda vacía
                    del self.por_album[cancion.album]
            # Eliminar de me gusta si existe
            if cancion in self.me_gusta:
                self.me_gusta.remove(cancion)
            # Eliminar de favoritos si existe
            if cancion in self.favoritos:
                self.favoritos.remove(cancion)
            return True
        except ValueError:
            return False

    # Eliminar todas las canciones de un directorio
    def eliminar_directorio(self, ruta: Path) -> List[Cancion]:
        if not ruta.is_dir():
            raise NotADirectoryError(f"No es un directorio: {ruta}")
        canciones_eliminadas = []
        # Encontrar todas las canciones del directorio
        for cancion in self.canciones[:]:  # Creamos una copia para iterar
            if str(ruta) in str(cancion.ruta_cancion):
                if self.eliminar_cancion(cancion):
                    canciones_eliminadas.append(cancion)
        return canciones_eliminadas

    # Agrega una canción a la lista me gusta
    def marcar_me_gusta(self, cancion: Cancion):
        cancion.me_gusta = not cancion.me_gusta
        if cancion.me_gusta:
            self.me_gusta.append(cancion)
        else:
            self.me_gusta.remove(cancion)

    # Agrega una canción a la lista de favoritos
    def marcar_favorito(self, cancion: Cancion):
        cancion.favorito = not cancion.favorito
        if cancion.favorito:
            self.favoritos.append(cancion)
        else:
            self.favoritos.remove(cancion)

    # Buscar canciones por texto en título, artista y álbum
    def buscar(self, texto: str) -> List[Cancion]:
        texto = texto.lower()
        return [
            cancion
            for cancion in self.canciones
            if texto in cancion.titulo_cancion.lower()
            or texto in cancion.artista.lower()
            or texto in cancion.album.lower()
        ]

    # Ordenar las canciones por un criterio
    def ordenar_por(self, criterio: str) -> List[Cancion]:
        if criterio == "titulo":
            return sorted(self.canciones, key=lambda x: x.titulo)
        elif criterio == "artista":
            return sorted(self.canciones, key=lambda x: x.artista)
        elif criterio == "album":
            return sorted(self.canciones, key=lambda x: x.album)
        elif criterio == "duracion":
            return sorted(self.canciones, key=lambda x: x.duracion)
        return self.canciones
