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
        crear_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_atajos,
            ancho=ANCHO_ATAJOS,
            alto=ALTO_ATAJOS,
            titulo="Atajos",
            color_fondo=self.color_fondo,
            funcion_cierre=self.cerrar_ventana_atajos,
            controlador=self.controlador_tema,
        )
        # =================================================================================================

        # ======================================== Panel principal ========================================
        # Crear el panel principal de la ventana de atajos
        panel_principal_atajos = ctk.CTkFrame(
            self.ventana_atajos,
            fg_color=self.color_fondo_principal,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_principal_atajos.pack(fill="both", expand=True)
        self.componentes.append(panel_principal_atajos)

        # **************************************** Panel de atajos ****************************************
        # Crear el panel de atajos
        panel_atajos_general = ctk.CTkFrame(
            panel_principal_atajos,
            fg_color=self.color_fondo,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_atajos_general.pack(pady=3, padx=3, fill="both", expand=True)

        # -------------------------------------- Etiquetas de atajos --------------------------------------
        # Crear etiquetas para los atajos
        etiqueta_atajos_general = ctk.CTkLabel(
            panel_atajos_general,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TITULO, "bold"),
            text_color=self.color_texto,
            text="Atajos de teclado",
        )
        etiqueta_atajos_general.pack()
        self.componentes.append(etiqueta_atajos_general)
        self.controlador_tema.registrar_etiqueta(etiqueta_atajos_general)
        # -------------------------------------------------------------------------------------------------

        # ----------------------------------------- Botón cerrar ------------------------------------------
        # Botón para cerrar la ventana de estadísticas
        boton_cerrar_atajos = ctk.CTkButton(
            panel_atajos_general,
            width=ANCHO_BOTON,
            height=ALTO_BOTON + 5,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            command=self.cerrar_ventana_atajos,
        )
        boton_cerrar_atajos.pack(pady=3)
        self.componentes.append(boton_cerrar_atajos)
        crear_tooltip(boton_cerrar_atajos, "Cerrar ventana de atajos")
        # -------------------------------------------------------------------------------------------------

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
