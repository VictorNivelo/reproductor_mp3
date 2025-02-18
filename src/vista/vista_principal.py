from vista.componentes.mini_reproductor import MiniReproductor
from vista.componentes.configuracion import Configuracion
from controlador.controlador_tema import ControladorTema
from vista.utiles_vista import establecer_icono_tema
from vista.constantes import *
import customtkinter as ctk
import tkinter as tk
import tracemalloc
import random


# decorador para medir el consumo de memoria
def medir_consumo_memoria(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        resultado = func(*args, **kwargs)
        actual, pico = tracemalloc.get_traced_memory()
        print(f"{func.__name__} - Memoria actual: {actual / 1024:.2f} KB")
        print(f"{func.__name__} - Pico de memoria: {pico / 1024:.2f} KB")
        tracemalloc.stop()
        return resultado

    return wrapper


# FUNCIONES DE LOS BOTONES


# Función para cambiar el tema de la interfaz
def cambiar_tema():
    global TEMA_ACTUAL
    TEMA_ACTUAL = "oscuro" if TEMA_ACTUAL == "claro" else "claro"
    controlador.cambiar_tema()
    color_barra = HOVER_CLARO if TEMA_ACTUAL == "claro" else HOVER_OSCURO
    for barra in barras_espectro:
        canvas_espectro.itemconfig(barra, fill=color_barra)
    # cambiar iconos de los botones
    if TEMA_ACTUAL == "oscuro":
        controlador.registrar_botones("modo_claro", boton_tema)
        # estado de reproducción
        if REPRODUCIENDO:
            controlador.registrar_botones("pausa", boton_reproducir)
        else:
            controlador.registrar_botones("reproducir", boton_reproducir)
        # orden de reproducción
        if ORDEN:
            controlador.registrar_botones("aleatorio", boton_aleatorio)
        else:
            controlador.registrar_botones("orden", boton_aleatorio)
        # repeticion de reproducción
        if REPETICION == 0:
            controlador.registrar_botones("no_repetir", boton_repetir)
        elif REPETICION == 1:
            controlador.registrar_botones("repetir_actual", boton_repetir)
        else:
            controlador.registrar_botones("repetir_todo", boton_repetir)
        # volumen
        if SILENCIADO:
            controlador.registrar_botones("silencio", boton_silenciar)
        else:
            if VOLUMEN == 0:
                controlador.registrar_botones("sin_volumen", boton_silenciar)
            elif VOLUMEN <= 33:
                controlador.registrar_botones("volumen_bajo", boton_silenciar)
            elif VOLUMEN <= 66:
                controlador.registrar_botones("volumen_medio", boton_silenciar)
            else:
                controlador.registrar_botones("volumen_alto", boton_silenciar)
        # me gusta y favorito
        if ME_GUSTA:
            controlador.registrar_botones("me_gusta_rojo", boton_me_gusta)
        else:
            controlador.registrar_botones("me_gusta", boton_me_gusta)
        if FAVORITO:
            controlador.registrar_botones("favorito_amarillo", boton_favorito)
        else:
            controlador.registrar_botones("favorito", boton_favorito)
    else:
        cambiar_icono_tema("claro")
        controlador.registrar_botones("modo_oscuro", boton_tema)
        # estado de reproducción
        if REPRODUCIENDO:
            controlador.registrar_botones("pausa", boton_reproducir)
        else:
            controlador.registrar_botones("reproducir", boton_reproducir)
        # orden de reproducción
        if TIEMPO_ACTUAL:
            controlador.registrar_botones("aleatorio", boton_aleatorio)
        else:
            controlador.registrar_botones("orden", boton_aleatorio)
        # repeticion de reproducción
        if REPETICION == 0:
            controlador.registrar_botones("no_repetir", boton_repetir)
        elif REPETICION == 1:
            controlador.registrar_botones("repetir_actual", boton_repetir)
        else:
            controlador.registrar_botones("repetir_todo", boton_repetir)
        # volumen
        if SILENCIADO:
            controlador.registrar_botones("silencio", boton_silenciar)
        else:
            if VOLUMEN == 0:
                controlador.registrar_botones("sin_volumen", boton_silenciar)
            elif VOLUMEN <= 33:
                controlador.registrar_botones("volumen_bajo", boton_silenciar)
            elif VOLUMEN <= 66:
                controlador.registrar_botones("volumen_medio", boton_silenciar)
            else:
                controlador.registrar_botones("volumen_alto", boton_silenciar)
        # me gusta y favorito
        if ME_GUSTA:
            controlador.registrar_botones("me_gusta_rojo", boton_me_gusta)
        else:
            controlador.registrar_botones("me_gusta", boton_me_gusta)
        if FAVORITO:
            controlador.registrar_botones("favorito_amarillo", boton_favorito)
        else:
            controlador.registrar_botones("favorito", boton_favorito)


# Función para cambiar el estado de reproducción
def cambiar_estado_reproduccion():
    global REPRODUCIENDO
    REPRODUCIENDO = not REPRODUCIENDO
    if REPRODUCIENDO:
        controlador.registrar_botones("pausa", boton_reproducir)
        actualizar_espectro()
    else:
        controlador.registrar_botones("reproducir", boton_reproducir)


# Función para cambiar el volumen
def cambiar_volumen(event=None):
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
def cambiar_silencio():
    global SILENCIADO
    SILENCIADO = not SILENCIADO
    if SILENCIADO:
        controlador.registrar_botones("silencio", boton_silenciar)
    else:
        cambiar_volumen()


# Función para cambiar el orden de reproducción
def cambiar_orden():
    global ORDEN
    ORDEN = not ORDEN
    if ORDEN:
        controlador.registrar_botones("aleatorio", boton_aleatorio)
    else:
        controlador.registrar_botones("orden", boton_aleatorio)


# Función para cambiar la repetición de reproducción
def cambiar_repeticion():
    global REPETICION
    REPETICION = (REPETICION + 1) % 3
    # icono de no repetir
    if REPETICION == 0:
        controlador.registrar_botones("no_repetir", boton_repetir)
    # icono de repetir actual
    elif REPETICION == 1:
        controlador.registrar_botones("repetir_actual", boton_repetir)
    # icono de repetir todo
    else:
        controlador.registrar_botones("repetir_todo", boton_repetir)


# Función para cambiar la visibilidad del panel
def cambiar_visibilidad():
    global PANEL_VISIBLE
    PANEL_VISIBLE = not PANEL_VISIBLE
    if PANEL_VISIBLE:
        # Mostrar el panel
        contenedor_derecha.configure(width=ANCHO_PANEL_DERECHA)
        contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
        controlador.registrar_botones("ocultar", boton_visibilidad)
    else:
        # Ocultar el panel
        contenedor_derecha.pack_forget()
        contenedor_derecha.configure(width=0)
        controlador.registrar_botones("mostrar", boton_visibilidad)


# Función para cambiar el estado de boton me gusta
def cambiar_me_gusta():
    global ME_GUSTA
    ME_GUSTA = not ME_GUSTA
    if ME_GUSTA:
        controlador.registrar_botones("me_gusta_rojo", boton_me_gusta)
    else:
        controlador.registrar_botones("me_gusta", boton_me_gusta)


# Función para cambiar el estado de favorito
def cambiar_favorito():
    global FAVORITO
    FAVORITO = not FAVORITO
    if FAVORITO:
        controlador.registrar_botones("favorito_amarillo", boton_favorito)
    else:
        controlador.registrar_botones("favorito", boton_favorito)


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
            alturas_barras[i] = alturas_barras[i] * 0.7 + altura_objetivo * 0.3
            # Actualizar altura de la barra
            try:
                x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
                canvas_espectro.coords(
                    barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i]
                )
            except:
                return  # Sí hay error al actualizar, detener la animación
    # Llamar a la función nuevamente después de un delay
    if REPRODUCIENDO:
        ventana_principal.after(50, actualizar_espectro)


# Función para iniciar el arrastre del progreso de la canción
def iniciar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = True
    actualizar_progreso(event)


# Función para arrastrar el progreso de la canción
def durante_arrastre_progreso(event):
    if ARRASTRANDO_PROGRESO:
        actualizar_progreso(event)


# Función para finalizar el arrastre del progreso
def finalizar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = False
    actualizar_progreso(event)


# Función para actualizar el progreso de la canción
def actualizar_progreso(event):
    global TIEMPO_ACTUAL
    # Obtener dimensiones y calcular posición
    ancho_total = barra_progreso.winfo_width()
    posicion_relativa = max(0, min(1, event.x / ancho_total))
    # Actualizar barra de progreso
    barra_progreso.set(posicion_relativa)
    # Calcular y actualizar tiempo
    TIEMPO_ACTUAL = int(DURACION_TOTAL * posicion_relativa)
    actualizar_etiqueta_tiempo()


# Función para actualizar la etiqueta de tiempo
def actualizar_etiqueta_tiempo():
    # Convertir segundos a formato mm:ss
    minutos_actual = TIEMPO_ACTUAL // 60
    segundos_actual = TIEMPO_ACTUAL % 60
    minutos_total = DURACION_TOTAL // 60
    segundos_total = DURACION_TOTAL % 60
    # Actualizar etiquetas
    etiqueta_tiempo_actual.configure(text=f"{minutos_actual:02d}:{segundos_actual:02d}")
    etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")


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
def scroll_frame_configuracion(event):
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

    if contenido_altura > canvas_altura:
        canvas_canciones.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ====================================== Ventana principal ======================================

# Crear ventana
ventana_principal = ctk.CTk()

# apariencia de la interfaz por defecto es claro
ctk.set_appearance_mode("light")

# icono de la ventana
cambiar_icono_tema()

# controlador de tema
controlador = ControladorTema()

# mini reproductor
mini_reproductor = MiniReproductor(ventana_principal, controlador)

configuracion = Configuracion(ventana_principal, controlador)

# obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()

# calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ANCHO_PRINCIPAL) // 2
posicion_alto = (alto_pantalla - ALTO_PRINCIPAL) // 3

# establecer la geometría de la ventana
ventana_principal.geometry(f"{ANCHO_PRINCIPAL}x{ALTO_PRINCIPAL}+{posicion_ancho}+{posicion_alto}")

# título de la ventana
ventana_principal.title("Reproductor de música")

# ===============================================================================================


# ==================================== Contenedor principal =====================================

# contenedor principal
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

# contenedor izquierda
# contenedor_izquierda = tk.Frame(conenedor_principal)
# contenedor_izquierda.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=FONDO_CLARO)
# contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)

# contenedor izquierdo hecho con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    conenedor_principal, fg_color=FONDO_CLARO, corner_radius=BORDES_REDONDEADOS_PANEL
)
contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)
controlador.registrar_frame(contenedor_izquierda, es_ctk=True)


# ------------------------------- Seccion de controles superiores --------------------------------

# contenedor superior
contenedor_superior = tk.Frame(contenedor_izquierda)
contenedor_superior.configure(bg=FONDO_CLARO)
contenedor_superior.pack(fill="both", padx=10, pady=(10, 3))
controlador.registrar_frame(contenedor_superior)

# botones de la parte superior

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
    command=cambiar_tema,
)
boton_tema.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("modo_oscuro", boton_tema)

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
    command=cambiar_visibilidad,
)
boton_visibilidad.pack(side=tk.RIGHT)
controlador.registrar_botones("ocultar", boton_visibilidad)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(bg=FONDO_CLARO)
contenedor_imagen.pack(fill="both", expand=True, padx=10, pady=3)
controlador.registrar_frame(contenedor_imagen)

# etiqueta de la imagen de la canción
imagen_cancion = ctk.CTkLabel(
    contenedor_imagen,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_VOLUMEN),
    text_color=TEXTO_CLARO,
    text="Imagen de la Canción",
)
imagen_cancion.pack(expand=True)
controlador.registrar_etiqueta(imagen_cancion)


# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(bg=FONDO_CLARO)
contenedor_informacion.pack(fill="both", padx=10, pady=5)
controlador.registrar_frame(contenedor_informacion)

# etiqueta de información de la canción
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

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion botones de gustos -------------------------------------

# contenedor de botones de gustos
contenedor_botones_gustos = tk.Frame(contenedor_izquierda)
contenedor_botones_gustos.configure(bg=FONDO_CLARO)
contenedor_botones_gustos.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_botones_gustos)

# panel de botones de gustos
panel_botones_gustos = tk.Frame(contenedor_botones_gustos)
panel_botones_gustos.configure(bg=FONDO_CLARO)
panel_botones_gustos.pack(expand=True)
controlador.registrar_frame(panel_botones_gustos)

# botones de gustos
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
    command=cambiar_me_gusta,
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
    command=cambiar_favorito,
)
boton_favorito.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("favorito", boton_favorito)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
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

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(bg=FONDO_CLARO)
contenedor_progreso.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_progreso)

# panel de progreso
panel_progreso = tk.Frame(contenedor_progreso)
panel_progreso.configure(bg=FONDO_CLARO)
panel_progreso.pack(fill="x", expand=True)
controlador.registrar_frame(panel_progreso)

# barra de progreso
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(height=6, progress_color=FONDO_OSCURO, fg_color="lightgray")
barra_progreso.pack(fill="x", padx=12, pady=(0, 3))
barra_progreso.set(0)
barra_progreso.bind("<Button-1>", iniciar_arrastre_progreso)
barra_progreso.bind("<B1-Motion>", durante_arrastre_progreso)
barra_progreso.bind("<ButtonRelease-1>", finalizar_arrastre_progreso)
controlador.registrar_progress_bar(barra_progreso)

# panel de tiempo
panel_tiempo = tk.Frame(contenedor_progreso)
panel_tiempo.configure(bg=FONDO_CLARO)
panel_tiempo.pack(fill="x", expand=True)
controlador.registrar_frame(panel_tiempo)

# etiqueta de tiempo actual
etiqueta_tiempo_actual = ctk.CTkLabel(
    panel_tiempo,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_actual.pack(side=tk.LEFT)
controlador.registrar_etiqueta(etiqueta_tiempo_actual)

# etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color=FONDO_CLARO,
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_total.pack(side=tk.RIGHT)
controlador.registrar_etiqueta(etiqueta_tiempo_total)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(bg=FONDO_CLARO)
contenedor_controles.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_controles)

# panel de controles
panel_controles = tk.Frame(contenedor_controles)
panel_controles.configure(bg=FONDO_CLARO)
panel_controles.pack(expand=True)
controlador.registrar_frame(panel_controles)

# botones de control
boton_aleatorio = ctk.CTkButton(
    panel_controles,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_orden,
)
boton_aleatorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("aleatorio", boton_aleatorio)

boton_repetir = ctk.CTkButton(
    panel_controles,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_repeticion,
)
boton_repetir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("no_repetir", boton_repetir)

boton_retroceder = ctk.CTkButton(
    panel_controles,
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
    panel_controles,
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
    panel_controles,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_estado_reproduccion,
)
boton_reproducir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("reproducir", boton_reproducir)

boton_siguiente = ctk.CTkButton(
    panel_controles,
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
    panel_controles,
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
    panel_controles,
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
    panel_controles,
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

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(bg=FONDO_CLARO)
contenedor_volumen.pack(fill="both", padx=10, pady=(7, 10))
controlador.registrar_frame(contenedor_volumen)

# panel de volumen
panel_volumen = tk.Frame(contenedor_volumen)
panel_volumen.configure(bg=FONDO_CLARO)
panel_volumen.pack(expand=True)
controlador.registrar_frame(panel_volumen)

# botón de silenciar
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
    command=cambiar_silencio,
)
boton_silenciar.pack(side=tk.LEFT)
controlador.registrar_botones("silencio", boton_silenciar)

# panel de elementos de volumen
panel_elementos_volumen = tk.Frame(panel_volumen, bg=FONDO_CLARO)
panel_elementos_volumen.pack(side=tk.LEFT, fill="x", expand=True)
controlador.registrar_frame(panel_elementos_volumen)

# barra de volumen
barra_volumen = ctk.CTkSlider(panel_elementos_volumen)
barra_volumen.configure(
    progress_color=FONDO_OSCURO,
    fg_color=HOVER_CLARO,
    button_color=FONDO_OSCURO,
    button_hover_color=HOVER_OSCURO,
    number_of_steps=100,
    from_=0,
    to=100,
    command=cambiar_volumen,
)
barra_volumen.set(VOLUMEN)
barra_volumen.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
controlador.registrar_slider(barra_volumen)

# etiqueta de porcentaje de volumen
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


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecha
# contenedor_derecha = tk.Frame(conenedor_principal)
# contenedor_derecha.configure(
#     padx=10, pady=5, relief="solid", borderwidth=1, bg=FONDO_CLARO, width=ancho_panel_derecha
# )
# contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
# contenedor_derecha.pack_propagate(False)

# contenedor de panel derecho hecho con customtkinter
contenedor_derecha = ctk.CTkFrame(
    conenedor_principal,
    width=ANCHO_PANEL_DERECHA if PANEL_VISIBLE else 0,
    fg_color=FONDO_CLARO,
    corner_radius=BORDES_REDONDEADOS_PANEL,
)

# Configurar visibilidad inicial
if PANEL_VISIBLE:
    contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
    controlador.registrar_botones("ocultar", boton_visibilidad)
else:
    controlador.registrar_botones("mostrar", boton_visibilidad)

contenedor_derecha.pack_propagate(False)
controlador.registrar_frame(contenedor_derecha, es_ctk=True)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(bg=FONDO_CLARO)
contenedor_busqueda_ordenamiento.pack(fill="both", padx=10, pady=(10, 0))
controlador.registrar_frame(contenedor_busqueda_ordenamiento)

# panel de busqueda y ordenamiento
panel_elementos = tk.Frame(contenedor_busqueda_ordenamiento)
panel_elementos.configure(bg=FONDO_CLARO)
panel_elementos.pack(fill="x", expand=True)
controlador.registrar_frame(panel_elementos)

# entrada de busqueda
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

# opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Duración"]

# combobox de ordenamiento
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
# contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(
    contenedor_derecha
    #   , relief="solid", borderwidth=1
)
contenedor_lista_canciones.configure(height=ALTO_TABVIEW, bg=FONDO_CLARO)
contenedor_lista_canciones.pack(fill="both", expand=True, padx=10)
contenedor_lista_canciones.pack_propagate(False)
controlador.registrar_frame(contenedor_lista_canciones)

# lista de canciones

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

# paginas de la lista de canciones
paginas_canciones.add("Canciones")
paginas_canciones.add("Álbumes")
paginas_canciones.add("Artistas")
paginas_canciones.add("Me gusta")
paginas_canciones.add("Favoritos")
paginas_canciones.add("Listas")

# boton de prueba en canciones
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


# lista_canciones = tk.Listbox(
#     contenedor_lista_canciones,
#     font=(LETRA, 10),
#     bg=FONDO_CLARO,
#     selectbackground=FONDO_OSCURO,
# )

# # agregar canciones a la lista
# lista_canciones.insert(0, "Canción 1")
# lista_canciones.insert(1, "Canción 2")
# lista_canciones.insert(2, "Canción 3")
# lista_canciones.insert(3, "Canción 4")
# lista_canciones.insert(4, "Canción 5")

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de botones inferiores ---------------------------------
# contenedor de botones inferiores
contenedor_inferior = tk.Frame(contenedor_derecha)
contenedor_inferior.configure(bg=FONDO_CLARO)
contenedor_inferior.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_inferior)

# panel de botones
panel_botones = tk.Frame(contenedor_inferior)
panel_botones.configure(bg=FONDO_CLARO, padx=5)
panel_botones.pack(expand=True)
controlador.registrar_frame(panel_botones)

# botones inferiores
boton_agregar_cancion = ctk.CTkButton(
    panel_botones,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Canción",
    hover_color=HOVER_CLARO,
)
boton_agregar_cancion.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cancion", boton_agregar_cancion)

boton_agregar_directorio = ctk.CTkButton(
    panel_botones,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Carpeta",
    hover_color=HOVER_CLARO,
)
boton_agregar_directorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_carpeta", boton_agregar_directorio)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# muestre el icono del volumen actual de la barra de volumen
cambiar_volumen(None)

# mostrar la ventana
ventana_principal.mainloop()
