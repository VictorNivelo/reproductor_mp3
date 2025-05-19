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
ventana_principal_prototipo = tk.Tk()

# obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal_prototipo.winfo_screenwidth()
alto_pantalla = ventana_principal_prototipo.winfo_screenheight()

# calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ancho) // 2
posicion_alto = (alto_pantalla - alto) // 2

# establecer la geometría de la ventana
ventana_principal_prototipo.geometry(f"{ancho}x{alto}+{posicion_ancho}+{posicion_alto}")

# título de la ventana
ventana_principal_prototipo.title("Prototipo reproductor de música")

# ===============================================================================================


# ==================================== Contenedor principal =====================================

# contenedor principal
contenedor_principal_prototipo = tk.Frame(ventana_principal_prototipo)
contenedor_principal_prototipo.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_principal_prototipo.pack(fill="both", expand=True)

# etiqueta del contenedor principal
etiqueta = tk.Label(contenedor_principal_prototipo, text="Contenedor principal", font=(letra, 16), bg=claro)
etiqueta.pack()

# ===============================================================================================


# ======================================= Panel izquierda =======================================

# contenedor izquierdo
contenedor_izquierda_prototipo = tk.Frame(contenedor_principal_prototipo)
contenedor_izquierda_prototipo.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro)
contenedor_izquierda_prototipo.pack(side="left", fill="both", expand=True)

# etiqueta izquierda
etiqueta_izquierda_prototipo = tk.Label(
    contenedor_izquierda_prototipo, text="Panel izquierda", font=(letra, 13), bg=claro
)
etiqueta_izquierda_prototipo.pack()


# ------------------------------- Seccion de botones superiores ---------------------------------
# contenedor superior
contenedor_superior_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_superior_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_superior_prototipo.pack(pady=5, fill="both")

# etiqueta del reproductor
etiqueta_prototipo = tk.Label(
    contenedor_superior_prototipo, text="Botones superiores", font=(letra, 10), bg=claro
)
etiqueta_prototipo.pack(expand=True)
# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de imagen de la canción -------------------------------

# contenedor de imagen de la canción
contenedor_imagen_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_imagen_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_imagen_prototipo.pack(pady=5, fill="both", expand=True)

# etiqueta de imagen de la canción
etiqueta_imagen = tk.Label(
    contenedor_imagen_prototipo, text="Imagen de la Canción", font=(letra, 10), bg=claro
)
etiqueta_imagen.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ----------------------------- Seccion de información de la canción ----------------------------
# contenedor de información de la canción
contenedor_informacion_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_informacion_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_informacion_prototipo.pack(pady=5, fill="both")

# etiqueta de información de la canción
etiqueta_informacion_prototipo = tk.Label(
    contenedor_informacion_prototipo, text="Informacion cancion ", font=(letra, 10), bg=claro
)
etiqueta_informacion_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de espectro de audio ----------------------------------
# contenedor de espectro de audio
contenedor_espectro_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_espectro_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_espectro_prototipo.pack(pady=5, fill="both")

# etiqueta de espectro de audio
etiqueta_espectro_prototipo = tk.Label(
    contenedor_espectro_prototipo, text="Espectro de Audio", font=(letra, 10), bg=claro
)
etiqueta_espectro_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de progreso ---------------------------------

# contenedor de barra de progreso
contenedor_progreso_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_progreso_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_progreso_prototipo.pack(pady=5, fill="both")

# etiqueta de barra de progreso
etiqueta_progreso_prototipo = tk.Label(
    contenedor_progreso_prototipo, text="Barra de Progreso", font=(letra, 10), bg=claro
)
etiqueta_progreso_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de controles de reproducción --------------------------

# contenedor de controles de reproducción
contenedor_controles_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_controles_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_controles_prototipo.pack(pady=5, fill="both")

# etiqueta de controles de reproducción
etiqueta_controles_prototipo = tk.Label(
    contenedor_controles_prototipo, text="Controles de Reproducción", font=(letra, 10), bg=claro
)
etiqueta_controles_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de barra de volumen -----------------------------------

# contenedor de barra de volumen
contenedor_volumen_prototipo = tk.Frame(contenedor_izquierda_prototipo)
contenedor_volumen_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_volumen_prototipo.pack(pady=5, fill="both")

# etiqueta de barra de volumen
etiqueta_volumen_prototipo = tk.Label(
    contenedor_volumen_prototipo, text="Barra de Volumen", font=(letra, 10), bg=claro
)
etiqueta_volumen_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================


# ======================================== Panel derecha ========================================

# contenedor de panel derecho
contenedor_derecha_prototipo = tk.Frame(contenedor_principal_prototipo)
contenedor_derecha_prototipo.configure(padx=10, pady=5, relief="solid", borderwidth=1, bg=claro, width=425)
contenedor_derecha_prototipo.pack(side="left", fill="both", padx=(10, 0))
contenedor_derecha_prototipo.pack_propagate(False)

# etiqueta de panel derecha
etiqueta_derecha_prototipo = tk.Label(
    contenedor_derecha_prototipo, text="Panel derecha", font=(letra, 13), bg=claro
)
etiqueta_derecha_prototipo.pack()

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento_prototipo = tk.Frame(contenedor_derecha_prototipo)
contenedor_busqueda_ordenamiento_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_busqueda_ordenamiento_prototipo.pack(pady=5, fill="both")

# etiqueta de busqueda y ordenamiento
etiqueta_busqueda_ordenamiento_prototipo = tk.Label(
    contenedor_busqueda_ordenamiento_prototipo,
    text="Busqueda y Ordenamiento",
    font=(letra, 10),
    bg=claro,
)
etiqueta_busqueda_ordenamiento_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de lista de canciones --------------------------------
# contenedor de lista de canciones
contenedor_lista_canciones_prototipo = tk.Frame(contenedor_derecha_prototipo)
contenedor_lista_canciones_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_lista_canciones_prototipo.pack(pady=5, fill="both", expand=True)

# etiqueta de lista de canciones
etiqueta_lista_canciones_prototipo = tk.Label(
    contenedor_lista_canciones_prototipo, text="Lista de Canciones", font=(letra, 10), bg=claro
)
etiqueta_lista_canciones_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ------------------------------- Seccion de botones inferiores ---------------------------------
# contenedor de botones inferiores
contenedor_inferior_prototipo = tk.Frame(contenedor_derecha_prototipo)
contenedor_inferior_prototipo.configure(padx=10, relief="solid", borderwidth=1, bg=claro)
contenedor_inferior_prototipo.pack(pady=5, fill="both")

# etiqueta de botones inferiores
etiqueta_inferior_prototipo = tk.Label(
    contenedor_inferior_prototipo, text="Botones inferiores", font=(letra, 10), bg=claro
)
etiqueta_inferior_prototipo.pack(expand=True)

# -----------------------------------------------------------------------------------------------


# ===============================================================================================

# mostrar la ventana
ventana_principal_prototipo.mainloop()
