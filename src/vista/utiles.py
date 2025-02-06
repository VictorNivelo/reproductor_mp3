import customtkinter as ctk
from PIL import Image
import os


tamanio = 20


def cargar_iconos(tema="claro"):
    iconos = {}
    ruta_iconos = os.path.join("recursos", "iconos", tema)
    archivos_iconos = {
        # botones de gustos
        "me_gusta": "me_gusta",
        "favorito": "favorito",
        # botones de reproducción
        "retroceder": "retroceder",
        "anterior": "anterior",
        "reproducir": "reproducir",
        "pausa": "pausa",
        "siguiente": "siguiente",
        "adelantar": "adelantar",
        # botones de repeticion
        "no_repetir": "no_repetir",
        "repetir_actual": "repetir_actual",
        "repetir_todo": "repetir_todo",
        # botones de orden
        "aleatorio": "aleatorio",
        "orden": "orden",
        # botones de cola
        "lista_cancion": "lista_cancion",
        "agregar_cola": "agregar_cola",
        # botones varios
        "ajustes": "ajustes",
        "agregar_carpeta": "agregar_carpeta",
        "agregar_cancion": "agregar_cancion",
        # tamaño de la ventana
        "maximizar": "maximizar",
        "minimizar": "minimizar",
        # botones de volumen
        "silencio": "silencio",
        "sin_volumen": "sin_volumen",
        "volumen_bajo": "volumen_bajo",
        "volumen_medio": "volumen_medio",
        "volumen_alto": "volumen_alto",
        # botones de tema
        "modo_claro": "modo_claro",
        "modo_oscuro": "modo_oscuro",
        # botones de visibilidad
        "mostrar": "mostrar",
        "ocultar": "ocultar",
    }
    for nombre, archivo in archivos_iconos.items():
        try:
            nombre_archivo = f"{archivo}_{tema}.png"
            ruta = os.path.join(ruta_iconos, nombre_archivo)
            iconos[nombre] = ctk.CTkImage(
                light_image=Image.open(ruta), dark_image=Image.open(ruta), size=(tamanio, tamanio)
            )
        except Exception as e:
            print(f"Error al cargar el icono {nombre_archivo}: {e}")
            iconos[nombre] = None
    return iconos
