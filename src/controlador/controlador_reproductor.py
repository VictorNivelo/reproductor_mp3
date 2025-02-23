from modelo.cancion import Cancion
import customtkinter as ctk
from io import BytesIO
from PIL import Image
import pygame


class ControladorReproductor:
    def __init__(self):
        self.cancion_actual = None
        self.reproduciendo = False
        # Etiquetas de la interfaz
        self.etiqueta_nombre = None
        self.etiqueta_artista = None
        self.etiqueta_album = None
        self.etiqueta_anio = None
        self.etiqueta_imagen = None
        pygame.mixer.init()

    # Método que establece las etiquetas de la interfaz
    def establecer_informacion_interfaz(self, nombre, artista, album, anio, imagen):
        self.etiqueta_nombre = nombre
        self.etiqueta_artista = artista
        self.etiqueta_album = album
        self.etiqueta_anio = anio
        self.etiqueta_imagen = imagen
        # Establecer texto inicial
        self.etiqueta_nombre.configure(text="Sin reproducción")
        self.etiqueta_artista.configure(text="Artista: --")
        self.etiqueta_album.configure(text="Álbum: --")
        self.etiqueta_anio.configure(text="Año: --")
        self.etiqueta_imagen.configure(text="Sin carátula")

    # Método que actualiza la información de la interfaz
    def actualizar_informacion_interfaz(self):
        if self.cancion_actual and self.etiqueta_nombre:
            # Actualizar texto de las etiquetas
            self.etiqueta_nombre.configure(text=self.cancion_actual.titulo_cancion)
            self.etiqueta_artista.configure(text=f"Artista: {self.cancion_actual.artista}")
            self.etiqueta_album.configure(text=f"Álbum: {self.cancion_actual.album}")
            self.etiqueta_anio.configure(text=f"Año: {self.cancion_actual.anio}")
            # Actualizar carátula
            if self.cancion_actual.caratula_cancion:
                try:
                    # Crear imagen desde los bytes de la carátula
                    imagen = Image.open(BytesIO(self.cancion_actual.caratula_cancion))
                    # Redimensionar la imagen manteniendo la proporción
                    ancho = 300
                    ratio = ancho / float(imagen.size[0])
                    alto = int(float(imagen.size[1]) * float(ratio))
                    imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
                    # Convertir a formato CTkImage
                    foto = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))
                    # Actualizar la etiqueta
                    self.etiqueta_imagen.configure(image=foto, text="")
                except Exception as e:
                    print(f"Error al cargar la carátula: {e}")
                    self.etiqueta_imagen.configure(image=None, text="Sin carátula")
            else:
                self.etiqueta_imagen.configure(image=None, text="Sin carátula")

    # Método que reproduce una canción
    def reproducir_cancion(self, cancion: Cancion) -> None:
        self.cancion_actual = cancion
        pygame.mixer.music.load(str(cancion.ruta_cancion))
        pygame.mixer.music.play()
        self.reproduciendo = True
        self.actualizar_informacion_interfaz()

    # Métodos que controlan la reproducción de la canción
    def pausar_reproduccion(self) -> None:
        if self.reproduciendo:
            pygame.mixer.music.pause()
            self.reproduciendo = False

    # Método que reanuda la reproducción de la canción
    def reanudar_reproduccion(self) -> None:
        if not self.reproduciendo:
            pygame.mixer.music.unpause()
            self.reproduciendo = True

    # Método que detiene la reproducción de la canción
    def detener_reproduccion(self) -> None:
        pygame.mixer.music.stop()
        self.reproduciendo = False

    # Método que ajusta el volumen de la canción
    @staticmethod
    def ajustar_volumen(volumen: float) -> None:
        pygame.mixer.music.set_volume(volumen / 100.0)
