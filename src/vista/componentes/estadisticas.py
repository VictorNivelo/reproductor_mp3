from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_vista import *
from animacion import AnimacionGeneral
from customtkinter import CTkImage
from utiles import UtilesGeneral
import customtkinter as ctk
from constantes import *


class Estadisticas(UtilesGeneral):
    def __init__(
        self, ventana_principal, controlador_tema, controlador_archivos, controlador_biblioteca=None
    ):
        super().__init__(controlador_externo=controlador_tema)
        self.ventana_estadisticas = None
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.controlador_archivos = controlador_archivos
        self.controlador_biblioteca = controlador_biblioteca
        self.componentes = []
        self.animacion = AnimacionGeneral()
        self.animacion_artista = AnimacionGeneral()
        self.animacion_album = AnimacionGeneral()
        self.animacion_ultima = AnimacionGeneral()

    # Función para crear la ventana de estadísticas
    def crear_ventana_estadisticas(self):
        # Configurar colores
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear el panel principal de la ventana de estadísticas
        self.ventana_estadisticas = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana para que no se pueda maximizar ni minimizar
        self.ventana_estadisticas.resizable(False, False)
        # Configurar la ventana de estadísticas
        crear_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_estadisticas,
            ancho=ANCHO_ESTADISTICAS,
            alto=ALTO_ESTADISTICAS,
            titulo="Estadísticas",
            color_fondo=self.color_fondo_principal,
            funcion_cierre=self.cerrar_ventana_estadisticas,
            controlador=self.controlador_tema,
        )
        # =================================================================================================

        # ======================================== Panel principal ========================================
        # ************************************* Panel de estadísticas *************************************
        # Panel de estadísticas general
        panel_estadisticas_general = ctk.CTkFrame(
            self.ventana_estadisticas, fg_color=self.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
        )
        panel_estadisticas_general.pack(fill="both", expand=True, padx=3, pady=3)

        # -------------------------------------- Etiqueta de título ---------------------------------------
        # Etiqueta de título general
        etiqueta_titulo_general = ctk.CTkLabel(
            panel_estadisticas_general,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TITULO, "bold"),
            text_color=self.color_texto,
            text="Análisis de tu música",
        )
        etiqueta_titulo_general.pack()
        self.componentes.append(etiqueta_titulo_general)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_general)
        # -------------------------------------------------------------------------------------------------

        # Obtener estadísticas de reproducción
        estadisticas = self.controlador_archivos.obtener_estadisticas_json_controlador()
        if not estadisticas or estadisticas.get("canciones_escuchadas", 0) == 0:
            # Mostrar mensaje si no hay estadísticas
            self.mostrar_sin_estadisticas(panel_estadisticas_general)
        else:
            # Mostrar estadísticas generales
            self.mostrar_resumen_general(panel_estadisticas_general, estadisticas)
            # Mostrar tarjetas de estadísticas
            self.mostrar_tarjeta_cancion(panel_estadisticas_general, estadisticas)
            self.mostrar_tarjeta_artista(panel_estadisticas_general, estadisticas)
            self.mostrar_tarjeta_album(panel_estadisticas_general, estadisticas)
            # Mostrar última reproducción
            self.mostrar_ultima_reproduccion(panel_estadisticas_general, estadisticas)

        # ---------------------------------- Botón cerrar ---------------------------------
        # Botón para cerrar la ventana de estadísticas
        boton_cerrar_estadisticas = ctk.CTkButton(
            panel_estadisticas_general,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            command=self.cerrar_ventana_estadisticas,
        )
        boton_cerrar_estadisticas.pack(side="bottom", pady=3)
        self.componentes.append(boton_cerrar_estadisticas)
        crear_tooltip(boton_cerrar_estadisticas, "Cerrar ventana de estadísticas")
        # ---------------------------------------------------------------------------------

    # Función para mostrar mensaje si no hay estadísticas
    def mostrar_sin_estadisticas(self, panel_padre):
        # ***************************** Panel de mensaje **********************************
        # Panel de mensaje
        panel_mensaje = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
        )
        panel_mensaje.pack(fill="both", expand=True)
        self.componentes.append(panel_mensaje)

        # ------------------------------ Etiqueta de mensaje ------------------------------
        # Etiqueta de mensaje si no hay estadísticas
        etiqueta_mensaje = ctk.CTkLabel(
            panel_mensaje,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_MENSAJE),
            text_color=self.color_texto,
            text="Aún no hay estadísticas disponibles.\nReproducir música para generar análisis.",
        )
        etiqueta_mensaje.pack()
        self.componentes.append(etiqueta_mensaje)
        self.controlador_tema.registrar_etiqueta(etiqueta_mensaje)
        # ---------------------------------------------------------------------------------
        # *********************************************************************************

    # Función para mostrar resumen general de estadísticas
    def mostrar_resumen_general(self, panel_padre, estadisticas):
        # ******************************* Panel de resumen ********************************
        # Panel para resumen
        panel_resumen = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_resumen.pack(fill="x", padx=3, pady=(3, 0))
        self.componentes.append(panel_resumen)

        # ---------------------------- Panel para información resumen ---------------------
        # Panel para información de canción
        panel_informacion_resumen = ctk.CTkFrame(panel_resumen, fg_color="transparent")
        panel_informacion_resumen.pack(fill="x")
        self.componentes.append(panel_informacion_resumen)
        # ------------------------

        # ---------------------------- Etiqueta de informacion ----------------------------
        # Etiqueta de información general de canciones
        etiqueta_informacion_canciones = ctk.CTkLabel(
            panel_informacion_resumen,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"Canciones escuchadas: {estadisticas['canciones_escuchadas']}",
        )
        etiqueta_informacion_canciones.pack()
        self.componentes.append(etiqueta_informacion_canciones)
        self.controlador_tema.registrar_etiqueta(etiqueta_informacion_canciones)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Etiqueta de tiempo total ---------------------------
        # Etiqueta de tiempo total
        etiqueta_informacion_tiempo = ctk.CTkLabel(
            panel_informacion_resumen,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"Tiempo total de reproducción: {estadisticas['tiempo_total_reproduccion']}",
        )
        etiqueta_informacion_tiempo.pack()
        self.componentes.append(etiqueta_informacion_tiempo)
        self.controlador_tema.registrar_etiqueta(etiqueta_informacion_tiempo)
        # ---------------------------------------------------------------------------------
        # *********************************************************************************

    # Función para mostrar tarjeta de canción más reproducida
    def mostrar_tarjeta_cancion(self, panel_padre, estadisticas):
        # Si no hay canción más reproducida, no mostrar tarjeta
        if not estadisticas["cancion_mas_reproducida"]:
            return
        cancion = estadisticas["cancion_mas_reproducida"]

        # ******************************** Panel de tarjeta *******************************
        # Panel de tarjeta de estadísticas
        panel_tarjeta_cancion = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_tarjeta_cancion.pack(fill="x", padx=3, pady=(3, 0))
        self.componentes.append(panel_tarjeta_cancion)

        # ------------------------------ Etiqueta de título -------------------------------
        # Etiqueta de título
        etiqueta_titulo_cancion = ctk.CTkLabel(
            panel_tarjeta_cancion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_SUBTITULO, "bold"),
            text_color=self.color_texto,
            text="Canción más reproducida",
        )
        etiqueta_titulo_cancion.pack(pady=(3, 0))
        self.componentes.append(etiqueta_titulo_cancion)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_cancion)
        # ---------------------------------------------------------------------------------

        # ------------------------ Panel para contenido de la tarjeta ---------------------
        # Panel para contenido con imagen y texto
        panel_contenido = ctk.CTkFrame(panel_tarjeta_cancion, fg_color="transparent")
        panel_contenido.pack(fill="x")
        self.componentes.append(panel_contenido)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Subpanel para la carátula --------------------------
        # Panel para la carátula (a la izquierda)
        panel_caratula = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_caratula.pack(side="left")
        self.componentes.append(panel_caratula)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Etiqueta para la carátula --------------------------
        # Etiqueta para la carátula
        etiqueta_caratula = ctk.CTkLabel(panel_caratula, text="", fg_color="transparent")
        etiqueta_caratula.pack()
        self.componentes.append(etiqueta_caratula)
        # ---------------------------------------------------------------------------------

        if self.controlador_biblioteca:
            # Primero obtener la carátula como imagen PIL
            caratula_pil = self.controlador_biblioteca.obtener_caratula_album_controlador(
                cancion["album"], formato="PIL", ancho=75, alto=75
            )
            if caratula_pil:
                # Convertir a CTkImage
                caratula_ctk = CTkImage(light_image=caratula_pil, dark_image=caratula_pil, size=(75, 75))
                etiqueta_caratula.configure(image=caratula_ctk, text="")
                # Guardar referencia
                etiqueta_caratula.image = caratula_ctk
            else:
                etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        else:
            etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Panel para información de canción ------------------
        # Panel para información de canción (a la derecha)
        panel_informacion_cancion = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_informacion_cancion.pack(side="left", fill="x", expand=True)
        self.componentes.append(panel_informacion_cancion)
        # ---------------------------------------------------------------------------------

        # ------------------------- Etiqueta con titulo de cancion -------------------------
        # Etiqueta con título de canción
        etiqueta_titulo_cancion = ctk.CTkLabel(
            panel_informacion_cancion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "bold"),
            text_color=self.color_texto,
            text=cancion["titulo"],
        )
        etiqueta_titulo_cancion.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_titulo_cancion)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_cancion)
        # ---------------------------------------------------------------------------------

        # ------------------------- Etiqueta con artista de cancion ------------------------
        # Etiqueta con artista de canción
        etiqueta_artista_cancion = ctk.CTkLabel(
            panel_informacion_cancion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"{cancion['artista']}",
        )
        etiqueta_artista_cancion.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_artista_cancion)
        self.controlador_tema.registrar_etiqueta(etiqueta_artista_cancion)
        # ---------------------------------------------------------------------------------

        # ------------------------- Etiqueta con album de cancion --------------------------
        # Etiqueta con álbum de canción
        etiqueta_album_cancion = ctk.CTkLabel(
            panel_informacion_cancion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"{cancion['album']}",
        )
        etiqueta_album_cancion.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_album_cancion)
        self.controlador_tema.registrar_etiqueta(etiqueta_album_cancion)
        # ---------------------------------------------------------------------------------

        # Crear un diccionario con los textos que pueden necesitar desplazamiento
        textos_animados = {
            "titulo": (cancion["titulo"], etiqueta_titulo_cancion),
            "artista": (cancion["artista"], etiqueta_artista_cancion),
            "album": (cancion["album"], etiqueta_album_cancion),
        }
        self.animacion = AnimacionGeneral()
        # Iniciar el desplazamiento con longitud máxima adecuada
        self.animacion.configurar_desplazamiento_etiqueta(panel_informacion_cancion, textos_animados, 440)

        # ------------------------- Etiqueta con reproducciones de cancion -----------------------
        # Etiqueta con reproducciones de canción
        etiqueta_reproducciones_cancion = ctk.CTkLabel(
            panel_informacion_cancion,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"Reproducciones: {cancion['reproducciones']}",
        )
        etiqueta_reproducciones_cancion.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_reproducciones_cancion)
        self.controlador_tema.registrar_etiqueta(etiqueta_reproducciones_cancion)
        # ---------------------------------------------------------------------------------
        # *********************************************************************************

    # Función para mostrar tarjeta de artista más escuchado
    def mostrar_tarjeta_artista(self, panel_padre, estadisticas):
        # Si no hay artista más escuchado, no mostrar tarjeta
        if not estadisticas["artista_mas_escuchado"]:
            return
        artista = estadisticas["artista_mas_escuchado"]

        # ******************************** Panel de tarjeta *******************************
        # Panel de tarjeta de estadísticas
        panel_tarjeta_artista = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_tarjeta_artista.pack(fill="x", padx=3, pady=(3, 0))
        self.componentes.append(panel_tarjeta_artista)

        # ------------------------------- Etiqueta de título ------------------------------
        # Etiqueta de título
        etiqueta_titulo_artista = ctk.CTkLabel(
            panel_tarjeta_artista,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_SUBTITULO, "bold"),
            text_color=self.color_texto,
            text="Artista más escuchado",
        )
        etiqueta_titulo_artista.pack(pady=(3, 0))
        self.componentes.append(etiqueta_titulo_artista)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_artista)
        # ---------------------------------------------------------------------------------

        # -------------------------- Panel para información del artista -------------------
        # Panel para información del artista
        panel_informacion_artista = ctk.CTkFrame(panel_tarjeta_artista, fg_color="transparent")
        panel_informacion_artista.pack(fill="x")
        self.componentes.append(panel_informacion_artista)
        # ---------------------------------------------------------------------------------

        # ------------------------- Etiqueta con nombre de artista -------------------------
        # Etiqueta con nombre de artista
        etiqueta_nombre_artista = ctk.CTkLabel(
            panel_informacion_artista,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "bold"),
            text_color=self.color_texto,
            text=artista["nombre"],
        )
        etiqueta_nombre_artista.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_nombre_artista)
        self.controlador_tema.registrar_etiqueta(etiqueta_nombre_artista)
        # ---------------------------------------------------------------------------------

        # Crear un diccionario con los textos que pueden necesitar desplazamiento
        textos_animados = {
            "nombre": (artista["nombre"], etiqueta_nombre_artista),
        }
        self.animacion_artista = AnimacionGeneral()
        # Iniciar el desplazamiento con longitud máxima adecuada
        self.animacion_artista.configurar_desplazamiento_etiqueta(
            panel_informacion_artista, textos_animados, 440
        )

        # ------------------------- Etiqueta con album de artista --------------------------
        # Etiqueta con las reproducciones del artista
        etiqueta_reproducciones_artista = ctk.CTkLabel(
            panel_informacion_artista,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"Reproducciones: {artista['reproducciones']}",
        )
        etiqueta_reproducciones_artista.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_reproducciones_artista)
        self.controlador_tema.registrar_etiqueta(etiqueta_reproducciones_artista)
        # ---------------------------------------------------------------------------------
        # *********************************************************************************

    def mostrar_tarjeta_album(self, panel_padre, estadisticas):
        # Si no hay álbum más escuchado, no mostrar tarjeta
        if not estadisticas["album_mas_escuchado"]:
            return
        album = estadisticas["album_mas_escuchado"]

        # ******************************** Panel de tarjeta *******************************
        # Panel de tarjeta de estadísticas
        panel_tarjeta_album = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_tarjeta_album.pack(fill="x", padx=3, pady=(3, 0))
        self.componentes.append(panel_tarjeta_album)

        # ------------------------------- Etiqueta de título ------------------------------
        # Etiqueta de título
        etiqueta_titulo_album = ctk.CTkLabel(
            panel_tarjeta_album,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_SUBTITULO, "bold"),
            text_color=self.color_texto,
            text="Álbum más escuchado",
        )
        etiqueta_titulo_album.pack(pady=(3, 0))
        self.componentes.append(etiqueta_titulo_album)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_album)
        # ---------------------------------------------------------------------------------

        # ------------------------ Panel para contenido de la tarjeta ---------------------
        # Panel para contenido con imagen y texto
        panel_contenido = ctk.CTkFrame(panel_tarjeta_album, fg_color="transparent")
        panel_contenido.pack(fill="x")
        self.componentes.append(panel_contenido)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Subpanel para la carátula --------------------------
        # Panel para la carátula (a la izquierda)
        panel_caratula = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_caratula.pack(side="left")
        self.componentes.append(panel_caratula)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Etiqueta para la carátula --------------------------
        # Etiqueta para la carátula
        etiqueta_caratula = ctk.CTkLabel(panel_caratula, text="", fg_color="transparent")
        etiqueta_caratula.pack()
        self.componentes.append(etiqueta_caratula)
        # ---------------------------------------------------------------------------------

        if self.controlador_biblioteca:
            # Primero obtener la carátula como imagen PIL
            caratula_pil = self.controlador_biblioteca.obtener_caratula_album_controlador(
                album["nombre"], formato="PIL", ancho=75, alto=75
            )
            if caratula_pil:
                # Convertir a CTkImage
                caratula_ctk = CTkImage(light_image=caratula_pil, dark_image=caratula_pil, size=(75, 75))
                etiqueta_caratula.configure(image=caratula_ctk, text="")
                # Guardar referencia
                etiqueta_caratula.image = caratula_ctk
            else:
                etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        else:
            etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        # ---------------------------------------------------------------------------------

        # -------------------------- Panel para información del álbum ---------------------
        # Panel para información del álbum
        panel_informacion_album = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_informacion_album.pack(side="left", fill="x", expand=True)
        self.componentes.append(panel_informacion_album)
        # ---------------------------------------------------------------------------------

        # ------------------------ Etiqueta con nombre de álbum ---------------------------
        # Etiqueta con nombre de álbum
        etiqueta_nombre_album = ctk.CTkLabel(
            panel_informacion_album,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "bold"),
            text_color=self.color_texto,
            text=album["nombre"],
        )
        etiqueta_nombre_album.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_nombre_album)
        self.controlador_tema.registrar_etiqueta(etiqueta_nombre_album)
        # ---------------------------------------------------------------------------------

        # ------------------------- Etiqueta con artista de álbum -------------------------
        # Etiqueta con el artista del álbum (NUEVA ETIQUETA)
        etiqueta_artista_album = ctk.CTkLabel(
            panel_informacion_album,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"{album['artista']}",
        )
        etiqueta_artista_album.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_artista_album)
        self.controlador_tema.registrar_etiqueta(etiqueta_artista_album)
        # ---------------------------------------------------------------------------------

        # Crear un diccionario con los textos que pueden necesitar desplazamiento
        textos_animados = {
            "nombre": (album["nombre"], etiqueta_nombre_album),
            "artista": (album["artista"], etiqueta_artista_album),
        }
        self.animacion_album = AnimacionGeneral()
        # Iniciar el desplazamiento con longitud máxima adecuada
        self.animacion_album.configurar_desplazamiento_etiqueta(panel_informacion_album, textos_animados, 460)

        # ------------------------ Etiqueta con artista de álbum --------------------------
        # Etiqueta con la reproducción del álbum
        etiqueta_reproducciones_album = ctk.CTkLabel(
            panel_informacion_album,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"Reproducciones: {album['reproducciones']}",
        )
        etiqueta_reproducciones_album.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_reproducciones_album)
        self.controlador_tema.registrar_etiqueta(etiqueta_reproducciones_album)
        # ---------------------------------------------------------------------------------
        # *********************************************************************************

    def mostrar_ultima_reproduccion(self, panel_padre, estadisticas):
        # Si no hay última canción, no mostrar
        if not estadisticas["ultima_cancion"]:
            return
        ultima = estadisticas["ultima_cancion"]

        # ******************************** Panel de tarjeta *******************************
        # Panel para última reproducción
        panel_ultima_escuchada = ctk.CTkFrame(
            panel_padre,
            fg_color="transparent",
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_ultima_escuchada.pack(fill="x", padx=3, pady=(3, 0))
        self.componentes.append(panel_ultima_escuchada)

        # ------------------------------- Etiqueta de título ------------------------------
        # Etiqueta de título
        etiqueta_titulo_ultima = ctk.CTkLabel(
            panel_ultima_escuchada,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_SUBTITULO, "bold"),
            text_color=self.color_texto,
            text="Última canción reproducida",
        )
        etiqueta_titulo_ultima.pack(pady=(3, 0))
        self.componentes.append(etiqueta_titulo_ultima)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_ultima)
        # ---------------------------------------------------------------------------------

        # ------------------------ Panel para contenido de la tarjeta ---------------------
        # Panel para contenido con imagen y texto
        panel_contenido = ctk.CTkFrame(panel_ultima_escuchada, fg_color="transparent")
        panel_contenido.pack(fill="x")
        self.componentes.append(panel_contenido)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Subpanel para la carátula --------------------------
        # Panel para la carátula (a la izquierda)
        panel_caratula = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_caratula.pack(side="left")
        self.componentes.append(panel_caratula)
        # ---------------------------------------------------------------------------------

        # ---------------------------- Etiqueta para la carátula --------------------------
        # Etiqueta para la carátula
        etiqueta_caratula = ctk.CTkLabel(panel_caratula, text="", fg_color="transparent")
        etiqueta_caratula.pack()
        self.componentes.append(etiqueta_caratula)
        # ---------------------------------------------------------------------------------

        if self.controlador_biblioteca:
            # Primero obtener la carátula como imagen PIL
            caratula_pil = self.controlador_biblioteca.obtener_caratula_album_controlador(
                ultima["album"], formato="PIL", ancho=75, alto=75
            )
            if caratula_pil:
                # Convertir a CTkImage
                caratula_ctk = CTkImage(light_image=caratula_pil, dark_image=caratula_pil, size=(75, 75))
                etiqueta_caratula.configure(image=caratula_ctk, text="")
                # Guardar referencia
                etiqueta_caratula.image = caratula_ctk
            else:
                etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        else:
            etiqueta_caratula.configure(width=75, height=75, text="Sin\ncarátula", image=None)
        # ---------------------------------------------------------------------------------

        # -------------------------- Panel para información de la canción ------------------
        # Panel para información del álbum
        panel_informacion_ultima = ctk.CTkFrame(panel_contenido, fg_color="transparent")
        panel_informacion_ultima.pack(side="left", fill="x", expand=True)
        self.componentes.append(panel_informacion_ultima)
        # ---------------------------------------------------------------------------------

        # ------------------------ Etiqueta con nombre de canción -------------------------
        # Etiqueta con título de canción
        etiqueta_titulo_ultima = ctk.CTkLabel(
            panel_informacion_ultima,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION, "bold"),
            text_color=self.color_texto,
            text=ultima["titulo"],
        )
        etiqueta_titulo_ultima.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_titulo_ultima)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_ultima)
        # ---------------------------------------------------------------------------------

        # ------------------------ Etiqueta con artista de canción ------------------------
        # Etiqueta con artista de canción
        etiqueta_artista_ultima = ctk.CTkLabel(
            panel_informacion_ultima,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"{ultima['artista']}",
        )
        etiqueta_artista_ultima.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_artista_ultima)
        self.controlador_tema.registrar_etiqueta(etiqueta_artista_ultima)
        # ---------------------------------------------------------------------------------
        # ------------------------ Etiqueta con artista de canción ------------------------
        # Etiqueta con artista de canción
        etiqueta_album_ultima = ctk.CTkLabel(
            panel_informacion_ultima,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
            text_color=self.color_texto,
            text=f"{ultima['album']}",
        )
        etiqueta_album_ultima.pack(anchor="w", padx=(5, 0))
        self.componentes.append(etiqueta_album_ultima)
        self.controlador_tema.registrar_etiqueta(etiqueta_album_ultima)
        # ---------------------------------------------------------------------------------

        # Crear un diccionario con los textos que pueden necesitar desplazamiento
        textos_animados = {
            "titulo": (ultima["titulo"], etiqueta_titulo_ultima),
            "artista": (ultima["artista"], etiqueta_artista_ultima),
            "album": (ultima["album"], etiqueta_album_ultima),
        }
        self.animacion_ultima = AnimacionGeneral()
        # Iniciar el desplazamiento con longitud máxima adecuada
        self.animacion_ultima.configurar_desplazamiento_etiqueta(
            panel_informacion_ultima, textos_animados, 440
        )

        # *********************************************************************************

    # Método para mostrar la ventana de estadisticas
    def mostrar_ventana_estadisticas(self):
        if not hasattr(self, "ventana_estadisticas") or self.ventana_estadisticas is None:
            self.crear_ventana_estadisticas()
        else:
            try:
                # Verificar si la ventana aún existe y es válida
                if self.ventana_estadisticas.winfo_exists():
                    self.colores()
                    establecer_icono_tema(self.ventana_estadisticas, self.controlador_tema.tema_interfaz)
                    self.ventana_estadisticas.deiconify()
                else:
                    # La ventana ya no existe, crear una nueva
                    self.ventana_estadisticas = None
                    self.crear_ventana_estadisticas()
            except Exception as e:
                print(f"Error al mostrar la ventana de estadísticas: {e}")
                self.ventana_estadisticas = None
                self.crear_ventana_estadisticas()

    # Método para cerrar la ventana de estadisticas
    def cerrar_ventana_estadisticas(self):
        cerrar_ventana_modal(self.ventana_estadisticas, self.componentes, self.controlador_tema)
