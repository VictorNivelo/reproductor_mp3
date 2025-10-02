from modelo.biblioteca import Biblioteca
from modelo.cancion import Cancion
from typing import Dict, List
from pathlib import Path


class ControladorBiblioteca:

    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca

    # Método para agregar una cancion a la biblioteca
    def agregar_cancion_controlador(self, ruta: Path) -> Cancion:
        try:
            return self.biblioteca.agregar_cancion_biblioteca(ruta)
        except Exception as e:
            raise Exception(f"Error al agregar la canción: {e}")

    # Método para agregar una carpeta de canciones a la biblioteca
    def agregar_carpeta_canciones_controlador(self, ruta: Path) -> list:
        try:
            return self.biblioteca.agregar_carpeta_canciones_biblioteca(ruta)
        except Exception as e:
            raise Exception(f"Error al agregar las canciones de la carpeta: {e}")

    # Método para eliminar una cancion de la biblioteca
    def eliminar_cancion_controlador(self, cancion: Cancion) -> None:
        try:
            self.biblioteca.eliminar_cancion_biblioteca(cancion)
        except Exception as e:
            raise Exception(f"Error al eliminar la canción: {e}")

    # Método para eliminar un álbum de canciones de la biblioteca
    def eliminar_album_controlador(self, album: str) -> None:
        try:
            canciones_album = self.obtener_canciones_album_controlador(album)
            for cancion in canciones_album:
                self.biblioteca.eliminar_cancion_biblioteca(cancion)
        except Exception as e:
            raise Exception(f"Error al eliminar el álbum: {e}")

    # Método para eliminar un artista de canciones de la biblioteca
    def eliminar_artista_controlador(self, artista: str) -> None:
        try:
            canciones_artista = self.obtener_canciones_artista_controlador(artista)
            for cancion in canciones_artista:
                self.biblioteca.eliminar_cancion_biblioteca(cancion)
        except Exception as e:
            raise Exception(f"Error al eliminar el artista: {e}")

    # Método para eliminar una carpeta de canciones de la biblioteca
    def eliminar_carpeta_canciones_controlador(self, ruta: Path) -> None:
        try:
            self.biblioteca.eliminar_carpeta_canciones_biblioteca(ruta)
        except Exception as e:
            raise Exception(f"Error al eliminar las canciones de la carpeta: {e}")

    # Método para establecer la canción actual
    def establecer_cancion_actual_controlador(self, cancion: Cancion | None):
        self.biblioteca.establecer_cancion_actual_biblioteca(cancion)

    # Método para obtener la canción actual
    def obtener_cancion_actual_controlador(self) -> Cancion | None:
        return self.biblioteca.obtener_cancion_actual_biblioteca()

    # Método para obtener todas las canciones de la biblioteca
    def obtener_todas_canciones_controlador(self) -> list:
        try:
            return self.biblioteca.obtener_canciones_biblioteca()
        except Exception as e:
            raise Exception(f"Error al obtener las canciones: {e}")

    # Método para obtener todos los álbumes de la biblioteca
    def obtener_albumes_controlador(self) -> Dict[str, List[Cancion]]:
        try:
            return self.biblioteca.obtener_albums_biblioteca()
        except Exception as e:
            raise Exception(f"Error al obtener los álbumes: {e}")

    # Método para obtener todos los artistas de la biblioteca
    def obtener_artistas_controlador(self) -> Dict[str, List[Cancion]]:
        try:
            return self.biblioteca.obtener_artistas_biblioteca()
        except Exception as e:
            raise Exception(f"Error al obtener los artistas: {e}")

    # Método para obtener canciones de un álbum
    def obtener_canciones_album_controlador(self, nombre_album):
        try:
            return self.biblioteca.obtener_canciones_de_album_biblioteca(nombre_album)
        except Exception as e:
            raise Exception(f"Error al obtener las canciones del álbum: {e}")

    # Método para obtener canciones de un artista
    def obtener_canciones_artista_controlador(self, nombre_artista):
        try:
            return self.biblioteca.obtener_canciones_de_artista_biblioteca(nombre_artista)
        except Exception as e:
            raise Exception(f"Error al obtener las canciones del artista: {e}")

    # Método para ver si una cancion está en "Me gusta"
    def verificar_me_gusta_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.me_gusta
        except Exception as e:
            print(f"Error al verificar 'Me gusta': {e}")
            return False

    # Método para obtener todas las canciones de "Me gusta"
    def obtener_canciones_me_gusta_controlador(self):
        try:
            return self.biblioteca.me_gusta
        except Exception as e:
            print(f"Error al obtener las canciones de 'Me gusta': {e}")
            return []

    # Método para agregar una canción a "Me gusta"
    def agregar_cancion_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar la canción a 'Me gusta': {e}")

    # Método para agregar un álbum a "Me gusta"
    def agregar_album_me_gusta_controlador(self, album):
        try:
            canciones_album = self.obtener_canciones_album_controlador(album)
            for cancion in canciones_album:
                self.biblioteca.agregar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar el álbum a 'Me gusta': {e}")

    # Método para agregar un artista a "Me gusta"
    def agregar_artista_me_gusta_controlador(self, artista):
        try:
            canciones_artista = self.obtener_canciones_artista_controlador(artista)
            for cancion in canciones_artista:
                self.biblioteca.agregar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar el artista a 'Me gusta': {e}")

    # Método para quitar una canción de "Me gusta"
    def quitar_cancion_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.eliminar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar la canción de 'Me gusta': {e}")

    # Método para quitar un álbum de "Me gusta"
    def quitar_album_me_gusta_controlador(self, album):
        try:
            canciones_album = self.obtener_canciones_album_controlador(album)
            for cancion in canciones_album:
                self.biblioteca.eliminar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar el álbum de 'Me gusta': {e}")

    # Método para quitar un artista de "Me gusta"
    def quitar_artista_me_gusta_controlador(self, artista):
        try:
            canciones_artista = self.obtener_canciones_artista_controlador(artista)
            for cancion in canciones_artista:
                self.biblioteca.eliminar_cancion_me_gusta_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar el artista de 'Me gusta': {e}")

    # Método para ver si una cancion está en "Favorito"
    def verificar_favorito_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.favorito
        except Exception as e:
            print(f"Error al verificar 'Favorito': {e}")
            return False

    # Método para obtener todas las canciones de "Favorito"
    def obtener_canciones_favorito_controlador(self):
        try:
            return self.biblioteca.favorito
        except Exception as e:
            print(f"Error al obtener las canciones de 'Favorito': {e}")
            return []

    # Método para agregar una canción a "Favorito"
    def agregar_cancion_favorito_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar la canción a 'Favorito': {e}")

    # Método para agregar un álbum a "Favorito"
    def agregar_album_favorito_controlador(self, album):
        try:
            canciones_album = self.obtener_canciones_album_controlador(album)
            for cancion in canciones_album:
                self.biblioteca.agregar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar el álbum a 'Favorito': {e}")

    # Método para agregar un artista a "Favorito"
    def agregar_artista_favorito_controlador(self, artista):
        try:
            canciones_artista = self.obtener_canciones_artista_controlador(artista)
            for cancion in canciones_artista:
                self.biblioteca.agregar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al agregar el artista a 'Favorito': {e}")

    # Método para quitar una canción de "Favorito"
    def quitar_cancion_favorito_controlador(self, cancion):
        try:
            self.biblioteca.eliminar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar la canción de 'Favorito': {e}")

    # Método para quitar un álbum de "Favorito"
    def quitar_album_favorito_controlador(self, album):
        try:
            canciones_album = self.obtener_canciones_album_controlador(album)
            for cancion in canciones_album:
                self.biblioteca.eliminar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar el álbum de 'Favorito': {e}")

    # Método para quitar un artista de "Favorito"
    def quitar_artista_favorito_controlador(self, artista):
        try:
            canciones_artista = self.obtener_canciones_artista_controlador(artista)
            for cancion in canciones_artista:
                self.biblioteca.eliminar_cancion_favorito_biblioteca(cancion)
        except Exception as e:
            print(f"Error al quitar el artista de 'Favorito': {e}")

    # Método para buscar canciones en la biblioteca
    def buscar_canciones_controlador(self, termino_busqueda):
        try:
            return self.biblioteca.buscar_cancion_biblioteca(termino_busqueda)
        except Exception as e:
            raise Exception(f"Error al buscar canciones: {e}")

    # Método para ordenar canciones en la biblioteca
    def ordenar_canciones_controlador(self, criterio: str, descendente: bool = False) -> list:
        try:
            return self.biblioteca.ordenar_canciones_biblioteca(criterio, descendente)
        except Exception as e:
            raise Exception(f"Error al ordenar las canciones: {e}")

    # ====================================================================================================
    # Revisar
    # Método para obtener la caratula de un album
    def obtener_caratula_album_controlador(self, nombre_album, formato="bytes", ancho=None, alto=None):
        try:
            return self.biblioteca.obtener_caratula_album_biblioteca(nombre_album, formato, ancho, alto)
        except Exception as e:
            print(f"Error al obtener carátula del álbum: {e}")
            return None
