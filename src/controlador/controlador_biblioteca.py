from modelo.biblioteca import Biblioteca
from customtkinter import CTkButton
from modelo.cancion import Cancion
from pathlib import Path
from constantes import *


class ControladorBiblioteca:
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.vista_botones = {}
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

    # Métodos que actualizan la vista de las canciones en la biblioteca
    def actualizar_vista_canciones(self, panel_botones, controlador_tema, controlador_reproductor) -> None:
        # Limpiar botones existentes
        for boton in self.vista_botones.values():
            boton.destroy()
        self.vista_botones.clear()
        # Crear nuevos botones para cada canción
        for cancion in self.biblioteca.canciones:
            self.crear_boton_cancion(cancion, panel_botones, controlador_tema, controlador_reproductor)

    # Métodos que crean botones para cada canción en la biblioteca
    def crear_boton_cancion(
        self, cancion: Cancion, panel_botones, controlador_tema, controlador_reproductor
    ) -> None:
        boton = CTkButton(
            panel_botones,
            height=28,
            fg_color=BOTON_CLARO,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text=f"{cancion.titulo_cancion} - {cancion.artista}",
            hover_color=HOVER_CLARO,
            command=lambda: controlador_reproductor.reproducir_cancion(cancion),
        )
        boton.pack(fill="both", pady=2)
        controlador_tema.registrar_botones(f"cancion_{cancion.titulo_cancion}", boton)
        self.vista_botones[cancion] = boton
