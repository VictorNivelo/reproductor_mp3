from vista.componentes.utiles.utiles_componentes import cerrar_ventana_modal
from vista.utiles.utiles_vista import establecer_icono_tema
import customtkinter as ctk
from utiles import Utiles
from constantes import *


class Configuracion(Utiles):
    def __init__(self, ventana_principal, controlador):
        super().__init__(controlador_externo=controlador)
        self.ventana_configuracion = None
        self.ventana_principal = ventana_principal
        self.controlador = controlador
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

        # Establecer el título de la ventana de configuración
        self.ventana_configuracion.title("Configuración")

        # Establecer el tamaño de la ventana de configuración
        posicion_ancho = (
            self.ventana_principal.winfo_x()
            + (self.ventana_principal.winfo_width() - ANCHO_CONFIGURACION) // 2
        )
        posicion_alto = (
            self.ventana_principal.winfo_y()
            + (self.ventana_principal.winfo_height() - ALTO_CONFIGURACION) // 2
        )

        # Tamaño de la ventana de configuración
        tamanio_configuracion = f"{ANCHO_CONFIGURACION}x{ALTO_CONFIGURACION}+{posicion_ancho}+{posicion_alto}"

        # Establecer la geometría de la ventana de configuración
        self.ventana_configuracion.geometry(tamanio_configuracion)

        # Establecer el color de fondo de la ventana de configuración
        self.ventana_configuracion.configure(bg=self.color_fondo)

        # Configuración de la ventana como un modal
        self.ventana_configuracion.grab_set()

        # Evento para cerrar la ventana de configuración
        self.ventana_configuracion.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_configuracion)

        # icono de la ventana
        establecer_icono_tema(self.ventana_configuracion, self.controlador.tema_interfaz)
        # ===========================================================================================

        # ======================= Panel principal de la ventana de configuración ===================
        # Crear el panel principal de la ventana de configuración
        panel_principal_configuracion = ctk.CTkFrame(
            self.ventana_configuracion,
            fg_color=self.color_fondo,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_principal_configuracion.pack(fill="both", expand=True)
        self.componentes.append(panel_principal_configuracion)
        # ==========================================================================================

        # ======================= Componentes de la ventana de configuración =======================
        # titulo del modal
        etiqueta_titulo = ctk.CTkLabel(
            panel_principal_configuracion,
            text="Configuración",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA + 4),
            text_color=self.color_texto,
            fg_color=self.color_fondo,
        )
        etiqueta_titulo.pack(pady=5)
        self.componentes.append(etiqueta_titulo)
        # secciones de configuración
        secciones = ["General", "Audio", "Reproductor", "Interfaz", "Acerca de"]
        # creacion de los botones para cada una de las secciones
        for seccion in secciones:
            # botones de las secciones
            try:
                boton_seccion = ctk.CTkButton(
                    panel_principal_configuracion,
                    height=35,
                    fg_color=self.color_boton,
                    font=(LETRA, TAMANIO_LETRA_BOTON),
                    text_color=self.color_texto,
                    text=seccion,
                    hover_color=self.color_hover,
                    command=lambda s=seccion: self.abrir_seccion(s),
                )
                boton_seccion.pack(fill="x", pady=3, padx=5)
                self.componentes.append(boton_seccion)
            except Exception as e:
                print(f"Error al crear el botón de la sección {seccion}: {e}")
        # botón de cerrar la ventana
        boton_cerrar = ctk.CTkButton(
            panel_principal_configuracion,
            height=35,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            hover_color=self.color_hover,
            command=self.cerrar_ventana_configuracion,
        )
        boton_cerrar.pack(fill="x", pady=(215, 0), padx=5)
        self.componentes.append(boton_cerrar)
        # ==============================================================================================

    # Metodo para mostrar ventana de configuración
    def mostrar_ventana_configuracion(self):
        if not hasattr(self, "ventana_configuracion") or self.ventana_configuracion is None:
            self.crear_ventana_configuracion()
        else:
            try:
                # Verificar si la ventana aún existe y es válida
                self.colores()
                self.ventana_configuracion.winfo_exists()
                establecer_icono_tema(self.ventana_configuracion, self.controlador.tema_interfaz)
                self.ventana_configuracion.deiconify()
            except Exception as e:
                print(f"Error al mostrar la ventana de configuración: {e}")
                # Sí hay error, recrear la ventana
                self.ventana_configuracion = None
                self.crear_ventana_configuracion()

    # Metodo para cerrar ventana de configuración
    def cerrar_ventana_configuracion(self):
        cerrar_ventana_modal(self.ventana_configuracion, self.componentes, self.controlador)

    # Abrir sección de configuración
    @staticmethod
    def abrir_seccion(seccion):
        print(f"Configuración de {seccion}")
