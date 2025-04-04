from controlador.controlador_archivos import ControladorArchivos
from modelo.cancion import Cancion
from utiles import Utiles
from constantes import *
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
        # Carátula de la canción
        self.foto_caratula = None
        # Etiquetas de la interfaz
        self.etiqueta_nombre = None
        self.etiqueta_artista = None
        self.etiqueta_album = None
        self.etiqueta_anio = None
        self.etiqueta_imagen = None
        # Textos de la interfaz
        self.texto_titulo = None
        self.texto_artista = None
        self.texto_album = None
        # Desplazamiento de textos largos
        self.direccion_desplazamiento = None
        self.posicion_desplazamiento = None
        self.desplazamiento_activo = None
        # Temporizador de desplazamiento
        self.id_marcador_tiempo = None
        # Etiquetas de tiempo
        self.etiqueta_tiempo_actual = None
        self.etiqueta_tiempo_total = None
        self.id_temporizador = None
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
        # Instancia de Utiles
        self.utiles = Utiles()

    # Método que actualiza la carátula de la canción
    def actualizar_caratula(self, caratula_bytes=None, ancho=300):
        try:
            # Si no se proporcionan bytes, usar la carátula de la canción actual
            if caratula_bytes is None and self.cancion_actual:
                caratula_bytes = self.cancion_actual.caratula_cancion
            if caratula_bytes and self.etiqueta_imagen:
                foto, _, _ = self.utiles.crear_imagen_desde_bytes(caratula_bytes, ancho=ancho)
                if foto:
                    self.etiqueta_imagen.configure(image=foto, text="")
                    # Guardar referencia para evitar que se pierda por el recolector de basura
                    self.foto_caratula = foto
                    return True
                else:
                    self.etiqueta_imagen.configure(image=None, text="Sin carátula")
            else:
                self.etiqueta_imagen.configure(image=None, text="Sin carátula")
            return False
        except Exception as e:
            print(f"Error al actualizar carátula: {e}")
            self.etiqueta_imagen.configure(image=None, text="Sin carátula")
            return False

    # Método que establece las etiquetas de la interfaz
    def establecer_informacion_interfaz(self, nombre, artista, album, anio, imagen):
        self.etiqueta_nombre = nombre
        self.etiqueta_artista = artista
        self.etiqueta_album = album
        self.etiqueta_anio = anio
        self.etiqueta_imagen = imagen
        # Establecer texto inicial
        self.etiqueta_nombre.configure(text="")
        self.etiqueta_artista.configure(text="")
        self.etiqueta_album.configure(text="")
        self.etiqueta_anio.configure(text="")
        self.etiqueta_imagen.configure(text="Sin carátula")

    # Método que actualiza la información de la interfaz
    def actualizar_informacion_interfaz(self):
        if self.cancion_actual and self.etiqueta_nombre:
            # Guardar información de la canción actual
            self.texto_titulo = self.cancion_actual.titulo_cancion
            self.texto_artista = self.cancion_actual.artista
            self.texto_album = self.cancion_actual.album
            # Configurar texto inicial (sin desplazamiento aún)
            self.etiqueta_nombre.configure(text=self.texto_titulo)
            self.etiqueta_artista.configure(text=self.texto_artista)
            self.etiqueta_album.configure(text=self.texto_album)
            self.etiqueta_anio.configure(text=self.cancion_actual.fecha_formateada)
            # Cancelar cualquier timer de desplazamiento anterior
            if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
                self.etiqueta_nombre.after_cancel(self.id_marcador_tiempo)
                self.id_marcador_tiempo = None
            # Iniciar desplazamiento de textos largos si es necesario
            self.iniciar_desplazamiento_texto()
            # Actualizar carátula
            if self.cancion_actual.caratula_cancion:
                foto, _, _ = self.utiles.crear_imagen_desde_bytes(
                    self.cancion_actual.caratula_cancion, ancho=300
                )
                if foto:
                    self.etiqueta_imagen.configure(image=foto, text="")
                else:
                    self.etiqueta_imagen.configure(image=None, text="Sin carátula")
            else:
                self.etiqueta_imagen.configure(image=None, text="Sin carátula")

    # Método para iniciar desplazamiento de textos largos
    def iniciar_desplazamiento_texto(self):
        # Longitud máxima antes de activar desplazamiento
        longitud_maxima = 75
        # Variables para controlar el desplazamiento
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        # Comprobar si algún texto necesita desplazamiento
        textos = {
            "titulo": (self.texto_titulo, self.etiqueta_nombre),
            "artista": (self.texto_artista, self.etiqueta_artista),
            "album": (self.texto_album, self.etiqueta_album),
        }
        for clave, (texto, etiqueta) in textos.items():
            if len(texto) > longitud_maxima:
                self.desplazamiento_activo[clave] = True
                self.posicion_desplazamiento[clave] = 0
                self.direccion_desplazamiento[clave] = 1  # 1: derecha a izquierda
            else:
                self.desplazamiento_activo[clave] = False
        # Iniciar animación si hay textos para desplazar
        if any(self.desplazamiento_activo.values()):
            self.animar_desplazamiento_texto()

    # Método para animar el desplazamiento del texto
    def animar_desplazamiento_texto(self):
        if not hasattr(self, "desplazamiento_activo"):
            return
        # Si la reproducción está pausada, no animamos el desplazamiento
        if hasattr(self, "reproduciendo") and not self.reproduciendo:
            # Programar verificación periódica para reanudar cuando se reanude la reproducción
            self.id_marcador_tiempo = self.etiqueta_nombre.after(500, self.animar_desplazamiento_texto)
            return
        textos = {
            "titulo": (self.texto_titulo, self.etiqueta_nombre),
            "artista": (self.texto_artista, self.etiqueta_artista),
            "album": (self.texto_album, self.etiqueta_album),
        }
        # Actualizar cada texto que necesite desplazamiento
        for clave, (texto_completo, etiqueta) in textos.items():
            if not self.desplazamiento_activo.get(clave, False):
                continue
            # Obtener posición actual y longitud visible
            pos = self.posicion_desplazamiento[clave]
            longitud_maxima = 75
            # Si el texto es más largo que la longitud máxima, aplicar desplazamiento
            if len(texto_completo) > longitud_maxima:
                # Control de pausa al inicio
                if pos == 0:
                    # Si estamos al inicio, pausar durante más tiempo
                    if not hasattr(self, f"pausa_inicio_{clave}"):
                        setattr(self, f"pausa_inicio_{clave}", 0)
                    pausa_actual = getattr(self, f"pausa_inicio_{clave}")
                    if pausa_actual < 8:  # 8 * 125ms = 1 segundo de pausa
                        setattr(self, f"pausa_inicio_{clave}", pausa_actual + 1)
                        texto_visible = texto_completo[:longitud_maxima]
                        etiqueta.configure(text=texto_visible)
                        continue
                    else:
                        setattr(self, f"pausa_inicio_{clave}", 0)
                # Control de pausa al final
                if pos >= len(texto_completo) - longitud_maxima:
                    # Si llegamos al final, pausar antes de reiniciar
                    if not hasattr(self, f"pausa_final_{clave}"):
                        setattr(self, f"pausa_final_{clave}", 0)
                    pausa_actual = getattr(self, f"pausa_final_{clave}")
                    if pausa_actual < 8:  # 8 * 125ms = 1 segundo de pausa
                        texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                        etiqueta.configure(text=texto_visible)
                        setattr(self, f"pausa_final_{clave}", pausa_actual + 1)
                        continue
                    else:
                        # Reiniciar desde el principio
                        self.posicion_desplazamiento[clave] = 0
                        texto_visible = texto_completo[:longitud_maxima]
                        setattr(self, f"pausa_final_{clave}", 0)
                        etiqueta.configure(text=texto_visible)
                        continue
                # Desplazamiento normal
                texto_visible = texto_completo[pos : pos + longitud_maxima]
                self.posicion_desplazamiento[clave] += 1
                etiqueta.configure(text=texto_visible)
        # Programar próxima actualización
        self.id_marcador_tiempo = self.etiqueta_nombre.after(125, self.animar_desplazamiento_texto)

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
            self.id_temporizador = self.etiqueta_tiempo_actual.after(100, self.actualizar_tiempo)
        return False

    # Método que establece la barra de progreso
    def establecer_barra_progreso(self, barra):
        self.barra_progreso = barra

    # Método que establece la lista de reproducción actual
    def establecer_lista_reproduccion(self, canciones, indice=0):
        self.lista_reproduccion = canciones
        self.indice_actual = indice if 0 <= indice < len(canciones) else 0
        # Guardar la cola automáticamente
        controlador_archivos = ControladorArchivos()
        controlador_archivos.guardar_cola_reproduccion(self)

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
        if self.id_temporizador:
            self.etiqueta_tiempo_actual.after_cancel(self.id_temporizador)
            self.id_temporizador = None
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
        # Guardar la cola automáticamente
        controlador_archivos = ControladorArchivos()
        controlador_archivos.guardar_cola_reproduccion(self)

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
    def detener_reproduccion(self) -> bool:
        if self.id_temporizador:
            self.etiqueta_tiempo_actual.after_cancel(self.id_temporizador)
            self.id_temporizador = None
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

    # Método auxiliar para cambiar la posición de reproducción
    def cambiar_posicion_reproduccion(self, tiempo_segundos):
        if self.reproduciendo and self.cancion_actual:
            # Obtener la posición actual
            if self.tiempo_inicio is not None:
                tiempo_actual = self.tiempo_acumulado + (time.perf_counter() - self.tiempo_inicio)
            else:
                tiempo_actual = self.tiempo_acumulado
            # Calcular nueva posición
            nuevo_tiempo = max(0, min(tiempo_actual + tiempo_segundos, self.cancion_actual.duracion))
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

    # Método para adelantar la reproducción en segundos
    def adelantar_reproduccion(self, segundos=None):
        if segundos is None:
            segundos = TIEMPO_AJUSTE
        self.cambiar_posicion_reproduccion(segundos)

    # Método para retroceder la reproducción en segundos
    def retroceder_reproduccion(self, segundos=None):
        if segundos is None:
            segundos = TIEMPO_AJUSTE
        self.cambiar_posicion_reproduccion(-segundos)

    # Método que ajusta el volumen de la canción
    @staticmethod
    def ajustar_volumen(volumen: float) -> None:
        pygame.mixer.music.set_volume(volumen / 100.0)
