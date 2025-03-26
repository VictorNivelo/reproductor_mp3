from vista.componentes.utiles.utiles_componentes import configurar_ventana_modal, cerrar_ventana_modal
from vista.utiles.utiles_scroll import GestorScroll
import customtkinter as ctk
from utiles import Utiles
from constantes import *
import tkinter as tk


class ColaReproduccion:
    def __init__(self, ventana_principal, controlador_tema, controlador_reproductor):
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.controlador_reproductor = controlador_reproductor
        self.ventana_cola = None
        self.componentes = []
        self.gestor_scroll = None
        self.utiles = Utiles(controlador_tema)
        # Configurar un temporizador para comprobar cambios en la canción actual
        self.ultima_cancion = None
        self.iniciar_monitor_cambios()

    # Método para iniciar el temporizador de verificación de cambios
    def iniciar_monitor_cambios(self):
        self.verificar_cambio_cancion()

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
        self.utiles.colores()
        # Crear ventana modal
        self.ventana_cola = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana modal
        configurar_ventana_modal(
            self.ventana_principal,
            self.ventana_cola,
            ANCHO_COLA_REPRODUCCION,
            ALTO_COLA_REPRODUCCION,
            "Cola de reproducción",
            self.utiles.color_fondo_principal,
            lambda: cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema),
            self.controlador_tema,
        )
        # ===================================== Contenedor principal =====================================
        # Contenedor principal con margen reducido
        contenedor_principal = ctk.CTkFrame(
            self.ventana_cola, fg_color=self.utiles.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        contenedor_principal.pack(fill="both", expand=True, padx=3, pady=3)
        self.componentes.append(contenedor_principal)

        # ---------------------------------------- Etiqueta título ----------------------------------------
        # Etiqueta título con menos altura
        etiqueta_titulo = ctk.CTkLabel(
            contenedor_principal,
            height=15,
            fg_color="transparent",
            text="Cola de reproducción",
            font=(LETRA, 16, "bold"),
            text_color=self.utiles.color_texto,
        )
        etiqueta_titulo.pack(padx=10)
        self.componentes.append(etiqueta_titulo)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Etiqueta duración --------------------------------------
        # Duración total de la cola
        duracion_total = self.calcular_duracion_cola()
        etiqueta_duracion = ctk.CTkLabel(
            contenedor_principal,
            height=14,
            fg_color="transparent",
            text=f"Duración total: {duracion_total}",
            font=(LETRA, 11),
            text_color=self.utiles.color_texto,
        )
        etiqueta_duracion.pack(padx=10, pady=1)
        self.componentes.append(etiqueta_duracion)
        self.controlador_tema.registrar_etiqueta(etiqueta_duracion)
        # ------------------------------------------------------------------------------------------------

        # *********************************** Panel de canción actual ***********************************
        # ---------------------------------------- Panel cancion -----------------------------------------
        # Panel para la canción actual con mejor estilo
        panel_cancion_actual = ctk.CTkFrame(
            contenedor_principal,
            fg_color=self.utiles.color_segundario,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_cancion_actual.pack(fill="both", padx=5, pady=(0, 5))
        self.componentes.append(panel_cancion_actual)
        # ------------------------------------------------------------------------------------------------

        # -------------------------------- Etiqueta reproduciendo actual ---------------------------------
        # Etiqueta de reproducción actual
        etiqueta_reproduciendo = ctk.CTkLabel(
            panel_cancion_actual,
            height=15,
            text="Reproduciendo ahora:",
            font=(LETRA, 13, "bold"),
            text_color=self.utiles.color_texto,
        )
        etiqueta_reproduciendo.pack(anchor="w", padx=5, pady=(3, 0))
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
            contenedor_principal,
            fg_color=self.utiles.color_segundario,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_cola_reproduccion.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.componentes.append(panel_cola_reproduccion)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Panel componentes -------------------------------------
        # Cabecera con título y botón para limpiar cola
        panel_componentes = ctk.CTkFrame(
            panel_cola_reproduccion,
            fg_color="transparent",
        )
        panel_componentes.pack(fill="both", padx=5, pady=(3, 0))
        self.componentes.append(panel_componentes)
        # ------------------------------------------------------------------------------------------------

        # -------------------------------------- Etiqueta próximas canciones -----------------------------
        # Etiqueta de próximas canciones
        etiqueta_proximas = ctk.CTkLabel(
            panel_componentes,
            height=15,
            text="Próximas canciones:",
            font=(LETRA, 13, "bold"),
            text_color=self.utiles.color_texto,
        )
        etiqueta_proximas.pack(side="left")
        self.componentes.append(etiqueta_proximas)
        self.controlador_tema.registrar_etiqueta(etiqueta_proximas)
        # ------------------------------------------------------------------------------------------------

        # ---------------------------------------- Botón limpiar cola ------------------------------------
        # Botón para limpiar toda la cola
        if self.controlador_reproductor.lista_reproduccion:
            boton_limpiar_cola = ctk.CTkButton(
                panel_componentes,
                text="Limpiar cola",
                font=(LETRA, 10),
                fg_color=self.utiles.color_boton,
                hover_color=self.utiles.color_hover,
                text_color=self.utiles.color_texto,
                command=self.limpiar_cola,
                width=ANCHO_BOTON,
                height=ALTO_BOTON,
            )
            boton_limpiar_cola.pack(side="right")
            self.componentes.append(boton_limpiar_cola)
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
        boton_cerrar = ctk.CTkButton(
            contenedor_principal,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            text="Cerrar",
            fg_color=self.utiles.color_boton,
            hover_color=self.utiles.color_hover,
            text_color=self.utiles.color_texto,
            command=lambda: cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema),
        )
        boton_cerrar.pack(pady=3)
        self.componentes.append(boton_cerrar)
        # ------------------------------------------------------------------------------------------------
        # ************************************************************************************************

        # ================================================================================================

    # Método para mostrar la carátula de una canción en un panel
    def mostrar_caratula(self, panel_contenedor, imagen_bytes, ancho=60, padding_y=(0, 3)):
        foto, _, _ = self.utiles.crear_imagen_desde_bytes(imagen_bytes, ancho)
        if foto:
            # --------------------------------------- Etiqueta imagen ------------------------------------
            etiqueta_imagen = ctk.CTkLabel(panel_contenedor, image=foto, text="")
            etiqueta_imagen.image = foto
            etiqueta_imagen.pack(
                side="left" if panel_contenedor.pack_info().get("side") != "left" else "top",
                padx=(0, 3),
                pady=padding_y,
            )
            self.componentes.append(etiqueta_imagen)
            # --------------------------------------------------------------------------------------------
            return etiqueta_imagen
        return None

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

            if cancion_actual.caratula_cancion:
                self.mostrar_caratula(panel_imagen, cancion_actual.caratula_cancion, ancho=60)

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
                text=cancion_actual.titulo_cancion,
                font=(LETRA, 14, "bold"),
                text_color=self.utiles.color_texto,
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
                text=cancion_actual.artista,
                font=(LETRA, 12),
                text_color=self.utiles.color_texto,
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
                text=(
                    cancion_actual.album
                    if hasattr(cancion_actual, "album") and cancion_actual.album
                    else "Álbum desconocido"
                ),
                font=(LETRA, 12, "italic"),
                text_color=self.utiles.color_texto,
            )
            etiqueta_album.pack(anchor="w")
            self.componentes.append(etiqueta_album)
            self.controlador_tema.registrar_etiqueta(etiqueta_album)
            # -------------------------------------------------------------------------------------------------
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
                text="No hay ninguna canción en reproducción",
                font=(LETRA, 12),
                text_color=self.utiles.color_texto,
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
                text="La cola de reproducción está vacía",
                font=(LETRA, 12),
                text_color=self.utiles.color_texto,
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
                    text="La canción actual se repetirá",
                    font=(LETRA, 12, "italic"),
                    text_color=self.utiles.color_texto,
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
                text="Modo aleatorio activado - las canciones se elegirán al azar",
                font=(LETRA, 12, "italic"),
                text_color=self.utiles.color_texto,
            )
            etiqueta_info.pack(fill="both", pady=3)
            self.componentes.append(etiqueta_info)
            self.controlador_tema.registrar_etiqueta(etiqueta_info)
            # -------------------------------------------------------------------------------------------------
            # En modo aleatorio, mostrar todas las canciones disponibles
            disponibles = [cancion for i, cancion in enumerate(lista_reproduccion) if i != indice_actual]
            proximas_canciones = disponibles[:10]  # Limitar a 10 canciones
            if not proximas_canciones and modo_repeticion == 2:
                # ---------------------------------------- Etiqueta reinicio ----------------------------------
                etiqueta_reinicio = ctk.CTkLabel(
                    panel,
                    height=15,
                    text="Se reiniciará la reproducción aleatoria de todas las canciones",
                    font=(LETRA, 12, "italic"),
                    text_color=self.utiles.color_texto,
                )
                etiqueta_reinicio.pack(fill="both", pady=3)
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
                # ---------------------------------------------------------------------------------------------
        else:  # Reproducción secuencial
            # Mostrar las próximas canciones en orden
            if indice_actual < len(lista_reproduccion) - 1:
                proximas_canciones = lista_reproduccion[indice_actual + 1 : indice_actual + 11]
            elif modo_repeticion == 2:  # Repetir todo
                # ---------------------------------------- Etiqueta reinicio ----------------------------------
                etiqueta_reinicio = ctk.CTkLabel(
                    panel,
                    height=15,
                    text="Se reiniciará la reproducción desde el principio",
                    font=(LETRA, 12, "italic"),
                    text_color=self.utiles.color_texto,
                )
                etiqueta_reinicio.pack(fill="both", pady=3)
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
                # ---------------------------------------------------------------------------------------------
                proximas_canciones = lista_reproduccion[:15]
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
            panel_cancion.pack(fill="both", pady=(3, 0))
            self.componentes.append(panel_cancion)
            # ------------------------------------- Etiqueta número -------------------------------------------
            # Número de orden
            etiqueta_numero = ctk.CTkLabel(
                panel_cancion,
                height=15,
                text=f"{i+1}.",
                width=20,
                font=(LETRA, 12),
                text_color=self.utiles.color_texto,
            )
            etiqueta_numero.pack(side="left")
            self.componentes.append(etiqueta_numero)
            self.controlador_tema.registrar_etiqueta(etiqueta_numero)
            # -------------------------------------------------------------------------------------------------
            # Intentar mostrar la carátula
            if cancion.caratula_cancion:
                self.mostrar_caratula(panel_cancion, cancion.caratula_cancion, ancho=45)
            # Información de la canción
            # --------------------------------- Panel información canción -------------------------------------
            informacion_cancion_cola = ctk.CTkFrame(
                panel_cancion,
                fg_color="transparent",
            )
            informacion_cancion_cola.pack(side="left", fill="both", expand=True, padx=(0, 3), pady=3)
            self.componentes.append(informacion_cancion_cola)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Etiqueta título ----------------------------------------
            # Nombre de la canción
            etiqueta_titulo = ctk.CTkLabel(
                informacion_cancion_cola,
                height=15,
                text=cancion.titulo_cancion,
                font=(LETRA, 12, "bold"),
                text_color=self.utiles.color_texto,
            )
            etiqueta_titulo.pack(anchor="w")
            self.componentes.append(etiqueta_titulo)
            self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Etiqueta artista ---------------------------------------
            # Artista
            etiqueta_artista = ctk.CTkLabel(
                informacion_cancion_cola,
                height=15,
                text=cancion.artista,
                font=(LETRA, 10),
                text_color=self.utiles.color_texto,
            )
            etiqueta_artista.pack(anchor="w")
            self.componentes.append(etiqueta_artista)
            self.controlador_tema.registrar_etiqueta(etiqueta_artista)
            # -------------------------------------------------------------------------------------------------

            # ------------------------------------- Etiqueta album --------------------------------------------
            # Álbum
            etiqueta_album = ctk.CTkLabel(
                informacion_cancion_cola,
                height=15,
                text=cancion.album,
                font=(LETRA, 10, "italic"),
                text_color=self.utiles.color_texto,
            )
            etiqueta_album.pack(side="left")
            self.componentes.append(etiqueta_album)
            self.controlador_tema.registrar_etiqueta(etiqueta_album)
            # -------------------------------------------------------------------------------------------------

            # ---------------------------------------- Botón quitar -------------------------------------------
            # Botón para quitar de la cola
            boton_quitar = ctk.CTkButton(
                panel_cancion,
                text="×",
                width=ANCHO_BOTON,
                height=ALTO_BOTON,
                corner_radius=12,
                font=(LETRA, 14, "bold"),
                fg_color=self.utiles.color_boton,
                hover_color=self.utiles.color_hover,
                text_color=self.utiles.color_texto,
                command=lambda idx=indice_real: self.quitar_de_cola(idx),
            )
            boton_quitar.pack(side="right", padx=(0, 5))
            self.componentes.append(boton_quitar)
            # -------------------------------------------------------------------------------------------------

            # Añadir efecto hover al panel de canción
            def configurar_hover(panel_objetivo, enter=True):
                color = self.utiles.color_hover if enter else "transparent"
                panel_objetivo.configure(fg_color=color)

            # Configurar eventos de hover
            panel_cancion.bind("<Enter>", lambda e, f=panel_cancion: configurar_hover(f, True))
            panel_cancion.bind("<Leave>", lambda e, f=panel_cancion: configurar_hover(f, False))

            # Añadir evento de clic para reproducir la canción
            panel_cancion.bind("<Button-1>", lambda e, c=cancion: self.reproducir_cancion_seleccionada(c))
            etiqueta_titulo.bind("<Button-1>", lambda e, c=cancion: self.reproducir_cancion_seleccionada(c))
            etiqueta_artista.bind("<Button-1>", lambda e, c=cancion: self.reproducir_cancion_seleccionada(c))
            etiqueta_album.bind("<Button-1>", lambda e, c=cancion: self.reproducir_cancion_seleccionada(c))
            etiqueta_numero.bind("<Button-1>", lambda e, c=cancion: self.reproducir_cancion_seleccionada(c))
        if not proximas_canciones and modo_repeticion != 2:
            # ----------------------------------------- Etiqueta final ----------------------------------------
            etiqueta_final = ctk.CTkLabel(
                panel,
                height=15,
                text="No hay más canciones en la cola",
                font=(LETRA, 12),
                text_color=self.utiles.color_texto,
            )
            etiqueta_final.pack(pady=3)
            self.componentes.append(etiqueta_final)
            self.controlador_tema.registrar_etiqueta(etiqueta_final)
            # -------------------------------------------------------------------------------------------------

    # Método para reproducir una canción seleccionada de la cola
    def reproducir_cancion_seleccionada(self, cancion):
        if cancion:
            self.controlador_reproductor.reproducir_cancion(cancion)
            # Actualizar solo la sección de la canción actual si la ventana está abierta
            if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
                self.actualizar_cancion_actual_en_cola()

    # Método para quitar una canción de la cola de reproducción
    def quitar_de_cola(self, indice):
        if 0 <= indice < len(self.controlador_reproductor.lista_reproduccion):
            # Verificar si es la canción actual
            es_actual = indice == self.controlador_reproductor.indice_actual
            # Eliminar la canción de la lista
            self.controlador_reproductor.lista_reproduccion.pop(indice)
            # Ajustar el índice actual si es necesario
            if indice <= self.controlador_reproductor.indice_actual:
                self.controlador_reproductor.indice_actual -= 1
            # Si era la canción actual, reproducir la siguiente
            if es_actual and self.controlador_reproductor.reproduciendo:
                self.controlador_reproductor.reproducir_siguiente()
            # Actualizar la ventana de cola
            self.actualizar_ventana_cola()

    # Método para limpiar toda la cola de reproducción
    def limpiar_cola(self):
        # Guardar la canción actual si está reproduciéndose
        cancion_actual = None
        if self.controlador_reproductor.reproduciendo and self.controlador_reproductor.cancion_actual:
            cancion_actual = self.controlador_reproductor.cancion_actual
        # Limpiar la lista
        self.controlador_reproductor.lista_reproduccion = []
        # Si hay una canción reproduciéndose, mantenerla
        if cancion_actual:
            self.controlador_reproductor.lista_reproduccion.append(cancion_actual)
            self.controlador_reproductor.indice_actual = 0
        else:
            self.controlador_reproductor.indice_actual = -1
        # Actualizar la ventana de cola
        self.actualizar_ventana_cola()

    # Método para actualizar la ventana de la cola de reproducción
    def actualizar_ventana_cola(self):
        # Cerrar la ventana actual
        cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema)
        # Limpiar referencias
        self.ventana_cola = None
        self.componentes = []
        self.gestor_scroll = None
        # Abrir nueva ventana actualizada
        self.mostrar_ventana_cola()

    # Método para actualizar la información de la canción actual en la cola
    def actualizar_cancion_actual_en_cola(self):
        if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
            # Buscar el panel de la canción actual
            for componente in self.componentes:
                if isinstance(componente, ctk.CTkFrame) and componente.winfo_exists():
                    # Buscar el panel que tiene la etiqueta "Reproduciendo ahora:"
                    for child in componente.winfo_children():
                        if isinstance(child, ctk.CTkLabel) and hasattr(child, "cget"):
                            if child.cget("text") == "Reproduciendo ahora:":
                                # Encontramos el panel de la canción actual
                                panel_cancion_actual = componente
                                # Limpiar los componentes existentes excepto la etiqueta de título
                                for widget in list(panel_cancion_actual.winfo_children()):
                                    if widget != child:
                                        if widget in self.componentes:
                                            self.componentes.remove(widget)
                                        widget.destroy()
                                # Actualizar con la nueva información
                                self.mostrar_cancion_actual(panel_cancion_actual)
                                break
            # Buscar el panel y canvas de la cola de reproducción
            for componente in self.componentes:
                if isinstance(componente, tk.Canvas) and componente.winfo_exists():
                    # Este es probablemente nuestro canvas
                    canvas_cola = componente
                    # Buscar el panel dentro del canvas
                    for item_id in canvas_cola.find_all():
                        if canvas_cola.type(item_id) == "window":
                            # Encontramos la ventana del canvas
                            window_info = canvas_cola.itemconfigure(item_id)
                            window_id = window_info.get("window")[-1]
                            if window_id:
                                # Obtener el widget contenido
                                panel_canciones = canvas_cola.nametowidget(window_id)
                                # Limpiar el panel de canciones
                                for widget in panel_canciones.winfo_children():
                                    if widget in self.componentes:
                                        self.componentes.remove(widget)
                                    widget.destroy()
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
            duracion = cancion_actual.duracion
            minutos = int(duracion // 60)
            segundos = int(duracion % 60)
            return f"{minutos}min {segundos}s (repetición infinita)"
        # Calcular duración de la cola actual
        duracion_total = cancion_actual.duracion  # Duración de la canción actual
        # Añadir duración de las canciones en cola
        if indice_actual is not None and indice_actual >= 0:
            for i, cancion in enumerate(lista_reproduccion):
                if i > indice_actual:  # Solo las canciones que están después de la actual
                    duracion_total += cancion.duracion
        # Formatear la duración total
        horas = int(duracion_total // 3600)
        minutos = int((duracion_total % 3600) // 60)
        segundos = int(duracion_total % 60)
        # Caso 2: Repetir toda la lista (modo 2)
        if modo_repeticion == 2:
            # Si hay solo una canción en la lista
            if len(lista_reproduccion) == 1:
                return f"{minutos}min {segundos}s (repetición infinita)"
            # Si hay más de una canción
            duracion_completa = sum(cancion.duracion for cancion in lista_reproduccion)
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
