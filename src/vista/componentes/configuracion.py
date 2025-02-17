from vista.utiles import establecer_icono_tema
from vista.constantes import *
import customtkinter as ctk


class VentanaConfiguracion:
    def __init__(self, ventana_padre, controlador):
        self.ventana_padre = ventana_padre
        self.ventana_configuracion = ctk.CTkToplevel(ventana_padre)
        self.ventana_configuracion.title("Configuración")
        self.controlador = controlador
        self.widgets = []

        # icono de la ventana
        establecer_icono_tema(
            self.ventana_configuracion,
            "oscuro" if self.controlador.tema_interfaz == "oscuro" else "claro",
        )

        """
        establecer el icono de la ventana de configuración después de 200 ms
        uso cuando no se modifica el CTkToplevel de customtkinter
        """
        # if system() == "Windows":
        #     self.ventana_configuracion.after(
        #         200,
        #         lambda: self.ventana_configuracion.iconbitmap("recursos/iconos/reproductor.ico"),
        #     )

        # colores de componentes
        color_fondo = fondo_oscuro if self.controlador.tema_interfaz == "oscuro" else fondo_claro
        # Configuración de la ventana como un modal
        self.ventana_configuracion.grab_set()
        # Establecer el tamaño de la ventana de configuración
        posicion_ancho = (
            ventana_padre.winfo_x() + (ventana_padre.winfo_width() - ancho_configuracion) // 2
        )
        posicion_alto = (
            ventana_padre.winfo_y() + (ventana_padre.winfo_height() - alto_configuracion) // 2
        )
        # Establecer la geometría de la ventana de configuración
        self.ventana_configuracion.geometry(
            f"{ancho_configuracion}x{alto_configuracion}+{posicion_ancho}+{posicion_alto}"
        )
        # Crear los widgets de la ventana de configuración
        self._crear_widgets()
        # Establecer el color de fondo de la ventana de configuración
        self.ventana_configuracion.configure(bg=color_fondo)
        # Evento para cerrar la ventana de configuración
        self.ventana_configuracion.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def _crear_widgets(self):
        # colores de componentes
        color_fondo = fondo_oscuro if self.controlador.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.controlador.tema_interfaz == "oscuro" else texto_claro
        color_boton = boton_oscuro if self.controlador.tema_interfaz == "oscuro" else boton_claro
        color_hover = hover_oscuro if self.controlador.tema_interfaz == "oscuro" else hover_claro
        self.panel_principal_configuracion = ctk.CTkFrame(
            self.ventana_configuracion, fg_color=color_fondo, corner_radius=bordes_redondeados_frame
        )
        self.panel_principal_configuracion.pack(fill="both", expand=True)
        self.widgets.append(self.panel_principal_configuracion)
        # titulo del modal
        etiqueta_titulo = ctk.CTkLabel(
            self.panel_principal_configuracion,
            text="Configuración",
            font=(letra, tamanio_letra_etiqueta + 4),
            text_color=color_texto,
            fg_color=color_fondo,
        )
        etiqueta_titulo.pack(pady=5)
        self.widgets.append(etiqueta_titulo)
        # secciones de configuración
        secciones = ["General", "Audio", "Reproductor", "Interfaz", "Acerca de"]
        # creacion de los botones para cada una de las secciones
        for seccion in secciones:
            # botones de las secciones
            boton_seccion = ctk.CTkButton(
                self.panel_principal_configuracion,
                height=35,
                fg_color=color_boton,
                font=(letra, tamanio_letra_boton),
                text_color=color_texto,
                text=seccion,
                hover_color=color_hover,
                command=lambda s=seccion: self.abrir_seccion(s),
            )
            boton_seccion.pack(fill="x", pady=3, padx=5)
            self.widgets.append(boton_seccion)
        # botón de cerrar la ventana
        boton_cerrar = ctk.CTkButton(
            self.panel_principal_configuracion,
            height=35,
            fg_color=color_boton,
            font=(letra, tamanio_letra_boton),
            text_color=color_texto,
            text="Cerrar",
            hover_color=color_hover,
            command=self.cerrar_ventana,
        )
        boton_cerrar.pack(fill="x", pady=(215, 0), padx=5)
        self.widgets.append(boton_cerrar)

    # abrir sección de configuración
    def abrir_seccion(self, seccion):
        print(f"Configuración de {seccion}")

    # cerrar ventana de configuración
    def cerrar_ventana(self):
        # Eliminar widgets de la ventana de configuración
        try:
            # Eliminar referencias de los widgets en el controlador
            for widget in self.widgets:
                if widget in self.controlador.frames:
                    self.controlador.frames.remove(widget)
                if widget in self.controlador.etiquetas:
                    self.controlador.etiquetas.remove(widget)
                for nombre in list(self.controlador.botones.keys()):
                    if self.controlador.botones[nombre] == widget:
                        del self.controlador.botones[nombre]
            # Limpiar lista de widgets
            self.widgets.clear()
            # Liberar el modo modal
            self.ventana_configuracion.grab_release()
            # Destruir la ventana
            self.ventana_configuracion.destroy()
        except Exception as e:
            print(f"Error durante la limpieza: {e}")
