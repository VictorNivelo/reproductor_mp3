from enum import Enum


class Volumen(Enum):
    SILENCIADO = 0
    SIN_VOLUMEN = 0
    BAJO = 33
    MEDIO = 66
    ALTO = 100

    # Método para obtener el nombre descriptivo del nivel de volumen
    @property
    def nombre(self):
        if self.value > 100:
            return "Volumen máximo 100"
        if self.value == 0:
            return "Silenciado" if self == Volumen.SILENCIADO else "Sin Volumen"
        elif self.value < 33:
            return "Volumen Bajo"
        elif self.value < 66:
            return "Volumen Medio"
        else:
            return "Volumen Alto"
