from typing import List, Tuple, Dict
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image
import numpy as np


# Metodo para convertir un color RGB a hexadecimal
def rgb_a_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


# Metodo para convertir un color hexadecimal a RGB
def hex_a_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


# Metodo para extraer los colores dominantes de una imagen
def extraer_colores_dominantes(imagen_bytes: bytes, num_colores: int = 6) -> List[str]:
    try:
        # Cargar imagen desde bytes
        imagen = Image.open(BytesIO(imagen_bytes))
        # Redimensionar para acelerar el procesamiento
        imagen = imagen.resize((150, 150))
        # Convertir a RGB si es necesario
        if imagen.mode != "RGB":
            imagen = imagen.convert("RGB")
        # Convertir a array numpy
        array_imagen = np.array(imagen)
        # Reshape para K-means
        pixels = array_imagen.reshape(-1, 3)
        # Aplicar K-means para encontrar los colores dominantes
        kmeans = KMeans(n_clusters=num_colores)
        kmeans.fit(pixels)
        # Obtener los colores del modelo
        colores = kmeans.cluster_centers_
        # Convertir a enteros y luego a hex
        colores = colores.astype(int)
        colores_hex = [rgb_a_hex((int(color[0]), int(color[1]), int(color[2]))) for color in colores]
        return colores_hex
    except Exception as e:
        print(f"Error al extraer los colores dominantes: {e}")
        return ["#ffffff", "#000000", "#cccccc", "#333333", "#666666", "#999999"]


# Metodo para calcular el brillo de un color
def calcular_brillo(color_hex: str) -> float:
    r, g, b = hex_a_rgb(color_hex)
    return (r * 299 + g * 587 + b * 114) / 1000


# Metodo para calcular la saturación de un color
def calcular_saturacion(color_hex: str) -> float:
    r, g, b = hex_a_rgb(color_hex)
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    min_val = min(r, g, b)
    max_val = max(r, g, b)
    if max_val == 0:
        return 0
    return (max_val - min_val) / max_val


# Metodo para ordenar colores por brillo
def ordenar_colores_por_brillo(colores_hex: List[str]) -> List[str]:
    return sorted(colores_hex, key=calcular_brillo)


# Metodo para ordenar colores por saturación
def ordenar_colores_por_saturacion(colores_hex: List[str]) -> List[str]:
    return sorted(colores_hex, key=calcular_saturacion)


# Metodo para crear una paleta de colores a partir de una lista de colores
def crear_paleta_tema(colores_hex: List[str]) -> Dict[str, str]:
    if not colores_hex or len(colores_hex) < 4:
        # Colores por defecto si no hay suficientes
        return {
            "color_principal": "#181818",
            "color_segundario": "#1f1f1f",
            "color_fondo": "#2d2d2d",
            "color_base": "#383838",
            "color_texto": "#ffffff",
            "color_boton": "#2d2d2d",
            "color_hover": "#383838",
            "color_hover_oscuro": "#474747",
            "color_slider": "#555555",
            "color_borde": "#2d2d2d",
            "barra_progreso": "#474747",
        }
    # Ordenar colores por brillo
    colores_por_brillo = ordenar_colores_por_brillo(colores_hex)
    colores_por_saturacion = ordenar_colores_por_saturacion(colores_hex)
    # Seleccionar colores específicos para el tema
    colores_tema = {
        "color_principal": colores_por_brillo[0],
        "color_segundario": colores_por_brillo[1],
        "color_fondo": colores_por_brillo[2],
        "color_base": colores_por_brillo[3 % len(colores_por_brillo)],
        "color_texto": colores_por_brillo[-1],
        "color_boton": colores_por_saturacion[
            -2 % len(colores_por_saturacion)
        ],  # Color saturado para botones
        "color_hover": colores_por_saturacion[-1],
        "color_hover_oscuro": colores_por_brillo[1],
        "color_slider": colores_por_saturacion[-3 % len(colores_por_saturacion)],
        "color_borde": colores_por_brillo[2],
        "barra_progreso": colores_por_brillo[1],
    }
    return colores_tema


# Metodo para ajustar el contraste de una paleta de colores
def ajustar_contraste_paleta(paleta: Dict[str, str]) -> Dict[str, str]:
    paleta_ajustada = paleta.copy()
    # Calcular brillo del texto
    brillo_texto = calcular_brillo(paleta["color_texto"])
    # Si el texto no es lo suficientemente claro/oscuro respecto al fondo principal
    brillo_fondo = calcular_brillo(paleta["color_fondo"])
    # Si el contraste no es suficiente
    if abs(brillo_texto - brillo_fondo) < 128:
        # Invertir color del texto para máximo contraste
        if brillo_fondo > 128:
            paleta_ajustada["color_texto"] = "#000000"
        else:
            paleta_ajustada["color_texto"] = "#ffffff"
    return paleta_ajustada


# Metodo para crear la paleta de colores desde la caratula
def crear_paleta_desde_caratula(caratula_bytes: bytes) -> Dict[str, str]:
    try:
        if not caratula_bytes:
            return {}
        # Extraer colores dominantes
        colores_dominantes = extraer_colores_dominantes(caratula_bytes)
        # Crear paleta
        paleta = crear_paleta_tema(colores_dominantes)
        # Ajustar contraste para garantizar legibilidad
        paleta_ajustada = ajustar_contraste_paleta(paleta)
        return paleta_ajustada
    except Exception as e:
        print(f"Error al crear paleta desde carátula: {e}")
        return {}
