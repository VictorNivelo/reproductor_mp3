import random

from modelo.enums.enum_repeticion import Repeticion
from modelo.enums.enum_orden import Orden
from modelo.cancion import Cancion
from typing import List, Optional


class ColaReproduccion:
    def __init__(self):
        self.cola_original = []
        self.indice_actual = -1
        self.cola_actual = []
        self.historial = []
        self.indice_historial = -1
        self.orden = Orden.ORDEN
        self.repeticion = Repeticion.NO_REPETIR

    # Convertir a cadena para imprimir en la consola
    def __str__(self):
        return f"ColaReproduccion({len(self.cola_actual)} canciones, índice actual: {self.indice_actual})"

    # Convertir a objeto representable en consola
    def __repr__(self):
        return f"ColaReproduccion(canciones={len(self.cola_actual)}, indice_actual={self.indice_actual})"

    # Método para agregar una canción al final de la cola
    def agregar_cancion_cola(self, cancion: Cancion):
        try:
            if cancion not in self.cola_original:
                self.cola_original.append(cancion)
                self.cola_actual.append(cancion)
                print(f"Canción '{cancion.titulo_cancion}' agregada a la cola")
                return True
            else:
                print(f"La canción '{cancion.titulo_cancion}' ya está en la cola")
                return False
        except Exception as e:
            print(f"Error al agregar canción a la cola: {str(e)}")
            return False

    # Método para agregar canción al historial
    def agregar_historial(self, cancion: Cancion):
        try:
            self.historial.append(cancion)
            self.indice_historial = len(self.historial) - 1
            return True
        except Exception as e:
            print(f"Error al agregar al historial: {str(e)}")
            return False

    # Método para agregar canción como siguiente en la cola
    def agregar_siguiente_cola(self, cancion: Cancion):
        try:
            siguiente_posicion = self.indice_actual + 1
            return self.insertar_cancion_cola(cancion, siguiente_posicion)
        except Exception as e:
            print(f"Error al agregar canción como siguiente: {str(e)}")
            return False

    # Método para insertar una canción en una posición específica
    def insertar_cancion_cola(self, cancion: Cancion, posicion: int):
        try:
            if 0 <= posicion <= len(self.cola_original):
                self.cola_original.insert(posicion, cancion)
                self.cola_actual.insert(posicion, cancion)
                if posicion <= self.indice_actual:
                    self.indice_actual += 1
                print(f"Canción '{cancion.titulo_cancion}' insertada en posición {posicion}")
                return True
            else:
                print(f"Posición {posicion} fuera de rango")
                return False
        except Exception as e:
            print(f"Error al insertar canción en la cola: {str(e)}")
            return False

    # Método para eliminar una canción de la cola
    def eliminar_cancion_cola(self, cancion: Cancion):
        try:
            if cancion in self.cola_original:
                indice = self.cola_original.index(cancion)
                self.cola_original.remove(cancion)
                if cancion in self.cola_actual:
                    self.cola_actual.remove(cancion)
                # Ajustar índice si es necesario
                if indice < self.indice_actual:
                    self.indice_actual -= 1
                elif indice == self.indice_actual and self.indice_actual >= len(self.cola_actual):
                    self.indice_actual = len(self.cola_actual) - 1
                print(f"Canción '{cancion.titulo_cancion}' eliminada de la cola")
                return True
            else:
                print(f"La canción '{cancion.titulo_cancion}' no está en la cola")
                return False
        except Exception as e:
            print(f"Error al eliminar canción de la cola: {str(e)}")
            return False

    # Método para eliminar canción por índice
    def eliminar_cancion_indice_cola(self, indice: int):
        try:
            if 0 <= indice < len(self.cola_original):
                cancion = self.cola_original[indice]
                return self.eliminar_cancion_cola(cancion)
            else:
                print(f"Índice {indice} fuera de rango")
                return False
        except Exception as e:
            print(f"Error al eliminar canción por índice: {str(e)}")
            return False

    # Método para establecer la cola con una lista de canciones
    def establecer_cola(self, canciones: List[Cancion]):
        try:
            self.limpiar_cola()
            self.cola_original = canciones.copy()
            self.cola_actual = canciones.copy()
            if self.orden.esta_aleatorio():
                self.mezclar_cola()
            print(f"Cola establecida con {len(canciones)} canciones")
            return True
        except Exception as e:
            print(f"Error al establecer la cola: {str(e)}")
            return False

    # Método para mover una canción en la cola
    def mover_cancion_cola(self, indice_origen: int, indice_destino: int):
        try:
            if 0 <= indice_origen < len(self.cola_actual) and 0 <= indice_destino < len(self.cola_actual):
                cancion = self.cola_actual.pop(indice_origen)
                self.cola_actual.insert(indice_destino, cancion)
                # Ajustar índice actual si es necesario
                if indice_origen == self.indice_actual:
                    self.indice_actual = indice_destino
                elif indice_origen < self.indice_actual <= indice_destino:
                    self.indice_actual -= 1
                elif indice_destino <= self.indice_actual < indice_origen:
                    self.indice_actual += 1
                print(f"Canción movida de posición {indice_origen} a {indice_destino}")
                return True
            else:
                print("Índices fuera de rango")
                return False
        except Exception as e:
            print(f"Error al mover canción: {str(e)}")
            return False

    # Método para mezclar la cola (modo aleatorio)
    def mezclar_cola(self):
        try:
            if self.cola_actual:
                # Guardar canción actual si existe
                cancion_actual = None
                if 0 <= self.indice_actual < len(self.cola_actual):
                    cancion_actual = self.cola_actual[self.indice_actual]
                # Mezclar la cola
                random.shuffle(self.cola_actual)
                # Si había una canción actual, asegurar que esté en la posición actual
                if cancion_actual:
                    indice_nuevo = self.cola_actual.index(cancion_actual)
                    self.cola_actual[indice_nuevo], self.cola_actual[self.indice_actual] = (
                        self.cola_actual[self.indice_actual],
                        self.cola_actual[indice_nuevo],
                    )
                print("Cola mezclada aleatoriamente")
                return True
            return False
        except Exception as e:
            print(f"Error al mezclar la cola: {str(e)}")
            return False

    # Método para verificar si la cola está vacía
    def esta_vacia_cola(self) -> bool:
        return len(self.cola_actual) == 0

    # Método para verificar si hay siguiente canción
    def hay_siguiente_cola(self) -> bool:
        if self.repeticion.es_repetir_actual() or self.repeticion.es_repetir_todo():
            return True
        return self.indice_actual < len(self.cola_actual) - 1

    # Método para verificar si hay canción anterior
    def hay_anterior_cola(self) -> bool:
        if self.repeticion.es_repetir_actual() or self.repeticion.es_repetir_todo():
            return True
        return self.indice_actual > 0

    # Método para obtener el tamaño de la cola
    def obtener_tamanio_cola(self) -> int:
        return len(self.cola_actual)

    # Método para obtener la cola completa
    def obtener_cola_completa(self) -> List[Cancion]:
        return self.cola_actual.copy()

    # Método para obtener el tamaño del historial
    def obtener_tamanio_historial(self) -> int:
        return len(self.historial)

    # Método para obtener el historial completo
    def obtener_historial(self) -> List[Cancion]:
        return self.historial.copy()

    # Método para obtener índice de una canción
    def obtener_indice_cancion(self, cancion: Cancion) -> int:
        try:
            return self.cola_actual.index(cancion)
        except ValueError:
            return -1
        except Exception as e:
            print(f"Error al obtener índice: {str(e)}")
            return -1

    # Método para obtener la canción actual
    def obtener_cancion_actual_cola(self) -> Optional[Cancion]:
        try:
            if 0 <= self.indice_actual < len(self.cola_actual):
                return self.cola_actual[self.indice_actual]
            return None
        except Exception as e:
            print(f"Error al obtener canción actual: {str(e)}")
            return None

    # Método para obtener la siguiente canción
    def obtener_siguiente_cola(self) -> Optional[Cancion]:
        try:
            if not self.cola_actual:
                return None
            # Sí está en modo repetir actual, devolver la misma
            if self.repeticion.es_repetir_actual():
                return self.obtener_cancion_actual_cola()
            siguiente_indice = self.indice_actual + 1
            # Si llegamos al final
            if siguiente_indice >= len(self.cola_actual):
                if self.repeticion.es_repetir_todo():
                    self.indice_actual = 0
                    if self.orden.esta_aleatorio():
                        self.mezclar_cola()
                else:
                    return None
            else:
                self.indice_actual = siguiente_indice
            cancion = self.obtener_cancion_actual_cola()
            if cancion:
                self.agregar_historial(cancion)
            return cancion
        except Exception as e:
            print(f"Error al obtener siguiente canción: {str(e)}")
            return None

    # Método para obtener la canción anterior
    def obtener_anterior_cola(self) -> Optional[Cancion]:
        try:
            if not self.cola_actual:
                return None
            # Sí está en modo repetir actual, devolver la misma
            if self.repeticion.es_repetir_actual():
                return self.obtener_cancion_actual_cola()
            anterior_indice = self.indice_actual - 1
            # Si estamos al inicio
            if anterior_indice < 0:
                if self.repeticion.es_repetir_todo():
                    self.indice_actual = len(self.cola_actual) - 1
                else:
                    return None
            else:
                self.indice_actual = anterior_indice
            return self.obtener_cancion_actual_cola()
        except Exception as e:
            print(f"Error al obtener canción anterior: {str(e)}")
            return None

    # Método para obtener duración total de la cola
    def obtener_duracion_total_cola(self) -> float:
        try:
            return sum(cancion.duracion_cancion for cancion in self.cola_actual)
        except Exception as e:
            print(f"Error al calcular duración total: {str(e)}")
            return 0.0

    # Método para obtener duración total formateada
    def obtener_duracion_total_cola_formateada(self) -> str:
        try:
            duracion_total = self.obtener_duracion_total_cola()
            horas = int(duracion_total // 3600)
            minutos = int((duracion_total % 3600) // 60)
            segundos = int(duracion_total % 60)
            # Si hay horas, usar formato HH:MM:SS, si no MM:SS
            if horas > 0:
                return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                return f"{minutos:02d}:{segundos:02d}"
        except Exception as e:
            print(f"Error al formatear duración total: {str(e)}")
            return "00:00"

    # Método para obtener duración restante
    def obtener_duracion_restante_cola(self) -> float:
        try:
            if self.indice_actual < 0:
                return self.obtener_duracion_total_cola()
            return sum(cancion.duracion_cancion for cancion in self.cola_actual[self.indice_actual + 1 :])
        except Exception as e:
            print(f"Error al calcular duración restante: {str(e)}")
            return 0.0

    # Método para obtener duración restante formateada
    def obtener_duracion_restante_cola_formateada(self) -> str:
        try:
            duracion_restante = self.obtener_duracion_restante_cola()
            horas = int(duracion_restante // 3600)
            minutos = int((duracion_restante % 3600) // 60)
            segundos = int(duracion_restante % 60)
            # Si hay horas, usar formato HH:MM:SS, si no MM:SS
            if horas > 0:
                return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                return f"{minutos:02d}:{segundos:02d}"
        except Exception as e:
            print(f"Error al formatear duración restante: {str(e)}")
            return "00:00"

    # Método para cambiar el modo de orden
    def cambiar_orden(self, nuevo_orden: Orden):
        try:
            self.orden = nuevo_orden
            if nuevo_orden.esta_aleatorio():
                self.mezclar_cola()
            else:
                # Restaurar orden original
                self.cola_actual = self.cola_original.copy()
            print(f"Orden cambiado a: {nuevo_orden.obtener_nombre_orden}")
            return True
        except Exception as e:
            print(f"Error al cambiar orden: {str(e)}")
            return False

    # Método para cambiar el modo de repetición
    def cambiar_repeticion(self, nueva_repeticion: Repeticion):
        try:
            self.repeticion = nueva_repeticion
            print(f"Repetición cambiada a: {nueva_repeticion.obtener_nombre_repeticion}")
            return True
        except Exception as e:
            print(f"Error al cambiar repetición: {str(e)}")
            return False

    # Método para alternar entre modos de repetición
    def alternar_repeticion(self):
        try:
            if self.repeticion == Repeticion.NO_REPETIR:
                self.repeticion = Repeticion.REPETIR_TODO
            elif self.repeticion == Repeticion.REPETIR_TODO:
                self.repeticion = Repeticion.REPETIR_ACTUAL
            else:
                self.repeticion = Repeticion.NO_REPETIR
            return self.repeticion
        except Exception as e:
            print(f"Error al alternar repetición: {str(e)}")
            return None

    # Método para alternar entre orden normal y aleatorio
    def alternar_orden(self):
        try:
            if self.orden == Orden.ORDEN:
                self.orden = Orden.ALEATORIO
                self.mezclar_cola()
            else:
                self.orden = Orden.ORDEN
                self.cola_actual = self.cola_original.copy()
            return self.orden
        except Exception as e:
            print(f"Error al alternar orden: {str(e)}")
            return None

    # Método para restaurar orden original
    def restaurar_orden_original(self):
        try:
            self.cola_actual = self.cola_original.copy()
            self.orden = Orden.ORDEN
            print("Orden original restaurado")
            return True
        except Exception as e:
            print(f"Error al restaurar orden original: {str(e)}")
            return False

    # Método para obtener información de la cola
    def obtener_informacion_cola(self) -> dict:
        return {
            "total_canciones": len(self.cola_actual),
            "indice_actual": self.indice_actual,
            "orden": self.orden.obtener_nombre_orden,
            "repeticion": self.repeticion.obtener_nombre_repeticion,
            "hay_siguiente": self.hay_siguiente_cola(),
            "hay_anterior": self.hay_anterior_cola(),
            "canciones": [cancion.obtener_informacion_basica_cancion() for cancion in self.cola_actual],
        }

    # Método para limpiar toda la cola
    def limpiar_cola(self):
        try:
            self.cola_original.clear()
            self.cola_actual.clear()
            self.indice_actual = -1
            self.historial.clear()
            self.indice_historial = -1
            print("Cola de reproducción limpiada")
            return True
        except Exception as e:
            print(f"Error al limpiar la cola: {str(e)}")
            return False

    # Método para limpiar el historial
    def limpiar_historial(self):
        try:
            self.historial.clear()
            self.indice_historial = -1
            return True
        except Exception as e:
            print(f"Error al limpiar historial: {str(e)}")
            return False
