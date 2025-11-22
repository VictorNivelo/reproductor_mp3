from enum import Enum


class Repeticion(Enum):
    NO_REPETIR = "No repetir"
    REPETIR_ACTUAL = "Repetir actual"
    REPETIR_TODO = "Repetir todo"

    # Método para obtener el nombre legible de la repetición
    @property
    def obtener_nombre_repeticion(self) -> str:
        nombres = {
            Repeticion.NO_REPETIR: "No repetir",
            Repeticion.REPETIR_ACTUAL: "Repetir actual",
            Repeticion.REPETIR_TODO: "Repetir todo",
        }
        return nombres[self]

    # Métodos para verificar si es no repetir
    def es_no_repetir(self) -> bool:
        return self == Repeticion.NO_REPETIR

    # Método para verificar si es repetir actual
    def es_repetir_actual(self) -> bool:
        return self == Repeticion.REPETIR_ACTUAL

    # Método para verificar si es repetir todo
    def es_repetir_todo(self) -> bool:
        return self == Repeticion.REPETIR_TODO

    # Método para imprimir todos los nombres de repetición disponibles
    @classmethod
    def imprimir_nombre_repeticion(cls):
        print("---------------- Repeticiones ----------------")
        for repeticion in cls:
            print(repeticion.obtener_nombre_repeticion)
        print("----------------------------------------------")
