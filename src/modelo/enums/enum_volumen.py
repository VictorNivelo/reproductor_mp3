from enum import Enum


class Volumen(Enum):
    SILENCIADO = 0
    SIN_VOLUMEN = 0
    BAJO = 33
    MEDIO = 66
    ALTO = 100

    # Método para obtener el nombre descriptivo del nivel de volumen
    @property
    def obtener_nombre_volumen(self):
        if self.value > 100:
            return "Volumen máximo 100"
        if self.value == 0:
            return "Silenciado" if self == Volumen.SILENCIADO else "Sin volumen"
        elif self.value < 33:
            return "Volumen bajo"
        elif self.value < 66:
            return "Volumen medio"
        else:
            return "Volumen alto"

    # Método para obtener el enum correspondiente a un valor de volumen dado
    @classmethod
    def obtener_volumen_correspondiente(cls, valor: int) -> "Volumen":
        if valor <= 0:
            return Volumen.SIN_VOLUMEN
        elif valor <= 33:
            return Volumen.BAJO
        elif valor <= 66:
            return Volumen.MEDIO
        else:
            return Volumen.ALTO

    # Métodos para verificar si ests silenciado
    def esta_silenciado(self) -> bool:
        return self == Volumen.SILENCIADO

    # Método para verificar si es sin volumen
    def es_sin_volumen(self) -> bool:
        return self == Volumen.SIN_VOLUMEN

    # Método para verificar si el volumen es bajo
    def es_bajo(self) -> bool:
        return self == Volumen.BAJO

    # Método para verificar si el volumen es medio
    def es_medio(self) -> bool:
        return self == Volumen.MEDIO

    # Método para verificar si el volumen es alto
    def es_alto(self) -> bool:
        return self == Volumen.ALTO
