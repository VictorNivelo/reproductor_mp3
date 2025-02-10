from controlador.controlador_tema import Controlador_tema
from vista.constantes import *
import customtkinter as ctk
import tkinter as tk

# FUNCIONES DE LOS BOTONES


def cambiar_tema():
    global tema_actual
    tema_actual = "oscuro" if tema_actual == "claro" else "claro"
    controlador.cambiar_tema()
    # cambiar iconos de los botones
    if tema_actual == "oscuro":
        controlador.registrar_botones("modo_claro", boton_tema)
        # estado de reproducción
        if reproduciendo:
            controlador.registrar_botones("pausa", boton_reproducir)
        else:
            controlador.registrar_botones("reproducir", boton_reproducir)
        # orden de reproducción
        if orden:
            controlador.registrar_botones("aleatorio", boton_aleatorio)
        else:
            controlador.registrar_botones("orden", boton_aleatorio)
        # repeticion de reproducción
        if repeticion == 0:
            controlador.registrar_botones("no_repetir", boton_repetir)
        elif repeticion == 1:
            controlador.registrar_botones("repetir_actual", boton_repetir)
        else:
            controlador.registrar_botones("repetir_todo", boton_repetir)
        # volumen
        if silenciado:
            controlador.registrar_botones("silencio", boton_silenciar)
        else:
            if volumen == 0:
                controlador.registrar_botones("sin_volumen", boton_silenciar)
            elif volumen <= 33:
                controlador.registrar_botones("volumen_bajo", boton_silenciar)
            elif volumen <= 66:
                controlador.registrar_botones("volumen_medio", boton_silenciar)
            else:
                controlador.registrar_botones("volumen_alto", boton_silenciar)
    else:
        controlador.registrar_botones("modo_oscuro", boton_tema)
        # estado de reproducción
        if reproduciendo:
            controlador.registrar_botones("pausa", boton_reproducir)
        else:
            controlador.registrar_botones("reproducir", boton_reproducir)
        # orden de reproducción
        if orden:
            controlador.registrar_botones("aleatorio", boton_aleatorio)
        else:
            controlador.registrar_botones("orden", boton_aleatorio)
        # repeticion de reproducción
        if repeticion == 0:
            controlador.registrar_botones("no_repetir", boton_repetir)
        elif repeticion == 1:
            controlador.registrar_botones("repetir_actual", boton_repetir)
        else:
            controlador.registrar_botones("repetir_todo", boton_repetir)
        # volumen
        if silenciado:
            controlador.registrar_botones("silencio", boton_silenciar)
        else:
            if volumen == 0:
                controlador.registrar_botones("sin_volumen", boton_silenciar)
            elif volumen <= 33:
                controlador.registrar_botones("volumen_bajo", boton_silenciar)
            elif volumen <= 66:
                controlador.registrar_botones("volumen_medio", boton_silenciar)
            else:
                controlador.registrar_botones("volumen_alto", boton_silenciar)


# Función para cambiar el estado de reproducción
def cambiar_estado_reproduccion():
    global reproduciendo
    reproduciendo = not reproduciendo
    if reproduciendo:
        controlador.registrar_botones("pausa", boton_reproducir)
    else:
        controlador.registrar_botones("reproducir", boton_reproducir)


# Función para cambiar el volumen
def cambiar_volumen(event=None):
    global volumen, silenciado
    if not silenciado:
        nuevo_volumen = int(barra_volumen.get())
        volumen = nuevo_volumen
        etiqueta_porcentaje_volumen.configure(text=f"{volumen}%")
        if volumen == 0:
            controlador.registrar_botones("sin_volumen", boton_silenciar)
        elif volumen <= 33:
            controlador.registrar_botones("volumen_bajo", boton_silenciar)
        elif volumen <= 66:
            controlador.registrar_botones("volumen_medio", boton_silenciar)
        else:
            controlador.registrar_botones("volumen_alto", boton_silenciar)


# Función para cambiar el estado de silencio
def cambiar_silencio():
    global silenciado
    silenciado = not silenciado
    if silenciado:
        controlador.registrar_botones("silencio", boton_silenciar)
    else:
        cambiar_volumen()


# Función para cambiar el orden de reproducción
def cambiar_orden():
    global orden
    orden = not orden
    if orden:
        controlador.registrar_botones("aleatorio", boton_aleatorio)
    else:
        controlador.registrar_botones("orden", boton_aleatorio)


# Función para cambiar la repetición de reproducción
def cambiar_repeticion():
    global repeticion
    repeticion = (repeticion + 1) % 3
    if repeticion == 0:
        controlador.registrar_botones("no_repetir", boton_repetir)
    elif repeticion == 1:
        controlador.registrar_botones("repetir_actual", boton_repetir)
    else:
        controlador.registrar_botones("repetir_todo", boton_repetir)


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
ventana_principal = tk.Tk()

# icono de la ventana
icono = tk.PhotoImage(file=ruta_icono_aplicacion)

# establecer el icono de la ventana
ventana_principal.iconphoto(True, icono)

# controlador de tema
controlador = Controlador_tema()

# obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()

# calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ancho) // 2
posicion_alto = (alto_pantalla - alto) // 2

# establecer la geometría de la ventana
ventana_principal.geometry(f"{ancho}x{alto}+{posicion_ancho}+{posicion_alto}")

# título de la ventana
ventana_principal.title("Reproductor de música")

# ===============================================================================================


# ==================================== Contenedor principal =====================================

# contenedor principal
conenedor_principal = tk.Frame(ventana_principal)
conenedor_principal.configure(
    bg="#%02x%02x%02x"
    % tuple(max(0, int(fondo_claro.lstrip("#")[i : i + 2], 16) - 20) for i in (0, 2, 4)),
    padx=5,
    pady=5,
)
conenedor_principal.pack(fill="both", expand=True)

# ===============================================================================================


# ======================================= Panel izquierda =======================================

# contenedor izquierda
# contenedor_izquierda = tk.Frame(conenedor_principal)
# contenedor_izquierda.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=fondo_claro)
# contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)

# contenedor izquierda con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    conenedor_principal, fg_color=fondo_claro, corner_radius=bordes_redondeados
)
contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)
controlador.registrar_frame(contenedor_izquierda, es_ctk=True)


# ------------------------------- Seccion de controles superiores --------------------------------

# contenedor superior
contenedor_superior = tk.Frame(contenedor_izquierda)
contenedor_superior.configure(bg=fondo_claro)
contenedor_superior.pack(fill="both", padx=10, pady=(10, 3))
controlador.registrar_frame(contenedor_superior)

# botones de la parte superior

boton_ajustes = ctk.CTkButton(
    contenedor_superior,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_ajustes.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("ajustes", boton_ajustes)

boton_tema = ctk.CTkButton(
    contenedor_superior,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
    command=cambiar_tema,
)
boton_tema.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("modo_oscuro", boton_tema)

boton_visibilidad = ctk.CTkButton(
    contenedor_superior,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_visibilidad.pack(side=tk.RIGHT)
controlador.registrar_botones("ocultar", boton_visibilidad)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(bg=fondo_claro)
contenedor_imagen.pack(fill="both", expand=True, padx=10, pady=3)
controlador.registrar_frame(contenedor_imagen)

# etiqueta de la imagen de la canción
imagen_cancion = ctk.CTkLabel(
    contenedor_imagen,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_volumen),
    text_color=texto_claro,
    text="Imagen de la Canción",
)
imagen_cancion.pack(expand=True)
controlador.registrar_etiqueta(imagen_cancion)


# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(bg=fondo_claro)
contenedor_informacion.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_informacion)

# etiqueta de información de la canción
etiqueta_nombre_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_etiqueta),
    text_color=texto_claro,
    text="Nombre de la Canción",
)
etiqueta_nombre_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_nombre_cancion)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_etiqueta),
    text_color=texto_claro,
    text="Artista de la Canción",
)
etiqueta_artista_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_artista_cancion)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_etiqueta),
    text_color=texto_claro,
    text="Álbum de la Canción",
)
etiqueta_album_cancion.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_album_cancion)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion botones de gustos -------------------------------------

# contenedor de botones de gustos
contenedor_botones_gustos = tk.Frame(contenedor_izquierda)
contenedor_botones_gustos.configure(bg=fondo_claro)
contenedor_botones_gustos.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_botones_gustos)

# panel de botones de gustos
panel_botones_gustos = tk.Frame(contenedor_botones_gustos)
panel_botones_gustos.configure(bg=fondo_claro)
panel_botones_gustos.pack(expand=True)
controlador.registrar_frame(panel_botones_gustos)

# botones de gustos
boton_me_gusta = ctk.CTkButton(
    panel_botones_gustos,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_me_gusta.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("me_gusta", boton_me_gusta)

boton_favorito = ctk.CTkButton(
    panel_botones_gustos,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_favorito.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("favorito", boton_favorito)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(height=90, bg=fondo_claro)
contenedor_espectro.pack(fill="both", padx=10, pady=3)
contenedor_espectro.pack_propagate(False)
controlador.registrar_frame(contenedor_espectro)

# etiqueta de espectro de audio
etiqueta_espectro = ctk.CTkLabel(
    contenedor_espectro,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_etiqueta),
    text_color=texto_claro,
    text="Espectro de Audio",
)
etiqueta_espectro.pack(expand=True)
controlador.registrar_etiqueta(etiqueta_espectro)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de progreso ---------------------------------

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(bg=fondo_claro)
contenedor_progreso.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_progreso)

# panel de progreso
panel_progreso = tk.Frame(contenedor_progreso)
panel_progreso.configure(bg=fondo_claro)
panel_progreso.pack(fill="x", expand=True)
controlador.registrar_frame(panel_progreso)

# barra de progreso
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(height=5, progress_color=fondo_oscuro, fg_color="lightgray")
barra_progreso.pack(fill="x", padx=12, pady=(5, 0))
controlador.registrar_progress_bar(barra_progreso)

# panel de tiempo
panel_tiempo = tk.Frame(contenedor_progreso)
panel_tiempo.configure(bg=fondo_claro)
panel_tiempo.pack(fill="x", expand=True)
controlador.registrar_frame(panel_tiempo)

# etiqueta de tiempo actual
etiqueta_tiempo_actual = ctk.CTkLabel(
    panel_tiempo,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_tiempo),
    text_color=texto_claro,
    text="00:00",
)
etiqueta_tiempo_actual.pack(side=tk.LEFT)
controlador.registrar_etiqueta(etiqueta_tiempo_actual)

# etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_tiempo),
    text_color=texto_claro,
    text="00:00",
)
etiqueta_tiempo_total.pack(side=tk.RIGHT)
controlador.registrar_etiqueta(etiqueta_tiempo_total)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(bg=fondo_claro)
contenedor_controles.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_controles)

# panel de controles
panel_controles = tk.Frame(contenedor_controles)
panel_controles.configure(bg=fondo_claro)
panel_controles.pack(expand=True)
controlador.registrar_frame(panel_controles)

# botones de control
boton_aleatorio = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
    command=cambiar_orden,
)
boton_aleatorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("aleatorio", boton_aleatorio)

boton_repetir = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
    command=cambiar_repeticion,
)
boton_repetir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("no_repetir", boton_repetir)

boton_retroceder = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    hover_color=hover_claro,
)
boton_retroceder.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("retroceder", boton_retroceder)

boton_anterior = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_anterior.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("anterior", boton_anterior)

boton_reproducir = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
    command=cambiar_estado_reproduccion,
)
boton_reproducir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("reproducir", boton_reproducir)

boton_siguiente = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_siguiente.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("siguiente", boton_siguiente)

boton_adelantar = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_adelantar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("adelantar", boton_adelantar)

boton_agregar_cola = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_agregar_cola.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cola", boton_agregar_cola)

boton_minimizar = ctk.CTkButton(
    panel_controles,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
)
boton_minimizar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("minimizar", boton_minimizar)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de volumen -----------------------------------

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(bg=fondo_claro)
contenedor_volumen.pack(fill="both", padx=10, pady=(7, 10))
controlador.registrar_frame(contenedor_volumen)

# panel de volumen
panel_volumen = tk.Frame(contenedor_volumen)
panel_volumen.configure(bg=fondo_claro)
panel_volumen.pack(expand=True)
controlador.registrar_frame(panel_volumen)

# botón de silenciar
boton_silenciar = ctk.CTkButton(
    panel_volumen,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="",
    hover_color=hover_claro,
    command=cambiar_silencio,
)
boton_silenciar.pack(side=tk.LEFT)
controlador.registrar_botones("silencio", boton_silenciar)

# panel de elementos de volumen
panel_elementos_volumen = tk.Frame(panel_volumen, bg=fondo_claro)
panel_elementos_volumen.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
controlador.registrar_frame(panel_elementos_volumen)

# barra de volumen
barra_volumen = ctk.CTkSlider(panel_elementos_volumen)
barra_volumen.configure(
    progress_color=fondo_oscuro,
    fg_color=hover_claro,
    button_color=fondo_oscuro,
    button_hover_color=hover_oscuro,
    number_of_steps=100,
    from_=0,
    to=100,
    command=cambiar_volumen,
)
barra_volumen.set(volumen)
barra_volumen.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
controlador.registrar_slider(barra_volumen)

# etiqueta de porcentaje de volumen
etiqueta_porcentaje_volumen = ctk.CTkLabel(
    panel_elementos_volumen,
    fg_color=fondo_claro,
    font=(letra, tamanio_letra_volumen),
    text_color=texto_claro,
    text=f"{volumen} %",
)
etiqueta_porcentaje_volumen.pack(side="left")
controlador.registrar_etiqueta(etiqueta_porcentaje_volumen)


# -----------------------------------------------------------------------------------------------


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecha
# contenedor_derecha = tk.Frame(conenedor_principal)
# contenedor_derecha.configure(
#     padx=10, pady=5, relief="solid", borderwidth=1, bg=fondo_claro, width=ancho_panel_derecha
# )
# contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
# contenedor_derecha.pack_propagate(False)

# contenedor de panel derecha con customtkinter
contenedor_derecha = ctk.CTkFrame(
    conenedor_principal,
    width=ancho_panel_derecha,
    fg_color=fondo_claro,
    corner_radius=bordes_redondeados,
)
contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
contenedor_derecha.pack_propagate(False)
controlador.registrar_frame(contenedor_derecha, es_ctk=True)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(bg=fondo_claro)
contenedor_busqueda_ordenamiento.pack(fill="both", padx=10, pady=(10, 0))
controlador.registrar_frame(contenedor_busqueda_ordenamiento)

# panel de busqueda y ordenamiento
panel_elementos = tk.Frame(contenedor_busqueda_ordenamiento)
panel_elementos.configure(bg=fondo_claro)
panel_elementos.pack(fill="x", expand=True)
controlador.registrar_frame(panel_elementos)

# entrada de busqueda
entrada_busqueda = ctk.CTkEntry(
    panel_elementos,
    fg_color=fondo_claro,
    border_width=1,
    border_color=fondo_oscuro,
    font=(letra, tamanio_letra_entrada),
    placeholder_text="Buscar cancion...",
    placeholder_text_color=texto_claro,
    text_color=texto_claro,
)
entrada_busqueda.pack(side=tk.LEFT, fill="x", expand=True)
controlador.registrar_entrada(entrada_busqueda)

# opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Duración"]

# combobox de ordenamiento
combo_ordenamiento = ctk.CTkComboBox(
    panel_elementos,
    fg_color=fondo_claro,
    border_width=1,
    border_color=fondo_oscuro,
    button_color=fondo_claro,
    button_hover_color=hover_claro,
    dropdown_fg_color=fondo_claro,
    dropdown_hover_color=hover_claro,
    dropdown_text_color=texto_claro,
    font=(letra, tamanio_letra_combobox),
    text_color=texto_claro,
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
contenedor_lista_canciones.configure(height=alto_tabview, bg=fondo_claro)
contenedor_lista_canciones.pack(fill="both", expand=True, padx=10)
contenedor_lista_canciones.pack_propagate(False)
controlador.registrar_frame(contenedor_lista_canciones)

# lista de canciones

paginas_canciones = ctk.CTkTabview(
    contenedor_lista_canciones,
    fg_color=hover_claro,
    segmented_button_fg_color=fondo_claro,
    segmented_button_selected_color=hover_claro,
    segmented_button_selected_hover_color=hover_claro,
    segmented_button_unselected_color=fondo_claro,
    segmented_button_unselected_hover_color=hover_claro,
    text_color=texto_claro,
)
paginas_canciones.pack(fill="both", expand=True)
controlador.registrar_frame(paginas_canciones, es_ctk=True)

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
canvas_canciones = tk.Canvas(tab_canciones, bg=hover_claro, highlightthickness=0)
canvas_canciones.pack(side="left", fill="both", expand=True)

# Crear frame para los botones dentro del canvas
panel_botones_canciones = tk.Frame(canvas_canciones, bg=hover_claro)

# Vincular eventos
panel_botones_canciones.bind("<Configure>", scroll_frame_configuracion)
canvas_canciones.bind("<Configure>", scroll_canvas_configuracion)
canvas_canciones.bind_all("<MouseWheel>", scroll_raton_configuracion)

# Crear ventana en el canvas para el frame
canvas_window = canvas_canciones.create_window((0, 0), window=panel_botones_canciones, anchor="nw")

# Crear botones en el panel_botones_canciones
for i in range(10):
    boton_en_canciones = ctk.CTkButton(
        panel_botones_canciones,
        fg_color=boton_claro,
        font=(letra, tamanio_letra_boton),
        text_color=texto_claro,
        text=f"Cancion {i + 1}",
        hover_color=hover_claro,
        command=lambda: print("Botón presionado"),
    )
    boton_en_canciones.pack(fill="both", pady=2)
    controlador.registrar_botones(f"cancion_{i}", boton_en_canciones)


# lista_canciones = tk.Listbox(
#     contenedor_lista_canciones,
#     font=(letra, 10),
#     bg=fondo_claro,
#     selectbackground=fondo_oscuro,
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
contenedor_inferior.configure(bg=fondo_claro)
contenedor_inferior.pack(fill="both", padx=10, pady=3)
controlador.registrar_frame(contenedor_inferior)

# panel de botones
panel_botones = tk.Frame(contenedor_inferior)
panel_botones.configure(bg=fondo_claro, padx=5)
panel_botones.pack(expand=True)
controlador.registrar_frame(panel_botones)

# botones inferiores
boton_agregar_cancion = ctk.CTkButton(
    panel_botones,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="Agregar Canción",
    hover_color=hover_claro,
)
boton_agregar_cancion.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cancion", boton_agregar_cancion)

boton_agregar_directorio = ctk.CTkButton(
    panel_botones,
    width=ancho_boton,
    height=alto_boton,
    fg_color=boton_claro,
    font=(letra, tamanio_letra_boton),
    text_color=texto_claro,
    text="Agregar Carpeta",
    hover_color=hover_claro,
)
boton_agregar_directorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_carpeta", boton_agregar_directorio)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# muestre el icono del volumen actual de la barra de volumen
cambiar_volumen(None)

# mostrar la ventana
ventana_principal.mainloop()
