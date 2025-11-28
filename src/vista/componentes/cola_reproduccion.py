import customtkinter as ctk
import tkinter as tk

from controlador.controlador_archivos import ControladorArchivos
from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_scroll import GestorScroll
from vista.utiles.utiles_vista import *
from animacion import AnimacionGeneral
from utiles import UtilesGeneral
from constantes import *


class ColaReproduccion(UtilesGeneral):
    def __init__(
        self, ventana_principal, controlador_tema, controlador_reproductor, llamado_actualizacion=None
    ):
        super().__init__(controlador_externo=controlador_tema)
        self.controlador_reproductor = controlador_reproductor
        self.llamado_actualizacion = llamado_actualizacion
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.ultima_cancion = None
        self.gestor_scroll = None
        self.ventana_cola = None
        self.componentes = []
        # Instancia de utilidades
        self.animacion = AnimacionGeneral()
        self.animacion_cancion = AnimacionGeneral()
        # Configurar un temporizador para comprobar cambios en la canción actual
        self.iniciar_monitor_cambios()
        # Inicializar los textos actuales para la animación
        self.textos_actual = {}
        # Inicializar los textos de la cola
        self.textos_cola = {}

    # Método para iniciar el temporizador de verificación de cambios
    def iniciar_monitor_cambios(self):
        self.verificar_cambio_cancion()

    # Método para alternar entre reproducir y pausar la canción actual
    def alternar_reproduccion(self):
        if self.controlador_reproductor.reproduciendo:
            # Sí está reproduciendo, pausar
            self.controlador_reproductor.pausar_reproduccion_controlador()
        else:
            # Si está pausado, reproducir o reanudar
            self.controlador_reproductor.reproducir_o_reanudar_controlador()
        # Actualizar el estado de la interfaz principal
        if self.llamado_actualizacion:
            self.llamado_actualizacion()
        # Si la ventana de cola está abierta, actualizar solo el botón
        if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
            # Buscar el botón de reproducción/pausa en los componentes
            for componente in self.componentes:
                # Verificar si es un botón y existe
                if (
                    isinstance(componente, ctk.CTkButton)
                    and componente.winfo_exists()
                    and hasattr(componente, "cget")
                    and componente.cget("command") == self.alternar_reproduccion
                ):
                    # Determinar el icono según el estado de reproducción
                    icono_nombre = "pausa" if self.controlador_reproductor.reproduciendo else "reproducir"
                    icono_reproduccion = cargar_icono_con_tamanio(
                        icono_nombre, self.controlador_tema.tema_iconos, (18, 18)
                    )
                    # Actualizar el icono del botón
                    componente.configure(image=icono_reproduccion)
                    texto_tooltip = "Pausar" if self.controlador_reproductor.reproduciendo else "Reproducir"
                    actualizar_texto_tooltip(componente, texto_tooltip)
                    # Guardar referencia al icono para evitar que sea recolectado
                    componente.image = icono_reproduccion
                    break

    # Método para cerrar la ventana de la cola de reproducción
    def cerrar_ventana_cola(self):
        # Primero desactivar el gestor de scroll si existe
        if self.gestor_scroll:
            self.gestor_scroll.desactivar()
            self.gestor_scroll = None
        # Ahora cerrar la ventana normalmente
        cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema)
        self.ventana_cola = None
        self.componentes = []

    # Método para verificar si la canción actual cambió
    def verificar_cambio_cancion(self):
        cancion_actual = self.controlador_reproductor.cancion_actual
        # Si la canción cambió y la ventana está abierta
        if (
            cancion_actual != self.ultima_cancion
            and self.ventana_cola is not None
            and self.ventana_cola.winfo_exists()
        ):
            self.actualizar_cancion_actual_en_cola()
        # Actualizar referencia
        self.ultima_cancion = cancion_actual
        # Programar la próxima verificación
        self.ventana_principal.after(500, self.verificar_cambio_cancion)

    # Método para mostrar la ventana de la cola de reproducción
    def mostrar_ventana_cola(self):
        # Si ya existe una ventana abierta, mostrarla
        if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
            self.ventana_cola.lift()
            return
        # Actualizar colores
        self.colores()
        # Crear ventana modal
        self.ventana_cola = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana para que no se pueda maximizar ni minimizar
        self.ventana_cola.resizable(False, False)
        # # Eliminar la barra de título y los controles de ventana
        # self.ventana_cola.overrideredirect(True)
        # Configurar la ventana modal
        crear_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_cola,
            ancho=ANCHO_COLA_REPRODUCCION,
            alto=ALTO_COLA_REPRODUCCION,
            titulo="Cola de reproducción",
            color_fondo=self.color_fondo_principal,
            funcion_cierre=lambda: self.cerrar_ventana_cola(),
            controlador=self.controlador_tema,
        )
        # ===================================== Contenedor principal =====================================
        # Contenedor principal con margen reducido
        panel_principal_cola = ctk.CTkFrame(
            self.ventana_cola, fg_color=self.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        panel_principal_cola.pack(fill="both", expand=True, padx=3, pady=3)
        self.componentes.append(panel_principal_cola)

        # ---------------------------------------- Etiqueta título ----------------------------------------
        # Etiqueta título con menos altura
        etiqueta_titulo_general = ctk.CTkLabel(
            panel_principal_cola,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TITULO, "bold"),
            text_color=self.color_texto,
            text="Cola de reproducción",
        )
        etiqueta_titulo_general.pack()
        self.componentes.append(etiqueta_titulo_general)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_general)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Etiqueta duración --------------------------------------
        # Duración total de la cola
        duracion_total = self.calcular_duracion_cola()
        # Etiqueta con la duración total
        etiqueta_duracion = ctk.CTkLabel(
            panel_principal_cola,
            height=14,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TIEMPO),
            text_color=self.color_texto,
            text=f"Duración total: {duracion_total}",
        )
        etiqueta_duracion.pack(pady=1)
        self.componentes.append(etiqueta_duracion)
        self.controlador_tema.registrar_etiqueta(etiqueta_duracion)
        # ------------------------------------------------------------------------------------------------

        # *********************************** Panel de canción actual ***********************************
        # ---------------------------------------- Panel cancion -----------------------------------------
        # Panel para la canción actual con mejor estilo
        panel_cancion_actual = ctk.CTkFrame(
            panel_principal_cola,
            fg_color=self.color_segundario,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_cancion_actual.pack(fill="both", padx=3, pady=(0, 5))
        self.componentes.append(panel_cancion_actual)
        # ------------------------------------------------------------------------------------------------

        # -------------------------------- Etiqueta reproduciendo actual ---------------------------------
        # Etiqueta de reproducción actual
        etiqueta_reproduciendo = ctk.CTkLabel(
            panel_cancion_actual,
            height=15,
            font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
            text_color=self.color_texto,
            text="Reproduciendo ahora:",
        )
        etiqueta_reproduciendo.pack(anchor="w", padx=3, pady=(3, 0))
        self.componentes.append(etiqueta_reproduciendo)
        self.controlador_tema.registrar_etiqueta(etiqueta_reproduciendo)
        # ------------------------------------------------------------------------------------------------

        # Mostrar la canción actual
        self.mostrar_cancion_actual(panel_cancion_actual)
        # ************************************************************************************************

        # ********************************** Panel de próximas canciones *********************************
        # ---------------------------------------- Panel cola --------------------------------------------
        # Panel para las próximas canciones
        panel_cola_reproduccion = ctk.CTkFrame(
            panel_principal_cola,
            fg_color=self.color_segundario,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_cola_reproduccion.pack(fill="both", expand=True, pady=(0, 5))
        self.componentes.append(panel_cola_reproduccion)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Panel componentes -------------------------------------
        # Cabecera con título y botón para limpiar cola
        panel_componentes = ctk.CTkFrame(
            panel_cola_reproduccion,
            fg_color="transparent",
        )
        panel_componentes.pack(fill="both", padx=3, pady=(3, 0))
        self.componentes.append(panel_componentes)
        # ------------------------------------------------------------------------------------------------

        # -------------------------------------- Etiqueta próximas canciones -----------------------------
        # Etiqueta de próximas canciones
        etiqueta_proximas = ctk.CTkLabel(
            panel_componentes,
            height=15,
            font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
            text_color=self.color_texto,
            text="Próximas canciones:",
        )
        etiqueta_proximas.pack(side="left")
        self.componentes.append(etiqueta_proximas)
        self.controlador_tema.registrar_etiqueta(etiqueta_proximas)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Botón limpiar cola ------------------------------------
        # Botón para limpiar toda la cola
        icono_limpiar = cargar_icono_con_tamanio("limpiar", self.controlador_tema.tema_iconos, (15, 15))
        if self.controlador_reproductor.lista_reproduccion:
            boton_limpiar_cola = ctk.CTkButton(
                panel_componentes,
                width=ANCHO_BOTON - 10,
                height=ALTO_BOTON - 10,
                corner_radius=BORDES_REDONDEADOS_BOTON,
                fg_color=self.color_boton,
                hover_color=self.color_hover,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text_color=self.color_texto,
                text="Limpiar cola",
                image=icono_limpiar,
                command=self.limpiar_cola,
            )
            boton_limpiar_cola.pack(side="right")
            self.componentes.append(boton_limpiar_cola)
            crear_tooltip(boton_limpiar_cola, "Limpiar toda la cola de reproducción")
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Canvas cola -------------------------------------------
        # Canvas para las próximas canciones (sin scrollbar visible)
        canvas_cola = tk.Canvas(panel_cola_reproduccion, highlightthickness=0)
        canvas_cola.pack(fill="both", expand=True, padx=3)
        # Aplicar color de fondo según tema
        canvas_cola.configure(bg=panel_cola_reproduccion.cget("fg_color"))
        self.componentes.append(canvas_cola)
        self.controlador_tema.registrar_canvas(canvas_cola)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Panel canciones ---------------------------------------
        # panel para contener los elementos en el canvas
        panel_canciones = ctk.CTkFrame(
            canvas_cola,
            fg_color="transparent",
        )
        panel_canciones.pack(fill="both", padx=3, pady=3)
        self.componentes.append(panel_canciones)
        # ------------------------------------------------------------------------------------------------

        # Crear la ventana dentro del canvas
        canvas_window = canvas_cola.create_window((0, 0), window=panel_canciones, anchor="nw")
        # Configurar el gestor de scroll
        self.gestor_scroll = GestorScroll(canvas_cola, panel_canciones, canvas_window)
        # Mostrar las canciones en la cola
        self.mostrar_cola_canciones(panel_canciones)

        # ---------------------------------------- Botón cerrar ------------------------------------------
        # Botón para cerrar con mejor estilo
        boton_cerrar_cola = ctk.CTkButton(
            panel_principal_cola,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            command=lambda: self.cerrar_ventana_cola(),
        )
        boton_cerrar_cola.pack(side="bottom", pady=3)
        self.componentes.append(boton_cerrar_cola)
        crear_tooltip(boton_cerrar_cola, "Cerrar ventana de cola")
        # ------------------------------------------------------------------------------------------------
        # ************************************************************************************************

        # ================================================================================================

    # Método para mostrar la carátula de una canción en un panel
    def mostrar_caratula(self, panel_contenedor, cancion, ancho_caratula=60, alto_caratula=60):
        if cancion and cancion.caratula_cancion:
            foto = cancion.obtener_caratula_general_cancion(
                formato="ctk",
                ancho=ancho_caratula,
                alto=alto_caratula,
                bordes_redondeados=True,
                radio_borde=5,
                mostrar_calidad=False,
            )
            if foto:
                etiqueta_imagen = ctk.CTkLabel(panel_contenedor, image=foto, text="")
                etiqueta_imagen.image = foto
                etiqueta_imagen.pack(
                    side="left" if panel_contenedor.pack_info().get("side") != "left" else "top",
                    padx=(0, 3),
                )
                self.componentes.append(etiqueta_imagen)
                return etiqueta_imagen
        # Si no hay carátula, mostrar un placeholder
        etiqueta_sin_caratula = ctk.CTkLabel(
            panel_contenedor,
            width=ancho_caratula,
            height=alto_caratula,
            fg_color=self.color_segundario,
            corner_radius=5,
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text="Sin\ncarátula",
        )
        etiqueta_sin_caratula.pack(
            side="left" if panel_contenedor.pack_info().get("side") != "left" else "top",
            padx=(0, 3),
        )
        self.componentes.append(etiqueta_sin_caratula)
        self.controlador_tema.registrar_etiqueta(etiqueta_sin_caratula)
        return etiqueta_sin_caratula

    # Método para mostrar la información de la canción actual
    def mostrar_cancion_actual(self, panel):
        cancion_actual = self.controlador_reproductor.cancion_actual
        if cancion_actual:
            # =================================== Información de la canción ===================================

            # Crear un panel para mostrar la información de la canción
            # *********************************** Panel información canción ***********************************
            panel_informacion_cancion = ctk.CTkFrame(
                panel,
                fg_color="transparent",
            )
            panel_informacion_cancion.pack(fill="both", padx=3, pady=5)
            self.componentes.append(panel_informacion_cancion)

            # ----------------------------------------- Panel imagen  -----------------------------------------
            # Intentar mostrar la carátula
            panel_imagen = ctk.CTkFrame(
                panel_informacion_cancion,
                fg_color="transparent",
                width=60,
                height=60,
            )
            panel_imagen.pack(side="left", padx=3)
            self.componentes.append(panel_imagen)
            # -------------------------------------------------------------------------------------------------

            self.mostrar_caratula(panel_imagen, cancion_actual, ancho_caratula=60, alto_caratula=60)

            # *************************************************************************************************

            # ***************************** Panel información de la canción ***********************************
            # Información de la canción
            informacion_cancion = ctk.CTkFrame(panel_informacion_cancion, fg_color="transparent")
            informacion_cancion.pack(side="left", fill="both", expand=True, padx=(0, 3))
            self.componentes.append(informacion_cancion)

            # ---------------------------------------- Etiqueta título ----------------------------------------
            # Nombre de la canción
            etiqueta_titulo = ctk.CTkLabel(
                informacion_cancion,
                height=19,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION + 3, "bold"),
                text_color=self.color_texto,
                text=cancion_actual.titulo_cancion,
            )
            etiqueta_titulo.pack(anchor="w")
            self.componentes.append(etiqueta_titulo)
            self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Etiqueta artista ---------------------------------------
            # Artista
            etiqueta_artista = ctk.CTkLabel(
                informacion_cancion,
                height=19,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
                text_color=self.color_texto,
                text=cancion_actual.artista_cancion,
            )
            etiqueta_artista.pack(anchor="w")
            self.componentes.append(etiqueta_artista)
            self.controlador_tema.registrar_etiqueta(etiqueta_artista)
            # -------------------------------------------------------------------------------------------------

            # ------------------------------------- Etiqueta album --------------------------------------------
            # Álbum
            etiqueta_album = ctk.CTkLabel(
                informacion_cancion,
                height=19,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "italic"),
                text_color=self.color_texto,
                text=cancion_actual.album_cancion,
            )
            etiqueta_album.pack(anchor="w")
            self.componentes.append(etiqueta_album)
            self.controlador_tema.registrar_etiqueta(etiqueta_album)
            # -------------------------------------------------------------------------------------------------

            # ------------------------------------------ Panel boton ------------------------------------------
            # Panel para botón de reproducción/pausa
            panel_boton_reproduccion = ctk.CTkFrame(panel_informacion_cancion, fg_color="transparent")
            panel_boton_reproduccion.pack(side="right")
            self.componentes.append(panel_boton_reproduccion)
            # -------------------------------------------------------------------------------------------------

            # Determinar el icono según el estado de reproducción
            icono_nombre = "pausa" if self.controlador_reproductor.reproduciendo else "reproducir"
            icono_reproduccion = cargar_icono_con_tamanio(
                icono_nombre, self.controlador_tema.tema_iconos, (18, 18)
            )

            # -------------------------------- Botón reproducir/pausar ----------------------------------------
            # Botón de reproducción/pausa
            boton_reproducir_pausar = ctk.CTkButton(
                panel_boton_reproduccion,
                width=ANCHO_BOTON,
                height=ALTO_BOTON,
                corner_radius=BORDES_REDONDEADOS_BOTON,
                fg_color=self.color_boton,
                hover_color=self.color_hover,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text_color=self.color_texto,
                text="",
                image=icono_reproduccion,
                command=self.alternar_reproduccion,
            )
            boton_reproducir_pausar.pack()
            self.componentes.append(boton_reproducir_pausar)
            texto_tooltip_inicial = "Pausar" if self.controlador_reproductor.reproduciendo else "Reproducir"
            crear_tooltip(boton_reproducir_pausar, texto_tooltip_inicial)

            # -------------------------------------------------------------------------------------------------

            # Crear un diccionario con los textos que pueden necesitar desplazamiento
            self.textos_actual = {
                "titulo": (cancion_actual.titulo_cancion, etiqueta_titulo),
                "artista": (cancion_actual.artista_cancion, etiqueta_artista),
                "album": (cancion_actual.album_cancion, etiqueta_album),
            }
            # Iniciar el desplazamiento con longitud máxima adecuada
            self.animacion.configurar_desplazamiento_etiqueta(panel, self.textos_actual, 365)

            # *************************************************************************************************
            # =================================================================================================
        else:
            # =================================== Información de la canción ===================================
            panel_sin_cancion = ctk.CTkFrame(
                panel,
                fg_color="transparent",
            )
            panel_sin_cancion.pack(fill="both", expand=True, padx=3, pady=(0, 3))
            self.componentes.append(panel_sin_cancion)

            # ---------------------------------------- Etiqueta sin canción -----------------------------------
            etiqueta_no_cancion = ctk.CTkLabel(
                panel_sin_cancion,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                text_color=self.color_texto,
                text="No hay ninguna canción en reproducción",
            )
            etiqueta_no_cancion.pack(pady=3, fill="both", expand=True)
            self.componentes.append(etiqueta_no_cancion)
            self.controlador_tema.registrar_etiqueta(etiqueta_no_cancion)
            # -------------------------------------------------------------------------------------------------

            # =================================================================================================

    # Método para mostrar las canciones en la cola de reproducción
    def mostrar_cola_canciones(self, panel):
        # Obtener el estado actual del reproductor
        lista_reproduccion = self.controlador_reproductor.lista_reproduccion
        indice_actual = self.controlador_reproductor.indice_actual
        modo_repeticion = self.controlador_reproductor.modo_repeticion
        modo_aleatorio = self.controlador_reproductor.modo_aleatorio
        if not lista_reproduccion:
            # ----------------------------------------- Etiqueta vacía ----------------------------------------
            etiqueta_vacia = ctk.CTkLabel(
                panel,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                text_color=self.color_texto,
                text="La cola de reproducción está vacía",
            )
            etiqueta_vacia.pack(pady=3)
            self.componentes.append(etiqueta_vacia)
            self.controlador_tema.registrar_etiqueta(etiqueta_vacia)
            # -------------------------------------------------------------------------------------------------
            return
        # Determinar qué canciones se mostrarán a continuación
        proximas_canciones = []
        if modo_repeticion == 1:  # Repetir canción actual
            # Solo mostrar la canción actual que se repetirá
            if 0 <= indice_actual < len(lista_reproduccion):
                # --------------------------------------- Etiqueta repetición ---------------------------------
                etiqueta_info = ctk.CTkLabel(
                    panel,
                    height=15,
                    fg_color="transparent",
                    font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                    text_color=self.color_texto,
                    text="La canción actual se repetirá",
                )
                etiqueta_info.pack(fill="both", pady=3)
                self.componentes.append(etiqueta_info)
                self.controlador_tema.registrar_etiqueta(etiqueta_info)
                # ---------------------------------------------------------------------------------------------
                return
        elif modo_aleatorio:  # Reproducción aleatoria
            # ---------------------------------------- Etiqueta aleatorio -------------------------------------
            etiqueta_info = ctk.CTkLabel(
                panel,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                text_color=self.color_texto,
                text="Modo aleatorio activado - las canciones se elegirán al azar",
            )
            etiqueta_info.pack(fill="both", pady=3)
            self.componentes.append(etiqueta_info)
            self.controlador_tema.registrar_etiqueta(etiqueta_info)
            # -------------------------------------------------------------------------------------------------
            # En modo aleatorio, mostrar todas las canciones disponibles (eliminando la limitación)
            proximas_canciones = [
                cancion for i, cancion in enumerate(lista_reproduccion) if i != indice_actual
            ]
            if not proximas_canciones and modo_repeticion == 2:
                # ---------------------------------------- Etiqueta reinicio ----------------------------------
                etiqueta_reinicio = ctk.CTkLabel(
                    panel,
                    height=15,
                    fg_color="transparent",
                    font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                    text_color=self.color_texto,
                    text="Se reiniciará la reproducción aleatoria de todas las canciones",
                )
                etiqueta_reinicio.pack(fill="both", pady=3)
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
                # ---------------------------------------------------------------------------------------------
        else:  # Reproducción secuencial
            # Mostrar las próximas canciones en orden
            if indice_actual < len(lista_reproduccion) - 1:
                # Mostrar todas las canciones después del índice actual
                proximas_canciones = lista_reproduccion[indice_actual + 1 :]
            # Si está activado repetir todo y hay canciones antes de la actual, añadirlas después
            if modo_repeticion == 2 and indice_actual > 0:
                # ---------------------------------------- Etiqueta reinicio ----------------------------------
                etiqueta_reinicio = ctk.CTkLabel(
                    panel,
                    height=15,
                    fg_color="transparent",
                    font=(LETRA, TAMANIO_LETRA_MENSAJE, "italic"),
                    text_color=self.color_texto,
                    text="Se reiniciará la reproducción desde el principio",
                )
                etiqueta_reinicio.pack(fill="both", pady=3)
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
                # ---------------------------------------------------------------------------------------------
                proximas_canciones.extend(lista_reproduccion[:indice_actual])
        # Mostrar las próximas canciones con un diseño más compacto
        for i, cancion in enumerate(proximas_canciones):
            # Calcular el índice real en la lista de reproducción
            indice_real = indice_actual + i + 1
            if modo_aleatorio:
                # En modo aleatorio no podemos calcular el índice real fácilmente
                try:
                    indice_real = lista_reproduccion.index(cancion)
                except ValueError:
                    indice_real = -1
            elif modo_repeticion == 2 and indice_actual >= len(lista_reproduccion) - 1:
                indice_real = i  # Para el caso de repetir todo cuando estamos al final
            # ***************************************** Panel canción *****************************************
            # Crear un panel para cada canción con hover
            panel_cancion = ctk.CTkFrame(
                panel,
                fg_color="transparent",
            )
            panel_cancion.pack(fill="both")
            self.componentes.append(panel_cancion)
            # ------------------------------------- Etiqueta número -------------------------------------------
            # Número de orden
            etiqueta_numero = ctk.CTkLabel(
                panel_cancion,
                width=20,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_NUMERO),
                text_color=self.color_texto,
                text=f"{i+1}.",
            )
            etiqueta_numero.pack(side="left")
            self.componentes.append(etiqueta_numero)
            self.controlador_tema.registrar_etiqueta(etiqueta_numero)
            # -------------------------------------------------------------------------------------------------
            # Intentar mostrar la carátula
            self.mostrar_caratula(panel_cancion, cancion, ancho_caratula=45, alto_caratula=45)
            # Información de la canción
            # --------------------------------- Panel información canción -------------------------------------
            panel_cola_informacion = ctk.CTkFrame(
                panel_cancion,
                fg_color="transparent",
            )
            panel_cola_informacion.pack(side="left", fill="both", expand=True, padx=(0, 3), pady=3)
            self.componentes.append(panel_cola_informacion)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Etiqueta título ----------------------------------------
            # Nombre de la canción
            etiqueta_titulo_cola = ctk.CTkLabel(
                panel_cola_informacion,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION + 2, "bold"),
                text_color=self.color_texto,
                text=cancion.titulo_cancion,
            )
            etiqueta_titulo_cola.pack(anchor="w")
            self.componentes.append(etiqueta_titulo_cola)
            self.controlador_tema.registrar_etiqueta(etiqueta_titulo_cola)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Etiqueta artista ---------------------------------------
            # Artista
            etiqueta_artista_cola = ctk.CTkLabel(
                panel_cola_informacion,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
                text_color=self.color_texto,
                text=cancion.artista_cancion,
            )
            etiqueta_artista_cola.pack(anchor="w")
            self.componentes.append(etiqueta_artista_cola)
            self.controlador_tema.registrar_etiqueta(etiqueta_artista_cola)
            # -------------------------------------------------------------------------------------------------

            # ------------------------------------- Etiqueta album --------------------------------------------
            # Álbum
            etiqueta_album_cola = ctk.CTkLabel(
                panel_cola_informacion,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "italic"),
                text_color=self.color_texto,
                text=cancion.album_cancion,
            )
            etiqueta_album_cola.pack(anchor="w")
            self.componentes.append(etiqueta_album_cola)
            self.controlador_tema.registrar_etiqueta(etiqueta_album_cola)
            # -------------------------------------------------------------------------------------------------

            # Crear un diccionario para los textos animados de esta canción
            self.textos_cola = {
                "titulo": (cancion.titulo_cancion, etiqueta_titulo_cola),
                "artista": (cancion.artista_cancion, etiqueta_artista_cola),
                "album": (cancion.album_cancion, etiqueta_album_cola),
            }
            # Crear una instancia de animación para esta canción
            self.animacion_cancion = AnimacionGeneral()
            # Iniciar animación de desplazamiento para los textos largos de esta canción
            self.animacion_cancion.configurar_desplazamiento_etiqueta(
                panel_cola_informacion, self.textos_cola, 365
            )

            # ---------------------------------------- Botón quitar -------------------------------------------
            # Botón para quitar de la cola
            icono_quitar = cargar_icono_con_tamanio("quitar", self.controlador_tema.tema_iconos, (10, 10))
            boton_quitar = ctk.CTkButton(
                panel_cancion,
                width=ANCHO_BOTON - 10,
                height=ALTO_BOTON - 10,
                corner_radius=BORDES_REDONDEADOS_BOTON,
                fg_color=self.color_boton,
                hover_color=self.color_hover,
                font=(LETRA, TAMANIO_LETRA_BOTON, "bold"),
                text_color=self.color_texto,
                text="",
                image=icono_quitar,
                command=lambda idx=indice_real: self.quitar_de_cola(idx),
            )
            boton_quitar.pack(side="right", padx=(0, 3))
            self.componentes.append(boton_quitar)
            crear_tooltip(boton_quitar, "Quitar de la cola")
            # -------------------------------------------------------------------------------------------------

            # Añadir efecto hover al panel de canción
            def configurar_hover(panel_objetivo, enter=True):
                color = self.color_hover if enter else "transparent"
                panel_objetivo.configure(fg_color=color)

            # Configurar eventos de hover
            panel_cancion.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))
            panel_cola_informacion.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))
            etiqueta_titulo_cola.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))
            etiqueta_artista_cola.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))
            etiqueta_album_cola.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))
            etiqueta_numero.bind("<Enter>", lambda e=None, f=panel_cancion: configurar_hover(f, True))

            panel_cancion.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))
            panel_cola_informacion.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))
            etiqueta_titulo_cola.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))
            etiqueta_artista_cola.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))
            etiqueta_album_cola.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))
            etiqueta_numero.bind("<Leave>", lambda e=None, f=panel_cancion: configurar_hover(f, False))

            # Añadir evento de clic para reproducir la canción
            panel_cancion.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
            panel_cola_informacion.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
            etiqueta_titulo_cola.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
            etiqueta_artista_cola.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
            etiqueta_album_cola.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
            etiqueta_numero.bind(
                "<Button-1>", lambda e=None, c=cancion: self.reproducir_cancion_seleccionada(c)
            )
        if not proximas_canciones and modo_repeticion != 2:
            # ----------------------------------------- Etiqueta final ----------------------------------------
            etiqueta_final = ctk.CTkLabel(
                panel,
                height=15,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_MENSAJE),
                text_color=self.color_texto,
                text="No hay más canciones en la cola",
            )
            etiqueta_final.pack(pady=3)
            self.componentes.append(etiqueta_final)
            self.controlador_tema.registrar_etiqueta(etiqueta_final)
            # -------------------------------------------------------------------------------------------------

    # Método para reproducir una canción seleccionada de la cola
    def reproducir_cancion_seleccionada(self, cancion):
        if cancion:
            self.controlador_reproductor.reproducir_cancion_controlador(cancion)
            # Llamar al callback para actualizar el estado de la interfaz
            if self.llamado_actualizacion:
                self.llamado_actualizacion()
            # Actualizar solo la sección de la canción actual si la ventana está abierta
            if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
                self.actualizar_cancion_actual_en_cola()

    # Método para quitar una canción de la cola de reproducción
    def quitar_de_cola(self, indice):
        if 0 <= indice < len(self.controlador_reproductor.lista_reproduccion):
            # Delegar la acción al controlador
            self.controlador_reproductor.quitar_cancion_cola_controlador(indice)
            # Actualizar la ventana de cola
            self.actualizar_ventana_cola()
            # Guardar la cola actualizada
            controlador_archivos = ControladorArchivos()
            controlador_archivos.guardar_cola_reproduccion_json_controlador(self.controlador_reproductor)

    # Método para limpiar toda la cola de reproducción
    def limpiar_cola(self):
        # Delegar la acción al controlador
        self.controlador_reproductor.limpiar_cola_controlador(mantener_actual=True)
        # Actualizar la ventana de cola
        self.actualizar_ventana_cola()

    # Método para actualizar la ventana de la cola de reproducción
    def actualizar_ventana_cola(self):
        # Cerrar la ventana actual usando nuestro método seguro
        self.cerrar_ventana_cola()
        # Abrir nueva ventana actualizada
        self.mostrar_ventana_cola()

    # Método para actualizar la información de la canción actual en la cola
    def actualizar_cancion_actual_en_cola(self):
        if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
            # Buscar el panel de la canción actual
            for componente_principal in self.componentes:
                if isinstance(componente_principal, ctk.CTkFrame) and componente_principal.winfo_exists():
                    # Buscar el panel que tiene la etiqueta "Reproduciendo ahora:"
                    for child in componente_principal.winfo_children():
                        if isinstance(child, ctk.CTkLabel) and hasattr(child, "cget"):
                            if child.cget("text") == "Reproduciendo ahora:":
                                # Encontramos el panel de la canción actual
                                panel_cancion_actual = componente_principal
                                # Limpiar los componentes existentes excepto la etiqueta de título
                                for hijo in list(panel_cancion_actual.winfo_children()):
                                    if hijo != child:
                                        if hijo in self.componentes:
                                            self.componentes.remove(hijo)
                                        hijo.destroy()
                                # Actualizar con la nueva información
                                self.mostrar_cancion_actual(panel_cancion_actual)
                                break
            # Buscar el panel y canvas de la cola de reproducción
            for componente_canvas in self.componentes:
                if isinstance(componente_canvas, tk.Canvas) and componente_canvas.winfo_exists():
                    # Este es probablemente nuestro canvas
                    canvas_cola = componente_canvas
                    # Buscar el panel dentro del canvas
                    for item_id in canvas_cola.find_all():
                        if canvas_cola.type(item_id) == "window":
                            # Encontramos la ventana del canvas
                            window_info = canvas_cola.itemconfigure(item_id)
                            window_id = window_info.get("window")[-1]
                            if window_id:
                                # Obtener el componente contenido
                                panel_canciones = canvas_cola.nametowidget(window_id)
                                # Limpiar el panel de canciones
                                for elemento in panel_canciones.winfo_children():
                                    if elemento in self.componentes:
                                        self.componentes.remove(elemento)
                                    elemento.destroy()
                                # Mostrar las canciones actualizadas
                                self.mostrar_cola_canciones(panel_canciones)
                                break
            for comp in self.componentes:
                if isinstance(comp, ctk.CTkLabel) and comp.winfo_exists():
                    if comp.cget("text").startswith("Duración total:"):
                        duracion_total = self.calcular_duracion_cola()
                        comp.configure(text=f"Duración total: {duracion_total}")
                        break

    # Método para calcular la duración total de la cola de reproducción
    def calcular_duracion_cola(self):
        # Obtener información del reproductor
        cancion_actual = self.controlador_reproductor.cancion_actual
        lista_reproduccion = self.controlador_reproductor.lista_reproduccion
        indice_actual = self.controlador_reproductor.indice_actual
        modo_repeticion = self.controlador_reproductor.modo_repeticion
        # Verificar si hay reproducción
        if cancion_actual is None:
            return "0min 0s"
        # Caso 1: Repetir una canción (modo 1)
        if modo_repeticion == 1:
            # Calcular duración de la canción actual
            duracion = cancion_actual.duracion_cancion
            minutos = int(duracion // 60)
            segundos = int(duracion % 60)
            return f"{minutos}min {segundos}s (repetición infinita)"
        # Calcular duración de la cola actual
        duracion_total = cancion_actual.duracion_cancion  # Duración de la canción actual
        # Añadir duración de las canciones en cola
        if indice_actual is not None and indice_actual >= 0:
            for i, cancion in enumerate(lista_reproduccion):
                if i > indice_actual:  # Solo las canciones que están después de la actual
                    duracion_total += cancion.duracion_cancion
        # Formatear la duración total
        horas = int(duracion_total // 3600)
        minutos = int((duracion_total % 3600) // 60)
        segundos = int(duracion_total % 60)
        # Caso 2: Repetir toda la lista (modo 2)
        if modo_repeticion == 2:
            # Sí hay solo una canción en la lista
            if len(lista_reproduccion) == 1:
                return f"{minutos}min {segundos}s (repetición infinita)"
            # Sí hay más de una canción
            duracion_completa = sum(cancion.duracion_cancion for cancion in lista_reproduccion)
            min_completo = int((duracion_completa % 3600) // 60)
            seg_completo = int(duracion_completa % 60)
            if horas > 0:
                return (
                    f"{horas}h {minutos}min {segundos}s (ciclo completo: {min_completo}min {seg_completo}s)"
                )
            else:
                return f"{minutos}min {segundos}s (ciclo completo: {min_completo}min {seg_completo}s)"
        # Caso 3: Reproducción normal (sin repetición)
        if horas > 0:
            return f"{horas}h {minutos}min {segundos}s"
        else:
            return f"{minutos}min {segundos}s"
