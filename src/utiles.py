import customtkinter as ctk
from constantes import *
from io import BytesIO
from PIL import Image
import tracemalloc


# Método decorador para medir el consumo de memoria de una función
def medir_consumo_memoria(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        resultado = func(*args, **kwargs)
        actual, pico = tracemalloc.get_traced_memory()
        print(f"{func.__name__} - Memoria actual: {actual / 1024:.2f} KB")
        print(f"{func.__name__} - Pico de memoria: {pico / 1024:.2f} KB")
        tracemalloc.stop()
        return resultado

    return wrapper


class UtilesGeneral:
    def __init__(self, controlador_externo=None):
        # Si no hay controlador externo, esta instancia actúa como controlador
        self.es_controlador = controlador_externo is None
        # Almacena la referencia al controlador (self si es controlador)
        self.controlador = self if self.es_controlador else controlador_externo
        # Tema de la interfaz y de los iconos (solo inicializa si es controlador)
        if self.es_controlador:
            self.tema_interfaz = "claro"
            self.tema_iconos = "oscuro"
        # Inicializar todos los colores
        self.color_fondo_principal = None
        self.color_fondo = None
        self.color_texto = None
        self.color_boton = None
        self.color_hover = None
        self.color_base = None
        self.color_barras = None
        self.color_borde = None
        self.color_slider = None
        self.color_hover_oscuro = None
        self.color_barra_progreso = None
        self.color_segundario = None

    # Método para obtener los colores de la interfaz
    def colores(self):
        # Obtiene el tema del controlador (propio o externo)
        tema = self.controlador.tema_interfaz == "oscuro"
        # Colores base compartidos
        self.color_fondo_principal = FONDO_PRINCIPAL_OSCURO if tema else FONDO_PRINCIPAL_CLARO
        self.color_fondo = FONDO_OSCURO if tema else FONDO_CLARO
        self.color_texto = TEXTO_OSCURO if tema else TEXTO_CLARO
        self.color_boton = BOTON_OSCURO if tema else BOTON_CLARO
        self.color_hover, self.color_hover_oscuro = (
            (HOVER_OSCURO, HOVER_CLARO) if tema else (HOVER_CLARO, HOVER_OSCURO)
        )
        # Colores exclusivos de UtilesControlador
        self.color_base = OSCURO if tema else CLARO
        self.color_segundario = OSCURO_SEGUNDARIO if tema else CLARO_SEGUNDARIO
        self.color_borde = FONDO_CLARO if tema else FONDO_OSCURO
        self.color_barras = BARRA_OSCURO if tema else BARRA_CLARO
        self.color_slider = TEXTO_OSCURO if tema else FONDO_OSCURO
        self.color_barra_progreso = BARRA_PROGRESO_CLARO if tema else BARRA_PROGRESO_OSCURO

    # Método para obtener la imagen de la caratula
    @staticmethod
    def crear_imagen_desde_bytes(imagen_bytes, ancho, alto=None, mantener_proporcion=True):
        try:
            # Crear imagen desde los bytes
            imagen = Image.open(BytesIO(imagen_bytes))
            # Obtener dimensiones originales
            ancho_original = float(imagen.size[0])
            alto_original = float(imagen.size[1])
            # Calcular dimensiones finales según los parámetros
            if alto is None:
                # Si solo se proporciona ancho, calcular alto manteniendo proporción
                if mantener_proporcion:
                    ratio = ancho / ancho_original
                    alto = int(alto_original * ratio)
                else:
                    alto = ancho  # Cuadrado si no se mantiene proporción
            elif mantener_proporcion:
                # Si se proporcionan ambos (ancho y alto) pero queremos mantener proporción
                # Calculamos qué dimensión es más restrictiva
                ratio_ancho = ancho / ancho_original
                ratio_alto = alto / alto_original
                ratio = min(ratio_ancho, ratio_alto)  # Usamos el ratio más pequeño
                ancho = int(ancho_original * ratio)
                alto = int(alto_original * ratio)
            # Redimensionar la imagen
            imagen_redimensionada = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
            # Convertir a formato CTkImage
            foto = ctk.CTkImage(
                light_image=imagen_redimensionada, dark_image=imagen_redimensionada, size=(ancho, alto)
            )
            return foto, ancho, alto
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return None, None, None
