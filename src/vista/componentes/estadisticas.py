from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_vista import *
import customtkinter as ctk
from utiles import Utiles
from constantes import *


class Estadisticas(Utiles):
    def __init__(self, ventana_principal, controlador, controlador_archivos):
        super().__init__(controlador_externo=controlador)
        self.ventana_estadisticas = None
        self.ventana_principal = ventana_principal
        self.controlador = controlador
        self.controlador_archivos = controlador_archivos
        self.componentes = []

    def crear_ventana_estadisticas(self):
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear el panel principal de la ventana de estadísticas
        self.ventana_estadisticas = ctk.CTkToplevel(self.ventana_principal)

        # Configurar la ventana de estadísticas
        configurar_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_estadisticas,
            ancho=ANCHO_ESTADISTICAS,
            alto=ALTO_ESTADISTICAS,
            titulo="Estadísticas",
            color_fondo=self.color_fondo,
            funcion_cierre=self.cerrar_ventana_estadistica,
            controlador=self.controlador,
        )
        # =================================================================================================

        # ======================================== Panel principal ========================================
        # Crear el panel principal de la ventana de estadísticas
        panel_principal_estadisticas = ctk.CTkFrame(
            self.ventana_estadisticas, fg_color=self.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        panel_principal_estadisticas.pack(fill="both", expand=True)
        self.componentes.append(panel_principal_estadisticas)
        # =================================================================================================

    # Metodo para mostrar la ventana de estadisticas
    def mostrar_ventana_estadisticas(self):
        if not hasattr(self, "ventana_estadisticas") or self.ventana_estadisticas is None:
            self.crear_ventana_estadisticas()
        else:
            try:
                # Verificar si la ventana aún existe y es válida
                if self.ventana_estadisticas.winfo_exists():
                    self.colores()
                    establecer_icono_tema(self.ventana_estadisticas, self.controlador.tema_interfaz)
                    self.ventana_estadisticas.deiconify()
                else:
                    # La ventana ya no existe, crear una nueva
                    self.ventana_estadisticas = None
                    self.crear_ventana_estadisticas()
            except Exception as e:
                print(f"Error al mostrar la ventana de estadísticas: {e}")
                self.ventana_estadisticas = None
                self.crear_ventana_estadisticas()

    # Metodo para cerrar la ventana de estadisticas
    def cerrar_ventana_estadistica(self):
        cerrar_ventana_modal(self.ventana_estadisticas, self.componentes, self.controlador)
