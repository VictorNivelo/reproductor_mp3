from controlador.controlador_archivos import ControladorArchivos
from constantes import *


class GestorAtajos:
    def __init__(self):
        self.ruta_archivo = RUTA_ATAJOS
        self.atajos_por_defecto = {
            "reproducir_pausar": "space",
            "siguiente": "Control-Right",
            "anterior": "Control-Left",
            "aumentar_volumen": "Up",
            "disminuir_volumen": "Down",
            "silenciar": "m",
            "modo_aleatorio": "s",
            "repeticion": "r",
            "visibilidad_panel": "l",
            "me_gusta": "g",
            "favorito": "f",
            "cola": "c",
            "mini_reproductor": "p",
            "adelantar": "Right",
            "retroceder": "Left",
        }
        self.atajos = {}
        self.cargar_atajos()

    # Método para cargar los atajos desde el archivo JSON
    def cargar_atajos(self):
        try:
            controlador = ControladorArchivos()
            self.atajos = controlador.cargar_atajos_json_controlador()
            if not self.atajos:
                self.atajos = self.atajos_por_defecto.copy()
                controlador.guardar_atajos_json_controlador(self.atajos)
        except Exception as e:
            print(f"Error al cargar atajos: {e}")
            self.atajos = self.atajos_por_defecto.copy()

    # Método para guardar los atajos en el archivo JSON
    def guardar_atajos(self):
        try:
            controlador = ControladorArchivos()
            return controlador.guardar_atajos_json_controlador(self.atajos)
        except Exception as e:
            print(f"Error al guardar atajos: {e}")
            return False

    # Método para obtener el atajo de una acción
    def obtener_atajo(self, accion):
        return self.atajos.get(accion, self.atajos_por_defecto.get(accion, ""))

    # Método para establecer un nuevo atajo
    def establecer_atajo(self, accion, tecla):
        # Verificar si la tecla ya está en uso
        for act, key in self.atajos.items():
            if key == tecla and act != accion:
                return False, f"La tecla '{tecla}' ya está asignada a la acción '{act}'"
        self.atajos[accion] = tecla
        self.guardar_atajos()
        return True, f"Atajo para '{accion}' establecido correctamente"

    # Método para eliminar un atajo
    def eliminar_atajo(self, accion):
        if accion in self.atajos:
            self.atajos[accion] = self.atajos_por_defecto.get(accion, "")
            self.guardar_atajos()
            return True, f"Atajo para '{accion}' restaurado al valor por defecto"
        return False, "Acción no encontrada"

    # Método para obtener todos los atajos
    @staticmethod
    def obtener_nombres_atajos():
        return {
            "reproducir_pausar": "Reproducir/Pausar",
            "siguiente": "Siguiente canción",
            "anterior": "Canción anterior",
            "aumentar_volumen": "Aumentar volumen",
            "disminuir_volumen": "Disminuir volumen",
            "silenciar": "Silenciar",
            "modo_aleatorio": "Modo aleatorio",
            "repeticion": "Modo repetición",
            "visibilidad_panel": "Mostrar/Ocultar panel",
            "me_gusta": "Me gusta",
            "favorito": "Favorito",
            "cola": "Ver cola",
            "mini_reproductor": "Mini reproductor",
            "adelantar": "Adelantar",
            "retroceder": "Retroceder",
        }
