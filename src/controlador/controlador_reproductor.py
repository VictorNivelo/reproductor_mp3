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
        # Etiquetas de tiempo
        self.etiqueta_tiempo_actual = None
        self.etiqueta_tiempo_total = None
        self.timer_id = None
        # Barra de progreso
        self.barra_progreso = None
        # Inicializar pygame
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
        self.etiqueta_artista.configure(text="Artista: ")
        self.etiqueta_album.configure(text="Álbum: ")
        self.etiqueta_anio.configure(text="Lanzamiento: ")
        self.etiqueta_imagen.configure(text="Sin carátula")

    # Método que establece las etiquetas de tiempo
    def establecer_etiquetas_tiempo(self, etiqueta_actual, etiqueta_total):
        self.etiqueta_tiempo_actual = etiqueta_actual
        self.etiqueta_tiempo_total = etiqueta_total

    # Método que establece la barra de progreso
    def establecer_barra_progreso(self, barra):
        self.barra_progreso = barra

    # Método que actualiza la información de la interfaz
    def actualizar_informacion_interfaz(self):
        if self.cancion_actual and self.etiqueta_nombre:
            # Actualizar texto de las etiquetas
            self.etiqueta_nombre.configure(text=self.cancion_actual.titulo_cancion)
            self.etiqueta_artista.configure(text=f"Artista: {self.cancion_actual.artista}")
            self.etiqueta_album.configure(text=f"Álbum: {self.cancion_actual.album}")
            self.etiqueta_anio.configure(text=f"Lanzamiento: {self.cancion_actual.fecha_formateada}")
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

    # Método que actualiza el tiempo de reproducción de la canción
    def actualizar_tiempo(self):
        if self.reproduciendo and self.cancion_actual:
            try:
                # Obtener tiempo actual y total en segundos
                tiempo_total = self.cancion_actual.duracion
                tiempo_actual = pygame.mixer.music.get_pos() / 1000
                # Verificar si la canción ha terminado
                if tiempo_actual < 0:
                    self.detener_reproduccion()
                    return
                # Actualizar barra de progreso
                if self.barra_progreso:
                    progreso = tiempo_actual / tiempo_total if tiempo_total > 0 else 0
                    self.barra_progreso.set(progreso)
                # Convertir a formato mm:ss
                minutos_actual = int(tiempo_actual // 60)
                segundos_actual = int(tiempo_actual % 60)
                minutos_total = int(tiempo_total // 60)
                segundos_total = int(tiempo_total % 60)
                # Actualizar etiquetas
                if self.etiqueta_tiempo_actual:
                    self.etiqueta_tiempo_actual.configure(text=f"{minutos_actual:02d}:{segundos_actual:02d}")
                if self.etiqueta_tiempo_total:
                    self.etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")
                # Programar próxima actualización solo si está reproduciendo
                if self.reproduciendo:
                    if self.timer_id:
                        self.etiqueta_tiempo_actual.after_cancel(self.timer_id)
                    self.timer_id = self.etiqueta_tiempo_actual.after(100, self.actualizar_tiempo)
            except Exception as e:
                print(f"Error al actualizar tiempo: {e}")

    # Método que reproduce una canción
    def reproducir_cancion(self, cancion: Cancion) -> None:
        if self.timer_id:
            self.etiqueta_tiempo_actual.after_cancel(self.timer_id)
            self.timer_id = None
        self.cancion_actual = cancion
        pygame.mixer.music.load(str(cancion.ruta_cancion))
        pygame.mixer.music.play()
        self.reproduciendo = True
        self.actualizar_informacion_interfaz()
        # Iniciar actualización de tiempo
        self.actualizar_tiempo()

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
        if self.timer_id:
            self.etiqueta_tiempo_actual.after_cancel(self.timer_id)
            self.timer_id = None
        pygame.mixer.music.stop()
        self.reproduciendo = False
        # Resetear etiquetas de tiempo y barra de progreso
        if self.etiqueta_tiempo_actual:
            self.etiqueta_tiempo_actual.configure(text="00:00")
        if self.etiqueta_tiempo_total:
            self.etiqueta_tiempo_total.configure(text="00:00")
        if self.barra_progreso:
            self.barra_progreso.set(0)

    # Método que ajusta el volumen de la canción
    @staticmethod
    def ajustar_volumen(volumen: float) -> None:
        pygame.mixer.music.set_volume(volumen / 100.0)
