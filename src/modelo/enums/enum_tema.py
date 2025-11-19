from enum import Enum
import winreg


class Tema(Enum):
    CLARO = "claro"
    OSCURO = "oscuro"
    SISTEMA = "sistema"

    # Método para obtener el nombre legible del tema
    @property
    def obtener_nombre_tema(self) -> str:
        nombres = {
            Tema.CLARO: "Claro",
            Tema.OSCURO: "Oscuro",
            Tema.SISTEMA: "Sistema",
        }
        return nombres[self]

    # Método para verificar si el tema es claro
    def es_claro(self) -> bool:
        return self == Tema.CLARO

    # Método para verificar si el tema es oscuro
    def es_oscuro(self) -> bool:
        return self == Tema.OSCURO

    # Método para verificar si el tema es sistema
    def es_sistema(self) -> bool:
        return self == Tema.SISTEMA

    # Método estático para obtener el tema del sistema
    @staticmethod
    def obtener_tema_sistema() -> "Tema":
        try:
            # Abrir la clave del registro donde se guarda la preferencia de tema
            clave = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            # Leer el valor AppsUseLightTheme (0 = oscuro, 1 = claro)
            valor, _ = winreg.QueryValueEx(clave, "AppsUseLightTheme")
            winreg.CloseKey(clave)
            # Retornar el tema según el valor
            return Tema.CLARO if valor == 1 else Tema.OSCURO
        except Exception as e:
            print(f"Error al detectar tema del sistema: {e}")
            # Por defecto retornar tema claro si hay error
            return Tema.CLARO

    # Método para determinar el tema efectivo considerando el tema del sistema
    def determinar_tema(self) -> "Tema":
        if self.es_sistema():
            return Tema.obtener_tema_sistema()
        return self
