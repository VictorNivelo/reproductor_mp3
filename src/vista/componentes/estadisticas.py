from vista.componentes.utiles.utiles_componentes import cerrar_ventana_modal
from vista.utiles.utiles_vista import establecer_icono_tema
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

        # Establecer el título de la ventana de estadísticas
        self.ventana_estadisticas.title("Estadísticas")

        # Establecer el tamaño de la ventana de estadísticas
        posicion_ancho_estadisticas = (
            self.ventana_principal.winfo_x()
            + (self.ventana_principal.winfo_width() - ANCHO_ESTADISTICAS) // 2
        )
        posicion_alto_estadisticas = (
            self.ventana_principal.winfo_y()
            + (self.ventana_principal.winfo_height() - ALTO_ESTADISTICAS) // 2
        )

        # Tamaño de la ventana de estadísticas
        tamanio_estadisticas = f"{ANCHO_ESTADISTICAS}x{ALTO_ESTADISTICAS}+{posicion_ancho_estadisticas}+{posicion_alto_estadisticas}"

        # Establecer la geometría de la ventana de estadísticas
        self.ventana_estadisticas.geometry(tamanio_estadisticas)

        # Establecer el color de fondo de la ventana de estadísticas
        self.ventana_estadisticas.configure(fg_color=self.color_fondo)

        # Configuración de la ventana como un modal
        self.ventana_estadisticas.grab_set()

        # Evento para cerrar la ventana de estadísticas
        self.ventana_estadisticas.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_estadistica)

        # Establecer el icono de la ventana de estadísticas
        establecer_icono_tema(self.ventana_estadisticas, self.controlador.tema_interfaz)
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
                self.colores()
                self.ventana_estadisticas.winfo_exists()
                establecer_icono_tema(self.ventana_estadisticas, self.controlador.tema_interfaz)
                self.ventana_estadisticas.deiconify()
            except Exception as e:
                print(f"Error al mostrar la ventana de estadisticas: {e}")
                self.ventana_estadisticas = None
                self.crear_ventana_estadisticas()

    # Metodo para cerrar la ventana de estadisticas
    def cerrar_ventana_estadistica(self):
        cerrar_ventana_modal(self.ventana_estadisticas, self.componentes, self.controlador)
