import tkinter as tk

# dimensiones de la interfaz en altura y ancho en pixeles
ancho = 1280
alto = 720

# letra
letra = "SF Pro Display"

# fondos

claro = "#f0f0f0"
oscuro = "#333333"

# ====================================== Ventana principal ======================================

# Crear ventana
ventana_principal = tk.Tk()

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
conenedor_principal.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
conenedor_principal.pack(fill="both", expand=True)

# etiqueta del contenedor principal
etiqueta = tk.Label(conenedor_principal, text="Contenedor principal", font=(letra, 16), bg=claro)
etiqueta.pack()

# ===============================================================================================


# ======================================= Panel izquierda =======================================

# contenedor izquierda
contenedor_izquierda = tk.Frame(conenedor_principal)
contenedor_izquierda.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_izquierda.pack(side=tk.LEFT, fill="both", expand=True)

# etiqueta izquierda
etiqueta_izquierda = tk.Label(
    contenedor_izquierda, text="Panel izquierda", font=(letra, 13), bg=claro
)
etiqueta_izquierda.pack()


# ------------------------------- Seccion de botones superiores ---------------------------------
# contenedor superior
contenedor_superior = tk.Frame(contenedor_izquierda)
contenedor_superior.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_superior.pack(pady=5, fill="both")

# etiqueta del reproductor
etiqueta = tk.Label(contenedor_superior, text="Botones superiores", font=(letra, 10), bg=claro)
etiqueta.pack(expand=True)
# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_imagen.pack(pady=5, fill="both", expand=True)

# etiqueta de imagen de la canción
etiqueta_imagen = tk.Label(
    contenedor_imagen, text="Imagen de la Canción", font=(letra, 10), bg=claro
)
etiqueta_imagen.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_informacion.pack(pady=5, fill="both")

# etiqueta de información de la canción
etiqueta_informacion = tk.Label(
    contenedor_informacion, text="Informacion cancion ", font=(letra, 10), bg=claro
)
etiqueta_informacion.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_espectro.pack(pady=5, fill="both")

# etiqueta de espectro de audio
etiqueta_espectro = tk.Label(
    contenedor_espectro, text="Espectro de Audio", font=(letra, 10), bg=claro
)
etiqueta_espectro.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de progreso ---------------------------------

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_progreso.pack(pady=5, fill="both")

# etiqueta de barra de progreso
etiqueta_progreso = tk.Label(
    contenedor_progreso, text="Barra de Progreso", font=(letra, 10), bg=claro
)
etiqueta_progreso.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_controles.pack(pady=5, fill="both")

# etiqueta de controles de reproducción
etiqueta_controles = tk.Label(
    contenedor_controles, text="Controles de Reproducción", font=(letra, 10), bg=claro
)
etiqueta_controles.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de volumen -----------------------------------

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_volumen.pack(pady=5, fill="both")

# etiqueta de barra de volumen
etiqueta_volumen = tk.Label(contenedor_volumen, text="Barra de Volumen", font=(letra, 10), bg=claro)
etiqueta_volumen.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecha
contenedor_derecha = tk.Frame(conenedor_principal)
contenedor_derecha.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, width=425)
contenedor_derecha.pack(side=tk.LEFT, fill="both", padx=(10, 0))
contenedor_derecha.pack_propagate(False)

# etiqueta de panel derecha
etiqueta_derecha = tk.Label(contenedor_derecha, text="Panel derecha", font=(letra, 13), bg=claro)
etiqueta_derecha.pack()

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_busqueda_ordenamiento.pack(pady=5, fill="both")

# etiqueta de busqueda y ordenamiento
etiqueta_busqueda_ordenamiento = tk.Label(
    contenedor_busqueda_ordenamiento, text="Busqueda y Ordenamiento", font=(letra, 10), bg=claro
)
etiqueta_busqueda_ordenamiento.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de lista de canciones --------------------------------
# contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(contenedor_derecha)
contenedor_lista_canciones.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_lista_canciones.pack(pady=5, fill="both", expand=True)

# etiqueta de lista de canciones
etiqueta_lista_canciones = tk.Label(
    contenedor_lista_canciones, text="Lista de Canciones", font=(letra, 10), bg=claro
)
etiqueta_lista_canciones.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de botones inferiores ---------------------------------
# contenedor de botones inferiores
contenedor_inferior = tk.Frame(contenedor_derecha)
contenedor_inferior.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_inferior.pack(pady=5, fill="both")

# etiqueta de botones inferiores
etiqueta_inferior = tk.Label(
    contenedor_inferior, text="Botones inferiores", font=(letra, 10), bg=claro
)
etiqueta_inferior.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# mostrar la ventana
ventana_principal.mainloop()
