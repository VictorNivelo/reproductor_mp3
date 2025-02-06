from controlador.controlador_tema import Controlador_tema
import customtkinter as ctk
import tkinter as tk
import os

# ruta de los iconos
ruta_iconos = os.path.join("recursos", "iconos")

# dimensiones de la interfaz en altura y ancho en pixeles
ancho = 1280
alto = 720

# letra
letra = "SF Pro Display"

# tamaños de letra
tamanio_letra_tiempo = 12
tamanio_letra_boton = 12
tamanio_letra_entrada = 12.5
tamanio_letra_combobox = 12.5
tamanio_letra_etiqueta = 13
tamanio_letra_volumen = 13

# tema inicial establecido como claro
tema_inicial = "claro"

# fondos
claro = "#f0f0f0"
oscuro = "#333333"
claro_secundario = "#ffffff"
oscuro_secundario = "#2c2c2c"

# textos
claro_texto = "#000000"
oscuro_texto = "#ffffff"

# colores de botones
claro_boton = "#c0c0c0"
oscuro_boton = "#333333"

# hovers
claro_hover = "#e0e0e0"
oscuro_hover = "#2c2c2c"

# tamaño botones
ancho_boton = 20
alto_boton = 20

# tamaño panel derecha
ancho_panel_derecha = 450

# FUNCIONES DE LOS BOTONES


# llama a la función cambiar_tema del controlador
def cambiar_tema():
    controlador.cambiar_tema()


# ====================================== Ventana principal ======================================

# Crear ventana
ventana_principal = tk.Tk()

# icono de la ventana
icono = tk.PhotoImage(file=os.path.join(ruta_iconos, "reproductor.png"))

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
    padx=5,
    pady=5,
    bg="#%02x%02x%02x"
    % tuple(max(0, int(claro.lstrip("#")[i : i + 2], 16) - 20) for i in (0, 2, 4)),
)
conenedor_principal.pack(fill="both", expand=True)

# ===============================================================================================


# ======================================= Panel izquierda =======================================

# contenedor izquierda
contenedor_izquierda = tk.Frame(conenedor_principal)
contenedor_izquierda.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)

# ------------------------------- Seccion de controles superiores --------------------------------

# contenedor superior
contenedor_superior = tk.Frame(contenedor_izquierda)
contenedor_superior.configure(padx=5, pady=5, bg=claro)
contenedor_superior.pack(pady=5, fill="both")

# botones de la parte superior

boton_ajustes = ctk.CTkButton(
    contenedor_superior,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_ajustes.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("ajustes", boton_ajustes)

boton_tema = ctk.CTkButton(
    contenedor_superior,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
    command=cambiar_tema,
)
boton_tema.pack(side=tk.RIGHT, padx=(5, 0))
controlador.registrar_botones("modo_oscuro", boton_tema)

boton_visibilidad = ctk.CTkButton(
    contenedor_superior,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_visibilidad.pack(side=tk.RIGHT)
controlador.registrar_botones("ocultar", boton_visibilidad)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_imagen.pack(pady=5, fill="both", expand=True)

# etiqueta de la imagen de la canción
imagen_cancion = ctk.CTkLabel(
    contenedor_imagen,
    fg_color=claro,
    text="Imagen de la Canción",
    font=(letra, tamanio_letra_volumen),
    text_color=claro_texto,
)
imagen_cancion.pack(expand=True)


# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(padx=10, pady=5, bg=claro)
contenedor_informacion.pack(fill="both")

# etiqueta de información de la canción
etiqueta_nombre_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=claro,
    text="Nombre de la Canción",
    font=(letra, tamanio_letra_etiqueta),
    text_color=claro_texto,
)
etiqueta_nombre_cancion.pack(expand=True)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=claro,
    text="Artista de la Canción",
    font=(letra, tamanio_letra_etiqueta),
    text_color=claro_texto,
)
etiqueta_artista_cancion.pack(expand=True)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    fg_color=claro,
    text="Álbum de la Canción",
    font=(letra, tamanio_letra_etiqueta),
    text_color=claro_texto,
)
etiqueta_album_cancion.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion botones de gustos -------------------------------------

# contenedor de botones de gustos
contenedor_botones_gustos = tk.Frame(contenedor_izquierda)
contenedor_botones_gustos.configure(padx=10, bg=claro)
contenedor_botones_gustos.pack(pady=5, fill="both")

# panel de botones de gustos
panel_botones_gustos = tk.Frame(contenedor_botones_gustos)
panel_botones_gustos.configure(bg=claro)
panel_botones_gustos.pack(expand=True)

# botones de gustos
boton_me_gusta = ctk.CTkButton(
    panel_botones_gustos,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_me_gusta.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("me_gusta", boton_me_gusta)

boton_favorito = ctk.CTkButton(
    panel_botones_gustos,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_favorito.pack(side=tk.LEFT, padx=(5, 0))
controlador.registrar_botones("favorito", boton_favorito)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, height=90)
contenedor_espectro.pack(pady=5, fill="both")
contenedor_espectro.pack_propagate(False)

# etiqueta de espectro de audio
etiqueta_espectro = ctk.CTkLabel(
    contenedor_espectro,
    fg_color=claro,
    text="Espectro de Audio",
    font=(letra, tamanio_letra_etiqueta),
    text_color=claro_texto,
)

etiqueta_espectro.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de progreso ---------------------------------

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(padx=10, bg=claro)
contenedor_progreso.pack(pady=5, fill="both")

# panel de progreso
panel_progreso = tk.Frame(contenedor_progreso)
panel_progreso.configure(bg=claro)
panel_progreso.pack(expand=True, fill="x")

# barra de progreso
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(progress_color=oscuro, fg_color="lightgray", height=5)
barra_progreso.pack(pady=3, fill="x")

# panel de tiempo
panel_tiempo = tk.Frame(contenedor_progreso)
panel_tiempo.configure(bg=claro)
panel_tiempo.pack(expand=True, fill="x")

# etiqueta de tiempo actual
etiqueta_tiempo_actual = ctk.CTkLabel(
    panel_tiempo,
    fg_color=claro,
    text="00:00",
    font=(letra, tamanio_letra_tiempo),
    text_color=claro_texto,
)
etiqueta_tiempo_actual.pack(side=tk.LEFT)

# etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color=claro,
    text="00:00",
    font=(letra, tamanio_letra_tiempo),
    text_color=claro_texto,
)
etiqueta_tiempo_total.pack(side=tk.RIGHT)


# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(padx=10, bg=claro)
contenedor_controles.pack(fill="both")

# panel de controles
panel_controles = tk.Frame(contenedor_controles)
panel_controles.configure(bg=claro)
panel_controles.pack(expand=True)

# botones de control
boton_aleatorio = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_aleatorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("aleatorio", boton_aleatorio)

boton_repetir = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_repetir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("no_repetir", boton_repetir)

boton_retroceder = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_retroceder.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("retroceder", boton_retroceder)

boton_anterior = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_anterior.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("anterior", boton_anterior)

boton_reproducir = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_reproducir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("reproducir", boton_reproducir)

boton_siguiente = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_siguiente.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("siguiente", boton_siguiente)

boton_adelantar = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_adelantar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("adelantar", boton_adelantar)

boton_agregar_cola = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_agregar_cola.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cola", boton_agregar_cola)

boton_minimizar = ctk.CTkButton(
    panel_controles,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_minimizar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("minimizar", boton_minimizar)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de volumen -----------------------------------

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(padx=10, pady=5, bg=claro)
contenedor_volumen.pack(pady=5, fill="both")

# panel de volumen
panel_volumen = tk.Frame(contenedor_volumen)
panel_volumen.configure(bg=claro)
panel_volumen.pack(expand=True)

# botón de silenciar
boton_silenciar = ctk.CTkButton(
    panel_volumen,
    text="",
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_silenciar.pack(side=tk.LEFT)
controlador.registrar_botones("silencio", boton_silenciar)

# panel de elementos de volumen
panel_elementos_volumen = tk.Frame(panel_volumen, bg=claro)
panel_elementos_volumen.pack(side=tk.LEFT, expand=True, fill="x", padx=5)

# barra de volumen
barra_volumen = ctk.CTkSlider(panel_elementos_volumen)
barra_volumen.configure(
    progress_color=oscuro,
    fg_color="lightgray",
    button_color=oscuro,
    button_hover_color=oscuro_hover,
    number_of_steps=100,
)
barra_volumen.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 5))

# etiqueta de porcentaje de volumen
etiqueta_porcentaje_volumen = ctk.CTkLabel(
    panel_elementos_volumen,
    fg_color=claro,
    text="50%",
    font=(letra, tamanio_letra_volumen),
    text_color=claro_texto,
)
etiqueta_porcentaje_volumen.pack(side="left")


# -----------------------------------------------------------------------------------------------


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecha
contenedor_derecha = tk.Frame(conenedor_principal)
contenedor_derecha.configure(
    padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, width=ancho_panel_derecha
)
contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(5, 0))
contenedor_derecha.pack_propagate(False)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(pady=5, bg=claro)
contenedor_busqueda_ordenamiento.pack(fill="both")

# panel de busqueda y ordenamiento
panel_elementos = tk.Frame(contenedor_busqueda_ordenamiento)
panel_elementos.configure(bg=claro)
panel_elementos.pack(fill="x", expand=True)

# entrada de busqueda
entrada_busqueda = ctk.CTkEntry(
    panel_elementos,
    placeholder_text="Buscar cancion...",
    placeholder_text_color=claro_texto,
    font=(letra, tamanio_letra_entrada),
    text_color=claro_texto,
    fg_color=claro,
    border_color=oscuro,
    border_width=1,
)
entrada_busqueda.pack(side=tk.LEFT, fill="x", expand=True)

# opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Duración"]

# combobox de ordenamiento
combo_ordenamiento = ctk.CTkComboBox(
    panel_elementos,
    text_color=claro_texto,
    values=opciones_ordenamiento,
    font=(letra, tamanio_letra_combobox),
    fg_color=claro,
    border_color=oscuro,
    border_width=1,
    button_color=claro_boton,
    button_hover_color=claro_hover,
    dropdown_fg_color=claro,
    dropdown_hover_color=claro_hover,
    dropdown_text_color=claro_texto,
    state="readonly",
)
combo_ordenamiento.set("Elija una opcion")
combo_ordenamiento.pack(side=tk.LEFT, padx=(5, 0))

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de lista de canciones --------------------------------
# contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(contenedor_derecha)
contenedor_lista_canciones.configure(bg=claro)
contenedor_lista_canciones.pack(fill="both", expand=True)

# lista de canciones

paginas_canciones = ctk.CTkTabview(
    contenedor_lista_canciones,
    fg_color=claro_hover,
    segmented_button_fg_color=claro,
    segmented_button_selected_color=claro_hover,
    segmented_button_selected_hover_color=claro_hover,
    segmented_button_unselected_color=claro,
    segmented_button_unselected_hover_color=claro_hover,
    text_color=claro_texto,
)
paginas_canciones.pack(fill="both", expand=True)

paginas_canciones.add("Canciones")
paginas_canciones.add("Álbumes")
paginas_canciones.add("Artistas")
paginas_canciones.add("Me gusta")
paginas_canciones.add("Favoritos")
paginas_canciones.add("Listas")


# lista_canciones = tk.Listbox(
#     contenedor_lista_canciones,
#     font=(letra, 10),
#     bg=claro,
#     selectbackground=oscuro,
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
contenedor_inferior.configure(padx=10, bg=claro)
contenedor_inferior.pack(pady=5, fill="both")

# panel de botones
panel_botones = tk.Frame(contenedor_inferior)
panel_botones.configure(bg=claro)
panel_botones.pack(expand=True)

# botones inferiores
boton_agregar_cancion = ctk.CTkButton(
    panel_botones,
    text="Agregar Canción",
    text_color=claro_texto,
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_agregar_cancion.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cancion", boton_agregar_cancion)

boton_agregar_directorio = ctk.CTkButton(
    panel_botones,
    text="Agregar Carpeta",
    text_color=claro_texto,
    font=(letra, tamanio_letra_boton),
    width=ancho_boton,
    height=alto_boton,
    fg_color=claro_boton,
    hover_color=claro_hover,
)
boton_agregar_directorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_carpeta", boton_agregar_directorio)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# mostrar la ventana
ventana_principal.mainloop()
