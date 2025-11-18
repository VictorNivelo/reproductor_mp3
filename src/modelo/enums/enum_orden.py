from enum import Enum


class Orden(Enum):
    ORDEN = "Orden"
    ALEATORIO = "Aleatorio"

    # Método para obtener el nombre legible del orden
    @property
    def obtener_nombre_orden(self) -> str:
        nombres = {
            Orden.ORDEN: "Orden",
            Orden.ALEATORIO: "Aleatorio",
        }
        return nombres[self]

    # Método para verificar si el orden es el normal
    def esta_orden(self) -> bool:
        return self == Orden.ORDEN

    # Método para verificar si el orden es aleatorio
    def esta_aleatorio(self) -> bool:
        return self == Orden.ALEATORIO
