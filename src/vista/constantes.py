import os

# ======================== constantes de la vista ========================
# tamaño de la pantalla
ancho = 1280
alto = 720

# tamaño panel derecha
ancho_panel_derecha = 435

# tamaño altura tabview
alto_tabview = 400

# tamaño de los botones
ancho_boton = 20
alto_boton = 20

# bordes redondeados
bordes_redondeados = 10

# ========================================================================

# ========================= ruta de los recursos =========================
# ruta base del proyecto
ruta_base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# ruta de los recursos
ruta_recursos = os.path.join(ruta_base, "recursos")
ruta_iconos = os.path.join(ruta_recursos, "iconos")
ruta_imagenes = os.path.join(ruta_recursos, "imagenes")

# rutas del icono de la aplicación
ruta_icono_aplicacion = os.path.join(ruta_iconos, "reproductor.png")

# ========================================================================

# ========================== colores y fuentes ===========================
# claro
claro = "#ffffff"
claro_segundario = "#f0f0f0"
fondo_claro = "#f0f0f0"
texto_claro = "#000000"
boton_claro = "#c0c0c0"
hover_claro = "#e0e0e0"

# oscuro
oscuro = "#000000"
oscuro_segundario = "#111111"
fondo_oscuro = "#333333"
texto_oscuro = "#ffffff"
boton_oscuro = "#666666"
hover_oscuro = "#444444"

# ========================================================================

# =============================== fuentes ================================
# letra
letra = "SF Pro Display"

# tamaños de las letras
tamanio_letra_tiempo = 12
tamanio_letra_boton = 12
tamanio_letra_entrada = 12.5
tamanio_letra_combobox = 12.5
tamanio_letra_etiqueta = 13
tamanio_letra_volumen = 13

# ========================================================================

# ========================= variables de estado ==========================
# tema actual
tema_actual = "claro"

# estados de los botones
reproduciendo = False
silenciado = False
orden = True
repeticion = 0
volumen = 100

# ========================================================================


# ======================== funciones de utilidad =========================
# obtener la ruta de un icono
def obtener_ruta_iconos(nombre_icono, tema):
    return os.path.join(ruta_iconos, tema, f"{nombre_icono}_{tema}.png")
