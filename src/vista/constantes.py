import os

# ======================== constantes de la vista ========================
# tamaño de la pantalla
ancho_principal = 1280
alto_principal = 720

# tamaño de la ventana de configuración
ancho_configuracion = 400
alto_configuracion = 500

# tamaño minireproductor
ancho_minireproductor = 450
alto_minireproductor = 175

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
ruta_icono_aplicacion_claro = os.path.join(ruta_iconos, "reproductor_claro.png")
ruta_icono_aplicacion_oscuro = os.path.join(ruta_iconos, "reproductor_oscuro.png")

# ========================================================================

# ========================== colores y fuentes ===========================
# claro
claro = "#ffffff"
claro_segundario = "#f8f8f8"
fondo_principal = "#dedede"
fondo_claro = "#f2f2f2"
texto_claro = "#1a1a1a"
boton_claro = "#e6e6e6"
hover_claro = "#d9d9d9"

# oscuro
oscuro = "#0a0a0a"
oscuro_segundario = "#141414"
fondo_principal_oscuro = "#181818"
fondo_oscuro = "#1f1f1f"
texto_oscuro = "#ffffff"
boton_oscuro = "#2d2d2d"
hover_oscuro = "#383838"

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
panel_visible = True
silenciado = False
orden = True
repeticion = 0
volumen = 100

# ========================================================================


# ======================== funciones de utilidad =========================
# obtener la ruta de un icono
def obtener_ruta_iconos(nombre_icono, tema):
    return os.path.join(ruta_iconos, tema, f"{nombre_icono}_{tema}.png")
