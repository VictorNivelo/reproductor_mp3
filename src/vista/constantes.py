import os

# ======================== constantes de la vista ========================
# tamaño de la pantalla
ancho_principal = 1200
alto_principal = 720

# tamaño de la ventana de configuración
ancho_configuracion = 400
alto_configuracion = 500

# tamaño minireproductor
ancho_minireproductor = 355
alto_minireproductor = 125

# tamaño panel derecha
ancho_panel_derecha = 435

# tamaño altura tabview
alto_tabview = 400

# tamaño de los botones
ancho_boton = 20
alto_boton = 20

# tamaño de las imagenes de los botones
ancho_imagen = 20
alto_imagen = 20

# bordes redondeados
bordes_redondeados_frame = 10
borde_redondeado_boton = 5

# tamaño de barras del espectro
numero_barras = 125
ancho_barra = 2
espacio_entre_barras = 1

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

# ruta del ucono de la aplicacion en ico
ruta_icono_aplicacion_claro_ico = os.path.join(ruta_iconos, "reproductor_claro.ico")
ruta_icono_aplicacion_oscuro_ico = os.path.join(ruta_iconos, "reproductor_oscuro.ico")

# ========================================================================

# ========================== colores y fuentes ===========================
# claro
claro = "#ffffff"
claro_segundario = "#f8f8f8"
fondo_principal_claro = "#dedede"
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
me_gusta = False
favorito = False

# estado de la barra de progreso
arrastrando_progreso = False
duracion_total = 0
tiempo_actual = 0

# ========================================================================


# ======================== funciones de utilidad =========================
# obtener la ruta de un icono
def obtener_ruta_iconos(nombre_icono, tema):
    # Iconos especiales que son independientes del tema
    iconos_especiales = ["me_gusta_rojo", "favorito_amarillo"]
    if nombre_icono in iconos_especiales:
        return os.path.join(ruta_iconos, f"{nombre_icono}.png")
    # Iconos normales que dependen del tema
    return os.path.join(ruta_iconos, tema, f"{nombre_icono}_{tema}.png")
