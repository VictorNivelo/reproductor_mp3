import os

# ======================== constantes de la vista ========================
# tamaño de la pantalla
ANCHO_PRINCIPAL = 1200
ALTO_PRINCIPAL = 720

# tamaño de la ventana de configuración
ANCHO_CONFIGURACION = 400
ALTO_CONFIGURACION = 500

# tamaño minireproductor
ANCHO_MINI_REPRODUCTOR = 355
ALTO_MINI_REPRODUCTOR = 125

# tamaño panel derecha
ANCHO_PANEL_DERECHA = 435

# tamaño altura tabview
ALTO_TABVIEW = 400

# tamaño de los botones
ANCHO_BOTON = 20
ALTO_BOTON = 20

# tamaño de las imagenes de los botones
ANCHO_IMAGEN = 20
ALTO_IMAGEN = 20

# bordes redondeados
BORDES_REDONDEADOS_PANEL = 10
BORDES_REDONDEADOS_BOTON = 5

# tamaño de barras del espectro
NUMERO_BARRA = 125
ANCHO_BARRA = 2
ESPACIO_ENTRE_BARRA = 1

# ========================================================================

# ========================= ruta de los recursos =========================
# ruta base del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# ruta de los recursos
RUTA_RECURSOS = os.path.join(RUTA_BASE, "recursos")
RUTA_ICONOS = os.path.join(RUTA_RECURSOS, "iconos")
RUTA_IMAGENES = os.path.join(RUTA_RECURSOS, "imagenes")

# rutas del icono de la aplicación
RUTA_ICONO_APLICACION_CLARO = os.path.join(RUTA_ICONOS, "reproductor_claro.png")
RUTA_ICONO_APLICACION_OSCURO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.png")

# ruta del ucono de la aplicacion en ico
RUTA_ICONO_APLICACION_CLARO_ICO = os.path.join(RUTA_ICONOS, "reproductor_claro.ico")
RUTA_ICONO_APLICACION_OSCURO_ICO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.ico")

# ========================================================================

# ========================== colores y fuentes ===========================
# claro
CLARO = "#ffffff"
CLARO_SEGUNDARIO = "#f8f8f8"
FONDO_PRINCIPAL_CLARO = "#dedede"
FONDO_CLARO = "#f2f2f2"
TEXTO_CLARO = "#1a1a1a"
BOTON_CLARO = "#e6e6e6"
HOVER_CLARO = "#d9d9d9"

# oscuro
OSCURO = "#0a0a0a"
OSCURO_SEGUNDARIO = "#141414"
FONDO_PRINCIPAL_OSCURO = "#181818"
FONDO_OSCURO = "#1f1f1f"
TEXTO_OSCURO = "#ffffff"
BOTON_OSCURO = "#2d2d2d"
HOVER_OSCURO = "#383838"

# ========================================================================

# =============================== fuentes ================================
# letra
LETRA = "SF Pro Display"

# tamaños de las letras
TAMANIO_LETRA_TIEMPO = 12
TAMANIO_LETRA_BOTON = 12
TAMANIO_LETRA_ENTRADA = 12.5
TAMANIO_LETRA_COMBOBOX = 12.5
TAMANIO_LETRA_ETIQUETA = 13
TAMANIO_LETRA_VOLUMEN = 13

# ========================================================================

# ========================= variables de estado ==========================
# tema actual
TEMA_ACTUAL = "claro"

# estados de los botones
REPRODUCIENDO = False
SILENCIADO = False
PANEL_VISIBLE = True
ORDEN = True
REPETICION = 0
VOLUMEN = 100
ME_GUSTA = False
FAVORITO = False

# estado de la barra de progreso
ARRASTRANDO_PROGRESO = False
DURACION_TOTAL = 0
TIEMPO_ACTUAL = 0

# ========================================================================


# ======================== funciones de utilidad =========================
# obtener la ruta de un icono
def obtener_ruta_iconos(nombre_icono, tema):
    # Iconos especiales que son independientes del tema
    iconos_especiales = ["me_gusta_rojo", "favorito_amarillo"]
    if nombre_icono in iconos_especiales:
        return os.path.join(RUTA_ICONOS, f"{nombre_icono}.png")
    # Iconos normales que dependen del tema
    return os.path.join(RUTA_ICONOS, tema, f"{nombre_icono}_{tema}.png")
