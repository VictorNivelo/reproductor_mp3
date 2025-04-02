import os

# ======================== Constantes de la vista ========================
# Tamaño de la pantalla
ANCHO_PRINCIPAL = 1200
ALTO_PRINCIPAL = 720

# Tamaño de la ventana de configuración
ANCHO_CONFIGURACION = 400
ALTO_CONFIGURACION = 500

# Tamaño minireproductor
ANCHO_MINI_REPRODUCTOR = 355
ALTO_MINI_REPRODUCTOR = 125

# Tamaño de la barra de progreso
ANCHO_ESTADISTICAS = 400
ALTO_ESTADISTICAS = 450

# Tamaño de la cola de reproducción
ANCHO_COLA_REPRODUCCION = 400
ALTO_COLA_REPRODUCCION = 600

# Tamaño panel derecha
ANCHO_PANEL_DERECHA = 435

# Tamaño altura tabview
ALTO_TABVIEW = 400

# Tamaño de los botones
ANCHO_BOTON = 20
ALTO_BOTON = 20

# Tamaño de las imagenes de los botones
ANCHO_IMAGEN = 20
ALTO_IMAGEN = 20

# Bordes redondeados
BORDES_REDONDEADOS_PANEL = 10
BORDES_REDONDEADOS_BOTON = 5

# Tamaño de barras del espectro
NUMERO_BARRA = 125
ANCHO_BARRA = 2
ESPACIO_ENTRE_BARRA = 1

# ========================================================================

# ========================= Ruta de los recursos =========================
# Ruta base del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(__file__))

# Ruta de los recursos
RUTA_RECURSOS = os.path.join(RUTA_BASE, "recursos")
RUTA_ICONOS = os.path.join(RUTA_RECURSOS, "iconos")
RUTA_IMAGENES = os.path.join(RUTA_RECURSOS, "imagenes")

# Rutas del icono de la aplicación
RUTA_ICONO_APLICACION_CLARO = os.path.join(RUTA_ICONOS, "reproductor_claro.png")
RUTA_ICONO_APLICACION_OSCURO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.png")

# Ruta del ucono de la aplicacion en ico
RUTA_ICONO_APLICACION_CLARO_ICO = os.path.join(RUTA_ICONOS, "reproductor_claro.ico")
RUTA_ICONO_APLICACION_OSCURO_ICO = os.path.join(RUTA_ICONOS, "reproductor_oscuro.ico")

# Ruta de los datos de la aplicación
RUTA_CARPETA_DATOS = "datos"
RUTA_CARPETA_LISTAS = os.path.join(RUTA_CARPETA_DATOS, "listas")
RUTA_CARPETA_FAVORITOS = os.path.join(RUTA_CARPETA_LISTAS, "favorito")
RUTA_CARPETA_ME_GUSTA = os.path.join(RUTA_CARPETA_LISTAS, "me_gusta")
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

# ========================================================================

# ========================== Colores y fuentes ===========================
# Claro
CLARO = "#ffffff"
CLARO_SEGUNDARIO = "#f8f8f8"
FONDO_PRINCIPAL_CLARO = "#dedede"
FONDO_CLARO = "#f2f2f2"
TEXTO_CLARO = "#1a1a1a"
BOTON_CLARO = "#e6e6e6"
HOVER_CLARO = "#d9d9d9"

# Oscuro
OSCURO = "#0a0a0a"
OSCURO_SEGUNDARIO = "#141414"
FONDO_PRINCIPAL_OSCURO = "#181818"
FONDO_OSCURO = "#1f1f1f"
TEXTO_OSCURO = "#ffffff"
BOTON_OSCURO = "#2d2d2d"
HOVER_OSCURO = "#383838"

# ========================================================================

# =============================== Fuentes ================================
# Letra
LETRA = "SF Pro Display"

# ========================================================================

# ======================== Tamaños de las letras =========================
# Tamaños de las letras
TAMANIO_LETRA_TIEMPO = 12
TAMANIO_LETRA_BOTON = 12
TAMANIO_LETRA_ENTRADA = 12.5
TAMANIO_LETRA_COMBOBOX = 12.5
TAMANIO_LETRA_ETIQUETA = 13
TAMANIO_LETRA_VOLUMEN = 13

# ========================================================================

# ========================= Constantes ===================================
# Tiempo de retoceso y avance
TIEMPO_AJUSTE = 10

# ========================================================================

# =================== Formatos de archivos soportados ====================
# Formatos de archivos soportados
FORMATOS_SOPORTADOS = {".mp3", ".flac", ".m4a", ".mp4", ".wav", ".ogg"}

# ========================================================================


# Obtener la ruta de un icono
def obtener_ruta_iconos(nombre_icono, tema):
    # Iconos especiales que son independientes del tema
    iconos_especiales = ["me_gusta_rojo", "favorito_amarillo"]
    if nombre_icono in iconos_especiales:
        return os.path.join(RUTA_ICONOS, f"{nombre_icono}.png")
    # Iconos normales que dependen del tema
    return os.path.join(RUTA_ICONOS, tema, f"{nombre_icono}_{tema}.png")
