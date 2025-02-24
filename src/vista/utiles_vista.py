from vista.tooltip import ToolTip
import customtkinter as ctk
from constantes import *
from PIL import Image
import tkinter as tk


def cargar_iconos(tema="claro"):
    iconos = {}
    archivos_iconos = {
        # Botones de gustos
        "me_gusta": "me_gusta",
        "favorito": "favorito",
        "me_gusta_rojo": "me_gusta_rojo",
        "favorito_amarillo": "favorito_amarillo",
        # Botones de reproducción
        "retroceder": "retroceder",
        "anterior": "anterior",
        "reproducir": "reproducir",
        "pausa": "pausa",
        "siguiente": "siguiente",
        "adelantar": "adelantar",
        # Botones de repeticion
        "no_repetir": "no_repetir",
        "repetir_actual": "repetir_actual",
        "repetir_todo": "repetir_todo",
        # Botones de orden
        "aleatorio": "aleatorio",
        "orden": "orden",
        # Botones de cola
        "lista_cancion": "lista_cancion",
        "agregar_cola": "agregar_cola",
        # Botones varios
        "ajustes": "ajustes",
        "agregar_carpeta": "agregar_carpeta",
        "agregar_cancion": "agregar_cancion",
        # Tamaño de la ventana
        "maximizar": "maximizar",
        "minimizar": "minimizar",
        # Botones de volumen
        "silencio": "silencio",
        "sin_volumen": "sin_volumen",
        "volumen_bajo": "volumen_bajo",
        "volumen_medio": "volumen_medio",
        "volumen_alto": "volumen_alto",
        # Botones de tema
        "modo_claro": "modo_claro",
        "modo_oscuro": "modo_oscuro",
        # Botones de visibilidad
        "mostrar": "mostrar",
        "ocultar": "ocultar",
    }
    for nombre, archivo in archivos_iconos.items():
        try:
            # Cargar los iconos
            if archivo in ["me_gusta_rojo", "favorito_amarillo"]:
                # Si el icono es me_gusta_rojo o favorito_amarillo, no se necesita el tema
                ruta_iconos = obtener_ruta_iconos(archivo, None)
            else:
                # Si el icono no es me_gusta_rojo o favorito_amarillo, se necesita el tema
                ruta_iconos = obtener_ruta_iconos(archivo, tema)
            # cargar el icono en una instancia de CTkImage
            iconos[nombre] = ctk.CTkImage(
                # Modo de imagen y tamaño
                light_image=Image.open(ruta_iconos),
                dark_image=Image.open(ruta_iconos),
                size=(ANCHO_IMAGEN, ALTO_IMAGEN),
            )
        except Exception as e:
            print(f"Error al cargar el icono {nombre}: {e}")
            iconos[nombre] = None
    return iconos


def establecer_icono_tema(ventana, tema="claro"):
    try:
        # Para Windows
        if tema == "claro":
            # Si el tema es claro, ponemos el icono oscuro
            ventana.iconbitmap(RUTA_ICONO_APLICACION_OSCURO.replace(".png", ".ico"))
        else:
            # Si el tema es oscuro, ponemos el icono claro
            ventana.iconbitmap(RUTA_ICONO_APLICACION_CLARO.replace(".png", ".ico"))
    except tk.TclError:
        # Para otros sistemas o como respaldo usando PhotoImage
        if tema == "claro":
            # Si el tema es claro, ponemos el icono oscuro
            icono = tk.PhotoImage(file=RUTA_ICONO_APLICACION_OSCURO)
        else:
            # Si el tema es oscuro, ponemos el icono claro
            icono = tk.PhotoImage(file=RUTA_ICONO_APLICACION_CLARO)
        ventana.iconphoto(True, icono)


def crear_tooltip(widget, text):
    return ToolTip(widget, text)
