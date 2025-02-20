from vista.componentes.utiles_componentes import UtilesComponentes
from vista.utiles_vista import establecer_icono_tema
import customtkinter as ctk
from constantes import *
import tkinter as tk


class MiniReproductor(UtilesComponentes):
    def __init__(self, ventana_principal, controlador):
        super().__init__(controlador)
        self.ventana_principal_mini_reproductor = None
        self.ventana_principal = ventana_principal
        self.controlador = controlador
        self.componentes = []

    # Metodo para crear la ventana del mini reproductors
    def crear_ventana_mini_reproductor(self):
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear la ventana del mini reproductor
        self.ventana_principal_mini_reproductor = ctk.CTkToplevel(self.ventana_principal)

        # Título de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.title("Minireproductor de música")
        # self.ventana_principal_mini_reproductor.iconbitmap("recursos/iconos/reproductor.ico")

        # Tamanio de componentes
        tamanio_minireproductor = f"{ANCHO_MINI_REPRODUCTOR}x{ALTO_MINI_REPRODUCTOR}"

        # Establecer la geometría de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.geometry(tamanio_minireproductor)

        # Configuración de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.resizable(False, False)

        # Configuración de la ventana como un modal
        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # Establecer el icono de la ventana del mini reproductor
        establecer_icono_tema(
            self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz
        )
        # =================================================================================================

        # ======================================= Panel principal =========================================
        # Crea el panel principal del mini reproductor
        panel_principal_mini_reproductor = ctk.CTkFrame(
            self.ventana_principal_mini_reproductor,
            fg_color=self.color_fondo_principal,
            corner_radius=0,
        )
        # panel_principal_mini_reproductor configure(bg=self.color_fondo_principal)
        panel_principal_mini_reproductor.pack(fill="x", expand=True)
        self.componentes.append(panel_principal_mini_reproductor)
        # =================================================================================================

        # ========================================= Panel derecho =========================================
        # Crea el panel derecho del mini reproductor
        panel_derecha = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=240, height=125
        )
        panel_derecha.pack(side="right", padx=(0, 5), pady=4)
        panel_derecha.pack_propagate(False)
        self.componentes.append(panel_derecha)
        # =================================================================================================

        # ======================================== Panel informacion ======================================
        # Crea el panel de información del mini reproductor
        panel_informacion = ctk.CTkFrame(panel_derecha, fg_color=self.color_fondo)
        panel_informacion.pack(fill="x", padx=5, pady=3)
        self.componentes.append(panel_informacion)

        # Crea las etiquetas del mini reproductor
        etiqueta_nombre_cancion = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=self.color_texto,
            text="Nombre de la canción",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_nombre_cancion.pack()
        self.componentes.append(etiqueta_nombre_cancion)

        etiqueta_artista = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=self.color_texto,
            text="Artista",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_artista.pack()
        self.componentes.append(etiqueta_artista)

        etiqueta_album = ctk.CTkLabel(
            panel_informacion,
            height=18,
            text_color=self.color_texto,
            text="Álbum",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_album.pack()
        self.componentes.append(etiqueta_album)
        # =================================================================================================

        # ======================================== Panel progreso =========================================
        # Crea el panel de progreso del mini reproductor
        panel_progreso = ctk.CTkFrame(panel_derecha, fg_color=self.color_fondo)
        panel_progreso.pack(fill="x", padx=5)
        self.componentes.append(panel_progreso)

        # Crea la barra de progreso del mini reproductor
        barra_progreso_mini = ctk.CTkProgressBar(
            panel_progreso, height=5, progress_color=self.color_hover, fg_color="lightgray"
        )
        barra_progreso_mini.pack(fill="x")
        barra_progreso_mini.set(0)
        self.componentes.append(barra_progreso_mini)
        # =================================================================================================

        # ======================================== Panel tiempo ===========================================
        # Crea el panel de tiempo del mini reproductor
        panel_tiempo = ctk.CTkFrame(panel_progreso, fg_color=self.color_fondo)
        panel_tiempo.pack(fill="x")
        self.componentes.append(panel_tiempo)

        # Crea las etiquetas de tiempo del mini reproductor
        etiqueta_tiempo_inicio = ctk.CTkLabel(
            panel_tiempo,
            height=18,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color=self.color_fondo,
        )
        etiqueta_tiempo_inicio.pack(side="left")
        self.componentes.append(etiqueta_tiempo_inicio)

        etiqueta_tiempo_final = ctk.CTkLabel(
            panel_tiempo,
            height=18,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color=self.color_fondo,
        )
        etiqueta_tiempo_final.pack(side="right")
        self.componentes.append(etiqueta_tiempo_final)
        # =================================================================================================

        # ======================================== Panel botones ==========================================
        # Crea el panel de botones del mini reproductor
        panel_botones = ctk.CTkFrame(panel_derecha, fg_color=self.color_fondo)
        panel_botones.pack(fill="x", padx=5, pady=(0, 5))
        self.componentes.append(panel_botones)

        # Crea el contenedor de botones del mini reproductor
        contenedor_botones = ctk.CTkFrame(panel_botones, fg_color=self.color_fondo)
        contenedor_botones.pack(pady=(0, 3), expand=True)
        self.componentes.append(contenedor_botones)

        # Crea los botones del mini reproductor
        boton_me_gusta = ctk.CTkButton(
            contenedor_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_me_gusta.pack(side="left", padx=5)
        self.controlador.registrar_botones("me_gusta_mini", boton_me_gusta)

        boton_anterior = ctk.CTkButton(
            contenedor_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_anterior.pack(side="left", padx=5)
        self.controlador.registrar_botones("anterior_mini", boton_anterior)

        boton_reproducir = ctk.CTkButton(
            contenedor_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_reproducir.pack(side="left", padx=5)
        self.controlador.registrar_botones("reproducir_mini", boton_reproducir)

        boton_siguiente = ctk.CTkButton(
            contenedor_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_siguiente.pack(side="left", padx=5)
        self.controlador.registrar_botones("siguiente_mini", boton_siguiente)

        boton_maximizar = ctk.CTkButton(
            contenedor_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
            command=self.ocultar,
        )
        boton_maximizar.pack(side="left", padx=5)
        self.controlador.registrar_botones("maximizar_mini", boton_maximizar)
        # =================================================================================================

        # ======================================== Panel izquierda ========================================
        # Crea el panel izquierdo del mini reproductor
        panel_izquierda = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=100, height=125
        )
        panel_izquierda.pack(side="left", padx=(5, 0), pady=4)
        panel_izquierda.pack_propagate(False)
        self.componentes.append(panel_izquierda)

        # Crea la imagen de la canción del mini reproductor
        imagen_cancion = ctk.CTkLabel(
            panel_izquierda, text_color=self.color_texto, text="img", fg_color=self.color_fondo
        )
        imagen_cancion.pack(pady=5)
        self.componentes.append(imagen_cancion)
        # =================================================================================================

        # Protocolo para cerrar la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # self.ventana_principal_mini_reproductor.mainloop()

    # Metodo para mostrar la ventana del mini reproductor
    def mostrar_ventana_mini_reproductor(self):
        if self.ventana_principal_mini_reproductor is None:
            self.crear_ventana_mini_reproductor()
        else:
            try:
                # Verificar si la ventana del mini reproductor fue destruida
                self.colores()
                establecer_icono_tema(
                    self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz
                )
                self.actualizar_colores()
            except tk.TclError:
                # Si la ventana fue destruida, crear una nueva
                self.ventana_principal_mini_reproductor = None
                self.crear_ventana_mini_reproductor()
        # Mostrar la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.deiconify()
        self.ventana_principal.withdraw()

    # Metodo para ocultar la ventana del mini reproductor
    def ocultar(self):
        if self.ventana_principal_mini_reproductor:
            self.ventana_principal_mini_reproductor.withdraw()
            self.ventana_principal.deiconify()

    # Metodo para actualizar los colores de los componentes del mini reproductor
    def actualizar_colores(self):
        self.colores()
        # Actualizar colores de los componentes
        for widget in self.componentes:
            if isinstance(widget, ctk.CTkFrame):
                if widget.winfo_parent() == str(self.ventana_principal_mini_reproductor):
                    widget.configure(fg_color=self.color_fondo_principal)
                else:
                    widget.configure(fg_color=self.color_fondo)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(fg_color=self.color_fondo, text_color=self.color_texto)
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=self.color_boton,
                    text_color=self.color_texto,
                    hover_color=self.color_hover,
                )
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(progress_color=self.color_progreso, fg_color=self.color_fondo)
