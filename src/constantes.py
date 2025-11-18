import os

# ======================== Constantes de la vista ========================
# Tamaño de la pantalla
ANCHO_PRINCIPAL = 1200
ALTO_PRINCIPAL = 720

# Tamaño de la ventana de configuración
ANCHO_CONFIGURACION = 400
ALTO_CONFIGURACION = 500

# Tamaño de la ventana de atajos
ANCHO_ATAJOS = 370
ALTO_ATAJOS = 535

# Tamaño minireproductor
ANCHO_MINI_REPRODUCTOR = 410
ALTO_MINI_REPRODUCTOR = 132

# Tamaño de la barra de progreso
ANCHO_ESTADISTICAS = 425
ALTO_ESTADISTICAS = 450

# Tamaño de la cola de reproducción
ANCHO_COLA_REPRODUCCION = 400
ALTO_COLA_REPRODUCCION = 600

# Tamaño panel derecha
ANCHO_PANEL_DERECHA = 440

# Tamaño altura tabview
ALTO_TABVIEW = 400

# Tamaño de los botones
ANCHO_BOTON = 35
ALTO_BOTON = 35

# Tamaño de las imagenes de los botones
ANCHO_IMAGEN = 20
ALTO_IMAGEN = 20

# Tamaño de la carátula
ALTO_CARATULA = 325
ANCHO_CARATULA = 325

# Bordes redondeados
BORDES_REDONDEADOS_PANEL = 10
BORDES_REDONDEADOS_BOTON = 5
BORDES_REDONDEADOS_ENTRADAS = 7
BORDES_REDONDEADOS_CARATULA = 15

# Tamaño de barras del espectro
NUMERO_BARRA = 125
ANCHO_BARRA = 2
ESPACIO_ENTRE_BARRA = 1

# ========================================================================

# ========================= Ruta de los recursos =========================
# Ruta de la carpeta musica en el sistema
RUTA_CARPETA_MUSICA = os.path.join(os.path.expanduser("~"), "Music")

# Ruta base del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(__file__))

# Ruta de los recursos
RUTA_RECURSOS = os.path.join(RUTA_BASE, "recursos")
RUTA_ICONOS = os.path.join(RUTA_RECURSOS, "iconos")
RUTA_IMAGENES = os.path.join(RUTA_RECURSOS, "imagenes")

# Rutas del icono de la aplicación
RUTA_ICONO_APLICACION_CLARO = os.path.join(RUTA_ICONOS, "reproductor_claro.png")
RUTA_ICONO_APLICACION_OSCURO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.png")

# Ruta del icono de la aplicacion en ico
RUTA_ICONO_APLICACION_CLARO_ICO = os.path.join(RUTA_ICONOS, "reproductor_claro.ico")
RUTA_ICONO_APLICACION_OSCURO_ICO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.ico")

# Ruta de los datos de la aplicación
RUTA_CARPETA_DATOS = "datos"
RUTA_CARPETA_LISTAS = os.path.join(RUTA_CARPETA_DATOS, "listas")
RUTA_CARPETA_FAVORITOS = os.path.join(RUTA_CARPETA_LISTAS, "favorito")
RUTA_CARPETA_ME_GUSTA = os.path.join(RUTA_CARPETA_LISTAS, "me_gusta")
RUTA_CARPETA_LISTA_REPRODUCCION = os.path.join(RUTA_CARPETA_LISTAS, "listas_reproduccion")
RUTA_CARPETA_PERSONALIZADA = os.path.join(RUTA_CARPETA_LISTAS, "personalizada")
RUTA_CARPETA_ESTADISTICAS = os.path.join(RUTA_CARPETA_DATOS, "estadisticas")
RUTA_CARPETA_CONFIGURACION = os.path.join(RUTA_CARPETA_DATOS, "configuracion")

# Rutas de archivos
RUTA_COLA = os.path.join(RUTA_CARPETA_LISTAS, "cola.json")
RUTA_CANCIONES = os.path.join(RUTA_CARPETA_ESTADISTICAS, "canciones.json")
RUTA_FAVORITOS = os.path.join(RUTA_CARPETA_FAVORITOS, "favorito.json")
RUTA_ME_GUSTA = os.path.join(RUTA_CARPETA_ME_GUSTA, "me_gusta.json")
RUTA_REPRODUCCION = os.path.join(RUTA_CARPETA_ESTADISTICAS, "reproduccion.json")
RUTA_CONFIGURACION = os.path.join(RUTA_CARPETA_CONFIGURACION, "ajustes.json")
RUTA_ATAJOS = os.path.join(RUTA_CARPETA_CONFIGURACION, "atajos.json")

# ========================================================================

# ========================== Colores y fuentes ===========================
# Claro
CLARO = "#ffffff"
CLARO_SEGUNDARIO = "#f9f9f9"
FONDO_PRINCIPAL_CLARO = "#e5e5e5"
FONDO_CLARO = "#fafafa"
TEXTO_CLARO = "#000000"
BOTON_CLARO = "#E9ECEF"
HOVER_CLARO = "#DEE2E6"
BORDE_CLARO = "#CED4DA"
BARRA_CLARO = "#b3b3b3"
BARRA_PROGRESO_CLARO = "#b8b8b8"

# Oscuro
OSCURO = "#1A1818"
OSCURO_SEGUNDARIO = "#161616"
FONDO_PRINCIPAL_OSCURO = "#1a1a1a"
FONDO_OSCURO = "#1D1D1D"
TEXTO_OSCURO = "#ffffff"
BOTON_OSCURO = "#282A2C"
HOVER_OSCURO = "#495057"
BORDE_OSCURO = "#6C757D"
BARRA_OSCURO = "#413f3f"
BARRA_PROGRESO_OSCURO = "#555555"

# ========================================================================

# =============================== Fuentes ================================
# Letra
LETRA = "SF Pro Display"

# ========================================================================

# ======================== Tamaños de las letras =========================
# Tamaños de las letras
TAMANIO_LETRA_ETIQUETA = 13
TAMANIO_LETRA_ETIQUETA_INFORMACION = 12
TAMANIO_LETRA_TIEMPO = 12
TAMANIO_LETRA_COMBOBOX = 12.5
TAMANIO_LETRA_ENTRADA = 13
TAMANIO_LETRA_BOTON = 12

# Tamaños de las letras generales
TAMANIO_LETRA_TITULO = 18
TAMANIO_LETRA_SUBTITULO = 15
TAMANIO_LETRA_MENSAJE = 13
TAMANIO_LETRA_NUMERO = 12

# ========================================================================

# ========================= Constantes ===================================
# Constantes de la aplicación
TIEMPO_AJUSTE = 10
AUMENTO_VOLUMEN = 5

# ========================================================================

# ======================== Separadores de listas =========================
# Separadores de listas
SEPARADORES = [
    " ft ",
    " feat ",
    " feat. ",
    " featuring ",
    " with ",
    " & ",
    " and ",
    " con ",
    " junto a ",
    " x ",
    " vs ",
    " vs. ",
    " + ",
]

# ========================================================================

# ========================= Atajos de teclado ============================
# Atajos de teclado por defecto
ATAJOS_POR_DEFECTO = {
    "reproducir_pausar": "space",
    "siguiente": "Control-Right",
    "anterior": "Control-Left",
    "aumentar_volumen": "Up",
    "disminuir_volumen": "Down",
    "silenciar": "m",
    "modo_aleatorio": "s",
    "repeticion": "r",
    "visibilidad_panel": "l",
    "me_gusta": "g",
    "favorito": "f",
    "cola": "c",
    "mini_reproductor": "p",
    "adelantar": "Right",
    "retroceder": "Left",
}

# =================== Formatos de archivos soportados ====================
# Formatos de archivos soportados
FORMATOS_SOPORTADOS = {".mp3", ".flac", ".m4a", ".mp4", ".wav", ".ogg"}

# ========================================================================
