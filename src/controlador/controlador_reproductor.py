from modelo.cancion import Cancion
import customtkinter as ctk
from io import BytesIO
from PIL import Image
import pygame
import random
import time


class ControladorReproductor:
    def __init__(self):
        self.cancion_actual = None
        self.reproduciendo = False
        # Tiempo de reproducción
        self.tiempo_inicio = None
        self.tiempo_acumulado = 0
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
        # Lista de reproducción
        self.lista_reproduccion = []
        self.indice_actual = -1
        # Modo de repetición
        self.modo_repeticion = 0
        # Modo aleatorio
        self.modo_aleatorio = False
        # Historial de reproducción aleatoria
        self.historial_aleatorio = []
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

    # Método que establece las etiquetas de tiempo
    def establecer_etiquetas_tiempo(self, etiqueta_actual, etiqueta_total):
        self.etiqueta_tiempo_actual = etiqueta_actual
        self.etiqueta_tiempo_total = etiqueta_total

    # Método que actualiza el tiempo de reproducción de la canción
    def actualizar_tiempo(self):
        if self.cancion_actual:
            if self.tiempo_inicio is not None:
                tiempo_actual = self.tiempo_acumulado + (time.perf_counter() - self.tiempo_inicio)
            else:
                tiempo_actual = self.tiempo_acumulado
            tiempo_total = self.cancion_actual.duracion
            # Si el tiempo alcanzó o superó la duración, fijarlo en el total y detener la reproducción.
            if tiempo_actual >= tiempo_total:
                if self.barra_progreso:
                    self.barra_progreso.set(1)
                minutos_total = int(tiempo_total // 60)
                segundos_total = int(tiempo_total % 60)
                if self.etiqueta_tiempo_actual:
                    self.etiqueta_tiempo_actual.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")
                if self.etiqueta_tiempo_total:
                    self.etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")
                # Manejar el final de la canción según el modo de repetición
                if self.modo_repeticion == 1:  # Repetir canción actual
                    # Reiniciar la misma canción
                    self.reproducir_cancion(self.cancion_actual)
                    return
                elif self.lista_reproduccion and (
                    self.indice_actual < len(self.lista_reproduccion) - 1 or self.modo_repeticion == 2
                ):
                    # Reproducir siguiente canción
                    self.reproducir_siguiente()
                    return
                else:
                    # No hay más canciones o no está activada la repetición
                    self.detener_reproduccion()
                    # Señalizar a la vista que terminó la reproducción
                    self.reproduciendo = False
                    return True
            # Actualización normal del progreso
            if self.barra_progreso:
                progreso = tiempo_actual / tiempo_total if tiempo_total > 0 else 0
                self.barra_progreso.set(progreso)
            minutos_actual = int(tiempo_actual // 60)
            segundos_actual = int(tiempo_actual % 60)
            minutos_total = int(tiempo_total // 60)
            segundos_total = int(tiempo_total % 60)
            if self.etiqueta_tiempo_actual:
                self.etiqueta_tiempo_actual.configure(text=f"{minutos_actual:02d}:{segundos_actual:02d}")
            if self.etiqueta_tiempo_total:
                self.etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")
            self.timer_id = self.etiqueta_tiempo_actual.after(100, self.actualizar_tiempo)
        return False

    # Método que establece la barra de progreso
    def establecer_barra_progreso(self, barra):
        self.barra_progreso = barra

    # Método que establece la lista de reproducción actual
    def establecer_lista_reproduccion(self, canciones, indice=0):
        self.lista_reproduccion = canciones
        self.indice_actual = indice if 0 <= indice < len(canciones) else 0

    # Método que establece el modo de repetición
    def establecer_modo_repeticion(self, modo):
        self.modo_repeticion = modo

    # Método para establecer el modo de reproducción (aleatorio o secuencial)
    def establecer_modo_aleatorio(self, aleatorio: bool):
        self.modo_aleatorio = aleatorio
        # Resetear el historial cuando cambiamos de modo
        self.historial_aleatorio = []

    # Método que reproduce una canción
    def reproducir_cancion(self, cancion: Cancion) -> None:
        if self.timer_id:
            self.etiqueta_tiempo_actual.after_cancel(self.timer_id)
            self.timer_id = None
        self.cancion_actual = cancion
        # Actualizar el índice si la canción está en la lista de reproducción
        if self.lista_reproduccion:
            try:
                nuevo_indice = self.lista_reproduccion.index(cancion)
                # Si cambiamos el índice y estamos en modo aleatorio, actualizar historial
                if nuevo_indice != self.indice_actual and self.modo_aleatorio:
                    self.indice_actual = nuevo_indice
                    # Agregar al historial si no está ya
                    if self.indice_actual not in self.historial_aleatorio:
                        self.historial_aleatorio.append(self.indice_actual)
                else:
                    self.indice_actual = nuevo_indice
            except ValueError:
                # Si la canción no está en la lista, mantener el índice actual
                pass
        pygame.mixer.music.load(str(cancion.ruta_cancion))
        pygame.mixer.music.play()
        self.reproduciendo = True
        # Reiniciar cronómetro
        self.tiempo_acumulado = 0
        self.tiempo_inicio = time.perf_counter()
        self.actualizar_informacion_interfaz()
        self.actualizar_tiempo()

    # Métodos que controlan la reproducción de la canción
    def pausar_reproduccion(self) -> None:
        if self.reproduciendo:
            pygame.mixer.music.pause()
            # Acumular tiempo transcurrido hasta el momento de la pausa
            self.tiempo_acumulado += time.perf_counter() - self.tiempo_inicio
            self.tiempo_inicio = None
            # En este caso no cancelamos el timer para que la interfaz siga actualizándose
            self.reproduciendo = False

    # Método que reanuda la reproducción de la canción
    def reanudar_reproduccion(self) -> None:
        if not self.reproduciendo and self.cancion_actual:
            pygame.mixer.music.unpause()
            self.tiempo_inicio = time.perf_counter()
            self.reproduciendo = True
            self.actualizar_tiempo()

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
        return False

    # Método que reproduce la siguiente canción
    def reproducir_siguiente(self):
        if not self.lista_reproduccion:
            return False
        # Determinar el siguiente índice dependiendo del modo
        if self.modo_aleatorio:
            # Modo aleatorio
            if len(self.historial_aleatorio) >= len(self.lista_reproduccion):
                # Hemos reproducido todas las canciones
                if self.modo_repeticion == 2:  # Si está activado repetir todo
                    # Limpiar completamente el historial para permitir reproducir todas las canciones de nuevo
                    self.historial_aleatorio = []
                    # Elegir una nueva canción aleatoria
                    self.indice_actual = random.randint(0, len(self.lista_reproduccion) - 1)
                    self.historial_aleatorio.append(self.indice_actual)
                else:
                    # No repetir, detener reproducción
                    self.detener_reproduccion()
                    return False
            else:
                # Generar índice aleatorio que no esté en el historial
                indices_disponibles = [
                    i for i in range(len(self.lista_reproduccion)) if i not in self.historial_aleatorio
                ]
                if indices_disponibles:
                    self.indice_actual = random.choice(indices_disponibles)
                    self.historial_aleatorio.append(self.indice_actual)
                else:
                    return False
        else:
            # Modo secuencial
            if self.indice_actual < len(self.lista_reproduccion) - 1:
                self.indice_actual += 1
            else:
                # Si estamos en modo repetición todo (2), volver al principio
                if self.modo_repeticion == 2:
                    self.indice_actual = 0
                else:
                    # Si no hay repetición, detener la reproducción
                    self.detener_reproduccion()
                    return False
        cancion = self.lista_reproduccion[self.indice_actual]
        self.reproducir_cancion(cancion)
        return True

    # Método que reproduce la canción anterior
    def reproducir_anterior(self):
        if not self.lista_reproduccion:
            return False
        if self.modo_aleatorio:
            # En modo aleatorio, retrocedemos en el historial
            if len(self.historial_aleatorio) > 1:
                self.historial_aleatorio.pop()  # Quitar la canción actual
                self.indice_actual = self.historial_aleatorio[-1]  # Volver a la anterior
            else:
                self.indice_actual = random.randint(0, len(self.lista_reproduccion) - 1)
        else:
            # Modo secuencial
            if self.indice_actual > 0:
                self.indice_actual -= 1
            else:
                # Ir al final si es la primera canción
                self.indice_actual = len(self.lista_reproduccion) - 1
        cancion = self.lista_reproduccion[self.indice_actual]
        self.reproducir_cancion(cancion)
        return True

    # Método para adelantar la reproducción en segundos
    def adelantar_reproduccion(self, segundos=10):
        if self.reproduciendo and self.cancion_actual:
            # Obtener la posición actual
            if self.tiempo_inicio is not None:
                tiempo_actual = self.tiempo_acumulado + (time.perf_counter() - self.tiempo_inicio)
            else:
                tiempo_actual = self.tiempo_acumulado
            # Calcular nueva posición
            nuevo_tiempo = min(tiempo_actual + segundos, self.cancion_actual.duracion)
            # Detener reproducción actual
            pygame.mixer.music.stop()
            # Cargar y reproducir desde la nueva posición
            pygame.mixer.music.load(str(self.cancion_actual.ruta_cancion))
            pygame.mixer.music.play(start=nuevo_tiempo)
            # Actualizar tiempo acumulado
            self.tiempo_acumulado = nuevo_tiempo
            self.tiempo_inicio = time.perf_counter()
            # Actualizar interfaz
            if self.barra_progreso:
                progreso = nuevo_tiempo / self.cancion_actual.duracion
                self.barra_progreso.set(progreso)

    # Método para retroceder la reproducción en segundos
    def retroceder_reproduccion(self, segundos=10):
        if self.reproduciendo and self.cancion_actual:
            # Obtener la posición actual
            if self.tiempo_inicio is not None:
                tiempo_actual = self.tiempo_acumulado + (time.perf_counter() - self.tiempo_inicio)
            else:
                tiempo_actual = self.tiempo_acumulado
            # Calcular nueva posición
            nuevo_tiempo = max(0, tiempo_actual - segundos)
            # Detener reproducción actual
            pygame.mixer.music.stop()
            # Cargar y reproducir desde la nueva posición
            pygame.mixer.music.load(str(self.cancion_actual.ruta_cancion))
            pygame.mixer.music.play(start=nuevo_tiempo)
            # Actualizar tiempo acumulado
            self.tiempo_acumulado = nuevo_tiempo
            self.tiempo_inicio = time.perf_counter()
            # Actualizar interfaz
            if self.barra_progreso:
                progreso = nuevo_tiempo / self.cancion_actual.duracion
                self.barra_progreso.set(progreso)

    # Método que ajusta el volumen de la canción
    @staticmethod
    def ajustar_volumen(volumen: float) -> None:
        pygame.mixer.music.set_volume(volumen / 100.0)
