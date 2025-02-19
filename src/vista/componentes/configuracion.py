from vista.utiles_vista import establecer_icono_tema
from constantes import *
import customtkinter as ctk


class Configuracion:
    def __init__(self, ventana_principal, controlador):
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

    def crear_ventana_configuracion(self):
        # colores de componentes
        color_fondo = FONDO_OSCURO if self.controlador.tema_interfaz == "oscuro" else FONDO_CLARO
        color_texto = TEXTO_OSCURO if self.controlador.tema_interfaz == "oscuro" else TEXTO_CLARO
        color_boton = BOTON_OSCURO if self.controlador.tema_interfaz == "oscuro" else BOTON_CLARO
        color_hover = HOVER_OSCURO if self.controlador.tema_interfaz == "oscuro" else HOVER_CLARO
        # Crear el panel principal de la ventana de configuración

        self.ventana_configuracion = ctk.CTkToplevel(self.ventana_principal)
        self.ventana_configuracion.title("Configuración")

        # Configuración de la ventana como un modal
        self.ventana_configuracion.grab_set()
        # Establecer el tamaño de la ventana de configuración
        posicion_ancho = (
            self.ventana_principal.winfo_x()
            + (self.ventana_principal.winfo_width() - ANCHO_CONFIGURACION) // 2
        )
        posicion_alto = (
            self.ventana_principal.winfo_y()
            + (self.ventana_principal.winfo_height() - ALTO_CONFIGURACION) // 2
        )
        # Establecer la geometría de la ventana de configuración
        self.ventana_configuracion.geometry(
            f"{ANCHO_CONFIGURACION}x{ALTO_CONFIGURACION}+{posicion_ancho}+{posicion_alto}"
        )

        # Establecer el color de fondo de la ventana de configuración
        self.ventana_configuracion.configure(bg=color_fondo)
        # Evento para cerrar la ventana de configuración
        self.ventana_configuracion.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        # icono de la ventana
        establecer_icono_tema(
            self.ventana_configuracion,
            "oscuro" if self.controlador.tema_interfaz == "oscuro" else "claro",
        )

        # ======================= Panel principal de la ventana de configuración =======================
        self.panel_principal_configuracion = ctk.CTkFrame(
            self.ventana_configuracion, fg_color=color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        self.panel_principal_configuracion.pack(fill="both", expand=True)
        self.componentes.append(self.panel_principal_configuracion)
        # ==============================================================================================

        # ======================= Componentes de la ventana de configuración =======================
        # titulo del modal
        etiqueta_titulo = ctk.CTkLabel(
            self.panel_principal_configuracion,
            text="Configuración",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA + 4),
            text_color=color_texto,
            fg_color=color_fondo,
        )
        etiqueta_titulo.pack(pady=5)
        self.componentes.append(etiqueta_titulo)
        # secciones de configuración
        secciones = ["General", "Audio", "Reproductor", "Interfaz", "Acerca de"]
        # creacion de los botones para cada una de las secciones
        for seccion in secciones:
            # botones de las secciones
            boton_seccion = ctk.CTkButton(
                self.panel_principal_configuracion,
                height=35,
                fg_color=color_boton,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text_color=color_texto,
                text=seccion,
                hover_color=color_hover,
                command=lambda s=seccion: self.abrir_seccion(s),
            )
            boton_seccion.pack(fill="x", pady=3, padx=5)
            self.componentes.append(boton_seccion)
        # botón de cerrar la ventana
        boton_cerrar = ctk.CTkButton(
            self.panel_principal_configuracion,
            height=35,
            fg_color=color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=color_texto,
            text="Cerrar",
            hover_color=color_hover,
            command=self.cerrar_ventana,
        )
        boton_cerrar.pack(fill="x", pady=(215, 0), padx=5)
        self.componentes.append(boton_cerrar)
        # ==============================================================================================

    # abrir sección de configuración
    def abrir_seccion(self, seccion):
        print(f"Configuración de {seccion}")

    # mostrar ventana de configuración
    def mostrar_ventana_configuracion(self):
        if not hasattr(self, "ventana_configuracion") or self.ventana_configuracion is None:
            self.crear_ventana_configuracion()
        else:
            try:
                # Verificar si la ventana aún existe y es válida
                self.ventana_configuracion.winfo_exists()
                establecer_icono_tema(self.ventana_configuracion, self.controlador.tema_interfaz)
                self.ventana_configuracion.deiconify()
            except:
                # Si hay error, recrear la ventana
                self.ventana_configuracion = None
                self.crear_ventana_configuracion()

    # cerrar ventana de configuración
    def cerrar_ventana(self):
        # Eliminar componentes de la ventana de configuración
        try:
            # Eliminar referencias de los componentes en el controlador
            for widget in self.componentes:
                if widget in self.controlador.frames:
                    self.controlador.frames.remove(widget)
                if widget in self.controlador.etiquetas:
                    self.controlador.etiquetas.remove(widget)
                for nombre in list(self.controlador.botones.keys()):
                    if self.controlador.botones[nombre] == widget:
                        del self.controlador.botones[nombre]
            # Limpiar lista de componentes
            self.componentes.clear()
            # Liberar el modo modal
            self.ventana_configuracion.grab_release()
            # Destruir la ventana
            self.ventana_configuracion.destroy()
        except Exception as e:
            print(f"Error durante la limpieza: {e}")
