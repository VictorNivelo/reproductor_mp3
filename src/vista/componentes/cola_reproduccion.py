from vista.componentes.utiles.utiles_componentes import configurar_ventana_modal, cerrar_ventana_modal
from vista.utiles.utiles_scroll import GestorScroll
import customtkinter as ctk
from constantes import *
from io import BytesIO
from PIL import Image
import tkinter as tk


class ColaReproduccion:
    def __init__(self, ventana_principal, controlador_tema, controlador_reproductor):
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.controlador_reproductor = controlador_reproductor
        self.ventana_cola = None
        self.componentes = []
        self.gestor_scroll = None

    def mostrar_ventana_cola(self):
        # Si ya existe una ventana abierta, mostrarla
        if self.ventana_cola is not None and self.ventana_cola.winfo_exists():
            self.ventana_cola.lift()
            return
        
        # Crear ventana modal
        self.ventana_cola = ctk.CTkToplevel(self.ventana_principal)
        
        # Configurar la ventana modal
        color_fondo = FONDO_CLARO if self.controlador_tema.tema_interfaz == "claro" else FONDO_OSCURO
        configurar_ventana_modal(
            self.ventana_principal,
            self.ventana_cola,
            ANCHO_COLA_REPRODUCCION,
            ALTO_COLA_REPRODUCCION,
            "Cola de reproducción",
            color_fondo,
            lambda: cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema),
            self.controlador_tema,
        )
        
        # Contenedor principal con margen reducido
        contenedor_principal = ctk.CTkFrame(self.ventana_cola, fg_color="transparent")
        contenedor_principal.pack(fill="both", expand=True, padx=3, pady=3)
        self.componentes.append(contenedor_principal)
        self.controlador_tema.registrar_frame(contenedor_principal, es_ctk=True)
        
        # Etiqueta título con menos altura
        etiqueta_titulo = ctk.CTkLabel(
            contenedor_principal,
            height=15,
            text="Cola de reproducción",
            font=(LETRA, 18, "bold"),
            text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
        )
        etiqueta_titulo.pack(pady=(0, 8))
        self.componentes.append(etiqueta_titulo)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
        
        # Frame para la canción actual con mejor estilo
        frame_cancion_actual = ctk.CTkFrame(
            contenedor_principal,
            fg_color=HOVER_CLARO if self.controlador_tema.tema_interfaz == "claro" else HOVER_OSCURO,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        frame_cancion_actual.pack(fill="x", padx=3, pady=(0, 8))
        self.componentes.append(frame_cancion_actual)
        self.controlador_tema.registrar_frame(frame_cancion_actual, es_ctk=True)
        
        # Etiqueta de reproducción actual
        etiqueta_reproduciendo = ctk.CTkLabel(
            frame_cancion_actual,
            height=15,
            text="Reproduciendo ahora:",
            font=(LETRA, 14, "bold"),
            text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
        )
        etiqueta_reproduciendo.pack(anchor="w", padx=5, pady=(5, 0))
        self.componentes.append(etiqueta_reproduciendo)
        self.controlador_tema.registrar_etiqueta(etiqueta_reproduciendo)
        
        # Mostrar la canción actual
        self.mostrar_cancion_actual(frame_cancion_actual)
        
        # Frame para las próximas canciones
        frame_cola = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
        frame_cola.pack(fill="both", expand=True, padx=3)
        self.componentes.append(frame_cola)
        self.controlador_tema.registrar_frame(frame_cola, es_ctk=True)
        
        # Etiqueta de próximas canciones
        etiqueta_proximas = ctk.CTkLabel(
            frame_cola,
            height=15,
            text="Próximas canciones:",
            font=(LETRA, 14, "bold"),
            text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
        )
        etiqueta_proximas.pack(anchor="w")
        self.componentes.append(etiqueta_proximas)
        self.controlador_tema.registrar_etiqueta(etiqueta_proximas)
        
        # Canvas para las próximas canciones (sin scrollbar visible)
        canvas_cola = tk.Canvas(frame_cola, highlightthickness=0)
        canvas_cola.pack(fill="both", expand=True)
        
        # Aplicar color de fondo según tema
        color_bg = FONDO_CLARO if self.controlador_tema.tema_interfaz == "claro" else FONDO_OSCURO
        canvas_cola.configure(bg=color_bg)
        self.componentes.append(canvas_cola)
        self.controlador_tema.registrar_canvas(canvas_cola)
        
        # Frame para contener los elementos en el canvas
        frame_canciones = ctk.CTkFrame(canvas_cola, fg_color="transparent")
        self.componentes.append(frame_canciones)
        self.controlador_tema.registrar_frame(frame_canciones, es_ctk=True)
        
        # Crear la ventana dentro del canvas
        canvas_window = canvas_cola.create_window((0, 0), window=frame_canciones, anchor="nw")
        
        # Configurar el gestor de scroll
        self.gestor_scroll = GestorScroll(canvas_cola, frame_canciones, canvas_window)
        
        # Mostrar las canciones en la cola
        self.mostrar_cola_canciones(frame_canciones)
        
        # Botón para cerrar con mejor estilo
        boton_cerrar = ctk.CTkButton(
            contenedor_principal,
            text="Cerrar",
            fg_color=BOTON_CLARO if self.controlador_tema.tema_interfaz == "claro" else BOTON_OSCURO,
            hover_color=HOVER_CLARO if self.controlador_tema.tema_interfaz == "claro" else HOVER_OSCURO,
            text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            command=lambda: cerrar_ventana_modal(self.ventana_cola, self.componentes, self.controlador_tema),
            height=32,
        )
        boton_cerrar.pack(pady=(10, 5))
        self.componentes.append(boton_cerrar)

    def mostrar_cancion_actual(self, frame):
        cancion_actual = self.controlador_reproductor.cancion_actual
        if cancion_actual:
            # Crear un frame para mostrar la información de la canción
            frame_info = ctk.CTkFrame(frame, fg_color="transparent")
            frame_info.pack(fill="x", padx=5, pady=(0, 5))
            self.componentes.append(frame_info)
            self.controlador_tema.registrar_frame(frame_info, es_ctk=True)
            
            # Intentar mostrar la carátula
            frame_imagen = ctk.CTkFrame(frame_info, fg_color="transparent", width=40, height=40)
            frame_imagen.pack(side="left", padx=(0, 8))
            self.componentes.append(frame_imagen)
            
            if cancion_actual.caratula_cancion:
                try:
                    imagen = Image.open(BytesIO(cancion_actual.caratula_cancion))
                    ancho = 40
                    ratio = ancho / float(imagen.size[0])
                    alto = int(float(imagen.size[1]) * float(ratio))
                    imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
                    foto = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))
                    label_imagen = ctk.CTkLabel(frame_imagen, image=foto, text="")
                    label_imagen.image = foto  # Mantener referencia
                    label_imagen.pack()
                    self.componentes.append(label_imagen)
                except Exception as e:
                    print(f"Error al cargar la carátula: {e}")
            
            # Información de la canción
            info_cancion = ctk.CTkFrame(frame_info, fg_color="transparent")
            info_cancion.pack(side="left", fill="x", expand=True)
            self.componentes.append(info_cancion)
            self.controlador_tema.registrar_frame(info_cancion, es_ctk=True)
            
            # Nombre de la canción
            etiqueta_titulo = ctk.CTkLabel(
                info_cancion,
                height=15,
                text=cancion_actual.titulo_cancion,
                font=(LETRA, 12, "bold"),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                anchor="w",
            )
            etiqueta_titulo.pack(anchor="w")
            self.componentes.append(etiqueta_titulo)
            self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
            
            # Artista
            etiqueta_artista = ctk.CTkLabel(
                info_cancion,
                height=15,
                text=cancion_actual.artista,
                font=(LETRA, 10),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                anchor="w",
            )
            etiqueta_artista.pack(anchor="w")
            self.componentes.append(etiqueta_artista)
            self.controlador_tema.registrar_etiqueta(etiqueta_artista)
        else:
            etiqueta_no_cancion = ctk.CTkLabel(
                frame,
                height=15,
                text="No hay ninguna canción en reproducción",
                font=(LETRA, 12),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            )
            etiqueta_no_cancion.pack(padx=5, pady=5)
            self.componentes.append(etiqueta_no_cancion)
            self.controlador_tema.registrar_etiqueta(etiqueta_no_cancion)

    def mostrar_cola_canciones(self, frame):
        # Obtener el estado actual del reproductor
        lista_reproduccion = self.controlador_reproductor.lista_reproduccion
        indice_actual = self.controlador_reproductor.indice_actual
        modo_repeticion = self.controlador_reproductor.modo_repeticion
        modo_aleatorio = self.controlador_reproductor.modo_aleatorio
        
        if not lista_reproduccion:
            etiqueta_vacia = ctk.CTkLabel(
                frame,
                height=15,
                text="La cola de reproducción está vacía",
                font=(LETRA, 12),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            )
            etiqueta_vacia.pack(pady=5)
            self.componentes.append(etiqueta_vacia)
            self.controlador_tema.registrar_etiqueta(etiqueta_vacia)
            return
        
        # Determinar qué canciones se mostrarán a continuación
        proximas_canciones = []
        
        if modo_repeticion == 1:  # Repetir canción actual
            # Solo mostrar la canción actual que se repetirá
            if 0 <= indice_actual < len(lista_reproduccion):
                etiqueta_info = ctk.CTkLabel(
                    frame,
                    height=15,
                    text="La canción actual se repetirá",
                    font=(LETRA, 12, "italic"),
                    text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                )
                etiqueta_info.pack(anchor="w", pady=5)
                self.componentes.append(etiqueta_info)
                self.controlador_tema.registrar_etiqueta(etiqueta_info)
                return
        elif modo_aleatorio:  # Reproducción aleatoria
            etiqueta_info = ctk.CTkLabel(
                frame,
                height=15,
                text="Modo aleatorio activado - las canciones se elegirán al azar",
                font=(LETRA, 12, "italic"),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            )
            etiqueta_info.pack(anchor="w", pady=(0, 5))
            self.componentes.append(etiqueta_info)
            self.controlador_tema.registrar_etiqueta(etiqueta_info)
            
            # En modo aleatorio, mostrar todas las canciones disponibles
            disponibles = [cancion for i, cancion in enumerate(lista_reproduccion) if i != indice_actual]
            proximas_canciones = disponibles[:10]  # Limitar a 10 canciones
            
            if not proximas_canciones and modo_repeticion == 2:  # Si no hay más y está en repetir todo
                etiqueta_reinicio = ctk.CTkLabel(
                    frame,
                    height=15,
                    text="Se reiniciará la reproducción aleatoria de todas las canciones",
                    font=(LETRA, 12, "italic"),
                    text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                )
                etiqueta_reinicio.pack(anchor="w", pady=(0, 5))
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
        else:  # Reproducción secuencial
            # Mostrar las próximas canciones en orden
            if indice_actual < len(lista_reproduccion) - 1:
                proximas_canciones = lista_reproduccion[indice_actual + 1 : indice_actual + 11]  # Limitar a 10 canciones
            elif modo_repeticion == 2:  # Repetir todo
                etiqueta_reinicio = ctk.CTkLabel(
                    frame,
                    height=15,
                    text="Se reiniciará la reproducción desde el principio",
                    font=(LETRA, 12, "italic"),
                    text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                )
                etiqueta_reinicio.pack(anchor="w", pady=(0, 5))
                self.componentes.append(etiqueta_reinicio)
                self.controlador_tema.registrar_etiqueta(etiqueta_reinicio)
                proximas_canciones = lista_reproduccion[:10]  # Mostrar las primeras 10 canciones
        
        # Mostrar las próximas canciones con un diseño más compacto
        for i, cancion in enumerate(proximas_canciones):
            # Crear un frame para cada canción con hover
            frame_cancion = ctk.CTkFrame(
                frame,
                fg_color="transparent",
                corner_radius=5
            )
            frame_cancion.pack(fill="x", pady=(0, 5))
            self.componentes.append(frame_cancion)
            self.controlador_tema.registrar_frame(frame_cancion, es_ctk=True)
            
            # Número de orden
            etiqueta_numero = ctk.CTkLabel(
                frame_cancion,
                height=15,
                text=f"{i+1}.",
                width=20,
                font=(LETRA, 12),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            )
            etiqueta_numero.pack(side="left")
            self.componentes.append(etiqueta_numero)
            self.controlador_tema.registrar_etiqueta(etiqueta_numero)
            
            # Intentar mostrar la carátula
            if cancion.caratula_cancion:
                try:
                    imagen = Image.open(BytesIO(cancion.caratula_cancion))
                    ancho = 30
                    ratio = ancho / float(imagen.size[0])
                    alto = int(float(imagen.size[1]) * float(ratio))
                    imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
                    foto = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(ancho, alto))
                    label_imagen = ctk.CTkLabel(frame_cancion, image=foto, text="")
                    label_imagen.image = foto  # Mantener referencia
                    label_imagen.pack(side="left", padx=(0, 5))
                    self.componentes.append(label_imagen)
                except Exception as e:
                    print(f"Error al cargar la carátula: {e}")
            
            # Información de la canción
            info_cancion = ctk.CTkFrame(frame_cancion, fg_color="transparent")
            info_cancion.pack(side="left", fill="x", expand=True)
            self.componentes.append(info_cancion)
            self.controlador_tema.registrar_frame(info_cancion, es_ctk=True)
            
            # Nombre de la canción
            etiqueta_titulo = ctk.CTkLabel(
                info_cancion,
                height=15,
                text=cancion.titulo_cancion,
                font=(LETRA, 12, "bold"),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                anchor="w",
            )
            etiqueta_titulo.pack(anchor="w")
            self.componentes.append(etiqueta_titulo)
            self.controlador_tema.registrar_etiqueta(etiqueta_titulo)
            
            # Artista
            etiqueta_artista = ctk.CTkLabel(
                info_cancion,
                height=15,
                text=cancion.artista,
                font=(LETRA, 10),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
                anchor="w",
            )
            etiqueta_artista.pack(anchor="w")
            self.componentes.append(etiqueta_artista)
            self.controlador_tema.registrar_etiqueta(etiqueta_artista)
            
            # Añadir efecto hover al frame de canción
            def configurar_hover(frame, enter=True):
                color = HOVER_CLARO if self.controlador_tema.tema_interfaz == "claro" else HOVER_OSCURO
                frame.configure(fg_color=color if enter else "transparent")
                
            frame_cancion.bind("<Enter>", lambda e, f=frame_cancion: configurar_hover(f, True))
            frame_cancion.bind("<Leave>", lambda e, f=frame_cancion: configurar_hover(f, False))
            
        if not proximas_canciones and modo_repeticion != 2:
            etiqueta_final = ctk.CTkLabel(
                frame,
                height=15,
                text="No hay más canciones en la cola",
                font=(LETRA, 12),
                text_color=TEXTO_CLARO if self.controlador_tema.tema_interfaz == "claro" else TEXTO_OSCURO,
            )
            etiqueta_final.pack(pady=5)
            self.componentes.append(etiqueta_final)
            self.controlador_tema.registrar_etiqueta(etiqueta_final)