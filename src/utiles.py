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


class Utiles:
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
        # Animaciones
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.id_marcador_tiempo = None
        self.textos_animados = {}

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
    def crear_imagen_desde_bytes(imagen_bytes, ancho, mantener_proporcion=True):
        try:
            # Crear imagen desde los bytes
            imagen = Image.open(BytesIO(imagen_bytes))
            # Calcular dimensiones finales
            ancho_original = float(imagen.size[0])
            alto_original = float(imagen.size[1])
            if mantener_proporcion:
                ratio = ancho / ancho_original
                alto = int(alto_original * ratio)
            else:
                alto = ancho  # Cuadrado si no se mantiene proporción
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

    # Método para iniciar desplazamiento de textos largos
    def iniciar_desplazamiento_texto(self, textos_dict, widget_principal, longitud_maxima=75):
        # Cancelar cualquier animación anterior
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            widget_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None
        # Variables para controlar el desplazamiento
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.textos_animados = textos_dict
        # Comprobar si algún texto necesita desplazamiento
        for clave, (texto, etiqueta) in textos_dict.items():
            if len(texto) > longitud_maxima:
                self.desplazamiento_activo[clave] = True
                self.posicion_desplazamiento[clave] = 0
                self.direccion_desplazamiento[clave] = 1  # 1: derecha a izquierda
            else:
                self.desplazamiento_activo[clave] = False
        # Iniciar animación si hay textos para desplazar
        if any(self.desplazamiento_activo.values()):
            self.animar_desplazamiento_texto(widget_principal)

    # Método para animar el desplazamiento del texto
    def animar_desplazamiento_texto(self, widget_principal, intervalo=125, reproduciendo=True):
        if not hasattr(self, "desplazamiento_activo") or not self.textos_animados:
            return
        # Si la reproducción está pausada, no animamos el desplazamiento
        if not reproduciendo:
            # Programar verificación periódica para reanudar cuando se reanude la reproducción
            self.id_marcador_tiempo = widget_principal.after(
                500, lambda: self.animar_desplazamiento_texto(widget_principal, intervalo, reproduciendo)
            )
            return
        # Actualizar cada texto que necesite desplazamiento
        longitud_maxima = 75
        for clave, (texto_completo, etiqueta) in self.textos_animados.items():
            if not self.desplazamiento_activo.get(clave, False):
                continue
            # Obtener posición actual
            posicion = self.posicion_desplazamiento[clave]
            # Si el texto es más largo que la longitud máxima, aplicar desplazamiento
            if len(texto_completo) > longitud_maxima:
                # Control de pausa al inicio
                if posicion == 0:
                    # Sí estamos al inicio, pausar durante más tiempo
                    if not hasattr(self, f"pausa_inicio_{clave}"):
                        setattr(self, f"pausa_inicio_{clave}", 0)
                    pausa_actual = getattr(self, f"pausa_inicio_{clave}")
                    if pausa_actual < 8:  # 8 * 125ms = 1 segundo de pausa
                        setattr(self, f"pausa_inicio_{clave}", pausa_actual + 1)
                        texto_visible = texto_completo[:longitud_maxima]
                        etiqueta.configure(text=texto_visible)
                        continue
                    else:
                        setattr(self, f"pausa_inicio_{clave}", 0)
                # Control de pausa al final
                if posicion >= len(texto_completo) - longitud_maxima:
                    # Si llegamos al final, pausar antes de reiniciar
                    if not hasattr(self, f"pausa_final_{clave}"):
                        setattr(self, f"pausa_final_{clave}", 0)
                    pausa_actual = getattr(self, f"pausa_final_{clave}")
                    if pausa_actual < 8:  # 8 * 125ms = 1 segundo de pausa
                        texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                        etiqueta.configure(text=texto_visible)
                        setattr(self, f"pausa_final_{clave}", pausa_actual + 1)
                        continue
                    else:
                        # Reiniciar desde el principio
                        self.posicion_desplazamiento[clave] = 0
                        texto_visible = texto_completo[:longitud_maxima]
                        setattr(self, f"pausa_final_{clave}", 0)
                        etiqueta.configure(text=texto_visible)
                        continue
                # Desplazamiento normal
                texto_visible = texto_completo[posicion : posicion + longitud_maxima]
                self.posicion_desplazamiento[clave] += 1
                etiqueta.configure(text=texto_visible)
        # Programar próxima actualización
        self.id_marcador_tiempo = widget_principal.after(
            intervalo, lambda: self.animar_desplazamiento_texto(widget_principal, intervalo, reproduciendo)
        )

    # Método para detener la animación
    def detener_desplazamiento_texto(self, widget_principal):
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            widget_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None
