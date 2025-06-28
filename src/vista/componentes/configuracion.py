from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_vista import *
from utiles import UtilesGeneral
import customtkinter as ctk
from constantes import *


class Configuracion(UtilesGeneral):
    def __init__(self, ventana_principal, controlador_tema):
        super().__init__(controlador_externo=controlador_tema)
        self.ventana_configuracion = None
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.componentes = []

        """
        establecer el icono de la ventana de configuración después de 200 ms
        uso cuando no se modifica el CTkToplevel de customtkinter
        """
        # if system() == "Windows":
        #     self.ventana_configuracion.after(
        #         200,
        #         lambda: self.ventana_configuracion.iconbitmap("recursos/iconos/reproductor.ico"),
        #     )

    # Crear ventana de configuración de la aplicación
    def crear_ventana_configuracion(self):
        # Establecer los colores de la interfaz
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear el panel principal de la ventana de configuración
        self.ventana_configuracion = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana para que no se pueda maximizar ni minimizar
        self.ventana_configuracion.resizable(False, False)
        # Configurar la ventana de configuración
        crear_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_configuracion,
            ancho=ANCHO_CONFIGURACION,
            alto=ALTO_CONFIGURACION,
            titulo="Configuración",
            color_fondo=self.color_fondo_principal,
            funcion_cierre=self.cerrar_ventana_configuracion,
            controlador=self.controlador_tema,
        )
        # ===========================================================================================

        # ======================= Panel principal de la ventana de configuración ===================
        # Crear el panel principal de la ventana de configuración
        panel_principal_configuracion = ctk.CTkFrame(
            self.ventana_configuracion, fg_color=self.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        panel_principal_configuracion.pack(fill="both", expand=True, padx=3, pady=3)
        self.componentes.append(panel_principal_configuracion)
        # ==========================================================================================

        # ======================= Componentes de la ventana de configuración =======================
        # titulo del modal
        etiqueta_titulo = ctk.CTkLabel(
            panel_principal_configuracion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TITULO, "bold"),
            text_color=self.color_texto,
            text="Configuración",
        )
        etiqueta_titulo.pack(pady=5)
        self.componentes.append(etiqueta_titulo)
        # secciones de configuración
        secciones = ["General", "Audio", "Reproductor", "Interfaz", "Acerca de"]
        # Creación de los botones para cada una de las secciones
        for seccion in secciones:
            # botones de las secciones
            try:
                boton_seccion = ctk.CTkButton(
                    panel_principal_configuracion,
                    width=ANCHO_BOTON,
                    height=ALTO_BOTON,
                    corner_radius=BORDES_REDONDEADOS_BOTON,
                    fg_color=self.color_boton,
                    hover_color=self.color_hover,
                    font=(LETRA, TAMANIO_LETRA_BOTON),
                    text_color=self.color_texto,
                    text=seccion,
                    command=lambda s=seccion: self.abrir_seccion(s),
                )
                boton_seccion.pack(fill="x", padx=3, pady=(0,3))
                self.componentes.append(boton_seccion)
                crear_tooltip(boton_seccion, f"Abrir configuración de {seccion}")
            except Exception as e:
                print(f"Error al crear el botón de la sección {seccion}: {e}")
        # ---------------------------------------- Botón cerrar ----------------------------------------
        # botón de cerrar la ventana
        boton_cerrar_configuracion = ctk.CTkButton(
            panel_principal_configuracion,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            command=self.cerrar_ventana_configuracion,
        )
        boton_cerrar_configuracion.pack(side="bottom", pady=3)
        self.componentes.append(boton_cerrar_configuracion)
        crear_tooltip(boton_cerrar_configuracion, "Cerrar ventana de configuración")
        # ----------------------------------------------------------------------------------------------
        # ==============================================================================================

    # Método para mostrar ventana de configuración
    def mostrar_ventana_configuracion(self):
        if not hasattr(self, "ventana_configuracion") or self.ventana_configuracion is None:
            self.crear_ventana_configuracion()
        else:
            try:
                # Verificar si la ventana aún existe y es válida
                if self.ventana_configuracion.winfo_exists():
                    self.colores()
                    establecer_icono_tema(self.ventana_configuracion, self.controlador_tema.tema_interfaz)
                    self.ventana_configuracion.deiconify()
                else:
                    # La ventana ya no existe, crear una nueva
                    self.ventana_configuracion = None
                    self.crear_ventana_configuracion()
            except Exception as e:
                print(f"Error al mostrar la ventana de configuración: {e}")
                # Sí hay error, recrear la ventana
                self.ventana_configuracion = None
                self.crear_ventana_configuracion()

    # Método para cerrar ventana de configuración
    def cerrar_ventana_configuracion(self):
        cerrar_ventana_modal(self.ventana_configuracion, self.componentes, self.controlador_tema)

    # Abrir sección de configuración
    @staticmethod
    def abrir_seccion(seccion):
        print(f"Configuración de {seccion}")
