from vista.utiles import establecer_icono_tema
from vista.constantes import *
import customtkinter as ctk


tamanio_minireproductor = f"{ancho_minireproductor}x{alto_minireproductor}"


class MiniReproductor:
    def __init__(self, ventana_principal, controlador):
        self.ventana_principal = ventana_principal
        self.controlador = controlador
        self.ventana_principal_mini_reproductor = None
        self.widgets = []

    def mostrar(self):
        if self.ventana_principal_mini_reproductor is None:
            self.crear_ventana()
        else:
            establecer_icono_tema(
                self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz
            )
            self.actualizar_colores()
        self.ventana_principal_mini_reproductor.deiconify()
        self.ventana_principal.withdraw()

    def ocultar(self):
        if self.ventana_principal_mini_reproductor:
            self.ventana_principal_mini_reproductor.withdraw()
            self.ventana_principal.deiconify()

    def actualizar_colores(self):
        color_fondo = fondo_oscuro if self.controlador.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.controlador.tema_interfaz == "oscuro" else texto_claro
        color_boton = boton_oscuro if self.controlador.tema_interfaz == "oscuro" else boton_claro
        color_hover = hover_oscuro if self.controlador.tema_interfaz == "oscuro" else hover_claro
        color_progreso = (
            texto_oscuro if self.controlador.tema_interfaz == "oscuro" else fondo_oscuro
        )
        for widget in self.widgets:
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=color_fondo)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(fg_color=color_fondo, text_color=color_texto)
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=color_boton, text_color=color_texto, hover_color=color_hover
                )
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(progress_color=color_progreso, fg_color=color_fondo)

    def crear_ventana(self):
        color_fondo_principal = (
            fondo_principal_claro
            if self.controlador.tema_interfaz == "claro"
            else fondo_principal_oscuro
        )
        color_fondo = fondo_oscuro if self.controlador.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.controlador.tema_interfaz == "oscuro" else texto_claro
        color_boton = boton_oscuro if self.controlador.tema_interfaz == "oscuro" else boton_claro
        color_hover = hover_oscuro if self.controlador.tema_interfaz == "oscuro" else hover_claro
        ctk.set_appearance_mode("dark" if self.controlador.tema_interfaz == "oscuro" else "light")

        self.ventana_principal_mini_reproductor = ctk.CTkToplevel(self.ventana_principal)
        self.ventana_principal_mini_reproductor.title("Minireproductor de música")
        # self.ventana_principal_mini_reproductor.iconbitmap("recursos/iconos/reproductor.ico")
        self.ventana_principal_mini_reproductor.geometry(tamanio_minireproductor)
        self.ventana_principal_mini_reproductor.resizable(False, False)
        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        establecer_icono_tema(
            self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz
        )

        panel_principal_mini_reproductor = ctk.CTkFrame(
            self.ventana_principal_mini_reproductor, fg_color=color_fondo_principal
        )
        panel_principal_mini_reproductor.pack(fill="x", expand=True)
        self.widgets.append(panel_principal_mini_reproductor)

        panel_derecha = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=color_fondo, width=240, height=125
        )
        panel_derecha.pack(side="right", padx=(0, 5), pady=3)
        panel_derecha.pack_propagate(False)
        self.widgets.append(panel_derecha)

        panel_informacion = ctk.CTkFrame(panel_derecha, fg_color=color_fondo)
        panel_informacion.pack(fill="x", padx=5, pady=3)
        self.widgets.append(panel_informacion)

        etiqueta_nombre_cancion = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=color_texto,
            text="Nombre de la canción",
            font=(letra, tamanio_letra_etiqueta - 1.5),
            fg_color=color_fondo,
        )
        etiqueta_nombre_cancion.pack()
        self.widgets.append(etiqueta_nombre_cancion)

        etiqueta_artista = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=color_texto,
            text="Artista",
            font=(letra, tamanio_letra_etiqueta - 1.5),
            fg_color=color_fondo,
        )
        etiqueta_artista.pack()
        self.widgets.append(etiqueta_artista)

        etiqueta_album = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=color_texto,
            text="Álbum",
            font=(letra, tamanio_letra_etiqueta - 1.5),
            fg_color=color_fondo,
        )
        etiqueta_album.pack()
        self.widgets.append(etiqueta_album)

        panel_progreso = ctk.CTkFrame(panel_derecha, fg_color=color_fondo)
        panel_progreso.pack(fill="x", padx=5)
        self.widgets.append(panel_progreso)

        barra_progreso_mini = ctk.CTkProgressBar(
            panel_progreso, height=5, progress_color=color_hover, fg_color="lightgray"
        )
        barra_progreso_mini.pack(fill="x")
        barra_progreso_mini.set(0)
        self.widgets.append(barra_progreso_mini)

        panel_tiempo = ctk.CTkFrame(panel_progreso, fg_color=color_fondo)
        panel_tiempo.pack(fill="x")
        self.widgets.append(panel_tiempo)

        etiqueta_tiempo_inicio = ctk.CTkLabel(
            panel_tiempo,
            height=18,
            text_color=color_texto,
            text="00:00",
            font=(letra, tamanio_letra_tiempo - 1),
            fg_color=color_fondo,
        )
        etiqueta_tiempo_inicio.pack(side="left")
        self.widgets.append(etiqueta_tiempo_inicio)

        etiqueta_tiempo_final = ctk.CTkLabel(
            panel_tiempo,
            height=18,
            text_color=color_texto,
            text="00:00",
            font=(letra, tamanio_letra_tiempo - 1),
            fg_color=color_fondo,
        )
        etiqueta_tiempo_final.pack(side="right")
        self.widgets.append(etiqueta_tiempo_final)

        panel_botones = ctk.CTkFrame(panel_derecha, fg_color=color_fondo)
        panel_botones.pack(fill="x", padx=5, pady=(0, 5))
        self.widgets.append(panel_botones)

        contenedor_botones = ctk.CTkFrame(panel_botones, fg_color=color_fondo)
        contenedor_botones.pack(pady=(0, 3), expand=True)
        self.widgets.append(contenedor_botones)

        boton_anterior = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=color_boton,
            font=(letra, tamanio_letra_boton),
            text_color=color_texto,
            text="",
            hover_color=color_hover,
        )
        boton_anterior.pack(side="left", padx=5)
        self.controlador.registrar_botones("anterior_mini", boton_anterior)
        # self.controlador.registrar_botones("anterior", boton_anterior)

        boton_reproducir = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=color_boton,
            font=(letra, tamanio_letra_boton),
            text_color=color_texto,
            text="",
            hover_color=color_hover,
        )
        boton_reproducir.pack(side="left", padx=5)
        self.controlador.registrar_botones("reproducir_mini", boton_reproducir)
        # self.controlador.registrar_botones("reproducir", boton_reproducir)

        boton_siguiente = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=color_boton,
            font=(letra, tamanio_letra_boton),
            text_color=color_texto,
            text="",
            hover_color=color_hover,
        )
        boton_siguiente.pack(side="left", padx=5)
        self.controlador.registrar_botones("siguiente_mini", boton_siguiente)
        # self.controlador.registrar_botones("siguiente", boton_siguiente)

        boton_maximizar = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=color_boton,
            font=(letra, tamanio_letra_boton),
            text_color=color_texto,
            text="",
            hover_color=color_hover,
            command=self.ocultar,
        )
        boton_maximizar.pack(side="left", padx=5)
        self.controlador.registrar_botones("maximizar_mini", boton_maximizar)
        # self.controlador.registrar_botones("maximizar", boton_maximizar)

        panel_izquierda = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=color_fondo, width=100, height=125
        )
        panel_izquierda.pack(side="left", padx=(5, 0), pady=5)
        panel_izquierda.pack_propagate(False)
        self.widgets.append(panel_izquierda)

        imagen_cancion = ctk.CTkLabel(
            panel_izquierda, text_color=color_texto, text="img", fg_color=color_fondo
        )
        imagen_cancion.pack(pady=5)
        self.widgets.append(imagen_cancion)

        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # self.ventana_principal_mini_reproductor.mainloop()
