import tkinter as tk

# Crear ventana
ventana_principal = tk.Tk()

# dimensiones de la interfaz en altura y ancho en pixeles
ancho = 1280
alto = 720

# letra
letra = "SF Pro Display"

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

# contenedor superior
contenedor_superior = tk.Frame(ventana_principal)
contenedor_superior.configure(relief="solid", borderwidth=1)
contenedor_superior.pack()

# etiqueta del reproductor
etiqueta = tk.Label(contenedor_superior, text="Botones superiores", font=(letra, 25))
etiqueta.pack()

# contenedor principal
conenedor_principal = tk.Frame(ventana_principal)
conenedor_principal.configure(padx=10, pady=10, relief="solid", borderwidth=1)
conenedor_principal.pack()

# etiqueta del contenedor principal
etiqueta = tk.Label(conenedor_principal, text="Contenedor principal", font=(letra, 15))
etiqueta.pack()

# contenedor izquierda
contenedor_izquierda = tk.Frame(conenedor_principal)
contenedor_izquierda.configure(relief="solid", borderwidth=1)
contenedor_izquierda.pack(side=tk.LEFT, padx=5)

# etiqueta izquierda
etiqueta_izquierda = tk.Label(contenedor_izquierda, text="Panel izquierda", font=(letra, 15))
etiqueta_izquierda.pack()

# contenedor de imagen de la canción
contenedor_imagen = tk.Frame(contenedor_izquierda)
contenedor_imagen.configure(relief="solid", borderwidth=1)
contenedor_imagen.pack()

# etiqueta de imagen de la canción
etiqueta_imagen = tk.Label(contenedor_imagen, text="Imagen de la Canción", font=(letra, 15))
etiqueta_imagen.pack()

# contenedor de información de la canción
contenedor_informacion = tk.Frame(contenedor_izquierda)
contenedor_informacion.configure(relief="solid", borderwidth=1)
contenedor_informacion.pack()

# etiqueta de información de la canción
etiqueta_informacion = tk.Label(
    contenedor_informacion, text="Informacion cancion ", font=(letra, 15)
)
etiqueta_informacion.pack()

# contenedor de espectro de audio
contenedor_espectro = tk.Frame(contenedor_izquierda)
contenedor_espectro.configure(relief="solid", borderwidth=1)
contenedor_espectro.pack()

# etiqueta de espectro de audio
etiqueta_espectro = tk.Label(contenedor_espectro, text="Espectro de Audio", font=(letra, 15))
etiqueta_espectro.pack()

# contenedor de barra de progreso
contenedor_progreso = tk.Frame(contenedor_izquierda)
contenedor_progreso.configure(relief="solid", borderwidth=1)
contenedor_progreso.pack()

# etiqueta de barra de progreso
etiqueta_progreso = tk.Label(contenedor_progreso, text="Barra de Progreso", font=(letra, 15))
etiqueta_progreso.pack()

# contenedor de controles de reproducción
contenedor_controles = tk.Frame(contenedor_izquierda)
contenedor_controles.configure(relief="solid", borderwidth=1)
contenedor_controles.pack()

# etiqueta de controles de reproducción
etiqueta_controles = tk.Label(
    contenedor_controles, text="Controles de Reproducción", font=(letra, 15)
)
etiqueta_controles.pack()

# contenedor de barra de volumen
contenedor_volumen = tk.Frame(contenedor_izquierda)
contenedor_volumen.configure(relief="solid", borderwidth=1)
contenedor_volumen.pack()

# etiqueta de barra de volumen
etiqueta_volumen = tk.Label(contenedor_volumen, text="Barra de Volumen", font=(letra, 15))
etiqueta_volumen.pack()

# contenedor de panel lateral
contenedor_derecha = tk.Frame(conenedor_principal)
contenedor_derecha.configure(relief="solid", borderwidth=1)
contenedor_derecha.pack(side=tk.LEFT, padx=5)

# etiqueta de panel lateral
etiqueta_derecha = tk.Label(contenedor_derecha, text="Panel derecha", font=(letra, 15))
etiqueta_derecha.pack()

# contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = tk.Frame(contenedor_derecha)
contenedor_busqueda_ordenamiento.configure(relief="solid", borderwidth=1)
contenedor_busqueda_ordenamiento.pack()

# etiqueta de busqueda y ordenamiento
etiqueta_busqueda_ordenamiento = tk.Label(
    contenedor_busqueda_ordenamiento, text="Busqueda y Ordenamiento", font=(letra, 15)
)
etiqueta_busqueda_ordenamiento.pack()

# contenedor de lista de canciones
contenedor_lista_canciones = tk.Frame(contenedor_derecha)
contenedor_lista_canciones.configure(relief="solid", borderwidth=1)
contenedor_lista_canciones.pack()

# etiqueta de lista de canciones
etiqueta_lista_canciones = tk.Label(
    contenedor_lista_canciones, text="Lista de Canciones", font=(letra, 15)
)
etiqueta_lista_canciones.pack()

# contenedor de botones inferiores
contenedor_inferior = tk.Frame(contenedor_derecha)
contenedor_inferior.configure(relief="solid", borderwidth=1)
contenedor_inferior.pack()

# etiqueta de botones inferiores
etiqueta_inferior = tk.Label(contenedor_inferior, text="Botones inferiores", font=(letra, 15))
etiqueta_inferior.pack()

# mostrar la ventana
ventana_principal.mainloop()
