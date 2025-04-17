from vista.componentes.tooltip import ToolTip
import customtkinter as ctk
from constantes import *
from PIL import Image
import tkinter as tk

# Diccionario para guardar los tooltips de los componentes
lista_tooltips = {}


# Método para obtener la ruta de los iconos de la aplicación
def cargar_iconos(tema="claro", tamanio=None):
    iconos = {}
    # Tamaño de los iconos
    tamanio_iconos = tamanio if tamanio else (ANCHO_IMAGEN, ALTO_IMAGEN)
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
        "mostrar_cola": "mostrar_cola",
        "agregar_cola": "agregar_cola",
        # Botones varios
        "ajustes": "ajustes",
        "opcion": "opcion",
        "atajos": "atajos",
        "estadistica": "estadistica",
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
        # Botones de creación, edición y eliminación
        "crear": "crear",
        "editar": "editar",
        "guardar": "guardar",
        "eliminar": "eliminar",
        "quitar": "quitar",
        "limpiar": "limpiar",
        "buscar": "buscar",
        "regresar": "regresar",
        # Botones de reproducción de video
        "microfono": "microfono",
        "audifonos": "audifonos",
        "bluetooth": "bluetooth",
        "sonido": "sonido",
        "enlace": "enlace",
        # Botones de mostrar lista
        "cuadricula": "cuadricula",
        "detalles": "detalles",
        "lista": "lista",
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
                size=tamanio_iconos,
            )
        except Exception as e:
            print(f"Error al cargar el icono {nombre}: {e}")
            iconos[nombre] = None
    return iconos


# Método para cargar un único icono con tamaño personalizado
def cargar_icono_personalizado(nombre, tema="claro", tamanio=None):
    try:
        # Determinar si el icono requiere tema
        if nombre in ["me_gusta_rojo", "favorito_amarillo"]:
            ruta_iconos = obtener_ruta_iconos(nombre, None)
        else:
            ruta_iconos = obtener_ruta_iconos(nombre, tema)
        # Usar tamaño predeterminado si no se especifica
        tamanio_icono = tamanio if tamanio else (ANCHO_IMAGEN, ALTO_IMAGEN)
        # Cargar el icono
        return ctk.CTkImage(
            light_image=Image.open(ruta_iconos),
            dark_image=Image.open(ruta_iconos),
            size=tamanio_icono,
        )
    except Exception as e:
        print(f"Error al cargar el icono personalizado {nombre}: {e}")
        return None


# Método para obtener la ruta de los iconos de la aplicación
def establecer_icono_tema(ventana, tema="claro"):
    try:
        # Para Windows
        if tema == "claro":
            # Si el tema es claro, ponemos el icono oscuro
            ventana.iconbitmap(RUTA_ICONO_APLICACION_OSCURO.replace(".png", ".ico"))
        else:
            # Si el tema es oscuro, ponemos el icono claro
            ventana.iconbitmap(RUTA_ICONO_APLICACION_CLARO.replace(".png", ".ico"))
    except Exception as e:
        print(f"Error al establecer el icono de la ventana: {e}")
        # Para otros sistemas o como respaldo usando PhotoImage
        if tema == "claro":
            # Si el tema es claro, ponemos el icono oscuro
            icono = tk.PhotoImage(file=RUTA_ICONO_APLICACION_OSCURO)
        else:
            # Si el tema es oscuro, ponemos el icono claro
            icono = tk.PhotoImage(file=RUTA_ICONO_APLICACION_CLARO)
        ventana.iconphoto(True, icono)


# Método para crear un tooltip en un componente de la aplicación
def crear_tooltip(componente, texto):
    # Guardar referencia al tooltip en el diccionario
    tooltip = ToolTip(componente, texto)
    lista_tooltips[componente] = tooltip
    return tooltip


# Método para actualizar el texto de un tooltip existente
def actualizar_texto_tooltip(componente, nuevo_texto):
    if componente in lista_tooltips:
        # Si el tooltip existe, actualizar su texto
        lista_tooltips[componente].texto_componente = nuevo_texto
    else:
        # Si no existe, crear uno nuevo
        crear_tooltip(componente, nuevo_texto)


# Método para eliminar un tooltip existente
def eliminar_tooltip():
    # Ocultar tooltips visibles antes de mostrar detalles
    for _, tooltip_existente in lista_tooltips.items():
        if tooltip_existente and tooltip_existente.tooltip is not None:
            try:
                if tooltip_existente.tooltip.winfo_exists():
                    tooltip_existente.tooltip.destroy()
                    tooltip_existente.tooltip = None
            except Exception as e:
                print(f"Error al eliminar tooltip: {e}")
                tooltip_existente.tooltip = None
