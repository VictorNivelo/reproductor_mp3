from vista.constantes import alto_boton, ancho_boton, obtener_ruta_iconos
from vista.constantes import *
import customtkinter as ctk
import tkinter as tk
from PIL import Image


def cargar_iconos(tema="claro"):
    iconos = {}
    archivos_iconos = {
        # botones de gustos
        "me_gusta": "me_gusta",
        "favorito": "favorito",
        "me_gusta_rojo": "me_gusta_rojo",
        "favorito_amarillo": "favorito_amarillo",
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
            if archivo in ["me_gusta_rojo", "favorito_amarillo"]:
                ruta_iconos = obtener_ruta_iconos(archivo, None)
            else:
                ruta_iconos = obtener_ruta_iconos(archivo, tema)
            iconos[nombre] = ctk.CTkImage(
                light_image=Image.open(ruta_iconos),
                dark_image=Image.open(ruta_iconos),
                size=(ancho_boton, alto_boton),
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
            ventana.iconbitmap(ruta_icono_aplicacion_oscuro.replace(".png", ".ico"))
        else:
            # Si el tema es oscuro, ponemos el icono claro
            ventana.iconbitmap(ruta_icono_aplicacion_claro.replace(".png", ".ico"))
    except:
        # Para otros sistemas o como respaldo usando PhotoImage
        if tema == "claro":
            # Si el tema es claro, ponemos el icono oscuro
            icono = tk.PhotoImage(file=ruta_icono_aplicacion_oscuro)
        else:
            # Si el tema es oscuro, ponemos el icono claro
            icono = tk.PhotoImage(file=ruta_icono_aplicacion_claro)
        ventana.iconphoto(True, icono)
