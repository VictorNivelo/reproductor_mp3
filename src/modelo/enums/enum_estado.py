from enum import Enum


class Estado(Enum):
    REPRODUCIENDO = "Reproduciendo"
    PAUSADO = "Pausado"
    DETENIDO = "Detenido"

    # Método para obtener el nombre legible del estado
    @property
    def obtener_nombre_estado(self) -> str:
        nombres = {
            Estado.REPRODUCIENDO: "Reproduciendo",
            Estado.PAUSADO: "Pausado",
            Estado.DETENIDO: "Detenido",
        }
        return nombres[self]

    # Método para verificar el estado activo
    def estado_activo(self) -> bool:
        return self in (Estado.REPRODUCIENDO, Estado.PAUSADO)

    # Método para verificar si se esta reproduciendo
    def esta_reproduciendo(self) -> bool:
        return self == Estado.REPRODUCIENDO

    # Método para verificar si esta pausado
    def esta_pausado(self) -> bool:
        return self == Estado.PAUSADO

    # Método para verificar si esta detenido
    def esta_detenido(self) -> bool:
        return self == Estado.DETENIDO
