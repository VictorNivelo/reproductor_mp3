from modelo.biblioteca import Biblioteca
from modelo.cancion import Cancion
from pathlib import Path


class ControladorBiblioteca:
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.cancion_actual = None

    # Método que agregan canciones a la biblioteca
    def agregar_cancion_controlador(self, ruta: Path) -> Cancion:
        try:
            return self.biblioteca.agregar_cancion_biblioteca(ruta)
        except Exception as e:
            raise ValueError(f"Error al agregar la canción: {e}")

    # Método que agregan directorios de canciones a la biblioteca
    def agregar_directorio_controlador(self, ruta: Path) -> list:
        try:
            return self.biblioteca.agregar_directorio_biblioteca(ruta)
        except Exception as e:
            print(f"Error al agregar el directorio: {e}")
            return []

    # Método para obtener todas las canciones de un artista específico
    def obtener_canciones_artista_controlador(self, nombre_artista):
        try:
            if nombre_artista in self.biblioteca.por_artista:
                return self.biblioteca.por_artista[nombre_artista]
            return []
        except Exception as e:
            print(f"Error al obtener canciones del artista: {e}")
            return []

    # Método para obtener todas las canciones de un álbum específico
    def obtener_canciones_album_controlador(self, nombre_album):
        try:
            if nombre_album in self.biblioteca.por_album:
                return self.biblioteca.por_album[nombre_album]
            return []
        except Exception as e:
            print(f"Error al obtener canciones del álbum: {e}")
            return []

    # Método que verifica si una canción está marcada como "Me gusta"
    def verificar_me_gusta_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.me_gusta
        except Exception as e:
            print(f"Error al verificar me gusta: {e}")
            return False

    # Método que agrega canciones como me gusta
    def agregar_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_me_gusta_biblioteca(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como me gusta: {e}")
            return False

    # Método que verifica si una canción está marcada como favorita
    def verificar_favorito_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.favorito
        except Exception as e:
            print(f"Error al verificar favorito: {e}")
            return False

    # Método que agrega canciones como favoritas
    def agregar_favorito_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_favorito_biblioteca(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como favorito: {e}")
            return False

    # Método para obtener la caratula de un album
    def obtener_caratula_album_controlador(self, nombre_album, formato="bytes", ancho=None, alto=None):
        try:
            return self.biblioteca.obtener_caratula_album_biblioteca(nombre_album, formato, ancho, alto)
        except Exception as e:
            print(f"Error al obtener carátula del álbum: {e}")
            return None

    # Método para obtener la caratula de un artista
    def obtener_caratula_artista_controlador(self, nombre_artista, formato="bytes", ancho=None, alto=None):
        try:
            return self.biblioteca.obtener_caratula_artista_biblioteca(nombre_artista, formato, ancho, alto)
        except Exception as e:
            print(f"Error al obtener carátula del artista: {e}")
            return None
