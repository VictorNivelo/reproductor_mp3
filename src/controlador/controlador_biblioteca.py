from modelo.biblioteca import Biblioteca
from customtkinter import CTkButton
from modelo.cancion import Cancion
from pathlib import Path
from constantes import *


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
