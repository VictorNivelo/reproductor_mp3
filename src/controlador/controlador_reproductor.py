from controlador.controlador_archivos import ControladorArchivos
from animacion import AnimacionGeneral
from modelo.cancion import Cancion
from utiles import UtilesGeneral
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
        # Instancia de utilidades
        self.utiles = UtilesGeneral()
        # Instancia de la animacion
        self.animacion = AnimacionGeneral()

    # Método que establece las etiquetas de la interfaz
    def establecer_informacion_controlador(self, nombre, artista, album, anio, imagen):
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

    # Método que actualiza la carátula de la canción
    def actualizar_caratula_controlador(self, caratula_bytes=None, ancho=300):
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

    # Método que actualiza la información de la interfaz
    def actualizar_informacion_controlador(self):
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
            # Cancelar cualquier tiempo de desplazamiento anterior
            if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
                self.etiqueta_nombre.after_cancel(self.id_marcador_tiempo)
                self.id_marcador_tiempo = None
            # Iniciar desplazamiento de textos largos si es necesario
            textos = {
                "titulo": (self.texto_titulo, self.etiqueta_nombre),
                "artista": (self.texto_artista, self.etiqueta_artista),
                "album": (self.texto_album, self.etiqueta_album),
            }
            self.animacion.configurar_desplazamiento_etiqueta(textos, self.etiqueta_nombre, 80)
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

    # Método que establece la barra de progreso
    def establecer_barra_progreso_controlador(self, barra):
        self.barra_progreso = barra

    # Método que establece las etiquetas de tiempo
    def establecer_etiquetas_tiempo_controlador(self, etiqueta_actual, etiqueta_total):
        self.etiqueta_tiempo_actual = etiqueta_actual
        self.etiqueta_tiempo_total = etiqueta_total

    # Método que actualiza el tiempo de reproducción de la canción
    def actualizar_tiempo_controlador(self):
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
                    self.reproducir_cancion_controlador(self.cancion_actual)
                    return False
                elif self.lista_reproduccion and (
                    self.indice_actual < len(self.lista_reproduccion) - 1 or self.modo_repeticion == 2
                ):
                    # Reproducir siguiente canción
                    self.reproducir_siguiente_controlador()
                    return False
                else:
                    # No hay más canciones o no está activada la repetición
                    self.detener_reproduccion_controlador()
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
            self.id_temporizador = self.etiqueta_tiempo_actual.after(100, self.actualizar_tiempo_controlador)
        return False

    # Método para obtener el porcentaje de volumen actual
    @staticmethod
    def obtener_volumen_controlador():
        return pygame.mixer.music.get_volume() * 100.0

    # Método que ajusta el volumen de la canción
    @staticmethod
    def ajustar_volumen_controlador(volumen: float) -> None:
        pygame.mixer.music.set_volume(volumen / 100.0)

    # Método para verificar si el reproductor está silenciado
    @staticmethod
    def obtener_estado_silenciado_controlador():
        return pygame.mixer.music.get_volume() == 0.0

    # Método para silenciar la reproducción
    @staticmethod
    def silenciar_controlador():
        # Guardar el volumen actual antes de silenciar
        volumen_anterior = pygame.mixer.music.get_volume() * 100.0
        # Establecer volumen a 0
        pygame.mixer.music.set_volume(0.0)
        return volumen_anterior

    # Método para quitar el silencio
    @staticmethod
    def quitar_silencio_controlador(volumen_anterior=None):
        # Si no se proporciona un volumen, usar 50% por defecto
        if volumen_anterior is None:
            volumen_anterior = 50.0
        # Asegurar que el valor esté entre 0 y 100
        volumen_anterior = max(0.0, min(100.0, volumen_anterior))
        # Restaurar volumen
        pygame.mixer.music.set_volume(volumen_anterior / 100.0)
        return volumen_anterior

    # Método que devuelve el estado del modo de repetición
    def obtener_estado_repeticion_controlador(self):
        return self.modo_repeticion

    # Método que establece el modo de repetición
    def modo_repeticion_controlador(self, modo):
        self.modo_repeticion = modo

    # Método que devuelve el estado del modo aleatorio
    def obtener_estado_aleatorio_controlador(self):
        return self.modo_aleatorio

    # Método para establecer el modo de reproducción (aleatorio o secuencial)
    def modo_orden_controlador(self, aleatorio: bool):
        self.modo_aleatorio = aleatorio
        # Resetear el historial cuando cambiamos de modo
        self.historial_aleatorio = []

    # Método que devuelve si hay una canción reproduciéndose actualmente
    def obtener_estado_reproduccion_controlador(self):
        return self.reproduciendo

    # Método que reproduce una canción
    def reproducir_cancion_controlador(self, cancion: Cancion) -> None:
        # Cancelar el temporizador anterior si existe
        if self.id_temporizador:
            self.etiqueta_tiempo_actual.after_cancel(self.id_temporizador)
            self.id_temporizador = None
        # Establecer la canción actual
        self.cancion_actual = cancion
        # Actualizar el índice solo si la canción está en la lista de reproducción
        if self.lista_reproduccion:
            # Buscar todas las ocurrencias de la canción en la lista
            indices_cancion = [i for i, c in enumerate(self.lista_reproduccion) if c == cancion]
            if indices_cancion:
                # Si hay múltiples instancias de la misma canción, elegir la primera que sea ≥ índice
                indices_mayores = [i for i in indices_cancion if i >= self.indice_actual]
                if indices_mayores:
                    # Tomar el primer índice mayor o igual al actual
                    self.indice_actual = indices_mayores[0]
                else:
                    # Si no hay índices mayores, tomar el primero
                    self.indice_actual = indices_cancion[0]
                # Actualizar historial en modo aleatorio
                if self.modo_aleatorio and self.indice_actual not in self.historial_aleatorio:
                    self.historial_aleatorio.append(self.indice_actual)
        else:
            # Si la canción no está en la lista, agregarla
            self.lista_reproduccion.append(cancion)
            self.indice_actual = 0
        # Cargar y reproducir la canción con pygame
        pygame.mixer.music.load(str(cancion.ruta_cancion))
        pygame.mixer.music.play()
        self.reproduciendo = True
        # Reiniciar cronómetro
        self.tiempo_acumulado = 0
        self.tiempo_inicio = time.perf_counter()
        # Actualizar interfaz
        self.actualizar_informacion_controlador()
        self.actualizar_tiempo_controlador()
        # Guardar la cola automáticamente
        controlador_archivos = ControladorArchivos()
        controlador_archivos.guardar_cola_reproduccion_json_controlador(self)

    # Métodos que controlan la reproducción de la canción
    def pausar_reproduccion_controlador(self) -> None:
        if self.reproduciendo:
            pygame.mixer.music.pause()
            # Acumular tiempo transcurrido hasta el momento de la pausa
            self.tiempo_acumulado += time.perf_counter() - self.tiempo_inicio
            self.tiempo_inicio = None
            # En este caso no cancelamos el tiempo para que la interfaz siga actualizándose
            self.reproduciendo = False

    # Método que reanuda la reproducción de la canción
    def reanudar_reproduccion_controlador(self) -> None:
        if not self.reproduciendo and self.cancion_actual:
            # Verificar el estado actual de pygame
            try:
                # Intentar reanudar primero
                pygame.mixer.music.unpause()
                # Si no hay sonido, volver a cargar y reproducir
                if pygame.mixer.music.get_busy() == 0:
                    # Recargar el archivo y comenzar desde el tiempo acumulado
                    pygame.mixer.music.load(str(self.cancion_actual.ruta_cancion))
                    pygame.mixer.music.play(start=self.tiempo_acumulado)
            except Exception as e:
                print(f"Error al reanudar reproducción, recargando: {e}")
                # Si hay error, volver a cargar el archivo
                pygame.mixer.music.load(str(self.cancion_actual.ruta_cancion))
                pygame.mixer.music.play(start=self.tiempo_acumulado)
            self.tiempo_inicio = time.perf_counter()
            self.reproduciendo = True
            self.actualizar_tiempo_controlador()

    # Método que reproduce o reanuda la canción actual
    def reproducir_o_reanudar_controlador(self) -> bool:
        # Comprobar primero si hay canción actual
        if self.cancion_actual:
            # Si la canción ya está cargada pero pausada, solo reanudar
            if not self.reproduciendo:
                self.reanudar_reproduccion_controlador()
                return True
            # Si ya está reproduciendo, no hacer nada
            return True
        # Si no hay canción actual, pero hay lista, reproducir la primera
        elif self.lista_reproduccion and self.indice_actual >= 0:
            cancion = self.lista_reproduccion[self.indice_actual]
            self.reproducir_cancion_controlador(cancion)
            return True
        # Ni canción actual ni lista de reproducción
        return False

    # Método que detiene la reproducción de la canción
    def detener_reproduccion_controlador(self) -> bool:
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

    # Método para reiniciar la canción actual
    def reiniciar_cancion_controlador(self):
        if self.cancion_actual:
            # Mover al inicio de la canción
            return self.mover_a_posicion_controlador(0)
        return False

    # Método que reproduce la siguiente canción
    def reproducir_siguiente_controlador(self):
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
                    self.detener_reproduccion_controlador()
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
                    self.detener_reproduccion_controlador()
                    return False
        cancion = self.lista_reproduccion[self.indice_actual]
        self.reproducir_cancion_controlador(cancion)
        return True

    # Método que reproduce la canción anterior
    def reproducir_anterior_controlador(self):
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
        self.reproducir_cancion_controlador(cancion)
        return True

    # Método para adelantar la reproducción en segundos
    def adelantar_reproduccion_controlador(self, segundos=None):
        if segundos is None:
            segundos = TIEMPO_AJUSTE
        self.mover_a_posicion_controlador(segundos)

    # Método para retroceder la reproducción en segundos
    def retroceder_reproduccion_controlador(self, segundos=None):
        if segundos is None:
            segundos = TIEMPO_AJUSTE
        self.mover_a_posicion_controlador(-segundos)

    # Método para mover la reproducción a una posición específica en segundos
    def mover_a_posicion_controlador(self, tiempo_segundos):
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

    # Método para obtener la posición actual de reproducción en segundos
    def obtener_posicion_actual_controlador(self):
        if self.cancion_actual:
            if self.tiempo_inicio is not None:
                tiempo_actual = self.tiempo_acumulado + (time.perf_counter() - self.tiempo_inicio)
            else:
                tiempo_actual = self.tiempo_acumulado
            return tiempo_actual
        return 0

    # Método para mover la reproducción a un porcentaje específico de la canción
    def mover_a_porcentaje_controlador(self, porcentaje):
        if self.cancion_actual:
            # Asegurar que el porcentaje esté entre 0 y 100
            porcentaje = max(0, min(porcentaje, 100))
            # Convertir el porcentaje a segundos
            posicion_segundos = (porcentaje / 100.0) * self.cancion_actual.duracion
            # Utilizar el método existente para mover a la posición
            return self.mover_a_posicion_controlador(posicion_segundos)
        return False

    # Método para obtener el porcentaje actual de reproducción
    def obtener_porcentaje_actual_controlador(self):
        if self.cancion_actual and self.cancion_actual.duracion > 0:
            tiempo_actual = self.obtener_posicion_actual_controlador()
            return (tiempo_actual / self.cancion_actual.duracion) * 100
        return 0

    # Método que establece la lista de reproducción actual
    def establecer_cola_reproduccion_controlador(self, canciones, indice=0):
        self.lista_reproduccion = canciones
        self.indice_actual = indice if 0 <= indice < len(canciones) else 0
        # Guardar la cola automáticamente
        controlador_archivos = ControladorArchivos()
        controlador_archivos.guardar_cola_reproduccion_json_controlador(self)

    # Método que agrega una canción a la cola de reproducción
    def agregar_cancion_a_cola_controlador(self, cancion):
        if cancion:
            self.lista_reproduccion.append(cancion)
            # Si no hay reproducción activa, configurar está como la siguiente
            if self.indice_actual == -1:
                self.indice_actual = 0
            # Guardar la cola automáticamente
            controlador_archivos = ControladorArchivos()
            controlador_archivos.guardar_cola_reproduccion_json_controlador(self)
            return True
        return False

    # Método que agrega una canción al inicio de la cola de reproducción
    def agregar_cancion_inicio_cola_controlador(self, cancion):
        if cancion:
            # Sí hay una canción en reproducción, insertar después de ella
            if self.indice_actual >= 0:
                # Insertar después de la posición actual
                posicion_insercion = self.indice_actual + 1
                self.lista_reproduccion.insert(posicion_insercion, cancion)
                # No es necesario ajustar el índice actual
            else:
                # Si no hay reproducción activa, insertar al inicio
                self.lista_reproduccion.insert(0, cancion)
                self.indice_actual = 0
            # Guardar la cola automáticamente
            controlador_archivos = ControladorArchivos()
            controlador_archivos.guardar_cola_reproduccion_json_controlador(self)
            return True
        return False

    # Método que agrega una canción al final de la cola de reproducción
    def agregar_cancion_final_cola_controlador(self, cancion):
        return self.agregar_cancion_a_cola_controlador(cancion)

    # Método que quita una canción de la cola de reproducción
    def quitar_cancion_cola_controlador(self, indice):
        if 0 <= indice < len(self.lista_reproduccion):
            # Verificar si es la canción actual
            es_actual = indice == self.indice_actual
            # Eliminar la canción de la lista
            self.lista_reproduccion.pop(indice)
            # Ajustar el índice actual si es necesario
            if indice <= self.indice_actual and self.indice_actual > 0:
                self.indice_actual -= 1
            elif len(self.lista_reproduccion) == 0:
                self.indice_actual = -1
            # Sí era la canción actual, reproducir la siguiente
            if es_actual and self.reproduciendo:
                return self.reproducir_siguiente_controlador()
            return True
        return False

    # Método que limpia la cola de reproducción
    def limpiar_cola_controlador(self, mantener_actual=True):
        # Guardar referencia a la canción actual si está reproduciéndose
        cancion_actual = None
        if mantener_actual and self.reproduciendo and self.cancion_actual:
            cancion_actual = self.cancion_actual
        # Limpiar la lista
        self.lista_reproduccion = []
        # Si hay una canción reproduciéndose y queremos mantenerla
        if cancion_actual:
            self.lista_reproduccion.append(cancion_actual)
            self.indice_actual = 0
        else:
            self.indice_actual = -1
        # Guardar la cola actualizada
        controlador_archivos = ControladorArchivos()
        controlador_archivos.guardar_cola_reproduccion_json_controlador(self)
        return True
