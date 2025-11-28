import uuid

from modelo.cancion import Cancion
from datetime import datetime
from copy import deepcopy


class ListaReproduccion:
    def __init__(self, nombre: str):
        self.id_lista = str(uuid.uuid4())
        self.nombre_lista = nombre
        self.fecha_creacion_lista = datetime.now()
        self.fecha_modificacion_lista = datetime.now()
        self.lista_cancion = []
        self.fecha_cancion_agregado = {}

    # Convertir a cadena para imprimir en la consola
    def __str__(self):
        return f"Lista: {self.nombre_lista} ({len(self.lista_cancion)} canciones)"

    # Convertir a objeto representable en consola
    def __repr__(self):
        return f"ListaReproduccion(nombre='{self.nombre_lista}', canciones={len(self.lista_cancion)})"

    # Agregar una canción a la lista de reproducción
    def agregar_cancion_lista(self, cancion: Cancion):
        if cancion not in self.lista_cancion:
            self.lista_cancion.append(cancion)
            self.fecha_cancion_agregado[id(cancion)] = datetime.now()
            self.fecha_modificacion_lista = datetime.now()
            return True
        return False

    # Agregar canción en posición específica
    def insertar_cancion_lista(self, cancion: Cancion, posicion: int) -> bool:
        try:
            if cancion not in self.lista_cancion and 0 <= posicion <= len(self.lista_cancion):
                self.lista_cancion.insert(posicion, cancion)
                self.fecha_cancion_agregado[id(cancion)] = datetime.now()
                self.fecha_modificacion_lista = datetime.now()
                return True
            return False
        except Exception as e:
            print(f"Error al insertar canción: {str(e)}")
            return False

    # Mover una canción a otra posición
    def mover_cancion_lista(self, indice_origen: int, indice_destino: int) -> bool:
        try:
            if 0 <= indice_origen < len(self.lista_cancion) and 0 <= indice_destino < len(self.lista_cancion):
                cancion = self.lista_cancion.pop(indice_origen)
                self.lista_cancion.insert(indice_destino, cancion)
                self.fecha_modificacion_lista = datetime.now()
                return True
            return False
        except (IndexError, ValueError):
            return False

    # Eliminar una canción de la lista de reproducción
    def eliminar_cancion_lista(self, cancion: Cancion):
        if cancion in self.lista_cancion:
            self.lista_cancion.remove(cancion)
            if id(cancion) in self.fecha_cancion_agregado:
                del self.fecha_cancion_agregado[id(cancion)]
            self.fecha_modificacion_lista = datetime.now()
            return True
        return False

    # Duplicar lista de reproducción
    def duplicar_lista(self, nuevo_nombre: str = None):
        nombre = nuevo_nombre or f"{self.nombre_lista} (copia)"
        nueva_lista = ListaReproduccion(nombre)
        nueva_lista.lista_cancion = self.lista_cancion.copy()
        nueva_lista.fecha_cancion_agregado = deepcopy(self.fecha_cancion_agregado)
        return nueva_lista

    # Buscar canciones en la lista
    def buscar_cancion_lista(self, termino: str) -> list[Cancion]:
        termino = termino.lower()
        return [
            cancion
            for cancion in self.lista_cancion
            if termino in cancion.titulo_cancion.lower()
            or termino in cancion.artista_cancion.lower()
            or termino in cancion.album_cancion.lower()
        ]

    # Verificar si la lista de reproducción tiene una canción específica
    def tiene_cancion(self, cancion: Cancion) -> bool:
        return cancion in self.lista_cancion

    # Obtener el tamaño de la lista de reproducción
    def obtener_tamanio_lista(self) -> int:
        return len(self.lista_cancion)

    # Obtener todas las canciones de la lista de reproducción
    def obtener_lista_cancion(self) -> list:
        return self.lista_cancion

    # Obtener fecha de agregado de una canción específica
    def obtener_fecha_agregado_cancion(self, cancion: Cancion) -> datetime | None:
        return self.fecha_cancion_agregado.get(id(cancion))

    # Obtener fecha formateada
    def obtener_fecha_agregado_formateada(self, cancion: Cancion) -> str:
        fecha = self.obtener_fecha_agregado_cancion(cancion)
        if fecha:
            return fecha.strftime("%d/%m/%Y %H:%M:%S")
        return "Fecha desconocida"

    # Obtener duración total de la lista de reproducción
    def obtener_duracion_total_lista(self) -> float:
        return sum(cancion.duracion_cancion for cancion in self.lista_cancion)

    # Obtener duración total formateada
    def obtener_duracion_total_formateada(self) -> str:
        duracion = self.obtener_duracion_total_lista()
        horas = int(duracion // 3600)
        minutos = int((duracion % 3600) // 60)
        segundos = int(duracion % 60)
        if horas > 0:
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return f"{minutos:02d}:{segundos:02d}"

    # Obtener información de la lista de reproducción
    def obtener_informacion_lista(self) -> dict:
        return {
            "id": self.id_lista,
            "nombre": self.nombre_lista,
            "fecha_creacion": self.fecha_creacion_lista.strftime("%d/%m/%Y %H:%M:%S"),
            "fecha_modificacion": self.fecha_modificacion_lista.strftime("%d/%m/%Y %H:%M:%S"),
            "total_canciones": len(self.lista_cancion),
            "canciones": [
                {
                    **cancion.obtener_informacion_basica_cancion(),
                    "fecha_agregado_lista": self.obtener_fecha_agregado_formateada(cancion),
                }
                for cancion in self.lista_cancion
            ],
        }
