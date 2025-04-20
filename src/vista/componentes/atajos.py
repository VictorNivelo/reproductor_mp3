from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_vista import *
from utiles import UtilesGeneral
import customtkinter as ctk
from constantes import *


class Atajos(UtilesGeneral):
    def __init__(self, ventana_principal, controlador_tema):
        super().__init__(controlador_externo=controlador_tema)
        self.ventana_atajos = None
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.componentes = []

    # Método para crear la ventana de atajos
    def crear_ventana_atajos(self):
        # Establecer los colores de la interfaz
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear el panel principal de la ventana de atajos
        self.ventana_atajos = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana para que no se pueda maximizar ni minimizar
        self.ventana_atajos.resizable(False, False)
        # Configurar la ventana de atajos
        configurar_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_atajos,
            ancho=ANCHO_ATAJOS,
            alto=ALTO_ATAJOS,
            titulo="Atajos",
            color_fondo=self.color_fondo,
            funcion_cierre=self.cerrar_ventana_atajos,
            controlador=self.controlador_tema,
        )

    # Método para mostrar la ventana de atajos
    def mostrar_ventana_atajos(self):
        if not hasattr(self, "ventana_atajos") or self.ventana_atajos is None:
            self.crear_ventana_atajos()
        else:
            try:
                if self.ventana_atajos.winfo_exists():
                    self.colores()
                    establecer_icono_tema(self.ventana_atajos, self.controlador_tema.tema_interfaz)
                    self.ventana_atajos.deiconify()
                else:
                    self.ventana_atajos = None
                    self.crear_ventana_atajos()
            except Exception as e:
                print(f"Error al mostrar la ventana de atajos: {e}")
                self.ventana_atajos = None
                self.crear_ventana_atajos()

    # Método para cerrar la ventana de atajos
    def cerrar_ventana_atajos(self):
        cerrar_ventana_modal(self.ventana_atajos, self.componentes, self.controlador_tema)
