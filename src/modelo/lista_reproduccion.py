import uuid


from modelo.cancion import Cancion
from datetime import datetime


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

    # Agregar una canción a la lista
    def agregar_cancion_lista(self, cancion: Cancion):
        if cancion not in self.lista_cancion:
            self.lista_cancion.append(cancion)
            self.fecha_cancion_agregado[id(cancion)] = datetime.now()
            self.fecha_modificacion_lista = datetime.now()
            return True
        return False

    # Mover una canción a otra posición
    def mover_cancion_lista(self, indice_origen: int, indice_destino: int) -> bool:
        try:
            if 0 <= indice_origen < len(self.lista_cancion) and 0 <= indice_destino < len(self.lista_cancion):
                cancion = self.lista_cancion.pop(indice_origen)
                self.lista_cancion.insert(indice_destino, cancion)
                self.fecha_modificacion = datetime.now()
                return True
            return False
        except (IndexError, ValueError):
            return False

    # Eliminar una canción de la lista
    def eliminar_cancion_lista(self, cancion: Cancion):
        if cancion in self.lista_cancion:
            self.lista_cancion.remove(cancion)
            if id(cancion) in self.fecha_cancion_agregado:
                del self.fecha_cancion_agregado[id(cancion)]
            self.fecha_modificacion_lista = datetime.now()
            return True
        return False

    # Obtener todas las canciones de la lista
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

    # Obtener información de la lista
    def obtener_informacion_lista(self) -> dict:
        return {
            "nombre": self.nombre_lista,
            "total_canciones": len(self.lista_cancion),
            "canciones": [
                {
                    **cancion.obtener_informacion_basica_cancion(),
                    "fecha_agregado_lista": self.obtener_fecha_agregado_formateada(cancion),
                }
                for cancion in self.lista_cancion
            ],
        }
