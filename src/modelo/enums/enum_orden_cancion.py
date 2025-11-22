from enum import Enum


class Orden_Cancion(Enum):
    TITULO = "Título"
    ARTISTA = "Artista"
    ALBUM = "Álbum"
    ANIO = "Añio"
    DURACION = "Duración"
    FECHA_AGREGADO = "Fecha agregado"
    FECHA_LANZAMIENTO = "Fecha lanzamiento"

    # Método para obtener el nombre legible del orden
    @property
    def obtener_nombre_orden(self) -> str:
        nombres = {
            Orden_Cancion.TITULO: "Título",
            Orden_Cancion.ARTISTA: "Artista",
            Orden_Cancion.ALBUM: "Álbum",
            Orden_Cancion.ANIO: "Año",
            Orden_Cancion.DURACION: "Duración",
            Orden_Cancion.FECHA_AGREGADO: "Fecha que se agrego",
            Orden_Cancion.FECHA_LANZAMIENTO: "Fecha de lanzamiento",
        }
        return nombres[self]

    # Método para verificar si es orden por título
    def es_orden_titulo(self) -> bool:
        return self == Orden_Cancion.TITULO

    # Método para verificar si es orden por artista
    def es_orden_artista(self) -> bool:
        return self == Orden_Cancion.ARTISTA

    # Método para verificar si es orden por álbum
    def es_orden_album(self) -> bool:
        return self == Orden_Cancion.ALBUM

    # Método para verificar si es orden por año
    def es_orden_anio(self) -> bool:
        return self == Orden_Cancion.ANIO

    # Método para verificar si es orden por duración
    def es_orden_duracion(self) -> bool:
        return self == Orden_Cancion.DURACION

    # Método para verificar si es orden por fecha agregado
    def es_orden_fecha_agregado(self) -> bool:
        return self == Orden_Cancion.FECHA_AGREGADO

    # Método para verificar si es orden por fecha de lanzamiento
    def es_orden_fecha_lanzamiento(self) -> bool:
        return self == Orden_Cancion.FECHA_LANZAMIENTO

    # Método para imprimir todos los nombres de orden disponibles
    @classmethod
    def imprimir_nombre_orden(cls):
        print("---------------- Órdenes ----------------")
        for orden in cls:
            print(orden.obtener_nombre_orden)
        print("-----------------------------------------")
