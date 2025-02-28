from modelo.biblioteca import Biblioteca
from modelo.cancion import Cancion
from pathlib import Path


class ControladorBiblioteca:
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.cancion_actual = None

    # Métodos que agregan canciones a la biblioteca
    def agregar_cancion(self, ruta: Path) -> Cancion:
        try:
            return self.biblioteca.agregar_cancion(ruta)
        except Exception as e:
            raise ValueError(f"Error al agregar la canción: {e}")

    # Métodos que agregan directorios de canciones a la biblioteca
    def agregar_directorio(self, ruta: Path) -> list:
        try:
            return self.biblioteca.agregar_directorio(ruta)
        except Exception as e:
            print(f"Error al agregar el directorio: {e}")
            return []

    # Métodos que marcan canciones como me gusta
    def marcar_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.marcar_me_gusta(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como me gusta: {e}")
            return False

    # Métodos que marcan canciones como favoritas
    def marcar_favorito_controlador(self, cancion):
        try:
            self.biblioteca.marcar_favorito(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como favorito: {e}")
            return False
