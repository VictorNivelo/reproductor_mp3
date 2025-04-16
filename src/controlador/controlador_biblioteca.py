from modelo.biblioteca import Biblioteca
from modelo.cancion import Cancion
from pathlib import Path


class ControladorBiblioteca:
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.cancion_actual = None

    # Métodos que agregan canciones a la biblioteca
    def agregar_cancion_controlador(self, ruta: Path) -> Cancion:
        try:
            return self.biblioteca.agregar_cancion_biblioteca(ruta)
        except Exception as e:
            raise ValueError(f"Error al agregar la canción: {e}")

    # Métodos que agregan directorios de canciones a la biblioteca
    def agregar_directorio_controlador(self, ruta: Path) -> list:
        try:
            return self.biblioteca.agregar_directorio_biblioteca(ruta)
        except Exception as e:
            print(f"Error al agregar el directorio: {e}")
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

    # Métodos que agrega canciones como me gusta
    def agregar_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.agregar_me_gusta_biblioteca(cancion)
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

    # Métodos que agrega canciones como favoritas
    def agregar_favorito_controlador(self, cancion):
        try:
            self.biblioteca.agregar_favorito_biblioteca(cancion)
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
