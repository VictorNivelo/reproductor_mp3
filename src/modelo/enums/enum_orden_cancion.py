from enum import Enum


class OrdenCancion(Enum):
    TITULO = "Título"
    ARTISTA = "Artista"
    ALBUM = "Álbum"
    ANIO = "Añio"
    DURACION = "Duración"
    FECHA_AGREGADO = "Fecha agregado"

    # Método para obtener el nombre legible del orden
    @property
    def obtener_nombre_orden(self) -> str:
        nombres = {
            OrdenCancion.TITULO: "Título",
            OrdenCancion.ARTISTA: "Artista",
            OrdenCancion.ALBUM: "Álbum",
            OrdenCancion.ANIO: "Año",
            OrdenCancion.DURACION: "Duración",
            OrdenCancion.FECHA_AGREGADO: "Fecha que se agrego",
        }
        return nombres[self]

    # Método para verificar si es orden por título
    def es_orden_titulo(self) -> bool:
        return self == OrdenCancion.TITULO

    # Método para verificar si es orden por artista
    def es_orden_artista(self) -> bool:
        return self == OrdenCancion.ARTISTA

    # Método para verificar si es orden por álbum
    def es_orden_album(self) -> bool:
        return self == OrdenCancion.ALBUM

    # Método para verificar si es orden por año
    def es_orden_anio(self) -> bool:
        return self == OrdenCancion.ANIO

    # Método para verificar si es orden por duración
    def es_orden_duracion(self) -> bool:
        return self == OrdenCancion.DURACION

    # Método para verificar si es orden por fecha agregado
    def es_orden_fecha_agregado(self) -> bool:
        return self == OrdenCancion.FECHA_AGREGADO

    # Método para imprimir todos los nombres de orden disponibles
    @classmethod
    def imprimir_nombre_orden(cls):
        print("---------------- Órdenes ----------------")
        for orden in cls:
            print(orden.obtener_nombre_orden)
        print("-----------------------------------------")
