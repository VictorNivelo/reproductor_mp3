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

    # Método para iniciar desplazamiento de textos largos
    def iniciar_desplazamiento_etiqueta(self, textos_dict, componente_principal, longitud_maxima):
        # Cancelar cualquier animación anterior
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            componente_principal.after_cancel(self.id_marcador_tiempo)
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
            self.animar_desplazamiento_etiqueta(componente_principal)

    # Método para detener la animación
    def detener_desplazamiento_etiqueta(self, componente_principal):
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            componente_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None

    # Método para animar el desplazamiento del texto
    def animar_desplazamiento_etiqueta(self, componente_principal, intervalo=125, reproduciendo=True):
        if not hasattr(self, "desplazamiento_activo") or not self.textos_animados:
            return
        # Si la reproducción está pausada, no animamos el desplazamiento
        if not reproduciendo:
            # Programar verificación periódica para reanudar cuando se reanude la reproducción
            self.id_marcador_tiempo = componente_principal.after(
                400,
                lambda: self.animar_desplazamiento_etiqueta(componente_principal, intervalo, reproduciendo),
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
        self.id_marcador_tiempo = componente_principal.after(
            intervalo,
            lambda: self.animar_desplazamiento_etiqueta(componente_principal, intervalo, reproduciendo),
        )

    # Método para iniciar el desplazamiento del texto en un botón
    def iniciar_desplazamiento_boton(self, boton):
        if hasattr(boton, "id_temporizador") and getattr(boton, "id_temporizador"):
            boton.after_cancel(getattr(boton, "id_temporizador"))
        setattr(boton, "posicion_desplazamiento", 0)
        self.animar_desplazamiento_boton(boton)

    # Método para detener el desplazamiento del texto en un botón
    @staticmethod
    def detener_desplazamiento_boton(boton, longitud_maxima=55):
        if hasattr(boton, "id_temporizador") and getattr(boton, "id_temporizador"):
            boton.after_cancel(getattr(boton, "id_temporizador"))
        texto_completo = getattr(boton, "texto_completo", "")
        boton.configure(text=texto_completo[:longitud_maxima] + "...")

    # Método para animar el texto en un botón
    def animar_desplazamiento_boton(self, boton, longitud_maxima=55):
        if not hasattr(boton, "texto_completo"):
            return
        texto_completo = getattr(boton, "texto_completo")
        pos = getattr(boton, "posicion_desplazamiento", 0)
        if pos == 0:
            if not hasattr(boton, "pausa_inicio"):
                setattr(boton, "pausa_inicio", 0)
            pausa_actual = getattr(boton, "pausa_inicio")
            if pausa_actual < 8:
                setattr(boton, "pausa_inicio", pausa_actual + 1)
                texto_visible = texto_completo[:longitud_maxima]
                boton.configure(text=texto_visible + "...")
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(boton, "pausa_inicio", 0)
        if pos >= len(texto_completo) - longitud_maxima:
            if not hasattr(boton, "pausa_final"):
                setattr(boton, "pausa_final", 0)
            pausa_actual = getattr(boton, "pausa_final")
            if pausa_actual < 8:
                setattr(boton, "pausa_final", pausa_actual + 1)
                texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                boton.configure(text=texto_visible)
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(boton, "pausa_final", 0)
                setattr(boton, "posicion_desplazamiento", 0)
                texto_visible = texto_completo[:longitud_maxima]
                boton.configure(text=texto_visible + "...")
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
        texto_visible = texto_completo[pos : pos + longitud_maxima]
        boton.configure(text=texto_visible)
        setattr(boton, "posicion_desplazamiento", pos + 1)
        id_temporizador = boton.after(125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima))
        setattr(boton, "id_temporizador", id_temporizador)

    # Método para configurar el desplazamiento de un botón
    def configurar_desplazamiento_boton(self, boton, texto_completo, longitud_maxima):
        if len(texto_completo) <= longitud_maxima:
            boton.configure(text=texto_completo)
            return
        setattr(boton, "texto_completo", texto_completo)
        setattr(boton, "posicion_desplazamiento", 0)
        setattr(boton, "id_temporizador", None)
        boton.bind("<Enter>", lambda event: self.iniciar_desplazamiento_boton(boton))
        boton.bind("<Leave>", lambda event: self.detener_desplazamiento_boton(boton, longitud_maxima))
        boton.configure(text=texto_completo[:longitud_maxima] + "...")
