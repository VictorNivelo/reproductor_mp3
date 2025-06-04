from controlador.controlador_reproductor import ControladorReproductor
from controlador.controlador_biblioteca import ControladorBiblioteca
from vista.componentes.cola_reproduccion import ColaReproduccion
from controlador.controlador_archivos import ControladorArchivos
from vista.componentes.mini_reproductor import MiniReproductor
from vista.componentes.configuracion import Configuracion
from controlador.controlador_tema import ControladorTema
from vista.componentes.estadisticas import Estadisticas
from vista.utiles.utiles_atajos import GestorAtajos
from vista.utiles.utiles_scroll import GestorScroll
from vista.componentes.atajos import Atajos
from modelo.biblioteca import Biblioteca
from vista.utiles.utiles_vista import *
from animacion import AnimacionGeneral
from utiles import UtilesGeneral
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
from constantes import *
import tkinter as tk
import random
import math

# FUNCIONES DE LOS BOTONES

# ========================= Variables de estado ==========================
# Estados de los botones
ESTADO_REPRODUCCION = False
ESTADO_SILENCIO = False
PANEL_LATERAL_VISIBLE = True
MODO_ALEATORIO = True
MODO_REPETICION = 0
NIVEL_VOLUMEN = 100
ME_GUSTA = False
FAVORITO = False

# Estado de la barra de progreso
ARRASTRANDO_PROGRESO = False
DURACION_TOTAL = 0
TIEMPO_ACTUAL = 0

# Estado de la animación del espectro
ANIMACION_ESPECTRO_ACTIVA = False
# ========================================================================

# Diccionario para almacenar los botones de canciones
botones_canciones = {}
botones_opciones_canciones = {}
vista_detalle_activa = False
vista_detalle_tipo = None
vista_detalle_elemento = None
vista_detalle_canvas = None
vista_detalle_panel = None
pestanas_cargadas = {
    "Canciones": True,
    "Me gusta": False,
    "Favoritos": False,
    "Álbumes": False,
    "Artistas": False,
    "Listas": False,
}


# Método para actualizar el tooltip
def actualizar_tooltip_vista():
    # Actualizar todos los tooltips visibles
    for _, tooltip_existente in lista_tooltips.items():
        if tooltip_existente.tooltip and tooltip_existente.tooltip.winfo_exists():
            tooltip_existente.actualizar_colores_tooltip()


# Función para cambiar el tema de la interfaz
def cambiar_tema_vista():
    # Ocultar cualquier tooltip activo antes del cambio de tema
    eliminar_tooltip()
    # Cambiar el tema
    controlador_tema.cambiar_tema_controlador()
    # Actualizar el icono del tema en la ventana
    cambiar_icono_tema(controlador_tema.tema_interfaz)
    # Actualizar todos los iconos
    actualizar_iconos()
    # Actualizar tooltips después del cambio de tema
    actualizar_tooltip_vista()
    # Actualizar tooltips existentes con el nuevo tema
    actualizar_tooltips_tema()
    # Guardar configuración
    guardar_todos_ajustes()


# Función para establecer el icono del tema
def cambiar_icono_tema(tema="claro"):
    try:
        # El icono debe ser opuesto al tema de la interfaz
        if tema == "oscuro":
            # Si el tema es oscuro, usar icono claro
            ruta_icono = RUTA_ICONO_APLICACION_CLARO_ICO
        else:
            # Si el tema es claro, usar icono oscuro
            ruta_icono = RUTA_ICONO_APLICACION_OSCURO_ICO
        # Verificar que el archivo existe
        if os.path.exists(ruta_icono):
            ventana_principal.iconbitmap(ruta_icono)
        else:
            print(f"Advertencia: No se encontró el icono en {ruta_icono}")
    except Exception as e:
        print(f"Error al cambiar el icono de la ventana: {e}")


# Función para cambiar el tema de la interfaz
def actualizar_iconos():
    # Estado de reproducción
    icono_reproduccion = "pausa" if ESTADO_REPRODUCCION else "reproducir"
    controlador_tema.registrar_botones(icono_reproduccion, boton_reproducir)
    # Orden de reproducción
    icono_orden = "aleatorio" if MODO_ALEATORIO else "orden"
    controlador_tema.registrar_botones(icono_orden, boton_aleatorio)
    # Repetición
    if MODO_REPETICION == 0:
        icono_repeticion = "no_repetir"
    elif MODO_REPETICION == 1:
        icono_repeticion = "repetir_actual"
    else:
        icono_repeticion = "repetir_todo"
    controlador_tema.registrar_botones(icono_repeticion, boton_repetir)
    # Volumen
    if ESTADO_SILENCIO:
        icono_volumen = "silencio"
    else:
        if NIVEL_VOLUMEN == 0:
            icono_volumen = "sin_volumen"
        elif NIVEL_VOLUMEN <= 33:
            icono_volumen = "volumen_bajo"
        elif NIVEL_VOLUMEN <= 66:
            icono_volumen = "volumen_medio"
        else:
            icono_volumen = "volumen_alto"
    # Panel visible
    if PANEL_LATERAL_VISIBLE:
        controlador_tema.registrar_botones("ocultar", boton_visibilidad)
    else:
        controlador_tema.registrar_botones("mostrar", boton_visibilidad)
    controlador_tema.registrar_botones(icono_volumen, boton_silenciar)
    # Me gusta y favoritos
    icono_me_gusta = "me_gusta_rojo" if ME_GUSTA else "me_gusta"
    icono_favorito = "favorito_amarillo" if FAVORITO else "favorito"
    controlador_tema.registrar_botones(icono_me_gusta, boton_me_gusta)
    controlador_tema.registrar_botones(icono_favorito, boton_favorito)
    # Tema
    icono_tema = "modo_claro" if APARIENCIA == "oscuro" else "modo_oscuro"
    controlador_tema.registrar_botones(icono_tema, boton_tema)
    # Actualizar también el tooltip del botón de tema
    tooltip_tema = "Cambiar a claro" if APARIENCIA == "oscuro" else "Cambiar a oscuro"
    actualizar_texto_tooltip(boton_tema, tooltip_tema)
    # Actualizar iconos en botones de opciones para todas las canciones
    for cancion, boton in botones_canciones.items():
        # Buscar el botón de opciones asociado y actualizar su icono
        frame_padre = boton.winfo_parent()
        if frame_padre:
            frame = boton.nametowidget(frame_padre)
            if frame and frame.winfo_exists():
                # Buscar el botón de opciones dentro del frame
                for componente in frame.winfo_children():
                    if isinstance(componente, ctk.CTkButton) and componente != boton:
                        # Actualizar el icono del botón de opciones
                        icono_opcion = cargar_icono_con_tamanio(
                            "opcion", controlador_tema.tema_iconos, (15, 20)
                        )
                        componente.configure(image=icono_opcion)
    # Actualizar el porcentaje de volumen
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")


# Función para guardar todos los ajustes
def guardar_todos_ajustes():
    configuracion_guardada = {
        "apariencia": APARIENCIA,
        "nivel_volumen": NIVEL_VOLUMEN,
        "modo_aleatorio": MODO_ALEATORIO,
        "modo_repeticion": MODO_REPETICION,
        "estado_silenciado": ESTADO_SILENCIO,
        "panel_lateral_visible": PANEL_LATERAL_VISIBLE,
    }
    controlador_archivos.guardar_ajustes_json_controlador(configuracion_guardada)


# Función para cargar todos los ajustes
def cargar_todos_ajustes():
    global APARIENCIA, NIVEL_VOLUMEN, MODO_ALEATORIO, MODO_REPETICION, ESTADO_SILENCIO, PANEL_LATERAL_VISIBLE
    # Cargar configuración desde archivo
    configuracion_cargada = controlador_archivos.cargar_ajustes_json_controlador()
    # Aplicar valores a las variables globales
    APARIENCIA = configuracion_cargada.get("apariencia", "claro")
    NIVEL_VOLUMEN = configuracion_cargada.get("nivel_volumen", 100)
    MODO_ALEATORIO = configuracion_cargada.get("modo_aleatorio", False)
    MODO_REPETICION = configuracion_cargada.get("modo_repeticion", 0)
    ESTADO_SILENCIO = configuracion_cargada.get("estado_silenciado", False)
    PANEL_LATERAL_VISIBLE = configuracion_cargada.get("panel_lateral_visible", True)
    # Ajustar tema
    controlador_tema.tema_interfaz = APARIENCIA
    controlador_tema.tema_iconos = "claro" if APARIENCIA == "oscuro" else "oscuro"
    ctk.set_appearance_mode("dark" if APARIENCIA == "oscuro" else "light")
    # Establecer el icono correcto según el tema cargado
    cambiar_icono_tema(APARIENCIA)
    # Ajustar volumen
    barra_volumen.set(NIVEL_VOLUMEN)
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)
    # Ajustar orden de reproducción
    controlador_reproductor.modo_orden_controlador(MODO_ALEATORIO)
    # Ajustar modo de repetición
    controlador_reproductor.modo_repeticion_controlador(MODO_REPETICION)
    # Ajustar panel visible
    if not PANEL_LATERAL_VISIBLE:
        cambiar_visibilidad_vista()
    # Actualizar todos los iconos según los estados cargados
    actualizar_iconos()
    # Recargar los colores del tema
    controlador_tema.colores()
    # Actualizar el tema de la interfaz
    controlador_tema.cambiar_tema_controlador()
    # Actualizar el tema de la interfaz forzando la actualización
    controlador_tema.cambiar_tema_controlador()


# Función para cargar la última canción reproducida
def cargar_ultima_cancion_reproducida():
    ultima_cancion_info = controlador_archivos.ultima_reproducida_json_controlador()
    if ultima_cancion_info:
        # Buscar la canción
        ruta_cancion = Path(ultima_cancion_info["ruta"])
        todas_canciones = controlador_biblioteca.obtener_todas_canciones_controlador()
        for cancion in todas_canciones:
            if str(cancion.ruta_cancion) == str(ruta_cancion):
                # Añadir la canción a la cola sin reproducirla
                if (
                    controlador_reproductor.lista_reproduccion == []
                    or cancion not in controlador_reproductor.lista_reproduccion
                ):
                    controlador_reproductor.lista_reproduccion = [cancion]
                    controlador_reproductor.indice_actual = 0
                    controlador_reproductor.cancion_actual = cancion
                # Actualizar la interfaz sin reproducir
                controlador_reproductor.actualizar_informacion_controlador()
                # Actualizar estado de los botones de me_gusta/favorito
                actualizar_estado_botones_gustos()
                return True
    return False


# Función para verificar el estado de reproducción
def verificar_estado_reproduccion(*args):
    global ESTADO_REPRODUCCION
    # Verificar si la reproducción ha terminado naturalmente
    if ESTADO_REPRODUCCION and not controlador_reproductor.reproduciendo:
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
    # Llamar a esta función nuevamente después de un breve retraso
    ventana_principal.after(500, verificar_estado_reproduccion, *args)


# Función para actualizar el estado de reproducción en la vista
def actualizar_estado_reproduccion_vista():
    global ESTADO_REPRODUCCION
    # Obtener el estado real del reproductor
    estado_actual = controlador_reproductor.reproduciendo
    # Actualizar variable global
    ESTADO_REPRODUCCION = estado_actual
    # Actualizar icono en interfaz principal
    if ESTADO_REPRODUCCION:
        controlador_tema.registrar_botones("pausa", boton_reproducir)
        actualizar_texto_tooltip(boton_reproducir, "Pausar")
    else:
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
        actualizar_texto_tooltip(boton_reproducir, "Reproducir")
    # Actualizar mini reproductor si está visible
    if (
        mini_reproductor.ventana_principal_mini_reproductor
        and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
    ):
        if ESTADO_REPRODUCCION:
            controlador_tema.registrar_botones("pausa_mini", mini_reproductor.boton_reproducir_mini)
        else:
            controlador_tema.registrar_botones("reproducir_mini", mini_reproductor.boton_reproducir_mini)
    # Iniciar o detener la animación del espectro
    global ANIMACION_ESPECTRO_ACTIVA
    if ESTADO_REPRODUCCION and not ANIMACION_ESPECTRO_ACTIVA:
        ANIMACION_ESPECTRO_ACTIVA = True
        actualizar_espectro()
    return ESTADO_REPRODUCCION


# Función para reproducir o pausar la canción
def reproducir_vista():
    global ESTADO_REPRODUCCION, ANIMACION_ESPECTRO_ACTIVA
    if not ESTADO_REPRODUCCION:
        # Verificar si hay una canción en la cola para reproducir
        if controlador_reproductor.reproducir_o_reanudar_controlador():
            # Actualizar estado e iconos usando la función centralizada
            actualizar_estado_reproduccion_vista()
    else:
        # Pausar reproducción
        controlador_reproductor.pausar_reproduccion_controlador()
        # Actualizar estado e iconos usando la función centralizada
        actualizar_estado_reproduccion_vista()


# Función para reproducir un álbum completo
def reproducir_album_completo(album):
    canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(album)
    if canciones_album:
        # Establecer la cola con todas las canciones del álbum y reproducir la primera
        controlador_reproductor.establecer_cola_reproduccion_controlador(canciones_album, 0)
        controlador_reproductor.reproducir_cancion_controlador(canciones_album[0])
        actualizar_estado_reproduccion_vista()
        actualizar_estado_botones_gustos()
        for cancion_item in canciones_album:  # Registrar reproducción de todas
            controlador_archivos.registrar_reproduccion_json_controlador(cancion_item)


# Función para reproducir un artista completo
def reproducir_artista_completo(artista):
    canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista)
    if canciones_artista:
        # Establecer la cola con todas las canciones del artista y reproducir la primera
        controlador_reproductor.establecer_cola_reproduccion_controlador(canciones_artista, 0)
        controlador_reproductor.reproducir_cancion_controlador(canciones_artista[0])
        actualizar_estado_reproduccion_vista()
        actualizar_estado_botones_gustos()
        for cancion_item in canciones_artista:  # Registrar reproducción de todas
            controlador_archivos.registrar_reproduccion_json_controlador(cancion_item)


# Función para reproducir la canción seleccionada
def reproducir_desde_lista_vista(cancion):
    global ESTADO_REPRODUCCION, ANIMACION_ESPECTRO_ACTIVA
    todas_canciones = controlador_biblioteca.obtener_todas_canciones_controlador()
    indice_cancion = todas_canciones.index(cancion)
    # Establecer la lista de reproducción actual
    controlador_reproductor.establecer_cola_reproduccion_controlador(todas_canciones, indice_cancion)
    # Reproducir la canción
    controlador_reproductor.reproducir_cancion_controlador(cancion)
    # Registrar la reproducción en las estadísticas
    controlador_archivos.registrar_reproduccion_json_controlador(cancion)
    # Actualizar estado usando la función centralizada
    actualizar_estado_reproduccion_vista()
    # Actualizar botones de Me Gusta y Favoritos
    actualizar_estado_botones_gustos()


# Función para actualizar el estado de reproducción desde la cola
def reproducir_desde_cola_vista():
    # Usar la función centralizada para actualizar el estado
    actualizar_estado_reproduccion_vista()
    # Actualizar botones de Me Gusta y Favoritos
    actualizar_estado_botones_gustos()


# Función para reproducir la canción siguiente
def reproducir_siguiente_vista():
    global ESTADO_REPRODUCCION, ANIMACION_ESPECTRO_ACTIVA
    resultado = controlador_reproductor.reproducir_siguiente_controlador()
    if resultado:
        # Canción reproducida exitosamente
        actualizar_estado_botones_gustos()
    else:
        # No se pudo reproducir la siguiente (fin de lista)
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
        actualizar_texto_tooltip(boton_reproducir, "Reproducir")


# Función para reproducir la canción anterior
def reproducir_anterior_vista():
    if controlador_reproductor.reproducir_anterior_controlador():
        # Canción reproducida exitosamente
        actualizar_estado_botones_gustos()


# Función para adelantar la reproducción
def adelantar_reproduccion_vista():
    controlador_reproductor.adelantar_reproduccion_controlador(TIEMPO_AJUSTE)
    # Actualizar tooltip con el valor actual
    crear_tooltip(boton_adelantar, f"Adelanta {TIEMPO_AJUSTE} segundos")


# Función para retroceder la reproducción
def retroceder_reproduccion_vista():
    controlador_reproductor.retroceder_reproduccion_controlador(TIEMPO_AJUSTE)
    # Actualizar tooltip con el valor actual
    crear_tooltip(boton_retroceder, f"Retrocede {TIEMPO_AJUSTE} segundos")


# Función para aumentar el volumen en incrementos fijos
def aumentar_volumen_vista():
    global NIVEL_VOLUMEN, ESTADO_SILENCIO
    # Sí está silenciado, primero quitar el silencio
    if ESTADO_SILENCIO:
        actualizar_estado_silencio_vista(False)
    # Calcular el nuevo nivel de volumen (máximo 100)
    NIVEL_VOLUMEN = min(100, NIVEL_VOLUMEN + AUMENTO_VOLUMEN)
    # Actualizar la barra de volumen visual
    barra_volumen.set(NIVEL_VOLUMEN)
    # Actualizar la etiqueta del porcentaje
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    # Ajustar el volumen real
    controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN)
    # Actualizar los iconos según el nuevo nivel
    actualizar_iconos()
    # Guardar los ajustes
    guardar_todos_ajustes()


# Función para disminuir el volumen en incrementos fijos
def disminuir_volumen_vista():
    global NIVEL_VOLUMEN
    # Calcular el nuevo nivel de volumen (mínimo 0)
    NIVEL_VOLUMEN = max(0, NIVEL_VOLUMEN - AUMENTO_VOLUMEN)
    # Actualizar la barra de volumen visual
    barra_volumen.set(NIVEL_VOLUMEN)
    # Actualizar la etiqueta del porcentaje
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    # Si el volumen llega a cero, activar silencio
    if NIVEL_VOLUMEN == 0:
        actualizar_estado_silencio_vista(True)
    else:
        # Ajustar el volumen real
        controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN)
        # Actualizar los iconos según el nuevo nivel
        actualizar_iconos()
    # Guardar los ajustes
    guardar_todos_ajustes()


# Función para cambiar el volumen
def cambiar_volumen_vista(_event=None):
    global NIVEL_VOLUMEN, ESTADO_SILENCIO
    NIVEL_VOLUMEN = int(barra_volumen.get())
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    # Si el volumen es ajustado manualmente, desactivamos el silencio
    if ESTADO_SILENCIO and NIVEL_VOLUMEN > 0:
        # Usar la función centralizada para quitar el silencio
        actualizar_estado_silencio_vista(False)
    else:
        # Ajustamos el volumen real sin cambiar el estado de silencio
        controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)
        # Actualizamos el icono sin cambiar el estado
        actualizar_iconos()
    # Guardamos los ajustes
    guardar_todos_ajustes()


# Función centralizada para actualizar el estado de silencio en todas las interfaces
def actualizar_estado_silencio_vista(silenciar=None):
    global ESTADO_SILENCIO
    # Si se especifica un estado, actualizar la variable global
    if silenciar is not None:
        ESTADO_SILENCIO = silenciar
    # Actualizar el volumen real según el estado
    if ESTADO_SILENCIO:
        # Silenciar el reproductor pero conservar el valor del volumen
        controlador_reproductor.ajustar_volumen_controlador(0)
        # Actualizar icono en interfaz principal
        controlador_tema.registrar_botones("silencio", boton_silenciar)
        actualizar_texto_tooltip(boton_silenciar, "Quitar silencio")
    else:
        # Restaurar el volumen anterior
        controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN)
        actualizar_texto_tooltip(boton_silenciar, "Silenciar")
        # Determinar el icono de volumen según el nivel actual
        if NIVEL_VOLUMEN == 0:
            icono_volumen = "sin_volumen"
        elif NIVEL_VOLUMEN <= 33:
            icono_volumen = "volumen_bajo"
        elif NIVEL_VOLUMEN <= 66:
            icono_volumen = "volumen_medio"
        else:
            icono_volumen = "volumen_alto"
        controlador_tema.registrar_botones(icono_volumen, boton_silenciar)
    # Actualizar mini reproductor si está visible y tiene botón de silencio
    if (
        mini_reproductor.ventana_principal_mini_reproductor
        and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
        and hasattr(mini_reproductor, "boton_silenciar_mini")
    ):
        if ESTADO_SILENCIO:
            controlador_tema.registrar_botones("silencio_mini", mini_reproductor.boton_silenciar_mini)
        else:
            # Usar el mismo icono de volumen pero con el sufijo _mini
            if NIVEL_VOLUMEN == 0:
                icono_mini = "sin_volumen_mini"
            elif NIVEL_VOLUMEN <= 33:
                icono_mini = "volumen_bajo_mini"
            elif NIVEL_VOLUMEN <= 66:
                icono_mini = "volumen_medio_mini"
            else:
                icono_mini = "volumen_alto_mini"
            controlador_tema.registrar_botones(icono_mini, mini_reproductor.boton_silenciar_mini)
    # Guardar el cambio en los ajustes
    guardar_todos_ajustes()
    return ESTADO_SILENCIO


# Función para cambiar el estado de silencio
def cambiar_silencio_vista():
    global ESTADO_SILENCIO
    # Invertir el estado actual
    nuevo_estado = not ESTADO_SILENCIO
    # Utilizar la función centralizada para actualizar el estado
    actualizar_estado_silencio_vista(nuevo_estado)


# Función centralizada para actualizar el estado del modo aleatorio en todas las interfaces
def actualizar_estado_aleatorio_vista(modo=None):
    global MODO_ALEATORIO
    # Si se especifica un modo, actualizar la variable global
    if modo is not None:
        MODO_ALEATORIO = modo
        # Informar al controlador sobre el cambio en el modo de reproducción
        controlador_reproductor.modo_orden_controlador(MODO_ALEATORIO)
    # Actualizar icono en interfaz principal según el modo actual
    if MODO_ALEATORIO:
        controlador_tema.registrar_botones("aleatorio", boton_aleatorio)
        actualizar_texto_tooltip(boton_aleatorio, "Reproducción aleatoria")
    else:
        controlador_tema.registrar_botones("orden", boton_aleatorio)
        actualizar_texto_tooltip(boton_aleatorio, "Reproducción en orden")
    # Guardar el cambio en los ajustes
    guardar_todos_ajustes()
    return MODO_ALEATORIO


# Función para cambiar el orden de reproducción
def cambiar_orden_vista():
    global MODO_ALEATORIO
    # Invertir el estado actual
    nuevo_modo = not MODO_ALEATORIO
    # Utilizar la función centralizada para actualizar el estado
    actualizar_estado_aleatorio_vista(nuevo_modo)


# Función centralizada para actualizar el estado del modo de repetición
def actualizar_estado_repeticion_vista(modo=None):
    global MODO_REPETICION
    # Si se especifica un modo, actualizar la variable global
    if modo is not None:
        MODO_REPETICION = modo % 3  # Asegurar que esté en el rango 0-2
        # Informar al controlador sobre el cambio
        controlador_reproductor.modo_repeticion_controlador(MODO_REPETICION)
    # Actualizar icono en interfaz principal según el modo actual
    if MODO_REPETICION == 0:
        controlador_tema.registrar_botones("no_repetir", boton_repetir)
        actualizar_texto_tooltip(boton_repetir, "No repetir")
    elif MODO_REPETICION == 1:
        controlador_tema.registrar_botones("repetir_actual", boton_repetir)
        actualizar_texto_tooltip(boton_repetir, "Repetir actual")
    else:  # MODO_REPETICION == 2
        controlador_tema.registrar_botones("repetir_todo", boton_repetir)
        actualizar_texto_tooltip(boton_repetir, "Repetir todo")
    # Guardar el cambio en los ajustes
    guardar_todos_ajustes()
    return MODO_REPETICION


# Función para cambiar la repetición de reproducción
def cambiar_repeticion_vista():
    global MODO_REPETICION
    # Calcular el siguiente modo
    nuevo_modo = (MODO_REPETICION + 1) % 3
    # Utilizar la función centralizada para actualizar el estado
    actualizar_estado_repeticion_vista(nuevo_modo)


# Función para cambiar la visibilidad del panel
def cambiar_visibilidad_vista():
    global PANEL_LATERAL_VISIBLE
    PANEL_LATERAL_VISIBLE = not PANEL_LATERAL_VISIBLE
    if PANEL_LATERAL_VISIBLE:
        # Mostrar el panel
        contenedor_derecha_principal.configure(width=ANCHO_PANEL_DERECHA + 5)
        contenedor_derecha_principal.pack(side="left", fill="both", padx=(5, 0))
        controlador_tema.registrar_botones("ocultar", boton_visibilidad)
        actualizar_texto_tooltip(boton_visibilidad, "Ocultar lateral")
    else:
        # Ocultar el panel
        contenedor_derecha_principal.configure(width=0)
        contenedor_derecha_principal.pack_forget()
        controlador_tema.registrar_botones("mostrar", boton_visibilidad)
        actualizar_texto_tooltip(boton_visibilidad, "Mostrar lateral")
    # Guardar configuración
    guardar_todos_ajustes()


# Función centralizada para actualizar el estado de "Me gusta" en todas las interfaces
def actualizar_estado_me_gusta_vista(cancion=None):
    global ME_GUSTA
    # Si no se especifica una canción, usar la canción actual
    if cancion is None:
        cancion = controlador_reproductor.cancion_actual
    # Verificar si hay una canción válida
    if cancion:
        # Actualizar el estado global
        ME_GUSTA = cancion.me_gusta
        # Actualizar icono en interfaz principal
        if ME_GUSTA:
            controlador_tema.registrar_botones("me_gusta_rojo", boton_me_gusta)
            actualizar_texto_tooltip(boton_me_gusta, "Quitar de Me gusta")
        else:
            controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
            actualizar_texto_tooltip(boton_me_gusta, "Agregar a Me gusta")
        # Actualizar mini reproductor si está visible
        if (
            mini_reproductor.ventana_principal_mini_reproductor
            and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
        ):
            if ME_GUSTA:
                controlador_tema.registrar_botones("me_gusta_rojo_mini", mini_reproductor.boton_me_gusta_mini)
            else:
                controlador_tema.registrar_botones("me_gusta_mini", mini_reproductor.boton_me_gusta_mini)
        # Actualizar la vista "Me gusta" siempre, sin verificar si está cargada
        actualizar_vista_me_gusta()
    else:
        # Si no hay canción, desactivar los botones
        ME_GUSTA = False
        controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
        actualizar_texto_tooltip(boton_me_gusta, "Agregar a Me gusta")
        if (
            mini_reproductor.ventana_principal_mini_reproductor
            and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
        ):
            controlador_tema.registrar_botones("me_gusta_mini", mini_reproductor.boton_me_gusta_mini)
    return ME_GUSTA


# Función para cambiar el estado de boton me gusta
def agregar_me_gusta_vista(cancion=None):
    # Si no se especifica canción, usar la canción actual
    if cancion is None:
        cancion = controlador_reproductor.cancion_actual
    # Verificar que hay una canción válida
    if not cancion:
        return
    # Modificar el estado
    controlador_biblioteca.agregar_cancion_me_gusta_controlador(cancion)
    # Actualizar interfaz según el contexto
    if controlador_reproductor.cancion_actual == cancion:
        # Es la canción actual, actualizar interfaz completa
        actualizar_estado_me_gusta_vista()
    else:
        # No es la canción actual, solo actualizar la vista de "Me gusta"
        actualizar_vista_me_gusta()
    # Marcar la pestaña como cargada
    pestanas_cargadas["Me gusta"] = True
    # Guardar cambios
    guardar_biblioteca()


# Función para agregar/quitar álbum completo de Me gusta
def agregar_album_me_gusta_vista(album):
    try:
        # Obtener todas las canciones del álbum
        canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(album)
        if not canciones_album:
            print(f"No se encontraron canciones en el álbum: {album}")
            return False
        # Verificar el estado actual del álbum
        album_totalmente_en_me_gusta = all(c.me_gusta for c in canciones_album)
        if album_totalmente_en_me_gusta:
            # Si todas las canciones están en "Me gusta", quitarlas
            for cancion in canciones_album:
                if cancion.me_gusta:
                    controlador_biblioteca.agregar_cancion_me_gusta_controlador(cancion)
            print(f"Álbum quitado de Me gusta: {album}")
        else:
            # Si no todas están en "Me gusta", agregarlas todas
            for cancion in canciones_album:
                if not cancion.me_gusta:
                    controlador_biblioteca.agregar_cancion_me_gusta_controlador(cancion)
            print(f"Álbum agregado a Me gusta: {album}")
        # Guardar cambios
        guardar_biblioteca()
        # Actualizar las vistas si es necesario
        actualizar_vista_me_gusta()
        # Si estamos en vista de detalle del álbum, actualizar
        if vista_detalle_activa and vista_detalle_tipo == "album" and vista_detalle_elemento == album:
            mostrar_canciones_elemento_filtradas(album, "Álbumes", "")
        return True
    except Exception as e:
        print(f"Error al agregar álbum a Me gusta: {e}")
        return False


# Función para agregar/quitar artista completo de Me gusta
def agregar_artista_me_gusta_vista(artista):
    try:
        # Obtener todas las canciones del artista
        canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista)
        if not canciones_artista:
            print(f"No se encontraron canciones del artista: {artista}")
            return False
        # Verificar el estado actual del artista
        artista_totalmente_en_me_gusta = all(c.me_gusta for c in canciones_artista)
        if artista_totalmente_en_me_gusta:
            # Si todas las canciones están en "Me gusta", quitarlas
            for cancion in canciones_artista:
                if cancion.me_gusta:
                    controlador_biblioteca.agregar_cancion_me_gusta_controlador(cancion)
            print(f"Artista quitado de Me gusta: {artista}")
        else:
            # Si no todas están en "Me gusta", agregarlas todas
            for cancion in canciones_artista:
                if not cancion.me_gusta:
                    controlador_biblioteca.agregar_cancion_me_gusta_controlador(cancion)
            print(f"Artista agregado a Me gusta: {artista}")
        # Guardar cambios
        guardar_biblioteca()
        # Actualizar las vistas si es necesario
        actualizar_vista_me_gusta()
        # Si estamos en vista de detalle del artista, actualizar
        if vista_detalle_activa and vista_detalle_tipo == "artista" and vista_detalle_elemento == artista:
            mostrar_canciones_elemento_filtradas(artista, "Artistas", "")
        return True
    except Exception as e:
        print(f"Error al agregar artista a Me gusta: {e}")
        return False


# Función centralizada para actualizar el estado de "Favorito" en todas las interfaces
def actualizar_estado_favorito_vista(cancion=None):
    global FAVORITO
    # Si no se especifica una canción, usar la canción actual
    if cancion is None:
        cancion = controlador_reproductor.cancion_actual
    # Verificar si hay una canción válida
    if cancion:
        # Actualizar el estado global
        FAVORITO = cancion.favorito
        # Actualizar icono en interfaz principal
        if FAVORITO:
            controlador_tema.registrar_botones("favorito_amarillo", boton_favorito)
            actualizar_texto_tooltip(boton_favorito, "Quitar de favorito")
        else:
            controlador_tema.registrar_botones("favorito", boton_favorito)
            actualizar_texto_tooltip(boton_favorito, "Agregar a favorito")
        # Actualizar la vista "Favoritos" siempre, sin verificar si está cargada
        actualizar_vista_favoritos()
    else:
        # Si no hay canción, desactivar los botones
        FAVORITO = False
        controlador_tema.registrar_botones("favorito", boton_favorito)
        actualizar_texto_tooltip(boton_favorito, "Agregar a favorito")
    return FAVORITO


# Función para agregar/quitar álbum completo de Favoritos
def agregar_album_favorito_vista(album):
    try:
        # Obtener todas las canciones del álbum
        canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(album)
        if not canciones_album:
            print(f"No se encontraron canciones en el álbum: {album}")
            return False
        # Verificar el estado actual del álbum
        album_totalmente_en_favoritos = all(c.favorito for c in canciones_album)
        if album_totalmente_en_favoritos:
            # Si todas las canciones están en "Favoritos", quitarlas
            for cancion in canciones_album:
                if cancion.favorito:
                    controlador_biblioteca.agregar_cancion_favorito_controlador(cancion)
            print(f"Álbum quitado de Favoritos: {album}")
        else:
            # Si no todas están en "Favoritos", agregarlas todas
            for cancion in canciones_album:
                if not cancion.favorito:
                    controlador_biblioteca.agregar_cancion_favorito_controlador(cancion)
            print(f"Álbum agregado a Favoritos: {album}")
        # Guardar cambios
        guardar_biblioteca()
        # Actualizar las vistas si es necesario
        actualizar_vista_favoritos()
        # Si estamos en vista de detalle del álbum, actualizar
        if vista_detalle_activa and vista_detalle_tipo == "album" and vista_detalle_elemento == album:
            mostrar_canciones_elemento_filtradas(album, "Álbumes", "")
        return True
    except Exception as e:
        print(f"Error al agregar álbum a Favoritos: {e}")
        return False


# Función para agregar/quitar artista completo de Favoritos
def agregar_artista_favorito_vista(artista):
    try:
        # Obtener todas las canciones del artista
        canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista)
        if not canciones_artista:
            print(f"No se encontraron canciones del artista: {artista}")
            return False
        # Verificar el estado actual del artista
        artista_totalmente_en_favoritos = all(c.favorito for c in canciones_artista)
        if artista_totalmente_en_favoritos:
            # Si todas las canciones están en "Favoritos", quitarlas
            for cancion in canciones_artista:
                if cancion.favorito:
                    controlador_biblioteca.agregar_cancion_favorito_controlador(cancion)
            print(f"Artista quitado de Favoritos: {artista}")
        else:
            # Si no todas están en "Favoritos", agregarlas todas
            for cancion in canciones_artista:
                if not cancion.favorito:
                    controlador_biblioteca.agregar_cancion_favorito_controlador(cancion)
            print(f"Artista agregado a Favoritos: {artista}")
        # Guardar cambios
        guardar_biblioteca()
        # Actualizar las vistas si es necesario
        actualizar_vista_favoritos()
        # Si estamos en vista de detalle del artista, actualizar
        if vista_detalle_activa and vista_detalle_tipo == "artista" and vista_detalle_elemento == artista:
            mostrar_canciones_elemento_filtradas(artista, "Artistas", "")
        return True
    except Exception as e:
        print(f"Error al agregar artista a Favoritos: {e}")
        return False


# Función para cambiar el estado de favorito
def agregar_favorito_vista(cancion=None):
    # Si no se especifica canción, usar la canción actual
    if cancion is None:
        cancion = controlador_reproductor.cancion_actual
    # Verificar que hay una canción válida
    if not cancion:
        return
    # Modificar el estado
    controlador_biblioteca.agregar_cancion_favorito_controlador(cancion)
    # Actualizar interfaz según el contexto
    if controlador_reproductor.cancion_actual == cancion:
        # Es la canción actual, actualizar interfaz completa
        actualizar_estado_favorito_vista()
    else:
        # No es la canción actual, solo actualizar la vista de "Favoritos"
        actualizar_vista_favoritos()
    # Marcar la pestaña como cargada
    pestanas_cargadas["Favoritos"] = True
    # Guardar cambios
    guardar_biblioteca()


# Funciona para actualizar el estado de los botones de me_gusta y favorito
def actualizar_estado_botones_gustos():
    # Usar las funciones centralizadas para actualizar ambos estados
    actualizar_estado_me_gusta_vista()
    actualizar_estado_favorito_vista()


# Función para agregar canciones (puede ser llamada desde un botón)
def agregar_cancion_vista():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar archivo de música",
        initialdir=RUTA_CARPETA_MUSICA,
        filetypes=[
            ("Archivos de audio", "*.mp3 *.flac *.m4a *.mp4 *.wav *.ogg"),
            ("Todos los archivos", "*.*"),
        ],
    )
    canciones_agregadas = []
    for ruta in rutas:
        cancion = controlador_biblioteca.agregar_cancion_controlador(Path(ruta))
        if cancion:
            canciones_agregadas.append(cancion)
    if canciones_agregadas:
        # Limpiar el diccionario de botones para evitar referencias obsoletas
        botones_canciones.clear()
        botones_opciones_canciones.clear()
        # Marcar todas las pestañas como no cargadas para forzar reconstrucción completa
        for pestana in pestanas_cargadas:
            pestanas_cargadas[pestana] = False
        # Actualizar todas las vistas
        actualizar_todas_vistas_canciones()
        guardar_biblioteca()
        # Restaurar el binding de scroll según la pestaña actual
        actualizar_pestana_seleccionada()


# Función para agregar directorio (puede ser llamada desde un botón)
def agregar_directorio_vista():
    ruta = filedialog.askdirectory(title="Seleccionar directorio de música", initialdir=RUTA_CARPETA_MUSICA)
    if ruta:
        controlador_biblioteca.agregar_directorio_controlador(Path(ruta))
        # Limpiar el diccionario de botones para evitar referencias obsoletas
        botones_canciones.clear()
        botones_opciones_canciones.clear()
        # Marcar todas las pestañas como no cargadas para forzar reconstrucción completa
        for pestana in pestanas_cargadas:
            pestanas_cargadas[pestana] = False
        # Actualizar todas las vistas
        actualizar_todas_vistas_canciones()
        guardar_biblioteca()
        # Restaurar el binding de scroll según la pestaña actual
        actualizar_pestana_seleccionada()


# Función para agregar una canción al inicio de la cola de reproducción
def agregar_inicio_cola_vista(cancion):
    # Usar el método del controlador para agregar la canción después de la actual
    if controlador_reproductor.agregar_cancion_inicio_cola_controlador(cancion):
        # Mostrar mensaje de confirmación
        print(f"Se ha agregado después de la canción actual: {cancion.titulo_cancion}")
        # Si la ventana de cola está abierta, actualizarla
        if (
            hasattr(cola_reproduccion, "ventana_cola")
            and cola_reproduccion.ventana_cola
            and cola_reproduccion.ventana_cola.winfo_exists()
        ):
            cola_reproduccion.actualizar_ventana_cola()
    else:
        print(f"No se pudo agregar después de la canción actual: {cancion.titulo_cancion}")


# Función para agregar una canción al final de la cola de reproducción
def agregar_fin_cola_vista(cancion):
    # Usar el método del controlador para agregar la canción al final de la cola
    if controlador_reproductor.agregar_cancion_final_cola_controlador(cancion):
        # Mostrar mensaje de confirmación
        print(f"Se ha agregado a la cola: {cancion.titulo_cancion}")
        # Si la ventana de cola está abierta, actualizarla
        if (
            hasattr(cola_reproduccion, "ventana_cola")
            and cola_reproduccion.ventana_cola
            and cola_reproduccion.ventana_cola.winfo_exists()
        ):
            cola_reproduccion.actualizar_ventana_cola()
    else:
        print(f"No se pudo agregar a la cola: {cancion.titulo_cancion}")


# Función para agregar un álbum completo al inicio de la cola
def agregar_album_inicio_cola(album):
    canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(album)
    if canciones_album:
        # Agregar en orden inverso para que la primera canción del álbum quede después de la actual
        for cancion_item in reversed(canciones_album):
            agregar_inicio_cola_vista(cancion_item)
        print(f"Álbum '{album}' agregado al inicio de la cola.")


# Función para agregar un álbum completo al inicio de la cola
def agregar_album_fin_cola(album):
    canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(album)
    if canciones_album:
        for cancion_item in canciones_album:
            agregar_fin_cola_vista(cancion_item)
        print(f"Álbum '{album}' agregado al final de la cola.")


# Función para agregar un artista completo al inicio de la cola
def agregar_artista_inicio_cola(artista):
    canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista)
    if canciones_artista:
        # Agregar en orden inverso para que la primera canción del artista quede después de la actual
        for cancion_item in reversed(canciones_artista):
            agregar_inicio_cola_vista(cancion_item)
        print(f"Artista '{artista}' agregado al inicio de la cola.")


# Función para agregar un artista completo al final de la cola
def agregar_artista_fin_cola(artista):
    canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista)
    if canciones_artista:
        for cancion_item in canciones_artista:
            agregar_fin_cola_vista(cancion_item)
        print(f"Artista '{artista}' agregado al final de la cola.")


# Función para manejar reproducción activa al eliminar canción
def detener_reproduccion_si_cancion_activa(cancion):
    if controlador_reproductor.cancion_actual == cancion:
        controlador_reproductor.detener_reproduccion_controlador()
        controlador_reproductor.cancion_actual = None
        controlador_reproductor.actualizar_informacion_controlador()
        return True
    return False


# Función para limpiar canción de cola y colecciones
def limpiar_cancion_colecciones(cancion):
    # Eliminar de la cola de reproducción
    if cancion in controlador_reproductor.lista_reproduccion:
        indice_actual = controlador_reproductor.indice_actual
        indice_cancion = controlador_reproductor.lista_reproduccion.index(cancion)
        controlador_reproductor.lista_reproduccion.remove(cancion)
        # Ajustar índices
        if indice_cancion <= indice_actual and indice_actual > 0:
            controlador_reproductor.indice_actual -= 1
        elif len(controlador_reproductor.lista_reproduccion) == 0:
            controlador_reproductor.indice_actual = -1
        controlador_archivos.guardar_cola_reproduccion_json_controlador(controlador_reproductor)
    # Limpiar estados de me_gusta y favorito
    controlador_biblioteca.eliminar_cancion_biblioteca_controlador(cancion)


# Función para actualizar interfaz después de eliminar canción
def reconstruir_interfaz_despues_eliminar_cancion(cancion):
    # Limpiar referencias de UI
    if cancion in botones_canciones:
        if botones_canciones[cancion].winfo_exists():
            botones_canciones[cancion].destroy()
        del botones_canciones[cancion]
    # Marcar pestañas para reconstrucción
    for pestana in pestanas_cargadas:
        pestanas_cargadas[pestana] = False
    # Reconstruir vista actual
    pestana_actual = paginas_canciones.get()
    if pestana_actual == "Canciones":
        for componente in panel_botones_canciones.winfo_children():
            componente.destroy()
        actualizar_vista_canciones(panel_botones_canciones)
    elif pestana_actual == "Me gusta":
        configurar_interfaz_me_gusta()
    elif pestana_actual == "Favoritos":
        configurar_interfaz_favoritos()
    elif pestana_actual == "Álbumes":
        configurar_interfaz_albumes()
    elif pestana_actual == "Artistas":
        configurar_interfaz_artistas()


# Función principal para eliminar una canción
def eliminar_cancion_vista(cancion):
    # Manejar si está reproduciéndose
    detener_reproduccion_si_cancion_activa(cancion)
    # Limpiar de todas las colecciones
    limpiar_cancion_colecciones(cancion)
    # Guardar cambios
    guardar_biblioteca()
    # Actualizar interfaz
    reconstruir_interfaz_despues_eliminar_cancion(cancion)
    # Mensaje de confirmación
    print(f"Se ha eliminado: {cancion.titulo_cancion}")


# Función para actualizar el progreso de la canción
def actualizar_progreso_vista(event):
    global TIEMPO_ACTUAL
    # Obtener dimensiones y calcular posición
    ancho_total = barra_progreso.winfo_width()
    posicion_relativa = max(0, min(1, event.x / ancho_total))
    # Actualizar barra de progreso
    barra_progreso.set(posicion_relativa)
    # Calcular y actualizar tiempo
    TIEMPO_ACTUAL = int(DURACION_TOTAL * posicion_relativa)
    actualizar_etiqueta_tiempo_vista()


# Función para actualizar la etiqueta de tiempo
def actualizar_etiqueta_tiempo_vista():
    # Convertir segundos a formato mm:ss
    minutos_actual = TIEMPO_ACTUAL // 60
    segundos_actual = TIEMPO_ACTUAL % 60
    minutos_total = DURACION_TOTAL // 60
    segundos_total = DURACION_TOTAL % 60
    # Actualizar etiquetas
    etiqueta_tiempo_actual.configure(text=f"{minutos_actual:02d}:{segundos_actual:02d}")
    etiqueta_tiempo_total.configure(text=f"{minutos_total:02d}:{segundos_total:02d}")


# Función para iniciar el arrastre del progreso de la canción
def iniciar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = True
    actualizar_progreso_vista(event)


# Función para arrastrar el progreso de la canción
def durante_arrastre_progreso(event):
    if ARRASTRANDO_PROGRESO:
        actualizar_progreso_vista(event)


# Función para finalizar el arrastre del progreso
def finalizar_arrastre_progreso(event):
    global ARRASTRANDO_PROGRESO
    ARRASTRANDO_PROGRESO = False
    actualizar_progreso_vista(event)


# Función para guardar las canciones cuando ocurren cambios
def guardar_biblioteca():
    controlador_archivos.guardar_biblioteca_json_controlador(biblioteca, controlador_reproductor)


# Función para cargar las canciones al iniciar
def cargar_biblioteca_vista():
    if controlador_archivos.cargar_biblioteca_json_controlador(biblioteca):
        # Cargar ajustes primero para tener el tema correcto
        cargar_todos_ajustes()
        # Actualizar vista principal de canciones
        actualizar_vista_canciones(panel_botones_canciones)
        # Configurar eventos para las pestañas (solo cargar cuando se seleccionan)
        paginas_canciones.configure(command=actualizar_pestana_seleccionada)
        # Reiniciar estado de las pestañas
        for key in pestanas_cargadas:
            pestanas_cargadas[key] = False


# Función para cargar la cola de reproducción guardada
def cargar_cola_vista():
    # Cargar la cola de reproducción
    controlador_archivos.cargar_cola_reproduccion_json_controlador(controlador_reproductor, biblioteca)
    # Sí hay canciones en la cola, actualizar la interfaz
    if controlador_reproductor.lista_reproduccion:
        # Establecer la canción actual sin reproducirla automáticamente
        indice = controlador_reproductor.indice_actual
        if 0 <= indice < len(controlador_reproductor.lista_reproduccion):
            controlador_reproductor.cancion_actual = controlador_reproductor.lista_reproduccion[indice]
            controlador_reproductor.actualizar_informacion_controlador()
            # Actualizar estado de los botones de me_gusta/favorito
            actualizar_estado_botones_gustos()
    # También podemos cargar la información de la última canción reproducida
    cargar_ultima_cancion_reproducida()


# Función para navegar al álbum de una canción específica
def ir_al_album(cancion):
    # Cambiar a la pestaña de álbumes
    paginas_canciones.set("Álbumes")
    # Marcar la pestaña como cargada
    pestanas_cargadas["Álbumes"] = True
    # Actualizar la vista de álbumes
    actualizar_vista_albumes()
    # Buscar y mostrar las canciones del álbum específico
    if cancion.album and cancion.album not in ["", "Unknown Album", "Desconocido"]:
        # Verificar si el álbum existe y tiene canciones
        canciones_album = controlador_biblioteca.obtener_canciones_album_controlador(cancion.album)
        if canciones_album:
            # Mostrar las canciones del álbum
            mostrar_canciones_album(cancion.album)
        else:
            # Si no hay canciones, mostrar un mensaje
            print(f"No se encontraron canciones en el álbum: {cancion.album}")
    else:
        # Si no hay información de álbum, mostrar un mensaje
        print(f"No hay información de álbum para: {cancion.titulo_cancion}")


# Función para navegar al artista de una canción específica
def ir_al_artista(cancion):
    # Cambiar a la pestaña de artistas
    paginas_canciones.set("Artistas")
    # Marcar la pestaña como cargada
    pestanas_cargadas["Artistas"] = True
    # Actualizar la vista de artistas
    actualizar_vista_artistas()
    # Extraer el artista principal (siempre es el primero antes de cualquier colaboración)
    artista_completo = cancion.artista
    # Lista de separadores comunes en nombres de artistas
    separadores = SEPARADORES
    # Obtener SIEMPRE el primer artista (antes del primer separador)
    artista_principal = artista_completo
    for separador in separadores:
        if separador.lower() in artista_completo.lower():
            artista_principal = artista_completo.split(separador, 1)[0].strip()
            print(f"Artista extraído: '{artista_principal}' de '{artista_completo}'")
            break
    # Buscar el artista principal
    artista_encontrado = None
    # Primero buscar coincidencia exacta (sin importar mayúsculas/minúsculas)
    todos_artistas = controlador_biblioteca.obtener_todos_artistas_controlador()
    for artista_key in todos_artistas:
        if artista_principal.lower() == artista_key.lower():
            artista_encontrado = artista_key
            break
    # Si no hay coincidencia exacta, buscar coincidencia parcial
    if not artista_encontrado:
        for artista_key in todos_artistas:
            if (
                artista_principal.lower() in artista_key.lower()
                or artista_key.lower() in artista_principal.lower()
            ):
                artista_encontrado = artista_key
                break
    # Si encontramos un artista que coincide, mostrar sus canciones
    if artista_encontrado:
        # Verificar si hay canciones para este artista
        canciones_artista = controlador_biblioteca.obtener_canciones_artista_controlador(artista_encontrado)
        if canciones_artista:
            mostrar_canciones_artista(artista_encontrado)
            print(f"Mostrando canciones del artista: {artista_encontrado}")
        else:
            print(f"No se encontraron canciones del artista: {artista_encontrado}")
    else:
        # Si no hay coincidencia, mostrar mensaje informativo
        print(f"No se encontró el artista principal '{artista_principal}'")


# Función para navegar al artista de un álbum específico
def ir_al_artista_album(album):
    try:
        # Cambiar a la pestaña de artistas
        paginas_canciones.set("Artistas")
        # Marcar la pestaña como cargada
        pestanas_cargadas["Artistas"] = True
        # Actualizar la vista de artistas
        actualizar_vista_artistas()
        # Obtener el artista principal del álbum usando el controlador
        artista_principal = controlador_biblioteca.obtener_artista_album_controlador(album)
        if artista_principal and artista_principal not in ["", "Unknown Artist", "Desconocido"]:
            # Buscar el artista
            artista_encontrado = None
            # Primero buscar coincidencia exacta (sin importar mayúsculas/minúsculas)
            todos_artistas = controlador_biblioteca.obtener_todos_artistas_controlador()
            for artista_key in todos_artistas:
                if artista_key.lower() == artista_principal.lower():
                    artista_encontrado = artista_key
                    break
            # Si no hay coincidencia exacta, buscar coincidencia parcial
            if not artista_encontrado:
                for artista_key in todos_artistas:
                    if (
                        artista_principal.lower() in artista_key.lower()
                        or artista_key.lower() in artista_principal.lower()
                    ):
                        artista_encontrado = artista_key
                        break
            # Si encontramos un artista que coincide, mostrar sus canciones
            if artista_encontrado:
                mostrar_canciones_artista(artista_encontrado)
                print(f"Navegando al artista del álbum '{album}': {artista_encontrado}")
            else:
                print(f"No se encontró el artista principal '{artista_principal}' del álbum '{album}'")
        else:
            print(f"No se pudo determinar el artista principal del álbum '{album}'")
    except Exception as e:
        print(f"Error al navegar al artista del álbum '{album}': {e}")


# Función para crear botones para cada canción
def crear_boton_cancion(cancion, panel):
    # Obtener colores del tema actual
    controlador_tema.colores()
    # Determinar si el texto es largo y necesita desplazamiento
    texto_cancion = f"{cancion.titulo_cancion} - {cancion.artista}"
    # Crear frame contenedor para el botón y el menú
    # ------------------------------------- Panel de canción ------------------------------------
    panel_lista_cancion = ctk.CTkFrame(panel, height=28, fg_color="transparent")
    panel_lista_cancion.pack(fill="both", expand=True, pady=(0, 2))
    panel_lista_cancion.pack_propagate(False)
    # -------------------------------------------------------------------------------------------

    # ------------------------------------- Botón de canción ------------------------------------
    # Crear el botón principal con texto inicial
    boton_cancion = ctk.CTkButton(
        panel_lista_cancion,
        width=ANCHO_BOTON,
        height=ALTO_BOTON,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text=texto_cancion,
        command=lambda c=cancion: reproducir_desde_lista_vista(c),
    )
    boton_cancion.pack(side="left", fill="both", expand=True)
    controlador_tema.registrar_botones(f"cancion_{cancion.titulo_cancion}", boton_cancion)
    # -------------------------------------------------------------------------------------------
    # Configurar desplazamiento si el texto es largo
    configurar_desplazamiento_texto(boton_cancion, texto_cancion)

    # ------------------------------------ Boton de opciones ------------------------------------
    # Cargar icono de opciones
    icono_opcion = cargar_icono_con_tamanio("opcion", controlador_tema.tema_iconos, (15, 20))
    # Botón de opciones
    boton_opciones = ctk.CTkButton(
        panel_lista_cancion,
        width=ANCHO_BOTON,
        height=ALTO_BOTON,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text="",
        image=icono_opcion,
        command=lambda c=cancion: mostrar_menu_opciones(c, panel_lista_cancion),
    )
    boton_opciones.pack(side="right", padx=(1, 0))
    controlador_tema.registrar_botones(f"opciones_{cancion.titulo_cancion}", boton_opciones)
    crear_tooltip(boton_opciones, "Opciones")
    # -------------------------------------------------------------------------------------------

    # Registrar botones en el controlador de tema
    botones_canciones[cancion] = boton_cancion
    # Vincular clic derecho al botón principal para mostrar el menú
    boton_cancion.bind("<Button-3>", lambda event, c=cancion: mostrar_menu_opciones(c, panel_lista_cancion))
    return panel_lista_cancion


# Función auxiliar para crear botones de álbumes
def crear_boton_album(albumes, panel_componente):
    # Crear botones para cada álbum
    for album in sorted(albumes):
        # Ignorar álbumes vacíos o sin nombre
        if album == "" or album == "Unknown Album" or album.lower() == "desconocido":
            continue

        # ------------------------------------- Panel de album ----------------------------------
        panel_lista_album = ctk.CTkFrame(panel_componente, height=28, fg_color="transparent")
        panel_lista_album.pack(fill="both", expand=True, pady=(0, 2))
        panel_lista_album.pack_propagate(False)
        # ---------------------------------------------------------------------------------------

        # ------------------------------------ Boton de álbum -----------------------------------
        boton_album = ctk.CTkButton(
            panel_lista_album,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=album,
            command=lambda a=album: mostrar_canciones_album(a),
        )
        boton_album.pack(side="left", fill="both", expand=True)
        controlador_tema.registrar_botones(f"album_{album}", boton_album)
        # ---------------------------------------------------------------------------------------
        # Configurar desplazamiento si el texto es largo
        configurar_desplazamiento_texto(boton_album, album)

        # ------------------------------------ Boton de opciones del álbum ----------------------
        icono_opcion_album = cargar_icono_con_tamanio("opcion", controlador_tema.tema_iconos, (15, 20))
        # Botón de opciones del álbum
        boton_opciones_album = ctk.CTkButton(
            panel_lista_album,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text="",
            image=icono_opcion_album,
            command=lambda a=album, p=panel_lista_album: mostrar_menu_opciones_album(a, p),
        )
        boton_opciones_album.pack(side="right", padx=(1, 0))
        controlador_tema.registrar_botones(f"opciones_album_{album}", boton_opciones_album)
        crear_tooltip(boton_opciones_album, "Opciones del álbum")
        # ---------------------------------------------------------------------------------------
        boton_album.bind(
            "<Button-3>", lambda event, a=album, p=panel_lista_album: mostrar_menu_opciones_album(a, p)
        )


# Función auxiliar para crear botones de artistas
def crear_boton_artista(artistas, panel_componente):
    # Crear botones para cada artista
    for artista in sorted(artistas):
        # Ignorar artistas sin nombre o desconocidos
        if artista == "" or artista == "Unknown Artist" or artista.lower() == "desconocido":
            continue

        # ------------------------------------- Panel de artista --------------------------------
        panel_lista_artista = ctk.CTkFrame(panel_componente, height=28, fg_color="transparent")
        panel_lista_artista.pack(fill="both", expand=True, pady=(0, 2))
        panel_lista_artista.pack_propagate(False)
        # ---------------------------------------------------------------------------------------

        # ----------------------------------- Boton de artista ----------------------------------
        boton_artista = ctk.CTkButton(
            panel_lista_artista,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=artista,
            command=lambda a=artista: mostrar_canciones_artista(a),
        )
        boton_artista.pack(side="left", fill="both", expand=True)
        controlador_tema.registrar_botones(f"artista_{artista}", boton_artista)
        # ---------------------------------------------------------------------------------------
        # Configurar desplazamiento si el texto es largo
        configurar_desplazamiento_texto(boton_artista, artista)

        # ------------------------------------ Boton de opciones del álbum ----------------------
        icono_opcion_album = cargar_icono_con_tamanio("opcion", controlador_tema.tema_iconos, (15, 20))
        # Botón de opciones del álbum
        boton_opciones_artista = ctk.CTkButton(
            panel_lista_artista,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text="",
            image=icono_opcion_album,
            command=lambda a=artista, p=panel_lista_artista: mostrar_menu_opciones_artista(a, p),
        )
        boton_opciones_artista.pack(side="right", padx=(1, 0))
        controlador_tema.registrar_botones(f"opciones_artista_{artista}", boton_opciones_artista)
        crear_tooltip(boton_opciones_artista, "Opciones del artista")
        # ---------------------------------------------------------------------------------------
        boton_artista.bind(
            "<Button-3>", lambda event, a=artista, p=panel_lista_artista: mostrar_menu_opciones_artista(a, p)
        )


# Función para crear una opción de menú en un menú contextual
def crear_opcion_menu(panel_menu_opciones, texto, funcion, tiene_separador=False, icono_nombre=None):
    if tiene_separador:
        # -------------------------..--- Separador entre opciones -------------------------------
        separador = ctk.CTkFrame(
            panel_menu_opciones,
            fg_color=controlador_tema.color_hover,
            border_color=controlador_tema.color_hover,
            border_width=1,
            height=1,
        )
        separador.pack(fill="x", padx=2, pady=2)
        # ---------------------------------------------------------------------------------------
    # Cargar icono si se especifica
    icono_opcion = None
    if icono_nombre:
        icono_opcion = cargar_icono_con_tamanio(icono_nombre, controlador_tema.tema_iconos, (15, 15))
    # ------------------------------------ Botón de opción --------------------------------------
    boton_opcion = ctk.CTkButton(
        panel_menu_opciones,
        width=ANCHO_BOTON - 3,
        height=ALTO_BOTON - 3,
        fg_color="transparent",
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text=texto,
        image=icono_opcion,
        anchor="w",
        compound="left",
        command=lambda: [funcion(), panel_menu_opciones.master.destroy()],
    )
    boton_opcion.pack(fill="x", padx=2, pady=(2, 0))
    # -------------------------------------------------------------------------------------------


# Función para mostrar el menú contextual personalizado de una canción
def mostrar_menu_opciones(cancion, panel_padre):
    # Verificar si ya existe un menú abierto y cerrarlo
    for componente in ventana_principal.winfo_children():
        if isinstance(componente, ctk.CTkToplevel) and hasattr(componente, "menu_opciones"):
            componente.destroy()
    # Obtener colores actuales del tema
    controlador_tema.colores()
    # ------------------------------------- Ventana de menú -------------------------------------
    # Crear una ventana de nivel superior para el menú
    menu_ventana = ctk.CTkToplevel(ventana_principal)
    # Marcar esta ventana como un menú contextual
    menu_ventana.menu_opciones = True
    menu_ventana.title("")
    menu_ventana.geometry("200x0")
    menu_ventana.overrideredirect(True)
    menu_ventana.configure(fg_color="green")
    menu_ventana.attributes("-topmost", True)
    menu_ventana.attributes("-toolwindow", True)
    menu_ventana.attributes("-transparentcolor", "green")
    # -------------------------------------------------------------------------------------------
    # ----------------------------------- Panel menu opciones -----------------------------------
    # Contenedor principal del menú
    panel_menu_opciones = ctk.CTkFrame(menu_ventana, corner_radius=7, fg_color=controlador_tema.color_base)
    panel_menu_opciones.pack(fill="both", expand=True)
    # -------------------------------------------------------------------------------------------
    # Agregar opciones al menú
    # ---------------------------------- Opciones reproducir ------------------------------------
    # Verificar si la canción del menú es la canción actual
    es_cancion_actual = controlador_reproductor.cancion_actual == cancion
    if es_cancion_actual:
        # Sí es la canción actual, mostrar Pausar o Reproducir según el estado
        if ESTADO_REPRODUCCION:
            crear_opcion_menu(panel_menu_opciones, "Pausar", lambda: reproducir_vista(), False, "pausa")
        else:
            crear_opcion_menu(
                panel_menu_opciones, "Reproducir", lambda: reproducir_vista(), False, "reproducir"
            )
    else:
        # Si no es la canción actual, mantener "Reproducir"
        crear_opcion_menu(
            panel_menu_opciones,
            "Reproducir",
            lambda: reproducir_desde_lista_vista(cancion),
            False,
            "reproducir",
        )
    # -------------------------------------------------------------------------------------------
    # -------------------------------- Opciones de cola de reproducción -------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al inicio de la cola",
        lambda: agregar_inicio_cola_vista(cancion),
        True,
        "agregar_cola",
    )

    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al final de la cola",
        lambda: agregar_fin_cola_vista(cancion),
        False,
        "agregar_cola",
    )
    # -------------------------------------------------------------------------------------------
    # ------------------------------------ Opciones de gusto ------------------------------------
    # Separador antes de opciones de Me_gusta/Favorito
    texto_me_gusta = "Quitar de Me gusta" if cancion.me_gusta else "Agregar a Me gusta"
    icono_me_gusta = "me_gusta_rojo" if cancion.me_gusta else "me_gusta"
    crear_opcion_menu(
        panel_menu_opciones,
        texto_me_gusta,
        lambda: agregar_me_gusta_vista(cancion),
        True,
        icono_me_gusta,
    )

    texto_favorito = "Quitar de Favoritos" if cancion.favorito else "Agregar a Favoritos"
    icono_favorito = "favorito_amarillo" if cancion.favorito else "favorito"
    crear_opcion_menu(
        panel_menu_opciones,
        texto_favorito,
        lambda: agregar_favorito_vista(cancion),
        False,
        icono_favorito,
    )
    # -------------------------------------------------------------------------------------------
    # ---------------------------------- Opciones de información --------------------------------
    if cancion.album and cancion.album not in ["", "Unknown Album", "Desconocido"]:
        crear_opcion_menu(panel_menu_opciones, "Ir al álbum", lambda: ir_al_album(cancion), True, "album")

    if cancion.artista and cancion.artista not in ["", "Unknown Artist", "Desconocido"]:
        crear_opcion_menu(
            panel_menu_opciones, "Ir al artista", lambda: ir_al_artista(cancion), False, "artista"
        )
    # -------------------------------------------------------------------------------------------
    # ---------------------------------- Opciones de eliminar -----------------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Ver información",
        lambda: print(f"Ver info de: {cancion.titulo_cancion}"),
        True,
        "informacion",
    )

    crear_opcion_menu(
        panel_menu_opciones,
        "Eliminar cancion",
        lambda: eliminar_cancion_vista(cancion),
        False,
        "eliminar",
    )
    # -------------------------------------------------------------------------------------------
    # Actualizar el panel para obtener su altura real
    panel_menu_opciones.update_idletasks()
    altura_real = panel_menu_opciones.winfo_reqheight() + 2
    # Posicionar el menú junto al botón
    x = panel_padre.winfo_rootx() + panel_padre.winfo_width() - 200
    y = panel_padre.winfo_rooty()
    # Asegurar que el menú no salga de la pantalla
    ancho_menu = menu_ventana.winfo_screenwidth()
    alto_menu = menu_ventana.winfo_screenheight()
    # Ajustar la posición horizontal del menú
    if x + 200 > ancho_menu:
        x = ancho_menu - 210
    # Ajustar la posición vertical del menú
    if y + altura_real > alto_menu:
        y = alto_menu - altura_real - 10
    menu_ventana.update()
    # Establecer la geometría con la altura exacta del contenido
    menu_ventana.geometry(f"200x{altura_real}+{x}+{y}")
    # Vincular eventos para cerrar el menú
    menu_ventana.bind("<FocusOut>", lambda event: cerrar_menu_opciones_al_desenfocar(menu_ventana, event))
    menu_ventana.bind("<Button-1>", lambda e: menu_ventana.destroy())
    # Vincular clic en cualquier parte de la pantalla para cerrar el menú
    ventana_principal.bind("<Button-1>", lambda e: menu_ventana.destroy())

    # Establecer una función para restablecer el binding cuando el menú se cierre
    def al_cerrar_menu():
        try:
            ventana_principal.unbind("<Button-1>")
        except Exception as e:
            print(f"Error al restablecer el binding: {e}")
            pass

    menu_ventana.protocol("WM_DELETE_WINDOW", al_cerrar_menu)
    # Dar foco al menú para detectar cuando lo pierde
    menu_ventana.focus_set()


# Función para mostrar el menú contextual personalizado de un álbum
def mostrar_menu_opciones_album(album, panel_padre):
    # Verificar si ya existe un menú abierto y cerrarlo
    for componente in ventana_principal.winfo_children():
        if isinstance(componente, ctk.CTkToplevel) and hasattr(componente, "menu_opciones_album"):
            componente.destroy()
    # Obtener colores actuales del tema
    controlador_tema.colores()
    # ------------------------------------- Ventana de menú álbum -------------------------------
    menu_ventana = ctk.CTkToplevel(ventana_principal)
    menu_ventana.menu_opciones_album = True
    menu_ventana.title("")
    menu_ventana.geometry("200x0")
    menu_ventana.overrideredirect(True)
    menu_ventana.configure(fg_color="green")
    menu_ventana.attributes("-topmost", True)
    menu_ventana.attributes("-toolwindow", True)
    menu_ventana.attributes("-transparentcolor", "green")
    # -------------------------------------------------------------------------------------------
    # ----------------------------------- Panel menu opciones álbum -----------------------------
    panel_menu_opciones = ctk.CTkFrame(menu_ventana, corner_radius=7, fg_color=controlador_tema.color_base)
    panel_menu_opciones.pack(fill="both", expand=True)
    # -------------------------------------------------------------------------------------------
    # Agregar opciones al menú
    # ---------------------------------- Opciones reproducir álbum ------------------------------
    crear_opcion_menu(
        panel_menu_opciones, "Reproducir álbum", lambda: reproducir_album_completo(album), False, "reproducir"
    )
    # -------------------------------------------------------------------------------------------
    # -------------------------------- Opciones de cola de reproducción -------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al inicio de la cola",
        lambda: agregar_album_inicio_cola(album),
        True,
        "agregar_cola",
    )

    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al final de la cola",
        lambda: agregar_album_fin_cola(album),
        False,
        "agregar_cola",
    )
    # -------------------------------------------------------------------------------------------
    # Obtener todas las canciones del álbum para verificar su estado colectivo
    canciones_del_album_obj = controlador_biblioteca.obtener_canciones_album_controlador(album)

    # Estado para "Me gusta"
    album_totalmente_en_me_gusta = False
    if canciones_del_album_obj:
        # Se considera que el álbum está en "Me gusta" si todas sus canciones lo están.
        album_totalmente_en_me_gusta = all(c.me_gusta for c in canciones_del_album_obj)

    texto_album_me_gusta = (
        "Quitar álbum de Me gusta" if album_totalmente_en_me_gusta else "Agregar álbum a Me gusta"
    )
    icono_album_me_gusta = "me_gusta_rojo" if album_totalmente_en_me_gusta else "me_gusta"

    crear_opcion_menu(
        panel_menu_opciones,
        texto_album_me_gusta,
        lambda: agregar_album_me_gusta_vista(album),
        True,
        icono_album_me_gusta,
    )

    # Estado para "Favoritos"
    album_totalmente_en_favoritos = False
    if canciones_del_album_obj:
        # Se considera que el álbum está en "Favoritos" si todas sus canciones lo están.
        album_totalmente_en_favoritos = all(c.favorito for c in canciones_del_album_obj)

    texto_album_favorito = (
        "Quitar álbum de Favoritos" if album_totalmente_en_favoritos else "Agregar álbum a Favoritos"
    )
    icono_album_favorito = "favorito_amarillo" if album_totalmente_en_favoritos else "favorito"

    crear_opcion_menu(
        panel_menu_opciones,
        texto_album_favorito,
        lambda: agregar_album_favorito_vista(album),
        False,
        icono_album_favorito,
    )
    # ---------------------------------- Opciones de información --------------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        f"Ir al artista del álbum",
        lambda: ir_al_artista_album(album),
        True,
        "artista",
    )
    # -------------------------------------------------------------------------------------------
    # ---------------------------------- Opciones de eliminar álbum -----------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Ver información",
        lambda: print(f"Ver info del album"),
        True,
        "informacion",
    )

    crear_opcion_menu(
        panel_menu_opciones, "Eliminar álbum", lambda: print("Eliminar album"), False, "eliminar"
    )
    # -------------------------------------------------------------------------------------------

    # Actualizar el panel para obtener su altura real
    panel_menu_opciones.update_idletasks()
    altura_real = panel_menu_opciones.winfo_reqheight() + 2
    # Posicionar el menú junto al botón
    x = panel_padre.winfo_rootx() + panel_padre.winfo_width() - 200
    y = panel_padre.winfo_rooty()
    # Asegurar que el menú no salga de la pantalla
    ancho_menu_pantalla = menu_ventana.winfo_screenwidth()
    alto_menu_pantalla = menu_ventana.winfo_screenheight()
    # Ajustar la posición horizontal del menú
    if x + 200 > ancho_menu_pantalla:
        x = ancho_menu_pantalla - 210
    if y + altura_real > alto_menu_pantalla:
        y = alto_menu_pantalla - altura_real - 10
    menu_ventana.update()
    # Establecer la geometría con la altura exacta del contenido
    menu_ventana.geometry(f"200x{altura_real}+{x}+{y}")
    # Vincular eventos para cerrar el menú
    menu_ventana.bind("<FocusOut>", lambda event: cerrar_menu_opciones_al_desenfocar(menu_ventana, event))
    menu_ventana.bind("<Button-1>", lambda e: menu_ventana.destroy())
    # Vincular clic en cualquier parte de la pantalla para cerrar el menú
    ventana_principal.bind("<Button-1>", lambda e: menu_ventana.destroy(), add="+")

    # Establecer una función para restablecer el binding cuando el menú se cierre
    def al_cerrar_menu_album():
        try:
            ventana_principal.unbind("<Button-1>")
        except Exception as e:
            print(f"Error al restablecer el binding (álbum): {e}")
            pass

    menu_ventana.protocol("WM_DELETE_WINDOW", al_cerrar_menu_album)
    # Dar foco al menú para detectar cuando lo pierde
    menu_ventana.focus_set()


# Función para mostrar el menú contextual personalizado de un artista
def mostrar_menu_opciones_artista(artista, panel_padre):
    # Verificar si ya existe un menú abierto y cerrarlo
    for componente in ventana_principal.winfo_children():
        if isinstance(componente, ctk.CTkToplevel) and hasattr(componente, "menu_opciones_artista"):
            componente.destroy()
    # Obtener colores actuales del tema
    controlador_tema.colores()
    # ------------------------------------- Ventana de menú artista -----------------------------
    menu_ventana = ctk.CTkToplevel(ventana_principal)
    menu_ventana.menu_opciones_artista = True
    menu_ventana.title("")
    menu_ventana.geometry("200x0")
    menu_ventana.overrideredirect(True)
    menu_ventana.configure(fg_color="green")
    menu_ventana.attributes("-topmost", True)
    menu_ventana.attributes("-toolwindow", True)
    menu_ventana.attributes("-transparentcolor", "green")
    # -------------------------------------------------------------------------------------------
    # ----------------------------------- Panel menu opciones artista --------------------------
    panel_menu_opciones = ctk.CTkFrame(menu_ventana, corner_radius=7, fg_color=controlador_tema.color_base)
    panel_menu_opciones.pack(fill="both", expand=True)
    # -------------------------------------------------------------------------------------------

    # Agregar opciones al menú
    # ---------------------------------- Opciones reproducir artista ---------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Reproducir artista",
        lambda: reproducir_artista_completo(artista),
        False,
        "reproducir",
    )
    # -------------------------------------------------------------------------------------------

    # -------------------------------- Opciones de cola de reproducción -------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al inicio de la cola",
        lambda: agregar_artista_inicio_cola(artista),
        True,
        "agregar_cola",
    )

    crear_opcion_menu(
        panel_menu_opciones,
        "Agregar al final de la cola",
        lambda: agregar_artista_fin_cola(artista),
        False,
        "agregar_cola",
    )
    # -------------------------------------------------------------------------------------------

    # Obtener todas las canciones del artista para verificar su estado colectivo
    canciones_del_artista_obj = controlador_biblioteca.obtener_canciones_artista_controlador(artista)

    # Estado para "Me gusta"
    artista_totalmente_en_me_gusta = False
    if canciones_del_artista_obj:
        # Se considera que el artista está en "Me gusta" si todas sus canciones lo están.
        artista_totalmente_en_me_gusta = all(c.me_gusta for c in canciones_del_artista_obj)

    texto_artista_me_gusta = (
        "Quitar artista de Me gusta" if artista_totalmente_en_me_gusta else "Agregar artista a Me gusta"
    )
    icono_artista_me_gusta = "me_gusta_rojo" if artista_totalmente_en_me_gusta else "me_gusta"

    crear_opcion_menu(
        panel_menu_opciones,
        texto_artista_me_gusta,
        lambda: agregar_artista_me_gusta_vista(artista),
        True,
        icono_artista_me_gusta,
    )

    # Estado para "Favoritos"
    artista_totalmente_en_favoritos = False
    if canciones_del_artista_obj:
        # Se considera que el artista está en "Favoritos" si todas sus canciones lo están.
        artista_totalmente_en_favoritos = all(c.favorito for c in canciones_del_artista_obj)

    texto_artista_favorito = (
        "Quitar artista de Favoritos" if artista_totalmente_en_favoritos else "Agregar artista a Favoritos"
    )
    icono_artista_favorito = "favorito_amarillo" if artista_totalmente_en_favoritos else "favorito"

    crear_opcion_menu(
        panel_menu_opciones,
        texto_artista_favorito,
        lambda: agregar_artista_favorito_vista(artista),
        False,
        icono_artista_favorito,
    )
    # -------------------------------------------------------------------------------------------

    # ---------------------------------- Opciones de información --------------------------------
    crear_opcion_menu(
        panel_menu_opciones,
        "Ver información",
        lambda: print(f"Ver info del artista: {artista}"),
        True,
        "informacion",
    )

    crear_opcion_menu(
        panel_menu_opciones, "Eliminar artista", lambda: print("eliminar artista"), False, "eliminar"
    )
    # -------------------------------------------------------------------------------------------

    # Actualizar el panel para obtener su altura real
    panel_menu_opciones.update_idletasks()
    altura_real = panel_menu_opciones.winfo_reqheight() + 2
    # Posicionar el menú junto al botón
    x = panel_padre.winfo_rootx() + panel_padre.winfo_width() - 200
    y = panel_padre.winfo_rooty()
    # Asegurar que el menú no salga de la pantalla
    ancho_menu_pantalla = menu_ventana.winfo_screenwidth()
    alto_menu_pantalla = menu_ventana.winfo_screenheight()
    # Ajustar la posición horizontal del menú
    if x + 200 > ancho_menu_pantalla:
        x = ancho_menu_pantalla - 210
    if y + altura_real > alto_menu_pantalla:
        y = alto_menu_pantalla - altura_real - 10
    menu_ventana.update()
    # Establecer la geometría con la altura exacta del contenido
    menu_ventana.geometry(f"200x{altura_real}+{x}+{y}")
    # Vincular eventos para cerrar el menú
    menu_ventana.bind("<FocusOut>", lambda event: cerrar_menu_opciones_al_desenfocar(menu_ventana, event))
    menu_ventana.bind("<Button-1>", lambda e: menu_ventana.destroy())
    # Vincular clic en cualquier parte de la pantalla para cerrar el menú
    ventana_principal.bind("<Button-1>", lambda e: menu_ventana.destroy(), add="+")

    # Establecer una función para restablecer el binding cuando el menú se cierre
    def al_cerrar_menu_artista():
        try:
            ventana_principal.unbind("<Button-1>")
        except Exception as e:
            print(f"Error al restablecer el binding (artista): {e}")
            pass

    menu_ventana.protocol("WM_DELETE_WINDOW", al_cerrar_menu_artista)
    # Dar foco al menú para detectar cuando lo pierde
    menu_ventana.focus_set()


# Función para cerrar el menú cuando pierde el foco
def cerrar_menu_opciones_al_desenfocar(menu_ventana, _event=None):
    # Verificar si el menú sigue existiendo
    if not menu_ventana.winfo_exists():
        return
    # Obtener el componente que tiene el foco ahora
    componente_enfocado = menu_ventana.focus_get()
    # Si nada tiene el foco o el foco no está en el menú o sus hijos
    if not componente_enfocado or not str(componente_enfocado).startswith(str(menu_ventana)):
        try:
            # Limpiar el binding adicional antes de destruir
            ventana_principal.unbind("<Button-1>")
            menu_ventana.destroy()
        except Exception as e:
            print(f"Error al cerrar menú: {e}")


# Función para mostrar los detalles de las canciones
def mostrar_detalles_cancion(pagina, elemento, funcion_regresar):
    global vista_detalle_activa, vista_detalle_tipo, vista_detalle_elemento, vista_detalle_canvas, vista_detalle_panel
    # Eliminar tooltip si existe
    eliminar_tooltip()
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña correspondiente
    pestania = paginas_canciones.tab(pagina)
    # Limpiar la pestaña
    for componente in pestania.winfo_children():
        componente.destroy()

    # Método para regresar a la lista de canciones
    def regresar_con_limpieza():
        global vista_detalle_activa, vista_detalle_tipo, vista_detalle_elemento, vista_detalle_canvas, vista_detalle_panel
        # Detener animación si está activa
        animacion.detener_desplazamiento_etiqueta()
        # Resetear el estado de vista detalle
        vista_detalle_activa = False
        vista_detalle_tipo = None
        vista_detalle_elemento = None
        vista_detalle_canvas = None
        vista_detalle_panel = None
        eliminar_tooltip()
        # Llamar a la función original de regreso
        funcion_regresar()

    # -------------------------------------- Panel detalles -------------------------------------
    # Crear contenedor para la visualización del detalle
    contenedor_detalles = ctk.CTkFrame(pestania, fg_color="transparent")
    contenedor_detalles.pack(fill="both", expand=True)
    # -------------------------------------------------------------------------------------------
    # ------------------------------------- Panel superior --------------------------------------
    # Panel superior con botón volver y título
    panel_superior = ctk.CTkFrame(contenedor_detalles, height=30, fg_color="transparent")
    panel_superior.pack(fill="x")
    panel_superior.pack_propagate(False)
    # -------------------------------------------------------------------------------------------
    # ------------------------------------- Botón regresar --------------------------------------
    # Icono de regresar
    icono_regresar = cargar_icono_con_tamanio("regresar", controlador_tema.tema_iconos, (12, 12))
    # Botón para volver a la lista
    boton_regresar = ctk.CTkButton(
        panel_superior,
        width=ANCHO_BOTON - 3,
        height=ALTO_BOTON - 3,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text="Regresar",
        image=icono_regresar,
        command=regresar_con_limpieza,
    )
    boton_regresar.pack(side="left")
    controlador_tema.registrar_botones(f"volver_{pagina.lower()}", boton_regresar)
    crear_tooltip(boton_regresar, "Regresar a la lista")
    # -------------------------------------------------------------------------------------------
    # -------------------------------------- Panel titulo ---------------------------------------
    # Panel contenedor para la etiqueta
    panel_titulo = ctk.CTkFrame(panel_superior, fg_color="transparent")
    panel_titulo.place(relx=0.5, rely=0.5, anchor="center")
    # -------------------------------------------------------------------------------------------
    # ------------------------------------ Etiqueta de elemento ---------------------------------
    # Título del elemento centrado
    etiqueta_elemento = ctk.CTkLabel(
        panel_titulo,
        height=25,
        fg_color="transparent",
        font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
        text_color=controlador_tema.color_texto,
        text=elemento,
        anchor="center",
    )
    etiqueta_elemento.pack()
    controlador_tema.registrar_etiqueta(etiqueta_elemento)
    # Crear diccionario para la animación con solo este elemento
    textos_animados = {"titulo": (elemento, etiqueta_elemento)}
    # Configurar el desplazamiento automático solo para el título
    animacion.configurar_desplazamiento_etiqueta(etiqueta_elemento, textos_animados, 275)
    # -------------------------------------------------------------------------------------------
    # Usar la función existente para crear el canvas con scroll
    canvas_canciones_general, panel_canciones, _ = crear_canvas_con_scroll(
        contenedor_detalles, True, paginas_canciones
    )
    # Configurar el estado de vista detalle
    vista_detalle_activa = True
    vista_detalle_tipo = "album" if pagina == "Álbumes" else "artista"
    vista_detalle_elemento = elemento
    vista_detalle_canvas = canvas_canciones_general
    vista_detalle_panel = panel_canciones
    # Mostrar las canciones del elemento (sin filtro inicialmente)
    mostrar_canciones_elemento_filtradas(elemento, pagina, "")


# Función para crear un canvas con scroll y panel de botones
def crear_canvas_con_scroll(contenedor_padre, es_pestania=True, es_pestania_padre=None):
    # -------------------------------- Crear canvas con scroll ----------------------------------
    canvas = tk.Canvas(contenedor_padre, bg=controlador_tema.color_base, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    controlador_tema.registrar_canvas(canvas, es_tabview=es_pestania, tabview_parent=es_pestania_padre)
    # -------------------------------------------------------------------------------------------
    # -------------------------------------- Panel botones --------------------------------------
    # Crear panel para el contenido
    panel_botones = ctk.CTkFrame(canvas, fg_color="transparent", corner_radius=0)
    panel_botones.pack(fill="both")
    controlador_tema.registrar_panel(panel_botones)
    # -------------------------------------------------------------------------------------------
    # Crear ventana en el canvas para el panel
    canvas_ventana_general = canvas.create_window((0, 0), window=panel_botones)
    # Configurar scroll
    GestorScroll(canvas, panel_botones, canvas_ventana_general)
    return canvas, panel_botones, canvas_ventana_general


# Función para actualizar todas las vistas de las canciones
def actualizar_todas_vistas_canciones():
    pestana_actual = paginas_canciones.get()
    # Actualizar la vista de canciones
    actualizar_vista_canciones(panel_botones_canciones)
    # Actualizar las demás pestañas inmediatamente
    actualizar_vista_me_gusta()
    actualizar_vista_favoritos()
    actualizar_vista_albumes()
    actualizar_vista_artistas()
    # Marcar todas las pestañas como cargadas
    pestanas_cargadas["Me gusta"] = True
    pestanas_cargadas["Favoritos"] = True
    pestanas_cargadas["Álbumes"] = True
    pestanas_cargadas["Artistas"] = True
    # Restablecer el scroll para la pestaña actual
    if pestana_actual == "Canciones":
        canvas_canciones.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e))
    # Guardar después de las actualizaciones
    guardar_biblioteca()


# Función para manejar cambios de pestaña
def actualizar_pestana_seleccionada():
    global vista_detalle_activa, vista_detalle_tipo, vista_detalle_elemento, vista_detalle_canvas, vista_detalle_panel
    # Obtener nombre de la pestaña activa
    pestana_actual = paginas_canciones.get()
    # Si cambiamos de pestaña y estábamos en vista detalle, resetear
    if vista_detalle_activa:
        # Detener cualquier animación activa
        animacion.detener_desplazamiento_etiqueta()  # Llamar sin argumentos
        vista_detalle_activa = False
        vista_detalle_tipo = None
        vista_detalle_elemento = None
        vista_detalle_canvas = None
        vista_detalle_panel = None
        # Limpiar la entrada de búsqueda
        entrada_busqueda.delete(0, "end")
    # Desvincular el scroll wheel de todos los canvas para evitar conflictos
    canvas_canciones.unbind_all("<MouseWheel>")
    # Actualizar solo si no se ha cargado previamente
    cargar_pestana_si_necesario(pestana_actual)
    # Restaurar el binding correcto dependiendo de la pestaña activa
    if pestana_actual == "Canciones":
        configurar_scroll_pestana("Canciones", canvas_canciones)
    elif pestana_actual in ["Me gusta", "Favoritos", "Álbumes", "Artistas"]:
        configurar_scroll_pestana(pestana_actual)


# Diccionario para rastrear si las pestañas han sido cargadas
def cargar_pestana_si_necesario(nombre_pestana):
    # Si es la pestaña "Canciones", no hacer nada ya que siempre está cargada
    if nombre_pestana == "Canciones":
        return
    if not pestanas_cargadas[nombre_pestana]:
        # Mapeo de pestañas a sus funciones de actualización
        funciones_actualizacion = {
            "Me gusta": actualizar_vista_me_gusta,
            "Favoritos": actualizar_vista_favoritos,
            "Álbumes": actualizar_vista_albumes,
            "Artistas": actualizar_vista_artistas,
            "Listas": lambda: None,
        }
        # Ejecutar la función correspondiente si existe
        if nombre_pestana in funciones_actualizacion:
            funciones_actualizacion[nombre_pestana]()
            pestanas_cargadas[nombre_pestana] = True


# Función para configurar el scroll de una pestaña específica
def configurar_scroll_pestana(nombre_pestana, canvas_principal=None):
    if nombre_pestana == "Canciones" and canvas_principal:
        canvas_principal.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_principal, e))
    else:
        pestania = paginas_canciones.tab(nombre_pestana)
        for componente in pestania.winfo_children():
            if isinstance(componente, tk.Canvas):
                componente.bind_all(
                    "<MouseWheel>", lambda e, canvas=componente: GestorScroll.scroll_simple(canvas, e)
                )


# Función para restablecer el scroll en una pestaña
def restablecer_scroll_vista1(canvas, panel, ventana_canvas):
    return GestorScroll.restablecer_scroll(canvas, panel, ventana_canvas)


# Función para mostrar canciones filtradas en vista de detalle (álbum/artista)
def mostrar_canciones_elemento_filtradas(elemento, tipo_pagina, texto_busqueda):
    global vista_detalle_activa, vista_detalle_panel, vista_detalle_canvas
    if not vista_detalle_activa:
        return
    # Verificar que el panel existe antes de intentar acceder a sus componentes
    if not vista_detalle_panel or not vista_detalle_panel.winfo_exists():
        return
    # Limpiar el panel actual
    for componente in vista_detalle_panel.winfo_children():
        componente.destroy()
    # Obtener las canciones del elemento
    if tipo_pagina == "Álbumes":
        canciones = controlador_biblioteca.obtener_canciones_album_controlador(elemento)
    elif tipo_pagina == "Artistas":
        canciones = controlador_biblioteca.obtener_canciones_artista_controlador(elemento)
    else:
        canciones = []
    # Filtrar canciones si hay texto de búsqueda
    if texto_busqueda.strip():
        canciones_filtradas = [
            cancion
            for cancion in canciones
            if (
                texto_busqueda.lower() in cancion.titulo_cancion.lower()
                or texto_busqueda.lower() in cancion.artista.lower()
                or texto_busqueda.lower() in cancion.album.lower()
            )
        ]
    else:
        canciones_filtradas = canciones
    # Crear botones para cada canción filtrada
    for cancion in canciones_filtradas:
        crear_boton_cancion(cancion, vista_detalle_panel)
    # Resetear el scroll del canvas y panel
    resetear_scroll_canvas(vista_detalle_canvas, vista_detalle_panel)


# Función genérica para configurar la interfaz de cualquier pestaña
def configurar_interfaz_pestania(nombre_pestania):
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña
    pestania = paginas_canciones.tab(nombre_pestania)
    # Limpiar la pestaña
    for componente in pestania.winfo_children():
        componente.destroy()
    # Crear canvas con scroll
    canvas, panel_botones, _ = crear_canvas_con_scroll(pestania, True, paginas_canciones)
    return canvas, panel_botones


# Función para configurar la interfaz de albumes
def configurar_interfaz_albumes():
    return configurar_interfaz_pestania("Álbumes")


# Función para configurar la interfaz artistas
def configurar_interfaz_artistas():
    return configurar_interfaz_pestania("Artistas")


# Función para configurar la interfaz de Me_gusta
def configurar_interfaz_me_gusta():
    return configurar_interfaz_pestania("Me gusta")


# Función para configurar la interfaz de Favoritos
def configurar_interfaz_favoritos():
    return configurar_interfaz_pestania("Favoritos")


# Función para mostrar las canciones de un álbum
def mostrar_canciones_album(album):
    return mostrar_detalles_cancion("Álbumes", album, actualizar_vista_albumes)


# Función para actualizar la vista de las canciones
def actualizar_vista_canciones(panel):
    try:
        # Limpiar completamente el panel de botones
        for componente in panel.winfo_children():
            componente.destroy()
        # Limpiar referencias en los diccionarios
        botones_canciones.clear()
        botones_opciones_canciones.clear()
        # Recrear todos los botones de canciones
        for cancion in controlador_biblioteca.obtener_todas_canciones_controlador():
            crear_boton_cancion(cancion, panel)
        # Resetear el scroll del canvas y panel
        resetear_scroll_canvas(canvas_canciones, panel)
    except Exception as e:
        print(f"Error al actualizar vista de canciones: {e}")


# Función para actualizar la vista de álbumes
def actualizar_vista_albumes():
    panel_botones_albumes = configurar_interfaz_albumes()[1]
    # Obtener todos los álbumes
    albumes = controlador_biblioteca.obtener_todos_albumes_controlador()
    crear_boton_album(albumes, panel_botones_albumes)
    # Obtener el canvas asociado a esta pestaña
    pestania_albumes = paginas_canciones.tab("Álbumes")
    for componente in pestania_albumes.winfo_children():
        if isinstance(componente, tk.Canvas):
            # Resetear el scroll del canvas y panel
            resetear_scroll_canvas(componente, panel_botones_albumes)
            break


# Función para actualizar la vista de artistas
def actualizar_vista_artistas():
    panel_botones_artistas = configurar_interfaz_artistas()[1]
    # Obtener todos los artistas
    artistas = controlador_biblioteca.obtener_todos_artistas_controlador()
    # Usar la función auxiliar para crear botones
    crear_boton_artista(artistas, panel_botones_artistas)
    # Obtener el canvas asociado a esta pestaña
    pestania_artistas = paginas_canciones.tab("Artistas")
    for componente in pestania_artistas.winfo_children():
        if isinstance(componente, tk.Canvas):
            # Resetear el scroll del canvas y panel
            resetear_scroll_canvas(componente, panel_botones_artistas)
            break


# Función genérica para configurar vista de listas de canciones
def configurar_vista_lista_canciones(nombre_pestania, lista_canciones, filtro=None):
    # Usar la función existente para la configuración básica de la interfaz
    canvas, panel_botones = configurar_interfaz_pestania(nombre_pestania)
    # Aplicar filtro si se especifica
    if filtro:
        canciones_a_mostrar = [
            c
            for c in lista_canciones
            if (
                filtro.lower() in c.titulo_cancion.lower()
                or filtro.lower() in c.artista.lower()
                or filtro.lower() in c.album.lower()
            )
        ]
    else:
        canciones_a_mostrar = lista_canciones
    # Crear botones para cada canción en la lista
    for cancion in canciones_a_mostrar:
        crear_boton_cancion(cancion, panel_botones)
    resetear_scroll_canvas(canvas, panel_botones)
    return canvas, panel_botones


# Función para mostrar las canciones de Me_gusta filtradas
def mostrar_me_gusta_filtrados(texto_busqueda):
    canciones_me_gusta = controlador_biblioteca.obtener_canciones_me_gusta_controlador()
    configurar_vista_lista_canciones("Me gusta", canciones_me_gusta, texto_busqueda)


# Función para mostrar las canciones de favoritos filtradas
def mostrar_favoritos_filtrados(texto_busqueda):
    canciones_favoritas = controlador_biblioteca.obtener_canciones_favorito_controlador()
    configurar_vista_lista_canciones("Favoritos", canciones_favoritas, texto_busqueda)


# Función para actualizar la vista de Me_gusta
def actualizar_vista_me_gusta():
    canciones_me_gusta = controlador_biblioteca.obtener_canciones_me_gusta_controlador()
    configurar_vista_lista_canciones("Me gusta", canciones_me_gusta)


# Función para actualizar la vista de favoritos
def actualizar_vista_favoritos():
    canciones_favoritas = controlador_biblioteca.obtener_canciones_favorito_controlador()
    configurar_vista_lista_canciones("Favoritos", canciones_favoritas)


# Función para mostrar las canciones de un artista
def mostrar_canciones_artista(artista):
    return mostrar_detalles_cancion("Artistas", artista, actualizar_vista_artistas)


# Función para buscar canciones según el texto introducido
def buscar_cancion_vista(_event=None):
    global vista_detalle_activa, vista_detalle_tipo, vista_detalle_elemento
    # Obtener el texto de búsqueda
    texto_busqueda = entrada_busqueda.get().strip().lower()
    # Obtener la pestaña actual
    pestana_actual = paginas_canciones.get()
    # Si estamos en una vista de detalle (álbum/artista), buscar dentro de esas canciones
    if vista_detalle_activa:
        tipo_pagina = "Álbumes" if vista_detalle_tipo == "album" else "Artistas"
        mostrar_canciones_elemento_filtradas(vista_detalle_elemento, tipo_pagina, texto_busqueda)
        return
    # Si no hay texto de búsqueda, restaurar la vista original
    if not texto_busqueda:
        if pestana_actual == "Canciones":
            actualizar_vista_canciones(panel_botones_canciones)
            canvas_canciones.bind_all(
                "<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e)
            )
        elif pestana_actual == "Me gusta":
            actualizar_vista_me_gusta()
        elif pestana_actual == "Favoritos":
            actualizar_vista_favoritos()
        elif pestana_actual == "Álbumes":
            actualizar_vista_albumes()
        elif pestana_actual == "Artistas":
            actualizar_vista_artistas()
        return
    # Limpiar la vista actual según la pestaña
    if pestana_actual == "Canciones":
        mostrar_canciones_filtradas(texto_busqueda)
    elif pestana_actual == "Me gusta":
        mostrar_me_gusta_filtrados(texto_busqueda)
    elif pestana_actual == "Favoritos":
        mostrar_favoritos_filtrados(texto_busqueda)
    elif pestana_actual == "Álbumes":
        mostrar_albumes_filtrados(texto_busqueda)
    elif pestana_actual == "Artistas":
        mostrar_artistas_filtrados(texto_busqueda)
    # Asegurarnos de restablecer el scroll para la pestaña actual
    actualizar_pestana_seleccionada()


# Función para mostrar las canciones filtradas en la vista de canciones
def mostrar_canciones_filtradas(texto_busqueda):
    # Limpiar el panel de canciones
    for componente in panel_botones_canciones.winfo_children():
        componente.destroy()
    # Obtener las canciones filtradas
    canciones_filtradas = controlador_biblioteca.buscar_canciones_controlador(texto_busqueda)
    # Mostrar las canciones filtradas
    for cancion in canciones_filtradas:
        crear_boton_cancion(cancion, panel_botones_canciones)
    # Restablecer el scroll del canvas y panel
    resetear_scroll_canvas(canvas_canciones, panel_botones_canciones)
    # Restablecer el scroll
    canvas_canciones.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e))


# Función para mostrar artistas filtrados
def mostrar_artistas_filtrados(texto_busqueda):
    canvas_artistas, panel_botones_artistas = configurar_interfaz_artistas()
    # Filtrar artistas
    artistas_filtrados = [
        artista
        for artista in controlador_biblioteca.obtener_todos_artistas_controlador()
        if texto_busqueda.lower() in artista.lower()
    ]
    # Usar la función auxiliar para crear botones
    crear_boton_artista(artistas_filtrados, panel_botones_artistas)
    # Restablecer el scroll del canvas y panel
    resetear_scroll_canvas(canvas_artistas, panel_botones_artistas)


# Función para actualizar la vista de albumes filtrados
def mostrar_albumes_filtrados(texto_busqueda):
    canvas_albumes, panel_botones_albumes = configurar_interfaz_albumes()
    # Filtrar álbumes
    albumes_filtrados = [
        album
        for album in controlador_biblioteca.obtener_todos_albumes_controlador()
        if texto_busqueda.lower() in album.lower()
    ]
    crear_boton_album(albumes_filtrados, panel_botones_albumes)
    # Restablecer el scroll del canvas y panel
    resetear_scroll_canvas(canvas_albumes, panel_botones_albumes)


# Función para crear las barras iniciales
def crear_barras_espectro():
    global barras_espectro
    controlador_tema.colores()
    # Limpiar barras existentes
    for barra in barras_espectro:
        try:
            canvas_espectro.delete(barra)
        except Exception as e:
            # Error cuando el componente del canvas ha sido destruido o no está disponible
            print(f"Error al eliminar la barra del espectro: {e}")
            return
    barras_espectro.clear()
    # Obtener dimensiones del canvas
    ancho_canvas = canvas_espectro.winfo_width()
    alto_canvas = canvas_espectro.winfo_height()
    # Calcular ancho de barra y espacio entre barras dinámicamente
    espacio_total = ancho_canvas
    ancho_barra = max(2, int((espacio_total / NUMERO_BARRA) * 0.7))  # 70% para la barra
    espacio_entre_barra = (espacio_total / NUMERO_BARRA) * 0.3  # 30% para el espacio
    # Calcular posición inicial para centrar las barras
    x_inicial = (
        ancho_canvas - (NUMERO_BARRA * (ancho_barra + espacio_entre_barra) - espacio_entre_barra)
    ) // 2
    # Crear barras
    for i in range(NUMERO_BARRA):
        x1 = x_inicial + i * (ancho_barra + espacio_entre_barra)
        x2 = x1 + ancho_barra
        y1 = alto_canvas
        y2 = alto_canvas
        barra = canvas_espectro.create_rectangle(x1, y1, x2, y2, fill=controlador_tema.color_barras, width=0)
        barras_espectro.append(barra)
    controlador_tema.registrar_barras_espectro(canvas_espectro, barras_espectro)


# Función para actualizar la animación del espectro
def actualizar_espectro(*args):
    global ANIMACION_ESPECTRO_ACTIVA, alturas_barras
    # Si ya hay una animación activa, no iniciar otra
    if not ESTADO_REPRODUCCION and not any(altura > 0 for altura in alturas_barras):
        ANIMACION_ESPECTRO_ACTIVA = False
        return
    if not canvas_espectro.winfo_exists():  # Verificar si el canvas existe
        ANIMACION_ESPECTRO_ACTIVA = False
        return
    alto_canvas = canvas_espectro.winfo_height()
    # Si no estamos reproduciendo, ocultar las barras con una animación suave
    if not ESTADO_REPRODUCCION:
        for i in range(min(NUMERO_BARRA, len(barras_espectro))):
            # Reducir gradualmente la altura hasta llegar a cero
            alturas_barras[i] = max(0, int(alturas_barras[i] * 0.9))
            try:
                x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
                canvas_espectro.coords(
                    barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i]
                )
            except Exception as e:
                print(f"Error al ocultar la barra del espectro: {e}")
                ANIMACION_ESPECTRO_ACTIVA = False
                return
        # Continuar la animación de desvanecimiento mientras haya barras visibles
        if any(altura > 0 for altura in alturas_barras):
            ventana_principal.after(60, actualizar_espectro, *args)
        else:
            ANIMACION_ESPECTRO_ACTIVA = False
        return
    # Generar alturas aleatorias para simular el espectro
    for i in range(min(NUMERO_BARRA, len(barras_espectro))):
        # Generar altura con variación según la posición (efecto de onda)
        factor_posicion = 0.5 + 0.5 * abs(math.sin((i / NUMERO_BARRA) * math.pi))
        altura_base = random.randint(10, int(alto_canvas * 0.9 * factor_posicion))
        # Suavizar los cambios entre frames para una animación más fluida
        factor_suavizado = 0.7 + 0.3 * random.random()  # Variar ligeramente el factor de suavizado
        altura_objetivo = int(altura_base * factor_posicion)
        alturas_barras[i] = int(
            alturas_barras[i] * factor_suavizado + altura_objetivo * (1 - factor_suavizado)
        )
        # Actualizar altura de la barra
        try:
            x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
            canvas_espectro.coords(barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i])
        except Exception as e:
            # Error cuando el componente del canvas ha sido destruido o no está disponible
            print(f"Error al actualizar la barra del espectro: {e}")
            ANIMACION_ESPECTRO_ACTIVA = False
            return
    # Llamar a la función nuevamente después de un delay
    ventana_principal.after(60, actualizar_espectro, *args)


# Función para configurar el desplazamiento de texto en botones
def configurar_desplazamiento_texto(boton, texto_completo):
    animacion.configurar_desplazamiento_boton(boton, texto_completo, 50)


# Función para resetear el scroll de un canvas y su panel asociado
def resetear_scroll_canvas(canvas, panel):
    try:
        if canvas and canvas.winfo_exists() and panel and panel.winfo_exists():
            # Actualizar el panel para reflejar los cambios
            panel.update_idletasks()
            # Mover el scroll al inicio
            canvas.yview_moveto(0)
            # Actualizar la región de desplazamiento
            canvas.configure(scrollregion=canvas.bbox("all"))
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al resetear scroll del canvas: {e}")
        return False


# Función para abrir la ventana de configuración
def abrir_configuracion():
    try:
        configuracion.mostrar_ventana_configuracion()
    except Exception as e:
        print(f"Error al abrir la configuración: {e}")


# Función para actualizar el mini reproductor
def actualizar_mini_reproductor(*args):
    # Actualizar información en el mini reproductor si está abierto
    if (
        mini_reproductor.ventana_principal_mini_reproductor
        and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
    ):
        mini_reproductor.actualizar_informacion()
        # Actualizar el tiempo actual
        if controlador_reproductor.cancion_actual:
            tiempo_actual = controlador_reproductor.obtener_posicion_actual_controlador()
            minutos_actual = int(tiempo_actual // 60)
            segundos_actual = int(tiempo_actual % 60)
            mini_reproductor.etiqueta_tiempo_inicio_mini.configure(
                text=f"{minutos_actual:02d}:{segundos_actual:02d}"
            )
            # Actualizar progreso
            mini_reproductor.barra_progreso_mini.set(barra_progreso.get())
    # Llamar a esta función cada 500 ms si el mini reproductor está visible
    if (
        mini_reproductor.ventana_principal_mini_reproductor
        and mini_reproductor.ventana_principal_mini_reproductor.winfo_exists()
    ):
        ventana_principal.after(500, actualizar_mini_reproductor, *args)


# Función para minimizar la ventana
def abrir_minireproductor():
    try:
        mini_reproductor.mostrar_ventana_mini_reproductor()
        actualizar_mini_reproductor()
    except Exception as e:
        print(f"Error al abrir el mini reproductor: {e}")


# Función para reproducir una canción desde la lista de canciones
def abrir_estadisticas():
    try:
        estadisticas.mostrar_ventana_estadisticas()
    except Exception as e:
        print(f"Error al abrir las estadísticas: {e}")


# Función para abrir la ventana de atajos
def abrir_atajos():
    try:
        atajos.mostrar_ventana_atajos()
    except Exception as e:
        print(f"Error al abrir la ventana de atajos: {e}")


# Función para abrir la ventana de cola de reproducción
def abrir_cola_reproduccion():
    try:
        cola_reproduccion.mostrar_ventana_cola()
    except Exception as e:
        print(f"Error al abrir la cola de reproducción: {e}")


# ************************************** Ventana principal **************************************
# Crear ventana
ventana_principal = ctk.CTk()

# Título de la ventana
ventana_principal.title("Reproductor de música")

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()

# Calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ANCHO_PRINCIPAL) // 2
posicion_alto = (alto_pantalla - ALTO_PRINCIPAL) // 3

# Establecer la geometría de la ventana
ventana_principal.geometry(f"{ANCHO_PRINCIPAL}x{ALTO_PRINCIPAL}+{posicion_ancho}+{posicion_alto}")

# ========================================= Utilidades ==========================================
# Biblioteca de canciones
biblioteca = Biblioteca()

# Utilidades
utiles = UtilesGeneral()

# Animación
animacion = AnimacionGeneral()

# ===============================================================================================

# =================================== Controladores =============================================
# Controlador_tema de tema
controlador_tema = ControladorTema()

# Controlador de la biblioteca
controlador_biblioteca = ControladorBiblioteca(biblioteca)

# Controlador del reproductor
controlador_reproductor = ControladorReproductor()

# Controlador de archivos
controlador_archivos = ControladorArchivos()

# ===============================================================================================

# ================================= Configuración de la interfaz ================================
# Primero, cargar configuración
configuracion = controlador_archivos.cargar_ajustes_json_controlador()

# Apariencia (claro/oscuro)
APARIENCIA = configuracion.get("apariencia", "claro")

# Aplicar tema según configuración cargada
ctk.set_appearance_mode("dark" if APARIENCIA == "oscuro" else "light")

# Establecer el tema en el controlador
controlador_tema.tema_interfaz = APARIENCIA

# Establecer el icono del tema
controlador_tema.tema_iconos = "claro" if APARIENCIA == "oscuro" else "oscuro"

# Icono de la ventana según el tema cargado
cambiar_icono_tema(APARIENCIA)

# ===============================================================================================

# ==================================== Componentes gráficos =====================================
# Mini reproductor
mini_reproductor = MiniReproductor(ventana_principal, controlador_tema, controlador_reproductor)

# Configuración
configuracion = Configuracion(ventana_principal, controlador_tema)

# Estadísticas
estadisticas = Estadisticas(ventana_principal, controlador_tema, controlador_archivos, controlador_biblioteca)

# Atajos
atajos = Atajos(ventana_principal, controlador_tema)

# Cola de reproducción
cola_reproduccion = ColaReproduccion(
    ventana_principal,
    controlador_tema,
    controlador_reproductor,
    lambda: reproducir_desde_cola_vista(),
)

# ===============================================================================================

# =========================================== Atajos ============================================
# Cargar atajos personalizados
gestor_atajos = GestorAtajos()


# Función para verificar si el foco está en un widget de entrada
def verificar_foco_entrada():
    widget_con_foco = ventana_principal.focus_get()
    if widget_con_foco:
        # Verificar si es un Entry, Text u otro widget de entrada
        tipo_widget = widget_con_foco.winfo_class()
        return tipo_widget in ["Entry", "Text", "CTkEntry"]
    return False


# Mapeo de acciones a funciones
mapeo_acciones = {
    "reproducir_pausar": lambda event: reproducir_vista() if not verificar_foco_entrada() else None,
    "siguiente": lambda event: reproducir_siguiente_vista() if not verificar_foco_entrada() else None,
    "anterior": lambda event: reproducir_anterior_vista() if not verificar_foco_entrada() else None,
    "aumentar_volumen": lambda event: aumentar_volumen_vista() if not verificar_foco_entrada() else None,
    "disminuir_volumen": lambda event: disminuir_volumen_vista() if not verificar_foco_entrada() else None,
    "silenciar": lambda event: cambiar_silencio_vista() if not verificar_foco_entrada() else None,
    "modo_aleatorio": lambda event: cambiar_orden_vista() if not verificar_foco_entrada() else None,
    "repeticion": lambda event: cambiar_repeticion_vista() if not verificar_foco_entrada() else None,
    "visibilidad_panel": lambda event: cambiar_visibilidad_vista() if not verificar_foco_entrada() else None,
    "me_gusta": lambda event: agregar_me_gusta_vista() if not verificar_foco_entrada() else None,
    "favorito": lambda event: agregar_favorito_vista() if not verificar_foco_entrada() else None,
    "cola": lambda event: abrir_cola_reproduccion() if not verificar_foco_entrada() else None,
    "mini_reproductor": lambda event: abrir_minireproductor() if not verificar_foco_entrada() else None,
    "adelantar": lambda event: adelantar_reproduccion_vista() if not verificar_foco_entrada() else None,
    "retroceder": lambda event: retroceder_reproduccion_vista() if not verificar_foco_entrada() else None,
}

# Lista de teclas que requieren sintaxis especial en Tkinter
teclas_especiales = ["space", "Return", "BackSpace", "Tab", "Escape", "Delete", "Up", "Down", "Left", "Right"]

# Enlazar los atajos personalizados
for accion, metodo in mapeo_acciones.items():
    atajo = gestor_atajos.obtener_atajo(accion)
    if atajo:
        if "-" in atajo:
            # Combinación de teclas (e.g., "Control-Right")
            ventana_principal.bind(f"<{atajo}>", metodo)
        elif atajo in teclas_especiales:
            # Teclas especiales que requieren sintaxis
            ventana_principal.bind(f"<{atajo}>", metodo)
        else:
            # Tecla simple (e.g., "a", "1", etc.)
            ventana_principal.bind(atajo, metodo)

# ===============================================================================================


# ***********************************************************************************************

# ==================================== Contenedor principal =====================================
# Contenedor principal
contenedor_principal = tk.Frame(ventana_principal)
contenedor_principal.configure(
    bg=controlador_tema.color_fondo_principal,
    padx=5,
    pady=5,
)
contenedor_principal.pack(fill="both", expand=True)
controlador_tema.registrar_panel(contenedor_principal, es_principal=True)

# ===============================================================================================

# ======================================= Panel izquierda =======================================
# Contenedor izquierdo hecho con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    contenedor_principal, fg_color=controlador_tema.color_fondo, corner_radius=BORDES_REDONDEADOS_PANEL
)
contenedor_izquierda.pack(side="left", fill="both", expand=True)
controlador_tema.registrar_panel(contenedor_izquierda, es_ctk=True)

# ------------------------------- Seccion de controles superiores --------------------------------
# Contenedor superior
contenedor_superior = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_superior.pack(fill="both", padx=10, pady=(10, 3))

# Boton de ajustes
boton_ajustes = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=abrir_configuracion,
)
boton_ajustes.pack(side="right", padx=(5, 0))
controlador_tema.registrar_botones("ajustes", boton_ajustes)
crear_tooltip(boton_ajustes, "Configuración")

# Botón del tema del reproductor
boton_tema = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=cambiar_tema_vista,
)
boton_tema.pack(side="right", padx=(5, 0))
controlador_tema.registrar_botones("modo_oscuro", boton_tema)
crear_tooltip(boton_tema, "Cambiar a oscuro")

# Botón del panel lateral
boton_visibilidad = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=cambiar_visibilidad_vista,
)
boton_visibilidad.pack(side="right", padx=(5, 0))
controlador_tema.registrar_botones("ocultar", boton_visibilidad)
crear_tooltip(boton_visibilidad, "Ocultar lateral")


# Botón de estadísticas de reproducción
boton_estadisticas = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=abrir_estadisticas,
)
boton_estadisticas.pack(side="right", padx=(5, 0))
controlador_tema.registrar_botones("estadistica", boton_estadisticas)
crear_tooltip(boton_estadisticas, "Estadísticas de reproducción")

# Botón de ayuda de atajos
boton_atajos = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=abrir_atajos,
)
boton_atajos.pack(side="right")
controlador_tema.registrar_botones("atajos", boton_atajos)
crear_tooltip(boton_atajos, "Mostrar atajos de teclado")
# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de imagen de la canción -------------------------------
# Contenedor de imagen de la canción
contenedor_imagen = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_imagen.pack(fill="both", expand=True, padx=10, pady=3)

# Etiqueta de la imagen de la canción
imagen_cancion = ctk.CTkLabel(
    contenedor_imagen,
    width=300,
    height=300,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=controlador_tema.color_texto,
    text="Sin carátula",
)
imagen_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(imagen_cancion)


# -----------------------------------------------------------------------------------------------

# ----------------------------- Seccion de información de la canción ----------------------------
# Contenedor de información de la canción
contenedor_informacion = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_informacion.pack(fill="both", padx=10, pady=5)

# Etiqueta de información de la canción
etiqueta_nombre_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=20,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA + 5, "bold"),
    text_color=controlador_tema.color_texto,
    text="",
)
etiqueta_nombre_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_nombre_cancion)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=20,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=controlador_tema.color_texto,
    text="",
)
etiqueta_artista_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_artista_cancion)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=20,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=controlador_tema.color_texto,
    text="",
)
etiqueta_album_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_album_cancion)

etiqueta_anio_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=20,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=controlador_tema.color_texto,
    text="",
)
etiqueta_anio_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_anio_cancion)

controlador_reproductor.establecer_informacion_controlador(
    etiqueta_nombre_cancion,
    etiqueta_artista_cancion,
    etiqueta_album_cancion,
    etiqueta_anio_cancion,
    imagen_cancion,
)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion botones de gustos -------------------------------------
# Contenedor de botones de gustos
contenedor_botones_gustos = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_botones_gustos.pack(fill="both", padx=10, pady=3)

# Panel de botones de gustos
panel_botones_gustos = ctk.CTkFrame(contenedor_botones_gustos, fg_color="transparent")
panel_botones_gustos.pack(expand=True)

# Botones de gustos
boton_me_gusta = ctk.CTkButton(
    panel_botones_gustos,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=agregar_me_gusta_vista,
)
boton_me_gusta.pack(side="left", padx=(5, 0))
controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
crear_tooltip(boton_me_gusta, "Agregar a Me Gusta")

boton_favorito = ctk.CTkButton(
    panel_botones_gustos,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=agregar_favorito_vista,
)
boton_favorito.pack(side="left", padx=(5, 0))
controlador_tema.registrar_botones("favorito", boton_favorito)
crear_tooltip(boton_favorito, "Agregar a Favoritos")

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de espectro de audio ----------------------------------
# Contenedor de espectro de audio
contenedor_espectro = ctk.CTkFrame(contenedor_izquierda, height=100, fg_color="transparent")
contenedor_espectro.pack(fill="both", padx=10, pady=2)
contenedor_espectro.pack_propagate(False)

# Canvas para el espectro
canvas_espectro = tk.Canvas(contenedor_espectro, bg=controlador_tema.color_fondo, highlightthickness=0)
canvas_espectro.pack(fill="both", expand=True)
controlador_tema.registrar_canvas(canvas_espectro, es_tabview=False)

# Variables para el espectro
alturas_barras = [0] * NUMERO_BARRA
barras_espectro = []

# Vincular la creación de barras al evento de configuración del canvas
canvas_espectro.bind("<Configure>", lambda e: crear_barras_espectro())

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de barra de progreso ---------------------------------
# Contenedor de barra de progreso
contenedor_progreso = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_progreso.pack(fill="both", padx=10, pady=3)

# Panel de progreso
panel_progreso = ctk.CTkFrame(contenedor_progreso, fg_color="transparent")
panel_progreso.pack(fill="x", expand=True)

# Barra de progreso
barra_progreso = ctk.CTkProgressBar(
    panel_progreso,
    height=7,
    bg_color="transparent",
    fg_color=controlador_tema.color_hover,
    progress_color=controlador_tema.color_barra_progreso,
)
barra_progreso.pack(fill="x", padx=6, pady=(0, 3))
barra_progreso.set(0)
barra_progreso.bind("<Button-1>", iniciar_arrastre_progreso)
barra_progreso.bind("<B1-Motion>", durante_arrastre_progreso)
barra_progreso.bind("<ButtonRelease-1>", finalizar_arrastre_progreso)
controlador_tema.registrar_progress_bar(barra_progreso)

controlador_reproductor.establecer_barra_progreso_controlador(barra_progreso)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de tiempo de la canción -------------------------------
# Panel de tiempo
panel_tiempo = ctk.CTkFrame(contenedor_progreso, fg_color="transparent")
panel_tiempo.pack(fill="x", expand=True)

# Etiqueta de tiempo actual
etiqueta_tiempo_actual = ctk.CTkLabel(
    panel_tiempo,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=controlador_tema.color_texto,
    text="00:00",
)
etiqueta_tiempo_actual.pack(side="left")
controlador_tema.registrar_etiqueta(etiqueta_tiempo_actual)

# Etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=controlador_tema.color_texto,
    text="00:00",
)
etiqueta_tiempo_total.pack(side="right")
controlador_tema.registrar_etiqueta(etiqueta_tiempo_total)

controlador_reproductor.establecer_etiquetas_tiempo_controlador(etiqueta_tiempo_actual, etiqueta_tiempo_total)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de controles de reproducción --------------------------
# Contenedor de controles de reproducción
contenedor_controles_reproduccion = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_controles_reproduccion.pack(fill="both", padx=10, pady=3)

# Panel de controles
panel_controles_reproduccion = ctk.CTkFrame(contenedor_controles_reproduccion, fg_color="transparent")
panel_controles_reproduccion.pack(expand=True)

# Botones de control
boton_aleatorio = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=cambiar_orden_vista,
)
boton_aleatorio.pack(side="left", padx=5)
controlador_tema.registrar_botones("aleatorio", boton_aleatorio)
crear_tooltip(boton_aleatorio, "Reproducción aleatoria")

boton_repetir = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=cambiar_repeticion_vista,
)
boton_repetir.pack(side="left", padx=5)
controlador_tema.registrar_botones("no_repetir", boton_repetir)
crear_tooltip(boton_repetir, "No repetir")

boton_anterior = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=reproducir_anterior_vista,
)
boton_anterior.pack(side="left", padx=5)
controlador_tema.registrar_botones("anterior", boton_anterior)
crear_tooltip(boton_anterior, "Reproducir anterior")

boton_retroceder = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=retroceder_reproduccion_vista,
)
boton_retroceder.pack(side="left", padx=5)
controlador_tema.registrar_botones("retroceder", boton_retroceder)
crear_tooltip(boton_retroceder, f"Retrocede {TIEMPO_AJUSTE} segundos")

boton_reproducir = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=reproducir_vista,
)
boton_reproducir.pack(side="left", padx=5)
controlador_tema.registrar_botones("reproducir", boton_reproducir)
crear_tooltip(boton_reproducir, "Reproducir")

boton_adelantar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=adelantar_reproduccion_vista,
)
boton_adelantar.pack(side="left", padx=5)
controlador_tema.registrar_botones("adelantar", boton_adelantar)
crear_tooltip(boton_adelantar, f"Adelanta {TIEMPO_AJUSTE} segundos")

boton_siguiente = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=reproducir_siguiente_vista,
)
boton_siguiente.pack(side="left", padx=5)
controlador_tema.registrar_botones("siguiente", boton_siguiente)
crear_tooltip(boton_siguiente, "Reproducir siguiente")

boton_mostrar_cola = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=abrir_cola_reproduccion,
)
boton_mostrar_cola.pack(side="left", padx=5)
controlador_tema.registrar_botones("mostrar_cola", boton_mostrar_cola)
crear_tooltip(boton_mostrar_cola, "Mostrar la cola")

# boton_agregar_cola = ctk.CTkButton(
#     panel_controles_reproduccion,
#     width=ANCHO_BOTON,
#     height=ALTO_BOTON,
#     corner_radius=BORDES_REDONDEADOS_BOTON,
# fg_color=controlador_tema.color_boton,
# hover_color=controlador_tema.color_hover,
# font=(LETRA, TAMANIO_LETRA_BOTON),
# text_color=controlador_tema.color_texto,
#     text="",
# )
# boton_agregar_cola.pack(side="left", padx=5)
# controlador_tema.registrar_botones("agregar_cola", boton_agregar_cola)
# crear_tooltip(boton_agregar_cola, "Agregar a la cola")

boton_minimizar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=abrir_minireproductor,
)
boton_minimizar.pack(side="left", padx=5)
controlador_tema.registrar_botones("minimizar", boton_minimizar)
crear_tooltip(boton_minimizar, "Minimizar")

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de barra de volumen -----------------------------------
# Contenedor de barra de volumen
contenedor_volumen = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_volumen.pack(fill="both", padx=10, pady=(7, 10))

# Panel de volumen
panel_volumen = ctk.CTkFrame(contenedor_volumen, fg_color="transparent")
panel_volumen.pack(expand=True)

# Botón de silenciar
boton_silenciar = ctk.CTkButton(
    panel_volumen,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="",
    command=cambiar_silencio_vista,
)
boton_silenciar.pack(side="left")
controlador_tema.registrar_botones("silencio", boton_silenciar)
crear_tooltip(boton_silenciar, "Silenciar")

# Panel de elementos de volumen
panel_elementos_volumen = ctk.CTkFrame(panel_volumen, fg_color="transparent")
panel_elementos_volumen.pack(side="left", fill="x", expand=True)

# Barra de volumen
barra_volumen = ctk.CTkSlider(
    panel_elementos_volumen,
    bg_color="transparent",
    fg_color=controlador_tema.color_hover,
    progress_color=controlador_tema.color_barra_progreso,
    button_color=controlador_tema.color_texto,
    number_of_steps=100,
    hover=False,
    from_=0,
    to=100,
    command=cambiar_volumen_vista,
)
barra_volumen.set(NIVEL_VOLUMEN)
barra_volumen.pack(side="left", fill="x", expand=True, padx=(0, 5))
controlador_tema.registrar_slider(barra_volumen)

# Etiqueta de porcentaje de volumen
etiqueta_porcentaje_volumen = ctk.CTkLabel(
    panel_elementos_volumen,
    width=35,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=controlador_tema.color_texto,
    text=f"{NIVEL_VOLUMEN}%",
)
etiqueta_porcentaje_volumen.pack(side="left")
controlador_tema.registrar_etiqueta(etiqueta_porcentaje_volumen)


# -----------------------------------------------------------------------------------------------
# =============================================================================s==================

# ======================================== Panel derecha ========================================
# Contenedor principal de panel derecho
contenedor_derecha_principal = ctk.CTkFrame(
    contenedor_principal,
    width=ANCHO_PANEL_DERECHA + 5 if PANEL_LATERAL_VISIBLE else 0,
    fg_color=controlador_tema.color_fondo,
    corner_radius=BORDES_REDONDEADOS_PANEL,
)
contenedor_derecha_principal.pack(side="left", fill="both", padx=(5, 0))
contenedor_derecha_principal.pack_propagate(False)
controlador_tema.registrar_panel(contenedor_derecha_principal, es_ctk=True)

# Contenedor de panel derecho interno
contenedor_derecha = ctk.CTkFrame(
    contenedor_derecha_principal,
    fg_color="transparent",
)
contenedor_derecha.pack(side="left", fill="both", expand=True, padx=3, pady=3)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------
# Contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = ctk.CTkFrame(contenedor_derecha, fg_color="transparent")
contenedor_busqueda_ordenamiento.pack(fill="both", padx=5, pady=(5, 2))

# Panel de busqueda y ordenamiento
panel_elementos = ctk.CTkFrame(contenedor_busqueda_ordenamiento, fg_color="transparent")
panel_elementos.pack(fill="x", expand=True)

# Entrada de busqueda
entrada_busqueda = ctk.CTkEntry(
    panel_elementos,
    fg_color=controlador_tema.color_fondo,
    border_width=1,
    border_color=controlador_tema.color_borde,
    font=(LETRA, TAMANIO_LETRA_ENTRADA),
    placeholder_text="Buscar cancion...",
    placeholder_text_color=controlador_tema.color_texto,
    text_color=controlador_tema.color_texto,
)
entrada_busqueda.pack(side="left", fill="x", expand=True)
controlador_tema.registrar_entrada(entrada_busqueda)

# Vincular el evento de liberación de tecla con la función de búsqueda
entrada_busqueda.bind("<KeyRelease>", lambda _event: buscar_cancion_vista())

# # Botón de buscar
# boton_buscar = ctk.CTkButton(
#     panel_elementos,
#     width=ANCHO_BOTON,
#     height=ALTO_BOTON,
#     corner_radius=BORDES_REDONDEADOS_BOTON,
#     fg_color=controlador_tema.color_boton,
#     hover_color=controlador_tema.color_hover,
#     font=(LETRA, TAMANIO_LETRA_BOTON),
#     text_color=controlador_tema.color_texto,
#     text="",
#     command=cambiar_silencio_vista,
# )
# boton_buscar.pack(side="left", padx=(5, 0))
# controlador_tema.registrar_botones("buscar", boton_buscar)
# crear_tooltip(boton_buscar, "Buscar")

# # Opciones de ordenamiento en combobox
# opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Año", "Duración"]

# # Combobox de ordenamiento
# combo_ordenamiento = ctk.CTkComboBox(
#     panel_elementos,
#     fg_color=controlador_tema.color_fondo,
#     border_width=1,
#     border_color=controlador_tema.color_borde,
#     button_color=controlador_tema.color_fondo,
#     button_hover_color=controlador_tema.color_hover,
#     dropdown_fg_color=controlador_tema.color_fondo,
#     dropdown_hover_color=controlador_tema.color_hover,
#     dropdown_text_color=controlador_tema.color_texto,
#     font=(LETRA, TAMANIO_LETRA_COMBOBOX),
#     text_color=controlador_tema.color_texto,
#     values=opciones_ordenamiento,
#     state="readonly",
# )
# combo_ordenamiento.set("Elija una opcion")
# combo_ordenamiento.pack(side="left", padx=(5, 0))
# controlador_tema.registrar_combobox(combo_ordenamiento)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de lista de canciones --------------------------------
# Contenedor de lista de canciones
contenedor_lista_canciones = ctk.CTkFrame(
    contenedor_derecha,
    height=ALTO_TABVIEW,
    fg_color="transparent",
)
contenedor_lista_canciones.pack(fill="both", expand=True, padx=2)
contenedor_lista_canciones.pack_propagate(False)

# Lista de canciones
paginas_canciones = ctk.CTkTabview(
    contenedor_lista_canciones,
    fg_color=controlador_tema.color_base,
    segmented_button_fg_color=controlador_tema.color_segundario,
    segmented_button_selected_color=controlador_tema.color_fondo,
    segmented_button_selected_hover_color=controlador_tema.color_hover,
    segmented_button_unselected_color=controlador_tema.color_hover,
    segmented_button_unselected_hover_color=controlador_tema.color_fondo,
    text_color=controlador_tema.color_texto,
)
paginas_canciones.pack(fill="both", expand=True)
controlador_tema.registrar_tabview(paginas_canciones)

# Paginas de la lista de canciones
paginas_canciones.add("Canciones")
paginas_canciones.add("Álbumes")
paginas_canciones.add("Artistas")
paginas_canciones.add("Me gusta")
paginas_canciones.add("Favoritos")
paginas_canciones.add("Listas")

# Boton de prueba en canciones
pestania_canciones = paginas_canciones.tab("Canciones")

# Usar la función para crear canvas con scroll
canvas_canciones, panel_botones_canciones, panel_canvas = crear_canvas_con_scroll(
    pestania_canciones, True, paginas_canciones
)
# Vincular eventos
gestion_scroll = GestorScroll(canvas_canciones, panel_botones_canciones, panel_canvas)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de botones inferiores ---------------------------------
# Contenedor de botones inferiores
contenedor_inferior = ctk.CTkFrame(contenedor_derecha, fg_color="transparent")
contenedor_inferior.pack(fill="both", padx=5, pady=(5, 3))

# Panel de botones
panel_botones_inferiores = ctk.CTkFrame(contenedor_inferior, fg_color="transparent")
panel_botones_inferiores.pack(expand=True)

# Botones inferiores
boton_agregar_cancion = ctk.CTkButton(
    panel_botones_inferiores,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="Agregar Canción",
    command=agregar_cancion_vista,
)
boton_agregar_cancion.pack(side="left", padx=(0, 5))
controlador_tema.registrar_botones("agregar_cancion", boton_agregar_cancion)
crear_tooltip(boton_agregar_cancion, "Agregar canción")

boton_agregar_directorio = ctk.CTkButton(
    panel_botones_inferiores,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=controlador_tema.color_boton,
    hover_color=controlador_tema.color_hover,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=controlador_tema.color_texto,
    text="Agregar Carpeta",
    command=agregar_directorio_vista,
)
boton_agregar_directorio.pack(side="left", padx=(0, 5))
controlador_tema.registrar_botones("agregar_carpeta", boton_agregar_directorio)
crear_tooltip(boton_agregar_directorio, "Agregar carpeta")

# -----------------------------------------------------------------------------------------------
# ===============================================================================================

# Cargar los ajustes guardados
cargar_todos_ajustes()

# Establecer volumen inicial
controlador_reproductor.ajustar_volumen_controlador(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)

# Actualizar los botones de la interfaz al iniciar la ejecución
actualizar_iconos()

# Verificar el estado de la reproducción
verificar_estado_reproduccion()

# Cargar las canciones al iniciar
cargar_biblioteca_vista()

# Cargar la cola de reproducción al iniciar
cargar_cola_vista()

# Configurar el foco global para la ventana principal
utiles.configurar_quitar_foco_global(ventana_principal)

# Mostrar la ventana
ventana_principal.mainloop()
