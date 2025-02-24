from controlador.controlador_reproductor import ControladorReproductor
from controlador.controlador_biblioteca import ControladorBiblioteca
from vista.componentes.mini_reproductor import MiniReproductor
from vista.componentes.configuracion import Configuracion
from controlador.controlador_tema import ControladorTema
from modelo.biblioteca import Biblioteca
from vista.utiles.utiles_vista import *
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
from constantes import *
import tkinter as tk
import random

# FUNCIONES DE LOS BOTONES


# Función para cambiar el tema de la interfaz
def cambiar_tema_vista():
    global TEMA_ACTUAL
    # Cambiar tema
    tema_actual_vista = "oscuro" if TEMA_ACTUAL == "claro" else "claro"
    controlador.cambiar_tema()
    # Actualizar barras del espectro
    color_barra = HOVER_CLARO if tema_actual_vista == "claro" else HOVER_OSCURO
    for barra in barras_espectro:
        canvas_espectro.itemconfig(barra, fill=color_barra)
    # Actualizar icono de tema
    if tema_actual_vista == "claro":
        cambiar_icono_tema("claro")
        controlador.registrar_botones("modo_oscuro", boton_tema)
    else:
        cambiar_icono_tema("oscuro")
        controlador.registrar_botones("modo_claro", boton_tema)
    actualizar_iconos()


# Función para cambiar el tema de la interfaz
def actualizar_iconos():
    # Estado de reproducción
    icon_reproduccion = "pausa" if REPRODUCIENDO else "reproducir"
    controlador.registrar_botones(icon_reproduccion, boton_reproducir)
    # Orden de reproducción
    icon_orden = "aleatorio" if ORDEN else "orden"
    controlador.registrar_botones(icon_orden, boton_aleatorio)
    # Repetición
    if REPETICION == 0:
        icon_repeticion = "no_repetir"
    elif REPETICION == 1:
        icon_repeticion = "repetir_actual"
    else:
        icon_repeticion = "repetir_todo"
    controlador.registrar_botones(icon_repeticion, boton_repetir)
    # Volumen
    if SILENCIADO:
        icon_volumen = "silencio"
    else:
        if VOLUMEN == 0:
            icon_volumen = "sin_volumen"
        elif VOLUMEN <= 33:
            icon_volumen = "volumen_bajo"
        elif VOLUMEN <= 66:
            icon_volumen = "volumen_medio"
        else:
            icon_volumen = "volumen_alto"
    if PANEL_VISIBLE:
        controlador.registrar_botones("ocultar", boton_visibilidad)
    else:
        controlador.registrar_botones("mostrar", boton_visibilidad)
    controlador.registrar_botones(icon_volumen, boton_silenciar)
    # Me gusta y favoritos
    icon_me_gusta = "me_gusta_rojo" if ME_GUSTA else "me_gusta"
    icon_favorito = "favorito_amarillo" if FAVORITO else "favorito"
    controlador.registrar_botones(icon_me_gusta, boton_me_gusta)
    controlador.registrar_botones(icon_favorito, boton_favorito)


# Función para cambiar el estado de reproducción
def reproducir_vista():
    global REPRODUCIENDO
    REPRODUCIENDO = not REPRODUCIENDO
    if REPRODUCIENDO:
        controlador.registrar_botones("pausa", boton_reproducir)
        controlador_reproductor.reanudar_reproduccion()
        actualizar_espectro()
    else:
        controlador.registrar_botones("reproducir", boton_reproducir)
        controlador_reproductor.pausar_reproduccion()


# Función para cambiar el volumen
def cambiar_volumen_vista(_event=None):
    global VOLUMEN, SILENCIADO
    if not SILENCIADO:
        nuevo_volumen = int(barra_volumen.get())
        VOLUMEN = nuevo_volumen
        etiqueta_porcentaje_volumen.configure(text=f"{VOLUMEN}%")
        if VOLUMEN == 0:
            controlador.registrar_botones("sin_volumen", boton_silenciar)
        elif VOLUMEN <= 33:
            controlador.registrar_botones("volumen_bajo", boton_silenciar)
        elif VOLUMEN <= 66:
            controlador.registrar_botones("volumen_medio", boton_silenciar)
        else:
            controlador.registrar_botones("volumen_alto", boton_silenciar)


# Función para cambiar el estado de silencio
def cambiar_silencio_vista():
    global SILENCIADO
    SILENCIADO = not SILENCIADO
    if SILENCIADO:
        controlador.registrar_botones("silencio", boton_silenciar)
    else:
        cambiar_volumen_vista()


# Función para cambiar el orden de reproducción
def cambiar_orden_vista():
    global ORDEN
    ORDEN = not ORDEN
    if ORDEN:
        controlador.registrar_botones("aleatorio", boton_aleatorio)
    else:
        controlador.registrar_botones("orden", boton_aleatorio)


# Función para cambiar la repetición de reproducción
def cambiar_repeticion_vista():
    global REPETICION
    REPETICION = (REPETICION + 1) % 3
    # Icono de no repetir
    if REPETICION == 0:
        controlador.registrar_botones("no_repetir", boton_repetir)
    # Icono de repetir actual
    elif REPETICION == 1:
        controlador.registrar_botones("repetir_actual", boton_repetir)
    # Icono de repetir todo
    else:
        controlador.registrar_botones("repetir_todo", boton_repetir)


# Función para cambiar la visibilidad del panel
def cambiar_visibilidad_vista():
    global PANEL_VISIBLE
    PANEL_VISIBLE = not PANEL_VISIBLE
    if PANEL_VISIBLE:
        # Mostrar el panel
        contenedor_derecha.configure(width=ANCHO_PANEL_DERECHA)
        contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
        controlador.registrar_botones("ocultar", boton_visibilidad)
    else:
        # Ocultar el panel
        contenedor_derecha.configure(width=0)
        contenedor_derecha.pack_forget()
        controlador.registrar_botones("mostrar", boton_visibilidad)


# Función para cambiar el estado de boton me gusta
def cambiar_me_gusta_vista():
    global ME_GUSTA
    ME_GUSTA = not ME_GUSTA
    if ME_GUSTA:
        controlador.registrar_botones("me_gusta_rojo", boton_me_gusta)
    else:
        controlador.registrar_botones("me_gusta", boton_me_gusta)


# Función para cambiar el estado de favorito
def cambiar_favorito_vista():
    global FAVORITO
    FAVORITO = not FAVORITO
    if FAVORITO:
        controlador.registrar_botones("favorito_amarillo", boton_favorito)
    else:
        controlador.registrar_botones("favorito", boton_favorito)


# Función para agregar canciones (puede ser llamada desde un botón)
def agregar_cancion_vista():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar canciones",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.flac *.m4a *.ogg"), ("Todos los archivos", "*.*")],
    )
    for ruta in rutas:
        cancion = controlador_biblioteca.agregar_cancion(Path(ruta))
        if cancion:
            controlador_biblioteca.actualizar_vista_canciones(
                panel_botones_canciones, controlador, controlador_reproductor
            )


# Función para agregar directorio (puede ser llamada desde un botón)
def agregar_directorio_vista():
    ruta = filedialog.askdirectory(title="Seleccionar directorio de música")
    if ruta:
        canciones = controlador_biblioteca.agregar_directorio(Path(ruta))
        if canciones:
            controlador_biblioteca.actualizar_vista_canciones(
                panel_botones_canciones, controlador, controlador_reproductor
            )


# Función para actualizar el progreso de la canción
def actualizar_progreso_vista(event):
    global TIEMPO_ACTUAL
    # Obtener dimensiones y calcular posición
    ancho_total = barra_progreso.winfo_width()
    posicion_relativa = max(0, min(1, event.x / ancho_total))
    # Actualizar barra de progreso
    barra_progreso.set(posicion_relativa)
    # Calcular y actualizar tiempo
    TIEMPO_ACTUAL = int(DURACION_TOTAL * posicion_relativa)
    actualizar_etiqueta_tiempo_vista()


# Función para actualizar la etiqueta de tiempo
def actualizar_etiqueta_tiempo_vista():
    # Convertir segundos a formato mm:ss
    minutos_actual = TIEMPO_ACTUAL // 60
    segundos_actual = TIEMPO_ACTUAL % 60
    minutos_total = DURACION_TOTAL // 60
    segundos_total = DURACION_TOTAL % 60
    # Actualizar etiquetas
    etiqueta_tiempo_actual.configure(text=f"{minutos_actual:02d}:{segundos_actual:02d}")
    etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")


# Función para iniciar el arrastre del progreso de la canción
def iniciar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = True
    actualizar_progreso_vista(event)


# Función para arrastrar el progreso de la canción
def durante_arrastre_progreso(event):
    if ARRASTRANDO_PROGRESO:
        actualizar_progreso_vista(event)


# Función para finalizar el arrastre del progreso
def finalizar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = False
    actualizar_progreso_vista(event)


# Función para crear las barras iniciales
def crear_barras_espectro():
    global barras_espectro, ANCHO_BARRA, ESPACIO_ENTRE_BARRA
    # Limpiar barras existentes
    for barra in barras_espectro:
        canvas_espectro.delete(barra)
    barras_espectro.clear()
    # Obtener dimensiones del canvas
    ancho_canvas = canvas_espectro.winfo_width()
    alto_canvas = canvas_espectro.winfo_height()
    # Calcular ancho de barra y espacio entre barras dinámicamente
    espacio_total = ancho_canvas  # Usar 90% del ancho para dejar márgenes
    ANCHO_BARRA = max(2, (espacio_total / NUMERO_BARRA) * 0.7)  # 70% para la barra
    ESPACIO_ENTRE_BARRA = (espacio_total / NUMERO_BARRA) * 0.3  # 30% para el espacio
    # Calcular posición inicial para centrar las barras
    x_inicial = (
        ancho_canvas - (NUMERO_BARRA * (ANCHO_BARRA + ESPACIO_ENTRE_BARRA) - ESPACIO_ENTRE_BARRA)
    ) // 2
    # Color según el tema
    color_barra = HOVER_CLARO if TEMA_ACTUAL == "claro" else HOVER_OSCURO
    # Crear barras
    for i in range(NUMERO_BARRA):
        x1 = x_inicial + i * (ANCHO_BARRA + ESPACIO_ENTRE_BARRA)
        x2 = x1 + ANCHO_BARRA
        y1 = alto_canvas
        y2 = alto_canvas - alturas_barras[i]
        barra = canvas_espectro.create_rectangle(x1, y1, x2, y2, fill=color_barra, width=0)
        barras_espectro.append(barra)


# Función para actualizar la animación del espectro
def actualizar_espectro():
    if not canvas_espectro.winfo_exists():  # Verificar si el canvas existe
        return
    alto_canvas = canvas_espectro.winfo_height()
    # Generar alturas aleatorias para simular el espectro
    for i in range(NUMERO_BARRA):
        if i < len(barras_espectro):  # Verificar que la barra existe
            altura_objetivo = random.randint(10, int(alto_canvas))
            alturas_barras[i] = int(alturas_barras[i] * 0.7 + altura_objetivo * 0.3)
            # Actualizar altura de la barra
            try:
                x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
                canvas_espectro.coords(
                    barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i]
                )
            except tk.TclError:
                # Error cuando el widget del canvas ha sido destruido o no está disponible
                print("Error: El canvas del espectro no está disponible")
                return
            except IndexError:
                # Error cuando se intenta acceder a una barra que no existe
                print(f"Error: No se encontró la barra {i} en el espectro")
                return
    # Llamar a la función nuevamente después de un delay
    if REPRODUCIENDO:
        ventana_principal.after(50, actualizar_espectro)


# Función para establecer el icono del tema
def cambiar_icono_tema(tema="claro"):
    establecer_icono_tema(ventana_principal, tema)


# Función para abrir la ventana de configuración
def abrir_configuracion():
    configuracion.mostrar_ventana_configuracion()


# Función para minimizar la ventana
def minimizar_ventana():
    mini_reproductor.mostrar_ventana_mini_reproductor()


# FUNCIONES DE LOS SCROLLS


# Funciones para el scroll de la lista de canciones del panel
def scroll_frame_configuracion(_event=None):
    canvas_canciones.configure(scrollregion=canvas_canciones.bbox("all"))
    # Obtener dimensiones
    contenido_altura = panel_botones_canciones.winfo_reqheight()
    canvas_altura = canvas_canciones.winfo_height()
    # Habilitar o deshabilitar el scroll
    if contenido_altura <= canvas_altura:
        canvas_canciones.unbind_all("<MouseWheel>")
    else:
        canvas_canciones.bind_all("<MouseWheel>", scroll_raton_configuracion)


# Funciones para el scroll de la lista de canciones del canvas
def scroll_canvas_configuracion(event):
    canvas_width = event.width
    canvas_canciones.itemconfig(canvas_window, width=canvas_width)
    # Verificar scroll después de redimensionar
    scroll_frame_configuracion(None)


# Funciones para el scroll de la lista de canciones con el ratón
def scroll_raton_configuracion(event):
    contenido_altura = panel_botones_canciones.winfo_reqheight()
    canvas_altura = canvas_canciones.winfo_height()
    # Desplazar el canvas
    if contenido_altura > canvas_altura:
        canvas_canciones.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ************************************** Ventana principal **************************************
# Crear ventana
ventana_principal = ctk.CTk()

# Apariencia de la interfaz por defecto es claro
ctk.set_appearance_mode("light")

# Icono de la ventana
cambiar_icono_tema()

# Controlador de tema
controlador = ControladorTema()

# Biblioteca de canciones
biblioteca = Biblioteca()

# Mini reproductor
mini_reproductor = MiniReproductor(ventana_principal, controlador)

# Configuración
configuracion = Configuracion(ventana_principal, controlador)

# Controlador de la biblioteca
controlador_biblioteca = ControladorBiblioteca(biblioteca)

# Controlador del reproductor
controlador_reproductor = ControladorReproductor()

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()

# Calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ANCHO_PRINCIPAL) // 2
posicion_alto = (alto_pantalla - ALTO_PRINCIPAL) // 3

# Establecer la geometría de la ventana
ventana_principal.geometry(f"{ANCHO_PRINCIPAL}x{ALTO_PRINCIPAL}+{posicion_ancho}+{posicion_alto}")

# Título de la ventana
ventana_principal.title("Reproductor de música")

# ***********************************************************************************************

# ==================================== Contenedor principal =====================================

# Contenedor principal
conenedor_principal = tk.Frame(ventana_principal)
conenedor_principal.configure(
    bg=FONDO_PRINCIPAL_CLARO,
    padx=5,
    pady=5,
)
conenedor_principal.pack(fill="both", expand=True)
controlador.registrar_frame(conenedor_principal, es_principal=True)

# ===============================================================================================

# ======================================= Panel izquierda =======================================

# Contenedor izquierdo hecho con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    conenedor_principal, fg_color=FONDO_CLARO, corner_radius=BORDES_REDONDEADOS_PANEL
)
contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)
controlador.registrar_frame(contenedor_izquierda, es_ctk=True)

# ------------------------------- Seccion de controles superiores --------------------------------

# Contenedor superior
contenedor_superior = tk.Frame(contenedor_izquierda)
contenedor_superior.configure(bg=FONDO_CLARO)
contenedor_superior.pack(fill="both", padx=10, pady=(10, 3))
controlador.registrar_frame(contenedor_superior)

# Botones de la parte superior
boton_ajustes = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=abrir_configuracion,
)
boton_ajustes.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("ajustes", boton_ajustes)
crear_tooltip(boton_ajustes, "Configuración")

boton_tema = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_tema_vista,
)
boton_tema.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("modo_oscuro", boton_tema)
crear_tooltip(boton_tema, "Cambiar a oscuro")

boton_visibilidad = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_visibilidad_vista,
)
boton_visibilidad.pack(side=tk.RIGHT)
controlador.registrar_botones("ocultar", boton_visibilidad)
crear_tooltip(boton_visibilidad, "Ocultar lateral")

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de imagen de la canción -------------------------------

# Contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(bg=FONDO_CLARO)
contenedor_imagen.pack(fill="both", expand=True, padx=10, pady=3)
controlador.registrar_frame(contenedor_imagen)

# Etiqueta de la imagen de la canción
imagen_cancion = ctk.CTkLabel(
    contenedor_imagen,
    width=300,
    height=300,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_VOLUMEN),
    text_color=TEXTO_CLARO,
    text="Sin carátula",
)
imagen_cancion.pack(expand=True)
controlador.registrar_etiqueta(imagen_cancion)


# -----------------------------------------------------------------------------------------------

# ----------------------------- Seccion de información de la canción ----------------------------
# Contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(bg=FONDO_CLARO)
contenedor_informacion.pack(fill="both", padx=10, pady=5)
controlador.registrar_frame(contenedor_informacion)

# Etiqueta de información de la canción
etiqueta_nombre_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Nombre de la Canción",
)
etiqueta_nombre_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_nombre_cancion)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Artista de la Canción",
)
etiqueta_artista_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_artista_cancion)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Álbum de la Canción",
)
etiqueta_album_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_album_cancion)

etiqueta_anio_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Lanzamiento de la Canción",
)
etiqueta_anio_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_anio_cancion)

controlador_reproductor.establecer_informacion_interfaz(
    etiqueta_nombre_cancion,
    etiqueta_artista_cancion,
    etiqueta_album_cancion,
    etiqueta_anio_cancion,
    imagen_cancion,
)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion botones de gustos -------------------------------------

# Contenedor de botones de gustos
contenedor_botones_gustos = tk.Frame(contenedor_izquierda)
contenedor_botones_gustos.configure(bg=FONDO_CLARO)
contenedor_botones_gustos.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_botones_gustos)

# Panel de botones de gustos
panel_botones_gustos = tk.Frame(contenedor_botones_gustos)
panel_botones_gustos.configure(bg=FONDO_CLARO)
panel_botones_gustos.pack(expand=True)
controlador.registrar_frame(panel_botones_gustos)

# Botones de gustos
boton_me_gusta = ctk.CTkButton(
    panel_botones_gustos,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_me_gusta_vista,
)
boton_me_gusta.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("me_gusta", boton_me_gusta)

boton_favorito = ctk.CTkButton(
    panel_botones_gustos,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_favorito_vista,
)
boton_favorito.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("favorito", boton_favorito)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de espectro de audio ----------------------------------
# Contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(height=100, bg=FONDO_CLARO)
contenedor_espectro.pack(fill="both", padx=10, pady=3)
contenedor_espectro.pack_propagate(False)
controlador.registrar_frame(contenedor_espectro)

# Canvas para el espectro
canvas_espectro = tk.Canvas(contenedor_espectro, bg=FONDO_CLARO, highlightthickness=0)
canvas_espectro.pack(fill="both", expand=True)
controlador.registrar_canvas(canvas_espectro, es_tabview=False)

# Variables para el espectro
alturas_barras = [0] * NUMERO_BARRA
barras_espectro = []

# Vincular la creación de barras al evento de configuración del canvas
canvas_espectro.bind("<Configure>", lambda e: crear_barras_espectro())

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de barra de progreso ---------------------------------

# Contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(bg=FONDO_CLARO)
contenedor_progreso.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_progreso)

# Panel de progreso
panel_progreso = tk.Frame(contenedor_progreso)
panel_progreso.configure(bg=FONDO_CLARO)
panel_progreso.pack(fill="x", expand=True)
controlador.registrar_frame(panel_progreso)

# Barra de progreso
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(height=6, progress_color=FONDO_OSCURO, fg_color="lightgray")
barra_progreso.pack(fill="x", padx=12, pady=(0, 3))
barra_progreso.set(0)
barra_progreso.bind("<Button-1>", iniciar_arrastre_progreso)
barra_progreso.bind("<B1-Motion>", durante_arrastre_progreso)
barra_progreso.bind("<ButtonRelease-1>", finalizar_arrastre_progreso)
controlador.registrar_progress_bar(barra_progreso)

controlador_reproductor.establecer_barra_progreso(barra_progreso)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de tiempo de la canción -------------------------------

# Panel de tiempo
panel_tiempo = tk.Frame(contenedor_progreso)
panel_tiempo.configure(bg=FONDO_CLARO)
panel_tiempo.pack(fill="x", expand=True)
controlador.registrar_frame(panel_tiempo)

# Etiqueta de tiempo actual
etiqueta_tiempo_actual = ctk.CTkLabel(
    panel_tiempo,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_actual.pack(side=tk.LEFT)
controlador.registrar_etiqueta(etiqueta_tiempo_actual)

# Etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_total.pack(side=tk.RIGHT)
controlador.registrar_etiqueta(etiqueta_tiempo_total)

controlador_reproductor.establecer_etiquetas_tiempo(etiqueta_tiempo_actual, etiqueta_tiempo_total)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de controles de reproducción --------------------------

# Contenedor de controles de reproducción
contenedor_controles_reproduccion = tk.Frame(contenedor_izquierda)
contenedor_controles_reproduccion.configure(bg=FONDO_CLARO)
contenedor_controles_reproduccion.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_controles_reproduccion)

# Panel de controles
panel_controles_reproduccion = tk.Frame(contenedor_controles_reproduccion)
panel_controles_reproduccion.configure(bg=FONDO_CLARO)
panel_controles_reproduccion.pack(expand=True)
controlador.registrar_frame(panel_controles_reproduccion)

# Botones de control
boton_aleatorio = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_orden_vista,
)
boton_aleatorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("aleatorio", boton_aleatorio)

boton_repetir = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_repeticion_vista,
)
boton_repetir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("no_repetir", boton_repetir)

boton_retroceder = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_retroceder.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("retroceder", boton_retroceder)

boton_anterior = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_anterior.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("anterior", boton_anterior)

boton_reproducir = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=reproducir_vista,
)
boton_reproducir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("reproducir", boton_reproducir)

boton_siguiente = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_siguiente.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("siguiente", boton_siguiente)

boton_adelantar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_adelantar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("adelantar", boton_adelantar)

boton_agregar_cola = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_agregar_cola.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cola", boton_agregar_cola)

boton_minimizar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=minimizar_ventana,
)
boton_minimizar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("minimizar", boton_minimizar)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de barra de volumen -----------------------------------

# Contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(bg=FONDO_CLARO)
contenedor_volumen.pack(fill="both", padx=10, pady=(7, 10))
controlador.registrar_frame(contenedor_volumen)

# Panel de volumen
panel_volumen = tk.Frame(contenedor_volumen)
panel_volumen.configure(bg=FONDO_CLARO)
panel_volumen.pack(expand=True)
controlador.registrar_frame(panel_volumen)

# Botón de silenciar
boton_silenciar = ctk.CTkButton(
    panel_volumen,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_silencio_vista,
)
boton_silenciar.pack(side=tk.LEFT)
controlador.registrar_botones("silencio", boton_silenciar)

# Panel de elementos de volumen
panel_elementos_volumen = tk.Frame(panel_volumen, bg=FONDO_CLARO)
panel_elementos_volumen.pack(side=tk.LEFT, fill="x", expand=True)
controlador.registrar_frame(panel_elementos_volumen)

# Barra de volumen
barra_volumen = ctk.CTkSlider(panel_elementos_volumen)
barra_volumen.configure(
    progress_color=FONDO_OSCURO,
    fg_color=HOVER_CLARO,
    button_color=FONDO_OSCURO,
    button_hover_color=HOVER_OSCURO,
    number_of_steps=100,
    from_=0,
    to=100,
    command=cambiar_volumen_vista,
)
barra_volumen.set(VOLUMEN)
barra_volumen.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
controlador.registrar_slider(barra_volumen)

# Etiqueta de porcentaje de volumen
etiqueta_porcentaje_volumen = ctk.CTkLabel(
    panel_elementos_volumen,
    width=35,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_VOLUMEN),
    text_color=TEXTO_CLARO,
    text=f"{VOLUMEN}%",
)
etiqueta_porcentaje_volumen.pack(side="left")
controlador.registrar_etiqueta(etiqueta_porcentaje_volumen)


# -----------------------------------------------------------------------------------------------
# =============================================================================s==================

# ======================================== Panel derecha ========================================

# Contenedor de panel derecho hecho con customtkinter
contenedor_derecha = ctk.CTkFrame(
    conenedor_principal,
    width=ANCHO_PANEL_DERECHA if PANEL_VISIBLE else 0,
    fg_color=FONDO_CLARO,
    corner_radius=BORDES_REDONDEADOS_PANEL,
)
contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
contenedor_derecha.pack_propagate(False)
controlador.registrar_frame(contenedor_derecha, es_ctk=True)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# Contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(bg=FONDO_CLARO)
contenedor_busqueda_ordenamiento.pack(fill="both", padx=10, pady=(10, 0))
controlador.registrar_frame(contenedor_busqueda_ordenamiento)

# Panel de busqueda y ordenamiento
panel_elementos = tk.Frame(contenedor_busqueda_ordenamiento)
panel_elementos.configure(bg=FONDO_CLARO)
panel_elementos.pack(fill="x", expand=True)
controlador.registrar_frame(panel_elementos)

# Entrada de busqueda
entrada_busqueda = ctk.CTkEntry(
    panel_elementos,
    fg_color=FONDO_CLARO,
    border_width=1,
    border_color=FONDO_OSCURO,
    font=(LETRA, TAMANIO_LETRA_ENTRADA),
    placeholder_text="Buscar cancion...",
    placeholder_text_color=TEXTO_CLARO,
    text_color=TEXTO_CLARO,
)
entrada_busqueda.pack(side=tk.LEFT, fill="x", expand=True)
controlador.registrar_entrada(entrada_busqueda)

# Opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Duración"]

# Combobox de ordenamiento
combo_ordenamiento = ctk.CTkComboBox(
    panel_elementos,
    fg_color=FONDO_CLARO,
    border_width=1,
    border_color=FONDO_OSCURO,
    button_color=FONDO_CLARO,
    button_hover_color=HOVER_CLARO,
    dropdown_fg_color=FONDO_CLARO,
    dropdown_hover_color=HOVER_CLARO,
    dropdown_text_color=TEXTO_CLARO,
    font=(LETRA, TAMANIO_LETRA_COMBOBOX),
    text_color=TEXTO_CLARO,
    values=opciones_ordenamiento,
    state="readonly",
)
combo_ordenamiento.set("Elija una opcion")
combo_ordenamiento.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_combobox(combo_ordenamiento)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de lista de canciones --------------------------------
# Contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(
    contenedor_derecha
    #   , relief="solid", borderwidth=1
)
contenedor_lista_canciones.configure(height=ALTO_TABVIEW, bg=FONDO_CLARO)
contenedor_lista_canciones.pack(fill="both", expand=True, padx=10)
contenedor_lista_canciones.pack_propagate(False)
controlador.registrar_frame(contenedor_lista_canciones)

# Lista de canciones
paginas_canciones = ctk.CTkTabview(
    contenedor_lista_canciones,
    fg_color=CLARO,
    segmented_button_fg_color=CLARO_SEGUNDARIO,
    segmented_button_selected_color=FONDO_CLARO,
    segmented_button_selected_hover_color=HOVER_CLARO,
    segmented_button_unselected_color=HOVER_CLARO,
    segmented_button_unselected_hover_color=FONDO_CLARO,
    text_color=TEXTO_CLARO,
)
paginas_canciones.pack(fill="both", expand=True)
controlador.registrar_tabview(paginas_canciones)

# Paginas de la lista de canciones
paginas_canciones.add("Canciones")
paginas_canciones.add("Álbumes")
paginas_canciones.add("Artistas")
paginas_canciones.add("Me gusta")
paginas_canciones.add("Favoritos")
paginas_canciones.add("Listas")

# Boton de prueba en canciones
tab_canciones = paginas_canciones.tab("Canciones")

# Crear canvas sin scrollbar visible
canvas_canciones = tk.Canvas(tab_canciones, bg=CLARO_SEGUNDARIO, highlightthickness=0)
canvas_canciones.pack(side="left", fill="both", expand=True)
controlador.registrar_canvas(canvas_canciones, es_tabview=True)

# Crear frame para los botones dentro del canvas
panel_botones_canciones = tk.Frame(canvas_canciones, bg=CLARO_SEGUNDARIO)
controlador.registrar_frame(panel_botones_canciones)

# Vincular eventos
panel_botones_canciones.bind("<Configure>", scroll_frame_configuracion)
canvas_canciones.bind("<Configure>", scroll_canvas_configuracion)
canvas_canciones.bind_all("<MouseWheel>", scroll_raton_configuracion)

# Crear ventana en el canvas para el frame
canvas_window = canvas_canciones.create_window((0, 0), window=panel_botones_canciones, anchor="nw")

# # Crear botones en el panel_botones_canciones
# for i in range(10):
#     boton_en_canciones = ctk.CTkButton(
#         panel_botones_canciones,
#         height=28,
#         fg_color=BOTON_CLARO,
#         font=(LETRA, TAMANIO_LETRA_BOTON),
#         text_color=TEXTO_CLARO,
#         text=f"Cancion {i + 1}",
#         hover_color=HOVER_CLARO,
#         command=lambda: print("Botón presionado"),
#     )
#     boton_en_canciones.pack(fill="both", pady=2)
#     controlador.registrar_botones(f"cancion_{i}", boton_en_canciones)


# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de botones inferiores ---------------------------------
# Contenedor de botones inferiores
contenedor_inferior = tk.Frame(contenedor_derecha)
contenedor_inferior.configure(bg=FONDO_CLARO)
contenedor_inferior.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_inferior)

# Panel de botones
panel_botones_inferiores = tk.Frame(contenedor_inferior)
panel_botones_inferiores.configure(bg=FONDO_CLARO, padx=5)
panel_botones_inferiores.pack(expand=True)
controlador.registrar_frame(panel_botones_inferiores)

# Botones inferiores
boton_agregar_cancion = ctk.CTkButton(
    panel_botones_inferiores,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Canción",
    hover_color=HOVER_CLARO,
    command=agregar_cancion_vista,
)
boton_agregar_cancion.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cancion", boton_agregar_cancion)

boton_agregar_directorio = ctk.CTkButton(
    panel_botones_inferiores,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Carpeta",
    hover_color=HOVER_CLARO,
    command=agregar_directorio_vista,
)
boton_agregar_directorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_carpeta", boton_agregar_directorio)

# -----------------------------------------------------------------------------------------------
# ===============================================================================================

# Muestre el icono del volumen actual de la barra de volumen
cambiar_volumen_vista(None)

# Actualizar los botones de la interfaz al iniciar la ejecución
actualizar_iconos()

# Mostrar la ventana
ventana_principal.mainloop()
