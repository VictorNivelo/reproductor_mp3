from controlador.controlador_tema import Controlador_tema
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk


# dimensiones de la interfaz en altura y ancho en pixeles
ancho = 1280
alto = 720

# letra
letra = "SF Pro Display"

# fondos
claro = "#f0f0f0"
oscuro = "#333333"

# tema inicial establecido como claro
tema_inicial = "claro"


# llama a la función cambiar_tema del controlador
def cambiar_tema():
    controlador.cambiar_tema()


# ====================================== Ventana principal ======================================

# Crear ventana
ventana_principal = tk.Tk()

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
ventana_principal.title("Prototipo reproductor de música")

# ===============================================================================================


# ==================================== Contenedor principal =====================================

# contenedor principal
conenedor_principal = tk.Frame(ventana_principal)
conenedor_principal.configure(
    padx=10,
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
contenedor_superior.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_superior.pack(pady=5, fill="both")

# botones de la parte superior
boton_ajustes = tk.Button(contenedor_superior, text="", font=(letra, 10), bg=claro)
boton_ajustes.pack(side=tk.RIGHT)
controlador.registrar_botones("ajustes", boton_ajustes)

boton_tema = tk.Button(
    contenedor_superior, text="", font=(letra, 10), bg=claro, command=cambiar_tema
)
boton_tema.pack(side=tk.RIGHT)
controlador.registrar_botones("modo_oscuro", boton_tema)

boton_visibilidad = tk.Button(contenedor_superior, text="", font=(letra, 10), bg=claro)
boton_visibilidad.pack(side=tk.RIGHT)
controlador.registrar_botones("ocultar", boton_visibilidad)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_imagen.pack(pady=5, fill="both", expand=True)

# etiqueta de la imagen de la canción
etiqueta_imagen = tk.Label(
    contenedor_imagen, text="Imagen de la Canción", font=(letra, 10), bg=claro
)
etiqueta_imagen.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_informacion.pack(pady=5, fill="both")

# etiqueta de información de la canción
etiqueta_nombre_cancion = tk.Label(
    contenedor_informacion, text="Nombre de la Canción", font=(letra, 10), bg=claro
)
etiqueta_nombre_cancion.pack(expand=True)

etiqueta_artista_cancion = tk.Label(
    contenedor_informacion, text="Artista de la Canción", font=(letra, 10), bg=claro
)
etiqueta_artista_cancion.pack(expand=True)

etiqueta_album_cancion = tk.Label(
    contenedor_informacion, text="Álbum de la Canción", font=(letra, 10), bg=claro
)
etiqueta_album_cancion.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion botones de gustos -------------------------------------

# contenedor de botones de gustos
contenedor_botones_gustos = tk.Frame(contenedor_izquierda)
contenedor_botones_gustos.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_botones_gustos.pack(pady=5, fill="both")

# panel de botones de gustos
panel_botones_gustos = tk.Frame(contenedor_botones_gustos)
panel_botones_gustos.configure(bg=claro)
panel_botones_gustos.pack(expand=True)

# botones de gustos
boton_me_gusta = tk.Button(panel_botones_gustos, text="", font=(letra, 10), bg=claro)
boton_me_gusta.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("me_gusta", boton_me_gusta)

boton_favorito = tk.Button(panel_botones_gustos, text="", font=(letra, 10), bg=claro)
boton_favorito.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("favorito", boton_favorito)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, height=90)
contenedor_espectro.pack(pady=5, fill="both")
contenedor_espectro.pack_propagate(False)

# etiqueta de espectro de audio
etiqueta_espectro = tk.Label(
    contenedor_espectro, text="Espectro de Audio", font=(letra, 10), bg=claro
)
etiqueta_espectro.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de progreso ---------------------------------

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_progreso.pack(pady=5, fill="both")

# panel de progreso
panel_progreso = tk.Frame(contenedor_progreso)
panel_progreso.configure(bg=claro)
panel_progreso.pack(expand=True, fill="x")

# barra de progreso
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(progress_color="black", fg_color="lightgray")
barra_progreso.pack(padx=10, pady=5, fill="x")

# panel de tiempo
panel_tiempo = tk.Frame(contenedor_progreso)
panel_tiempo.configure(bg=claro)
panel_tiempo.pack(expand=True, fill="x")

# etiqueta de tiempo actual
etiqueta_tiempo_actual = tk.Label(panel_tiempo, text="00:00", font=(letra, 9), bg=claro)
etiqueta_tiempo_actual.pack(side=tk.LEFT)

# etiqueta de tiempo total
etiqueta_tiempo_total = tk.Label(panel_tiempo, text="00:00", font=(letra, 9), bg=claro)
etiqueta_tiempo_total.pack(side=tk.RIGHT)

# # barra de progreso
# barra_progreso = tk.Scale(
#     panel_progreso,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     bg=claro,
#     highlightthickness=0,
#     sliderrelief="flat",
# )
# barra_progreso.set(0)
# barra_progreso.pack(pady=5, fill="x", padx=10)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_controles.pack(pady=5, fill="both")

# panel de controles
panel_controles = tk.Frame(contenedor_controles)
panel_controles.configure(bg=claro)
panel_controles.pack(expand=True)

# botones de control
boton_aleatorio = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_aleatorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("aleatorio", boton_aleatorio)

boton_repetir = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_repetir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("no_repetir", boton_repetir)

boton_retroceder = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_retroceder.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("retroceder", boton_retroceder)

boton_anterior = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_anterior.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("anterior", boton_anterior)

boton_reproducir = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_reproducir.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("reproducir", boton_reproducir)

boton_siguiente = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_siguiente.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("siguiente", boton_siguiente)

boton_adelantar = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_adelantar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("adelantar", boton_adelantar)

boton_agregar_cola = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_agregar_cola.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cola", boton_agregar_cola)

boton_minimizar = tk.Button(panel_controles, text="", font=(letra, 10), bg=claro)
boton_minimizar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("minimizar", boton_minimizar)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de volumen -----------------------------------

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_volumen.pack(pady=5, fill="both")

# panel de volumen
panel_volumen = tk.Frame(contenedor_volumen)
panel_volumen.configure(bg=claro)
panel_volumen.pack(expand=True)

# botón de silenciar
boton_silenciar = tk.Button(panel_volumen, text="", font=(letra, 10), bg=claro)
boton_silenciar.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("silencio", boton_silenciar)

# panel de elementos de volumen
panel_elementos_volumen = tk.Frame(panel_volumen, bg=claro)
panel_elementos_volumen.pack(side=tk.LEFT, expand=True, fill="x", padx=5)

# barra de volumen
barra_volumen = ctk.CTkProgressBar(panel_elementos_volumen)
barra_volumen.configure(progress_color="black", fg_color="lightgray")
barra_volumen.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 5))

# etiqueta de porcentaje de volumen
etiqueta_porcentaje_volumen = tk.Label(
    panel_elementos_volumen, text="50%", font=(letra, 10), bg=claro
)
etiqueta_porcentaje_volumen.pack(side=tk.LEFT)


# # barra de volumen
# barra_volumen = tk.Scale(
#     panel_volumen,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=200,
#     bg=claro,
#     highlightthickness=0,
#     sliderrelief="flat",
# )
# barra_volumen.set(50)
# barra_volumen.pack(pady=5)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecha
contenedor_derecha = tk.Frame(conenedor_principal)
contenedor_derecha.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, width=425)
contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(10, 0))
contenedor_derecha.pack_propagate(False)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_busqueda_ordenamiento.pack(pady=5, fill="both")

# panel de busqueda y ordenamiento
panel_elementos = tk.Frame(contenedor_busqueda_ordenamiento)
panel_elementos.configure(bg=claro)
panel_elementos.pack(expand=True)

# entrada de busqueda
entrada_busqueda = tk.Entry(panel_elementos, font=(letra, 10), bg=claro)
entrada_busqueda.pack(side=tk.LEFT, fill="x", expand=True)

# opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Duración"]

# combobox de ordenamiento
combo_ordenamiento = ttk.Combobox(
    panel_elementos, values=opciones_ordenamiento, font=(letra, 10), state="readonly"
)
combo_ordenamiento.set("Nombre")
combo_ordenamiento.pack(side=tk.LEFT, padx=5)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de lista de canciones --------------------------------
# contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(contenedor_derecha)
contenedor_lista_canciones.configure(relief="solid", borderwidth=1, bg=claro)
contenedor_lista_canciones.pack(pady=5, fill="both", expand=True)

# lista de canciones
lista_canciones = tk.Listbox(
    contenedor_lista_canciones,
    font=(letra, 10),
    bg=claro,
    selectbackground=oscuro,
)

# agregar canciones a la lista
lista_canciones.insert(0, "Canción 1")
lista_canciones.insert(1, "Canción 2")
lista_canciones.insert(2, "Canción 3")
lista_canciones.insert(3, "Canción 4")
lista_canciones.insert(4, "Canción 5")

lista_canciones.pack(fill="both", expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de botones inferiores ---------------------------------
# contenedor de botones inferiores
contenedor_inferior = tk.Frame(contenedor_derecha)
contenedor_inferior.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_inferior.pack(pady=5, fill="both")

# panel de botones
panel_botones = tk.Frame(contenedor_inferior)
panel_botones.configure(bg=claro)
panel_botones.pack(expand=True)

# botones inferiores
boton_agregar_cancion = tk.Button(panel_botones, text="Agregar cancion", font=(letra, 10), bg=claro)
boton_agregar_cancion.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_cancion", boton_agregar_cancion)

boton_agregar_directorio = tk.Button(
    panel_botones, text="Agregar Directorio", font=(letra, 10), bg=claro
)
boton_agregar_directorio.pack(side=tk.LEFT, padx=5)
controlador.registrar_botones("agregar_carpeta", boton_agregar_directorio)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# mostrar la ventana
ventana_principal.mainloop()
