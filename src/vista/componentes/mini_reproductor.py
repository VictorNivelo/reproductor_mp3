from vista.utiles.utiles_vista import establecer_icono_tema
from utiles import UtilesGeneral
import customtkinter as ctk
from constantes import *


class MiniReproductor(UtilesGeneral):
    def __init__(self, ventana_principal, controlador_tema):
        super().__init__(controlador_externo=controlador_tema)
        self.ventana_principal_mini_reproductor = None
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.controlador_reproductor = None
        self.foto_caratula_mini = None
        self.componentes = []
        self.posicion_mini_reproductor = "superior_izquierda"
        # Referencias a elementos que mostrarán información
        self.etiqueta_nombre_cancion_mini = None
        self.etiqueta_artista_mini = None
        self.etiqueta_album_mini = None
        self.imagen_cancion_mini = None
        self.etiqueta_tiempo_inicio_mini = None
        self.etiqueta_tiempo_final_mini = None
        self.barra_progreso_mini = None
        # Referencias a botones
        self.boton_reproducir_mini = None
        self.boton_anterior_mini = None
        self.boton_siguiente_mini = None
        self.boton_me_gusta_mini = None
        # Variables para el movimiento de la ventana
        self.x = None
        self.y = None

    # Método para establecer el controlador del reproductor
    def establecer_controlador_reproductor(self, controlador_reproductor):
        self.controlador_reproductor = controlador_reproductor
        # Aplicar eventos de movimiento si la ventana ya está creada
        if self.ventana_principal_mini_reproductor:
            self.aplicar_eventos_movimiento()

    # Método para crear la ventana del mini reproductor
    def crear_ventana_mini_reproductor(self):
        # Actualizar colores
        self.colores()

        # ======================================= Ventana principal =======================================
        # Crear la ventana del mini reproductor
        self.ventana_principal_mini_reproductor = ctk.CTkToplevel(self.ventana_principal)

        # Eliminar la barra de título y los bordes de la ventana
        self.ventana_principal_mini_reproductor.overrideredirect(True)

        # Título de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.title("Minireproductor de música")
        # self.ventana_principal_mini_reproductor.iconbitmap("recursos/iconos/reproductor.ico")

        # Tamanio de componentes
        tamanio_minireproductor = f"{ANCHO_MINI_REPRODUCTOR}x{ALTO_MINI_REPRODUCTOR}"

        # Establecer la geometría de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.geometry(tamanio_minireproductor)

        # Configuración de la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.resizable(False, False)

        # Establecer el icono de la ventana del mini reproductor
        establecer_icono_tema(self.ventana_principal_mini_reproductor, self.controlador_tema.tema_interfaz)
        # =================================================================================================

        # ======================================= Panel principal =========================================
        # Crea el panel principal del mini reproductor
        panel_principal_mini_reproductor = ctk.CTkFrame(
            self.ventana_principal_mini_reproductor,
            fg_color=self.color_fondo_principal,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        # panel_principal_mini_reproductor configure(bg=self.color_fondo_principal)
        panel_principal_mini_reproductor.pack(fill="x", expand=True)
        self.componentes.append(panel_principal_mini_reproductor)
        # =================================================================================================

        # ========================================= Panel derecho =========================================
        # Crea el panel derecho del mini reproductor
        panel_derecha_mini_reproductor = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=250, height=125
        )
        panel_derecha_mini_reproductor.pack(side="right", padx=(0, 5), pady=5)
        panel_derecha_mini_reproductor.pack_propagate(False)
        self.componentes.append(panel_derecha_mini_reproductor)
        # =================================================================================================

        # ======================================== Panel informacion ======================================
        # Crea el panel de información del mini reproductor
        panel_informacion_mini_reproductor = ctk.CTkFrame(
            panel_derecha_mini_reproductor, fg_color="transparent"
        )
        panel_informacion_mini_reproductor.pack(fill="x", padx=5, pady=3)
        self.componentes.append(panel_informacion_mini_reproductor)

        # -------------------------------------- Etiqueta de título ---------------------------------------
        # Crea las etiquetas del mini reproductor
        self.etiqueta_nombre_cancion_mini = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=20,
            text_color=self.color_texto,
            text="Sin reproducción",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1),
            fg_color="transparent",
        )
        self.etiqueta_nombre_cancion_mini.pack()
        self.componentes.append(self.etiqueta_nombre_cancion_mini)
        # -------------------------------------------------------------------------------------------------

        # ------------------------------------- Etiquetas de artista --------------------------------------
        self.etiqueta_artista_mini = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=20,
            text_color=self.color_texto,
            text="",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1),
            fg_color="transparent",
        )
        self.etiqueta_artista_mini.pack()
        self.componentes.append(self.etiqueta_artista_mini)
        # -------------------------------------------------------------------------------------------------

        # -------------------------------------- Etiquetas de álbum ---------------------------------------
        self.etiqueta_album_mini = ctk.CTkLabel(
            panel_informacion_mini_reproductor,
            height=20,
            text_color=self.color_texto,
            text="",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA - 1),
            fg_color="transparent",
        )
        self.etiqueta_album_mini.pack()
        self.componentes.append(self.etiqueta_album_mini)
        # -------------------------------------------------------------------------------------------------
        # =================================================================================================

        # ======================================== Panel progreso =========================================
        # Crea el panel de progreso del mini reproductor
        panel_progreso_mini_reproductor = ctk.CTkFrame(panel_derecha_mini_reproductor, fg_color="transparent")
        panel_progreso_mini_reproductor.pack(fill="x", padx=5)
        self.componentes.append(panel_progreso_mini_reproductor)

        # --------------------------------------- Barra de progreso ---------------------------------------
        # Crea la barra de progreso del mini reproductor
        self.barra_progreso_mini = ctk.CTkProgressBar(
            panel_progreso_mini_reproductor,
            height=6,
            progress_color=self.color_barra_progreso,
        )
        self.barra_progreso_mini.pack(fill="x")
        self.barra_progreso_mini.set(0)
        self.componentes.append(self.barra_progreso_mini)
        # -------------------------------------------------------------------------------------------------
        # =================================================================================================

        # ======================================== Panel tiempo ===========================================
        # Crea el panel de tiempo del mini reproductor
        panel_tiempo_mini_reproductor = ctk.CTkFrame(panel_progreso_mini_reproductor, fg_color="transparent")
        panel_tiempo_mini_reproductor.pack(fill="x")
        self.componentes.append(panel_tiempo_mini_reproductor)

        # ---------------------------------- Etiqueta de tiempo inicial -----------------------------------
        # Crea las etiquetas de tiempo del mini reproductor
        self.etiqueta_tiempo_inicio_mini = ctk.CTkLabel(
            panel_tiempo_mini_reproductor,
            height=20,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color="transparent",
        )
        self.etiqueta_tiempo_inicio_mini.pack(side="left")
        self.componentes.append(self.etiqueta_tiempo_inicio_mini)
        # -------------------------------------------------------------------------------------------------

        # ----------------------------------- Etiqueta de tiempo final ------------------------------------
        self.etiqueta_tiempo_final_mini = ctk.CTkLabel(
            panel_tiempo_mini_reproductor,
            height=20,
            text_color=self.color_texto,
            text="00:00",
            font=(LETRA, TAMANIO_LETRA_TIEMPO - 1),
            fg_color="transparent",
        )
        self.etiqueta_tiempo_final_mini.pack(side="right")
        self.componentes.append(self.etiqueta_tiempo_final_mini)
        # -------------------------------------------------------------------------------------------------
        # =================================================================================================

        # ======================================== Panel botones ==========================================
        # Crea el panel de botones del mini reproductor
        panel_botones_mini_reproductor = ctk.CTkFrame(panel_derecha_mini_reproductor, fg_color="transparent")
        panel_botones_mini_reproductor.pack(fill="x", padx=5, pady=(0, 5))
        self.componentes.append(panel_botones_mini_reproductor)

        # ----------------------------------------- Panel botones -----------------------------------------
        # Crea el contenedor de botones del mini reproductor
        contenedor_botones_mini_reproductor = ctk.CTkFrame(
            panel_botones_mini_reproductor, fg_color="transparent"
        )
        contenedor_botones_mini_reproductor.pack(pady=(0, 3), expand=True)
        self.componentes.append(contenedor_botones_mini_reproductor)
        # -------------------------------------------------------------------------------------------------

        # ---------------------------------------- Boton me gusta -----------------------------------------
        # Crea los botones del mini reproductor
        self.boton_me_gusta_mini = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="",
            command=self.cambiar_me_gusta,
        )
        self.boton_me_gusta_mini.pack(side="left", padx=5)
        self.controlador_tema.registrar_botones("me_gusta_mini", self.boton_me_gusta_mini)
        # -------------------------------------------------------------------------------------------------

        # ----------------------------------------- Boton anterior ----------------------------------------
        self.boton_anterior_mini = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="",
            command=self.reproducir_anterior,
        )
        self.boton_anterior_mini.pack(side="left", padx=5)
        self.controlador_tema.registrar_botones("anterior_mini", self.boton_anterior_mini)
        # -------------------------------------------------------------------------------------------------

        # --------------------------------- Boton reproducir/pausar ---------------------------------------
        self.boton_reproducir_mini = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="",
            command=self.reproducir_pausar,
        )
        self.boton_reproducir_mini.pack(side="left", padx=5)
        self.controlador_tema.registrar_botones("reproducir_mini", self.boton_reproducir_mini)
        # -------------------------------------------------------------------------------------------------

        # -------------------------------- Boton siguiente ------------------------------------------------
        self.boton_siguiente_mini = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="",
            command=self.reproducir_siguiente,
        )
        self.boton_siguiente_mini.pack(side="left", padx=5)
        self.controlador_tema.registrar_botones("siguiente_mini", self.boton_siguiente_mini)
        # -------------------------------------------------------------------------------------------------

        # -------------------------------- Boton maximizar mini reproductor -------------------------------
        boton_maximizar_mini_reproductor = ctk.CTkButton(
            contenedor_botones_mini_reproductor,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="",
            command=self.ocultar,
        )
        boton_maximizar_mini_reproductor.pack(side="left", padx=5)
        self.controlador_tema.registrar_botones("maximizar_mini", boton_maximizar_mini_reproductor)
        # -------------------------------------------------------------------------------------------------
        # =================================================================================================

        # ======================================== Panel izquierda ========================================
        # Crea el panel izquierdo del mini reproductor
        panel_izquierda_mini_reproductor = ctk.CTkFrame(
            panel_principal_mini_reproductor, fg_color=self.color_fondo, width=125, height=125
        )
        panel_izquierda_mini_reproductor.pack(side="left", padx=5, pady=5)
        panel_izquierda_mini_reproductor.pack_propagate(False)
        self.componentes.append(panel_izquierda_mini_reproductor)

        # ------------------------------------- Imagen de la canción ---------------------------------------
        # Crea la imagen de la canción del mini reproductor
        self.imagen_cancion_mini = ctk.CTkLabel(
            panel_izquierda_mini_reproductor,
            text_color=self.color_texto,
            text="Sin carátula",
            fg_color="transparent",
        )
        self.imagen_cancion_mini.pack(expand=True)
        self.componentes.append(self.imagen_cancion_mini)
        # -------------------------------------------------------------------------------------------------
        # =================================================================================================

        # Protocolo para cerrar la ventana del mini reproductor
        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # Aplicar eventos de movimiento a todos los componentes
        self.aplicar_eventos_movimiento()

    # Métodos para controlar la reproducción desde el mini reproductor
    def reproducir_pausar(self):
        from vista.vista_principal import actualizar_estado_reproduccion_vista

        if self.controlador_reproductor:
            # Verificar el estado actual
            if self.controlador_reproductor.reproduciendo:
                # Sí está reproduciendo, pausar
                self.controlador_reproductor.pausar_reproduccion_controlador()
            else:
                # Si está pausado, reanudar
                self.controlador_reproductor.reanudar_reproduccion_controlador()
            # Usar la función centralizada para actualizar todos los estados
            actualizar_estado_reproduccion_vista()

    # Métodos para poner la canción anterior
    def reproducir_anterior(self):
        if self.controlador_reproductor:
            if self.controlador_reproductor.reproducir_anterior_controlador():
                # Importar las funciones centralizadas para actualizar estados
                from vista.vista_principal import (
                    actualizar_estado_reproduccion_vista,
                    actualizar_estado_me_gusta_vista,
                )

                # Actualizar estado de reproducción
                actualizar_estado_reproduccion_vista()
                # Actualizar estado de me gusta
                actualizar_estado_me_gusta_vista()
                # Actualizar información visual
                self.actualizar_informacion()

    # Métodos para poner la canción siguiente
    def reproducir_siguiente(self):
        if self.controlador_reproductor:
            if self.controlador_reproductor.reproducir_siguiente_controlador():
                # Importar las funciones centralizadas para actualizar estados
                from vista.vista_principal import (
                    actualizar_estado_reproduccion_vista,
                    actualizar_estado_me_gusta_vista,
                )

                # Actualizar estado de reproducción
                actualizar_estado_reproduccion_vista()
                # Actualizar estado de me gusta
                actualizar_estado_me_gusta_vista()
                # Actualizar información visual
                self.actualizar_informacion()

    # Método para cambiar el estado de "me gusta" de la canción actual
    def cambiar_me_gusta(self):
        from vista.vista_principal import actualizar_estado_me_gusta_vista, guardar_biblioteca
        from vista.vista_principal import controlador_biblioteca

        if self.controlador_reproductor and self.controlador_reproductor.cancion_actual:
            # Obtener la canción actual
            cancion = self.controlador_reproductor.cancion_actual
            try:
                # Marcar o desmarcar la canción como "me gusta"
                controlador_biblioteca.agregar_me_gusta_controlador(cancion)
                # Actualizar el estado visual usando la función centralizada
                actualizar_estado_me_gusta_vista(cancion)
                # Guardar los cambios en la biblioteca
                guardar_biblioteca()
            except Exception as e:
                print(f"Error al cambiar estado de Me gusta: {e}")

    # Método para actualizar el estado de los botones según el estado de reproducción
    def actualizar_estado_reproduccion(self):
        if self.controlador_reproductor:
            # Actualizar el icono del botón de reproducción/pausa
            if self.controlador_reproductor.reproduciendo:
                self.controlador_tema.registrar_botones("pausa_mini", self.boton_reproducir_mini)
            else:
                self.controlador_tema.registrar_botones("reproducir_mini", self.boton_reproducir_mini)
            # Actualizar el icono de me_gusta según el estado de la canción actual
            self.actualizar_estado_me_gusta()

    # Método para actualizar el estado del botón "me gusta" según la canción actual
    def actualizar_estado_me_gusta(self):
        if self.controlador_reproductor and self.controlador_reproductor.cancion_actual:
            # Obtener el estado de me_gusta de la canción actual
            cancion = self.controlador_reproductor.cancion_actual
            if cancion.me_gusta:
                # Si tiene me gusta, mostrar icono rojo
                self.controlador_tema.registrar_botones("me_gusta_rojo_mini", self.boton_me_gusta_mini)
            else:
                # Si no tiene me gusta, mostrar icono normal
                self.controlador_tema.registrar_botones("me_gusta_mini", self.boton_me_gusta_mini)

    # Método para actualizar la información de la canción en el mini reproductor
    def actualizar_informacion(self):
        if self.controlador_reproductor and self.controlador_reproductor.cancion_actual:
            cancion = self.controlador_reproductor.cancion_actual
            # Actualizar etiquetas de texto
            self.etiqueta_nombre_cancion_mini.configure(text=cancion.titulo_cancion)
            self.etiqueta_artista_mini.configure(text=cancion.artista)
            self.etiqueta_album_mini.configure(text=cancion.album)
            # Actualizar carátula
            if cancion.caratula_cancion:
                foto, _, _ = self.crear_imagen_desde_bytes(cancion.caratula_cancion, ancho=125, alto=125)
                if foto:
                    self.imagen_cancion_mini.configure(image=foto, text="")
                    # Guardar referencia para evitar el garbage collector
                    self.foto_caratula_mini = foto
                else:
                    self.imagen_cancion_mini.configure(image=None, text="Sin carátula")
            else:
                self.imagen_cancion_mini.configure(image=None, text="Sin carátula")
            # Actualizar duración total
            minutos_total = int(cancion.duracion // 60)
            segundos_total = int(cancion.duracion % 60)
            self.etiqueta_tiempo_final_mini.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")
            # Sincronizar la barra de progreso con la principal
            if (
                hasattr(self.controlador_reproductor, "barra_progreso")
                and self.controlador_reproductor.barra_progreso
            ):
                valor_progreso = self.controlador_reproductor.barra_progreso.get()
                self.barra_progreso_mini.set(valor_progreso)
        else:
            # No hay canción en reproducción
            self.etiqueta_nombre_cancion_mini.configure(text="Sin reproducción")
            self.etiqueta_artista_mini.configure(text="")
            self.etiqueta_album_mini.configure(text="")
            self.etiqueta_tiempo_inicio_mini.configure(text="00:00")
            self.etiqueta_tiempo_final_mini.configure(text="00:00")
            self.imagen_cancion_mini.configure(image=None, text="Sin carátula")
            self.barra_progreso_mini.set(0)
        self.aplicar_eventos_movimiento()

    # Método para mostrar la ventana del mini reproductor
    def mostrar_ventana_mini_reproductor(self):
        # Verificar si la ventana del mini reproductor es None o fue destruida
        ventana_destruida = False
        if self.ventana_principal_mini_reproductor is not None:
            try:
                existe = self.ventana_principal_mini_reproductor.winfo_exists()
                if not existe:
                    ventana_destruida = True
            except Exception as e:
                print(f"Error al verificar si la ventana del mini reproductor existe: {e}")
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
                establecer_icono_tema(
                    self.ventana_principal_mini_reproductor, self.controlador_tema.tema_interfaz
                )
                self.actualizar_colores()
            except Exception as e:
                print(f"Error al mostrar la ventana del mini reproductor: {e}")
                # Si hay un error al actualizar, recrear la ventana
                self.ventana_principal_mini_reproductor = None
                self.crear_ventana_mini_reproductor()
        # Actualizar información de la canción actual
        self.actualizar_informacion()
        self.actualizar_estado_reproduccion()
        self.actualizar_estado_me_gusta()
        # Posicionar la ventana del mini reproductor en una ubicación visible
        try:
            # Obtener dimensiones de la pantalla
            ancho_pantalla = self.ventana_principal.winfo_screenwidth()
            alto_pantalla = self.ventana_principal.winfo_screenheight()
            # Calcular posición según la configuración
            if self.posicion_mini_reproductor == "superior_izquierda":
                x = 0  # Margen izquierdo
                y = 0  # Margen superior
            elif self.posicion_mini_reproductor == "superior_derecha":
                x = ancho_pantalla - ANCHO_MINI_REPRODUCTOR
                y = 0
            elif self.posicion_mini_reproductor == "inferior_izquierda":
                x = 0
                y = alto_pantalla - ALTO_MINI_REPRODUCTOR - 40
            elif self.posicion_mini_reproductor == "inferior_derecha":
                x = ancho_pantalla - ANCHO_MINI_REPRODUCTOR
                y = alto_pantalla - ALTO_MINI_REPRODUCTOR - 40
            elif self.posicion_mini_reproductor == "centro":
                x = (ancho_pantalla - ANCHO_MINI_REPRODUCTOR) // 2
                y = (alto_pantalla - ALTO_MINI_REPRODUCTOR) // 2
            else:
                # Posición por defecto (superior izquierda)
                x = 0
                y = 0
            # Aplicar posición
            self.ventana_principal_mini_reproductor.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"Error al posicionar el mini reproductor: {e}")
        # Mostrar la ventana del mini reproductor de forma segura
        try:
            if (
                self.ventana_principal_mini_reproductor
                and self.ventana_principal_mini_reproductor.winfo_exists()
            ):
                # Mostrar el mini reproductor
                self.ventana_principal_mini_reproductor.deiconify()
                self.ventana_principal_mini_reproductor.lift()
                self.ventana_principal_mini_reproductor.focus_set()
                # Ocultar la ventana principal
                self.ventana_principal.withdraw()
        except Exception as e:
            print(f"Error al mostrar el mini reproductor: {e}")

    # Método para ocultar la ventana del mini reproductor
    def ocultar(self):
        if self.ventana_principal_mini_reproductor:
            try:
                if self.ventana_principal_mini_reproductor.winfo_exists():
                    self.ventana_principal_mini_reproductor.withdraw()
            except Exception as e:
                print(f"Error al ocultar el mini reproductor: {e}")
                pass
            self.ventana_principal.deiconify()

    # Iniciar el movimiento de la ventana del mini reproductor
    def iniciar_movimiento(self, event):
        self.x = event.x
        self.y = event.y

    # Mover la ventana del mini reproductor según el movimiento del ratón
    def mover_ventana(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.ventana_principal_mini_reproductor.winfo_x() + deltax
        y = self.ventana_principal_mini_reproductor.winfo_y() + deltay
        self.ventana_principal_mini_reproductor.geometry(f"+{x}+{y}")

    # Detener el movimiento de la ventana del mini reproductor
    def detener_movimiento(self, _event):
        self.x = None
        self.y = None

    # Aplicar eventos de movimiento a la ventana del mini reproductor y sus componentes
    def aplicar_eventos_movimiento(self):
        # Primero al panel principal
        if self.ventana_principal_mini_reproductor and hasattr(self, "componentes"):
            # Aplicar eventos a la ventana principal primero
            self.ventana_principal_mini_reproductor.bind("<ButtonPress-1>", self.iniciar_movimiento)
            self.ventana_principal_mini_reproductor.bind("<ButtonRelease-1>", self.detener_movimiento)
            self.ventana_principal_mini_reproductor.bind("<B1-Motion>", self.mover_ventana)
            # Luego aplicar a todos los componentes
            for componente in self.componentes:
                try:
                    # Verificar si el componente existe y es válido
                    if componente and componente.winfo_exists():
                        componente.bind("<ButtonPress-1>", self.iniciar_movimiento)
                        componente.bind("<ButtonRelease-1>", self.detener_movimiento)
                        componente.bind("<B1-Motion>", self.mover_ventana)
                except Exception as e:
                    print(f"Error al aplicar eventos de movimiento: {e}")

    # Método para cambiar la posición del mini reproductor
    def cambiar_posicion(self, nueva_posicion):
        # Inicializar coordenadas
        x = 0
        y = 0
        # Definir posiciones válidas
        posiciones_validas = [
            "superior_izquierda",
            "superior_derecha",
            "inferior_izquierda",
            "inferior_derecha",
            "centro",
        ]
        if nueva_posicion in posiciones_validas:
            self.posicion_mini_reproductor = nueva_posicion
            # Si la ventana está visible, actualizar su posición inmediatamente
            if (
                self.ventana_principal_mini_reproductor
                and hasattr(self.ventana_principal_mini_reproductor, "winfo_exists")
                and self.ventana_principal_mini_reproductor.winfo_exists()
            ):
                # Obtener dimensiones de la pantalla
                ancho_pantalla = self.ventana_principal.winfo_screenwidth()
                alto_pantalla = self.ventana_principal.winfo_screenheight()
                # Calcular la nueva posición
                if nueva_posicion == "superior_izquierda":
                    x = 0
                    y = 0
                elif nueva_posicion == "superior_derecha":
                    x = ancho_pantalla - ANCHO_MINI_REPRODUCTOR
                    y = 0
                elif nueva_posicion == "inferior_izquierda":
                    x = 0
                    y = alto_pantalla - ALTO_MINI_REPRODUCTOR - 40
                elif nueva_posicion == "inferior_derecha":
                    x = ancho_pantalla - ANCHO_MINI_REPRODUCTOR
                    y = alto_pantalla - ALTO_MINI_REPRODUCTOR - 40
                elif nueva_posicion == "centro":
                    x = (ancho_pantalla - ANCHO_MINI_REPRODUCTOR) // 2
                    y = (alto_pantalla - ALTO_MINI_REPRODUCTOR) // 2
                # Aplicar la nueva posición
                self.ventana_principal_mini_reproductor.geometry(f"+{x}+{y}")
        else:
            print(f"Posición no válida: {nueva_posicion}. Las posiciones válidas son: {posiciones_validas}")

    # Método para actualizar los colores de los componentes del mini reproductor
    def actualizar_colores(self):
        self.colores()
        # Actualizar colores de los componentes
        for componente in self.componentes:
            try:
                if isinstance(componente, ctk.CTkFrame):
                    if componente.winfo_parent() == str(self.ventana_principal_mini_reproductor):
                        componente.configure(fg_color=self.color_fondo_principal)
                    else:
                        componente.configure(fg_color=self.color_fondo)
                elif isinstance(componente, ctk.CTkLabel):
                    componente.configure(fg_color=self.color_fondo, text_color=self.color_texto)
                elif isinstance(componente, ctk.CTkButton):
                    componente.configure(
                        fg_color=self.color_boton,
                        hover_color=self.color_hover,
                        text_color=self.color_texto,
                    )
                elif isinstance(componente, ctk.CTkProgressBar):
                    componente.configure(progress_color=self.color_barra_progreso)
            except Exception as e:
                print(f"Error al actualizar los colores del mini reproductor: {e}")
