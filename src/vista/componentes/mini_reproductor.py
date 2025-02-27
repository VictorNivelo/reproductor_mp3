from vista.componentes.utiles.utiles_componentes import UtilesComponentes
from vista.utiles.utiles_vista import establecer_icono_tema
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
        # Actualizar colores
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
        establecer_icono_tema(self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz)
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
        panel_derecha_mini_reproductor = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=240, height=125
        )
        panel_derecha_mini_reproductor.pack(side="right", padx=(0, 5), pady=4)
        panel_derecha_mini_reproductor.pack_propagate(False)
        self.componentes.append(panel_derecha_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel informacion ======================================
        # Crea el panel de información del mini reproductor
        panel_informacion_mini_reproductor = ctk.CTkFrame(
            panel_derecha_mini_reproductor, fg_color=self.color_fondo
        )
        panel_informacion_mini_reproductor.pack(fill="x", padx=5, pady=3)
        self.componentes.append(panel_informacion_mini_reproductor)

        # Crea las etiquetas del mini reproductor
        etiqueta_nombre_cancion_mini_reproductor = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=18,
            text_color=self.color_texto,
            text="Nombre de la canción",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_nombre_cancion_mini_reproductor.pack()
        self.componentes.append(etiqueta_nombre_cancion_mini_reproductor)

        etiqueta_artista_mini_reproductor = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=18,
            text_color=self.color_texto,
            text="Artista",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_artista_mini_reproductor.pack()
        self.componentes.append(etiqueta_artista_mini_reproductor)

        etiqueta_album_mini_reproductor = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=18,
            text_color=self.color_texto,
            text="Álbum",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1.5),
            fg_color=self.color_fondo,
        )
        etiqueta_album_mini_reproductor.pack()
        self.componentes.append(etiqueta_album_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel progreso =========================================
        # Crea el panel de progreso del mini reproductor
        panel_progreso_mini_reproductor = ctk.CTkFrame(
            panel_derecha_mini_reproductor, fg_color=self.color_fondo
        )
        panel_progreso_mini_reproductor.pack(fill="x", padx=5)
        self.componentes.append(panel_progreso_mini_reproductor)

        # Crea la barra de progreso del mini reproductor
        barra_progreso_mini_reproductor = ctk.CTkProgressBar(
            panel_progreso_mini_reproductor,
            height=5,
            progress_color=self.color_hover,
            fg_color="lightgray",
        )
        barra_progreso_mini_reproductor.pack(fill="x")
        barra_progreso_mini_reproductor.set(0)
        self.componentes.append(barra_progreso_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel tiempo ===========================================
        # Crea el panel de tiempo del mini reproductor
        panel_tiempo_mini_reproductor = ctk.CTkFrame(
            panel_progreso_mini_reproductor, fg_color=self.color_fondo
        )
        panel_tiempo_mini_reproductor.pack(fill="x")
        self.componentes.append(panel_tiempo_mini_reproductor)

        # Crea las etiquetas de tiempo del mini reproductor
        etiqueta_tiempo_inicio_mini_reproductor = ctk.CTkLabel(
            panel_tiempo_mini_reproductor,
            height=18,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color=self.color_fondo,
        )
        etiqueta_tiempo_inicio_mini_reproductor.pack(side="left")
        self.componentes.append(etiqueta_tiempo_inicio_mini_reproductor)

        etiqueta_tiempo_final_mini_reproductor = ctk.CTkLabel(
            panel_tiempo_mini_reproductor,
            height=18,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color=self.color_fondo,
        )
        etiqueta_tiempo_final_mini_reproductor.pack(side="right")
        self.componentes.append(etiqueta_tiempo_final_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel botones ==========================================
        # Crea el panel de botones del mini reproductor
        panel_botones_mini_reproductor = ctk.CTkFrame(
            panel_derecha_mini_reproductor, fg_color=self.color_fondo
        )
        panel_botones_mini_reproductor.pack(fill="x", padx=5, pady=(0, 5))
        self.componentes.append(panel_botones_mini_reproductor)

        # Crea el contenedor de botones del mini reproductor
        contenedor_botones_mini_reproductor = ctk.CTkFrame(
            panel_botones_mini_reproductor, fg_color=self.color_fondo
        )
        contenedor_botones_mini_reproductor.pack(pady=(0, 3), expand=True)
        self.componentes.append(contenedor_botones_mini_reproductor)

        # Crea los botones del mini reproductor
        boton_me_gusta_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_me_gusta_mini_reproductor.pack(side="left", padx=5)
        self.controlador.registrar_botones("me_gusta_mini", boton_me_gusta_mini_reproductor)

        boton_anterior_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_anterior_mini_reproductor.pack(side="left", padx=5)
        self.controlador.registrar_botones("anterior_mini", boton_anterior_mini_reproductor)

        boton_reproducir_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_reproducir_mini_reproductor.pack(side="left", padx=5)
        self.controlador.registrar_botones("reproducir_mini", boton_reproducir_mini_reproductor)

        boton_siguiente_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=TEXTO_CLARO,
            text="",
            hover_color=self.color_hover,
        )
        boton_siguiente_mini_reproductor.pack(side="left", padx=5)
        self.controlador.registrar_botones("siguiente_mini", boton_siguiente_mini_reproductor)

        boton_maximizar_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
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
        boton_maximizar_mini_reproductor.pack(side="left", padx=5)
        self.controlador.registrar_botones("maximizar_mini", boton_maximizar_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel izquierda ========================================
        # Crea el panel izquierdo del mini reproductor
        panel_izquierda_mini_reproductor = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=100, height=125
        )
        panel_izquierda_mini_reproductor.pack(side="left", padx=(5, 0), pady=4)
        panel_izquierda_mini_reproductor.pack_propagate(False)
        self.componentes.append(panel_izquierda_mini_reproductor)

        # Crea la imagen de la canción del mini reproductor
        imagen_cancion_mini_reproductor = ctk.CTkLabel(
            panel_izquierda_mini_reproductor,
            text_color=self.color_texto,
            text="img",
            fg_color=self.color_fondo,
        )
        imagen_cancion_mini_reproductor.pack(pady=5)
        self.componentes.append(imagen_cancion_mini_reproductor)
        # =================================================================================================

        # Protocolo para cerrar la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # self.ventana_principal_mini_reproductor.mainloop()

    # Metodo para mostrar la ventana del mini reproductor
    def mostrar_ventana_mini_reproductor(self):
        # Verificar si la ventana del mini reproductor es None o fue destruida
        ventana_destruida = False
        if self.ventana_principal_mini_reproductor is not None:
            try:
                existe = self.ventana_principal_mini_reproductor.winfo_exists()
                if not existe:
                    ventana_destruida = True
            except tk.TclError:
                ventana_destruida = True
        # Crear o recrear la ventana si es necesario
        if self.ventana_principal_mini_reproductor is None or ventana_destruida:
            self.ventana_principal_mini_reproductor = (
                None  # Asegurarse de que sea None antes de crear una nueva
            )
            self.crear_ventana_mini_reproductor()
        else:
            # La ventana existe, actualizar colores e icono
            try:
                self.colores()
                establecer_icono_tema(self.ventana_principal_mini_reproductor, self.controlador.tema_interfaz)
                self.actualizar_colores()
            except tk.TclError:
                # Si hay un error al actualizar, recrear la ventana
                self.ventana_principal_mini_reproductor = None
                self.crear_ventana_mini_reproductor()
        # Mostrar la ventana del mini reproductor de forma segura
        try:
            if (
                self.ventana_principal_mini_reproductor
                and self.ventana_principal_mini_reproductor.winfo_exists()
            ):
                self.ventana_principal_mini_reproductor.deiconify()
                self.ventana_principal.withdraw()
        except tk.TclError as e:
            print(f"Error al mostrar el mini reproductor: {e}")

    # Metodo para ocultar la ventana del mini reproductor
    def ocultar(self):
        if self.ventana_principal_mini_reproductor:
            try:
                if self.ventana_principal_mini_reproductor.winfo_exists():
                    self.ventana_principal_mini_reproductor.withdraw()
            except tk.TclError:
                pass
            self.ventana_principal.deiconify()

    # Metodo para actualizar los colores de los componentes del mini reproductor
    def actualizar_colores(self):
        self.colores()
        # Actualizar colores de los componentes
        for widget in self.componentes:
            try:
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
            except tk.TclError:
                print("Error al actualizar colores del mini reproductor")
