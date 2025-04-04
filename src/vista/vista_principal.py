from controlador.controlador_reproductor import ControladorReproductor
from controlador.controlador_biblioteca import ControladorBiblioteca
from vista.componentes.cola_reproduccion import ColaReproduccion
from controlador.controlador_archivos import ControladorArchivos
from vista.componentes.mini_reproductor import MiniReproductor
from vista.componentes.configuracion import Configuracion
from controlador.controlador_tema import ControladorTema
from vista.componentes.estadisticas import Estadisticas
from vista.utiles.utiles_scroll import GestorScroll
from modelo.biblioteca import Biblioteca
from vista.utiles.utiles_vista import *
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
from constantes import *
import tkinter as tk
import random

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

# ========================================================================

# Diccionario para almacenar los botones de canciones
botones_canciones = {}
botones_opciones_canciones = {}
pestanas_cargadas = {
    "Me gusta": False,
    "Favoritos": False,
    "Álbumes": False,
    "Artistas": False,
    "Listas": False,
}


# Función para cambiar el tema de la interfaz
def cambiar_tema_vista():
    global APARIENCIA
    # Cambiar tema
    controlador_tema.cambiar_tema()
    # Actualizar la variable global APARIENCIA
    APARIENCIA = "oscuro" if APARIENCIA == "claro" else "claro"
    # Actualizar icono de tema
    if APARIENCIA == "claro":
        cambiar_icono_tema("claro")
        controlador_tema.registrar_botones("modo_oscuro", boton_tema)
        actualizar_tooltip(boton_tema, "Cambiar a oscuro")
    else:
        cambiar_icono_tema("oscuro")
        controlador_tema.registrar_botones("modo_claro", boton_tema)
        actualizar_tooltip(boton_tema, "Cambiar a claro")
    # Guardar todos los ajustes
    guardar_todos_ajustes()
    # Actualizar iconos
    actualizar_iconos()


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
    # Actualizar iconos en botones de opciones para todas las canciones
    for cancion, boton in botones_canciones.items():
        # Buscar el botón de opciones asociado y actualizar su icono
        frame_padre = boton.winfo_parent()
        if frame_padre:
            frame = boton.nametowidget(frame_padre)
            if frame and frame.winfo_exists():
                # Buscar el botón de opciones dentro del frame
                for widget in frame.winfo_children():
                    if isinstance(widget, ctk.CTkButton) and widget != boton:
                        # Actualizar el icono del botón de opciones
                        icono_opcion = cargar_icono_personalizado(
                            "opcion", controlador_tema.tema_iconos, (15, 20)
                        )
                        widget.configure(image=icono_opcion)
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
    controlador_archivos.guardar_ajustes(configuracion_guardada)


# Función para cargar todos los ajustes
def cargar_todos_ajustes():
    global APARIENCIA, NIVEL_VOLUMEN, MODO_ALEATORIO, MODO_REPETICION, ESTADO_SILENCIO, PANEL_LATERAL_VISIBLE
    # Cargar configuración desde archivo
    configuracion_cargada = controlador_archivos.cargar_ajustes()
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
    if APARIENCIA == "oscuro":
        cambiar_icono_tema("oscuro")
        controlador_tema.registrar_botones("modo_claro", boton_tema)
    else:
        cambiar_icono_tema("claro")
        controlador_tema.registrar_botones("modo_oscuro", boton_tema)
    # Ajustar volumen
    barra_volumen.set(NIVEL_VOLUMEN)
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)
    # Ajustar orden de reproducción
    controlador_reproductor.establecer_modo_aleatorio(MODO_ALEATORIO)
    # Ajustar modo de repetición
    controlador_reproductor.establecer_modo_repeticion(MODO_REPETICION)
    # Ajustar panel visible
    if not PANEL_LATERAL_VISIBLE:
        contenedor_derecha_principal.configure(width=0)
    # Actualizar todos los iconos según los estados cargados
    actualizar_iconos()
    # Recargar los colores del tema
    controlador_tema.colores()
    # Actualizar el tema de la interfaz
    controlador_tema.cambiar_tema()
    # Actualizar el tema de la interfaz forzando la actualización
    controlador_tema.cambiar_tema()


# Función para cargar la última canción reproducida
def cargar_ultima_cancion_reproducida():
    ultima_cancion_info = controlador_archivos.obtener_ultima_cancion_reproducida()
    if ultima_cancion_info:
        # Buscar la canción en la biblioteca
        ruta_cancion = Path(ultima_cancion_info["ruta"])
        for cancion in biblioteca.canciones:
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
                controlador_reproductor.actualizar_informacion_interfaz()
                # Actualizar estado de los botones de me gusta/favorito
                actualizar_estado_botones_gustos()
                return True
    return False


# Función para reproducir o pausar la canción
def reproducir_vista():
    global ESTADO_REPRODUCCION
    if not ESTADO_REPRODUCCION:
        # Verificar si hay una canción en la cola para reproducir
        if controlador_reproductor.cancion_actual:
            # Si hay una canción cargada pero no estaba sonando, empezar a reproducirla
            if not controlador_reproductor.reproduciendo:
                controlador_reproductor.reproducir_cancion(controlador_reproductor.cancion_actual)
            else:
                # Si ya estaba sonando pero pausada, solo reanudar
                controlador_reproductor.reanudar_reproduccion()
            # Actualizar estado e iconos
            ESTADO_REPRODUCCION = True
            controlador_tema.registrar_botones("pausa", boton_reproducir)
            actualizar_tooltip(boton_reproducir, "Pausar")
            actualizar_espectro()
    else:
        # Pausar reproducción
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
        controlador_reproductor.pausar_reproduccion()
        actualizar_tooltip(boton_reproducir, "Reproducir")


# Función para reproducir la canción seleccionada
def reproducir_cancion_desde_lista(cancion):
    global ESTADO_REPRODUCCION, biblioteca
    # Establecer la lista de reproducción actual
    controlador_reproductor.establecer_lista_reproduccion(
        biblioteca.canciones, biblioteca.canciones.index(cancion)
    )
    # Reproducir la canción
    controlador_reproductor.reproducir_cancion(cancion)
    # Registrar la reproducción en las estadísticas
    controlador_archivos.registrar_reproduccion(cancion)
    # Actualizar estado de reproducción
    ESTADO_REPRODUCCION = True
    # Cambiar icono del botón a pausa
    controlador_tema.registrar_botones("pausa", boton_reproducir)
    # Actualizar tooltip del botón
    actualizar_tooltip(boton_reproducir, "Pausar")
    # Iniciar animación del espectro
    actualizar_espectro()
    # Actualizar botones de Me Gusta y Favoritos
    actualizar_estado_botones_gustos()


# Función para actualizar el estado de reproducción desde la cola
def actualizar_estado_reproduccion_desde_cola():
    global ESTADO_REPRODUCCION
    ESTADO_REPRODUCCION = True
    controlador_tema.registrar_botones("pausa", boton_reproducir)
    actualizar_tooltip(boton_reproducir, "Pausar")
    actualizar_estado_botones_gustos()
    # También iniciar la animación del espectro
    actualizar_espectro()


# Función para reproducir la canción siguiente
def reproducir_siguiente_vista():
    global controlador_reproductor, ESTADO_REPRODUCCION
    resultado = controlador_reproductor.reproducir_siguiente()
    if resultado:
        # Canción reproducida exitosamente
        actualizar_estado_botones_gustos()
    else:
        # No se pudo reproducir la siguiente (fin de lista)
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
        actualizar_tooltip(boton_reproducir, "Reproducir")


# Función para reproducir la canción anterior
def reproducir_anterior_vista():
    global controlador_reproductor
    if controlador_reproductor.reproducir_anterior():
        # Canción reproducida exitosamente
        actualizar_estado_botones_gustos()


# Función para adelantar la reproducción
def adelantar_reproduccion_vista():
    controlador_reproductor.adelantar_reproduccion(TIEMPO_AJUSTE)
    # Actualizar tooltip con el valor actual
    crear_tooltip(boton_adelantar, f"Adelanta {TIEMPO_AJUSTE} segundos")


# Función para retroceder la reproducción
def retroceder_reproduccion_vista():
    controlador_reproductor.retroceder_reproduccion(TIEMPO_AJUSTE)
    # Actualizar tooltip con el valor actual
    crear_tooltip(boton_retroceder, f"Retrocede {TIEMPO_AJUSTE} segundos")


# Función para cambiar el volumen
def cambiar_volumen_vista(_event=None):
    global NIVEL_VOLUMEN, ESTADO_SILENCIO
    NIVEL_VOLUMEN = int(barra_volumen.get())
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
    # Si el volumen es ajustado manualmente, desactivamos el silencio
    if ESTADO_SILENCIO and NIVEL_VOLUMEN > 0:
        ESTADO_SILENCIO = False
    # Ajustamos el volumen real
    controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)
    # Actualizamos el icono
    actualizar_iconos()
    # Guardamos los ajustes
    guardar_todos_ajustes()


# Función para cambiar el estado de silencio
def cambiar_silencio_vista():
    global ESTADO_SILENCIO
    ESTADO_SILENCIO = not ESTADO_SILENCIO
    if ESTADO_SILENCIO:
        # Guardar volumen actual y silenciar
        controlador_reproductor.ajustar_volumen(0)
        controlador_tema.registrar_botones("silencio", boton_silenciar)
        actualizar_tooltip(boton_silenciar, "Quitar silencio")
    else:
        # Restaurar volumen anterior
        controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN)
        actualizar_tooltip(boton_silenciar, "Silenciar")
        cambiar_volumen_vista()
    guardar_todos_ajustes()


# Función para cambiar el orden de reproducción
def cambiar_orden_vista():
    global MODO_ALEATORIO
    MODO_ALEATORIO = not MODO_ALEATORIO
    # Informar al controlador_tema sobre el cambio en el modo de reproducción
    controlador_reproductor.establecer_modo_aleatorio(MODO_ALEATORIO)
    if MODO_ALEATORIO:
        controlador_tema.registrar_botones("aleatorio", boton_aleatorio)
        actualizar_tooltip(boton_aleatorio, "Reproducción aleatoria")
    else:
        controlador_tema.registrar_botones("orden", boton_aleatorio)
        actualizar_tooltip(boton_aleatorio, "Reproducción en orden")
    # Guardar configuración
    guardar_todos_ajustes()


# Función para cambiar la repetición de reproducción
def cambiar_repeticion_vista():
    global MODO_REPETICION
    MODO_REPETICION = (MODO_REPETICION + 1) % 3
    controlador_reproductor.establecer_modo_repeticion(MODO_REPETICION)
    # Icono de no repetir
    if MODO_REPETICION == 0:
        controlador_tema.registrar_botones("no_repetir", boton_repetir)
        actualizar_tooltip(boton_repetir, "No repetir")
    # Icono de repetir actual
    elif MODO_REPETICION == 1:
        controlador_tema.registrar_botones("repetir_actual", boton_repetir)
        actualizar_tooltip(boton_repetir, "Repetir actual")
    # Icono de repetir todo
    else:
        controlador_tema.registrar_botones("repetir_todo", boton_repetir)
        actualizar_tooltip(boton_repetir, "Repetir todo")
    # Guardar configuración
    guardar_todos_ajustes()


# Función para cambiar la visibilidad del panel
def cambiar_visibilidad_vista():
    global PANEL_LATERAL_VISIBLE
    PANEL_LATERAL_VISIBLE = not PANEL_LATERAL_VISIBLE
    if PANEL_LATERAL_VISIBLE:
        # Mostrar el panel
        contenedor_derecha_principal.configure(width=ANCHO_PANEL_DERECHA + 5)
        contenedor_derecha_principal.pack(side="left", fill="both", padx=(5, 0))
        controlador_tema.registrar_botones("ocultar", boton_visibilidad)
        actualizar_tooltip(boton_visibilidad, "Ocultar lateral")
    else:
        # Ocultar el panel
        contenedor_derecha_principal.configure(width=0)
        contenedor_derecha_principal.pack_forget()
        controlador_tema.registrar_botones("mostrar", boton_visibilidad)
        actualizar_tooltip(boton_visibilidad, "Mostrar lateral")
    # Guardar configuración
    guardar_todos_ajustes()


# Función para cambiar el estado de boton me gusta
def cambiar_me_gusta_vista():
    global ME_GUSTA
    cancion_actual = controlador_reproductor.cancion_actual
    if cancion_actual:
        controlador_biblioteca.marcar_me_gusta_controlador(cancion_actual)
        ME_GUSTA = not ME_GUSTA
        if ME_GUSTA:
            controlador_tema.registrar_botones("me_gusta_rojo", boton_me_gusta)
            actualizar_tooltip(boton_me_gusta, "Quitar de me gusta")
        else:
            controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
            actualizar_tooltip(boton_me_gusta, "Agregar a me gusta")
        # Guardar cambios
        guardar_biblioteca()
        # Marcar pestaña como no cargada para forzar actualización
        pestanas_cargadas["Me gusta"] = False
        # Actualizar vista si estamos en esa pestaña
        if paginas_canciones.get() == "Me gusta":
            actualizar_vista_me_gusta()
            pestanas_cargadas["Me gusta"] = True


# Función para cambiar el estado de "me gusta" de una canción desde el menú
def cambiar_me_gusta_menu(cancion):
    controlador_biblioteca.marcar_me_gusta_controlador(cancion)
    # Marcar pestaña como no cargada para forzar actualización
    pestanas_cargadas["Me gusta"] = False
    # Actualizar vista si estamos en esa pestaña
    if paginas_canciones.get() == "Me gusta":
        actualizar_vista_me_gusta()
        pestanas_cargadas["Me gusta"] = True
    # Guardar cambios
    guardar_biblioteca()
    # Si es la canción actual, actualizar también los botones de la interfaz principal
    if controlador_reproductor.cancion_actual == cancion:
        actualizar_estado_botones_gustos()


# Función para cambiar el estado de favorito
def cambiar_favorito_vista():
    global FAVORITO
    cancion_actual = controlador_reproductor.cancion_actual
    if cancion_actual:
        controlador_biblioteca.marcar_favorito_controlador(cancion_actual)
        FAVORITO = not FAVORITO
        if FAVORITO:
            controlador_tema.registrar_botones("favorito_amarillo", boton_favorito)
            actualizar_tooltip(boton_favorito, "Quitar de favorito")
        else:
            controlador_tema.registrar_botones("favorito", boton_favorito)
            actualizar_tooltip(boton_favorito, "Agregar a favorito")
        # Guardar cambios
        guardar_biblioteca()
        # Marcar pestaña como no cargada para forzar actualización
        pestanas_cargadas["Favoritos"] = False
        # Actualizar vista si estamos en esa pestaña
        if paginas_canciones.get() == "Favoritos":
            actualizar_vista_favoritos()
            pestanas_cargadas["Favoritos"] = True


# Función para cambiar el estado de "favorito" de una canción desde el menú
def cambiar_favorito_menu(cancion):
    controlador_biblioteca.marcar_favorito_controlador(cancion)
    # Marcar pestaña como no cargada para forzar actualización
    pestanas_cargadas["Favoritos"] = False
    # Actualizar vista si estamos en esa pestaña
    if paginas_canciones.get() == "Favoritos":
        actualizar_vista_favoritos()
        pestanas_cargadas["Favoritos"] = True
    # Guardar cambios
    guardar_biblioteca()
    # Si es la canción actual, actualizar también los botones de la interfaz principal
    if controlador_reproductor.cancion_actual == cancion:
        actualizar_estado_botones_gustos()


# Funciona para actualizar el estado de los botones de me gusta y favorito
def actualizar_estado_botones_gustos():
    global ME_GUSTA, FAVORITO
    cancion_actual = controlador_reproductor.cancion_actual
    if cancion_actual:
        # Actualizar estado de Me Gusta
        ME_GUSTA = cancion_actual.me_gusta
        if ME_GUSTA:
            controlador_tema.registrar_botones("me_gusta_rojo", boton_me_gusta)
            actualizar_tooltip(boton_me_gusta, "Quitar de me gusta")
        else:
            controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
            actualizar_tooltip(boton_me_gusta, "Agregar a me gusta")
        # Actualizar estado de Favorito
        FAVORITO = cancion_actual.favorito
        if FAVORITO:
            controlador_tema.registrar_botones("favorito_amarillo", boton_favorito)
            actualizar_tooltip(boton_favorito, "Quitar de favorito")
        else:
            controlador_tema.registrar_botones("favorito", boton_favorito)
            actualizar_tooltip(boton_favorito, "Agregar a favorito")
    else:
        # Sin canción actual
        ME_GUSTA = False
        FAVORITO = False
        controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
        controlador_tema.registrar_botones("favorito", boton_favorito)
        actualizar_tooltip(boton_me_gusta, "Agregar a me gusta")
        actualizar_tooltip(boton_favorito, "Agregar a favorito")


# Función para agregar canciones (puede ser llamada desde un botón)
def agregar_cancion_vista():
    rutas = filedialog.askopenfilenames(
        title="Seleccionar archivo de música",
        filetypes=[
            ("Archivos de audio", "*.mp3 *.flac *.m4a *.mp4 *.wav *.ogg"),
            ("Todos los archivos", "*.*"),
        ],
    )
    canciones_agregadas = []
    for ruta in rutas:
        cancion = controlador_biblioteca.agregar_cancion(Path(ruta))
        if cancion:
            canciones_agregadas.append(cancion)
    if canciones_agregadas:
        # Guardar la pestaña actual
        # pestana_actual = paginas_canciones.get()
        actualizar_todas_vistas_canciones()
        guardar_biblioteca()
        # Restaurar el binding de scroll según la pestaña actual
        actualizar_pestana_seleccionada()


# Función para agregar directorio (puede ser llamada desde un botón)
def agregar_directorio_vista():
    ruta = filedialog.askdirectory(title="Seleccionar directorio de música")
    if ruta:
        controlador_biblioteca.agregar_directorio(Path(ruta))
        # Guardar la pestaña actual
        # pestana_actual = paginas_canciones.get()
        actualizar_todas_vistas_canciones()
        guardar_biblioteca()
        # Restaurar el binding de scroll según la pestaña actual
        actualizar_pestana_seleccionada()


# Función para agregar una canción a la cola de reproducción
def agregar_a_cola_vista(cancion):
    # Verificar si hay una lista de reproducción existente
    if not controlador_reproductor.lista_reproduccion:
        # Si no hay cola, crear una nueva con esta canción
        controlador_reproductor.establecer_lista_reproduccion([cancion])
        # Mostrar mensaje de confirmación
        print(f"Se ha agregado a la cola: {cancion.titulo_cancion}")
        return
    # Si la canción ya está en la lista, mostrar mensaje
    if cancion in controlador_reproductor.lista_reproduccion:
        print(f"La canción '{cancion.titulo_cancion}' ya está en la cola")
        return
    # Añadir la canción a la lista actual
    controlador_reproductor.lista_reproduccion.append(cancion)
    # Si no hay reproducción activa, configurar esta como la siguiente
    if controlador_reproductor.indice_actual == -1:
        controlador_reproductor.indice_actual = 0
    # Guardar la cola automáticamente
    controlador_archivos_cola = ControladorArchivos()
    controlador_archivos_cola.guardar_cola_reproduccion(controlador_reproductor)
    # Mostrar mensaje de confirmación
    print(f"Se ha agregado a la cola: {cancion.titulo_cancion}")


# Función para eliminar una canción de la biblioteca
def eliminar_cancion_vista(cancion):
    # Verificar si la canción que se elimina está en reproducción
    if controlador_reproductor.cancion_actual == cancion:
        # Si está reproduciéndose, detener la reproducción
        controlador_reproductor.detener_reproduccion()
        # Limpiar la información en la interfaz
        controlador_reproductor.cancion_actual = None
        controlador_reproductor.actualizar_informacion_interfaz()
    # Eliminar la canción de la cola de reproducción si está en ella
    if cancion in controlador_reproductor.lista_reproduccion:
        # Obtener índice actual
        indice_actual = controlador_reproductor.indice_actual
        indice_cancion = controlador_reproductor.lista_reproduccion.index(cancion)
        # Eliminar la canción de la lista
        controlador_reproductor.lista_reproduccion.remove(cancion)
        # Ajustar el índice actual si es necesario
        if indice_cancion <= indice_actual and indice_actual > 0:
            controlador_reproductor.indice_actual -= 1
        elif len(controlador_reproductor.lista_reproduccion) == 0:
            controlador_reproductor.indice_actual = -1
        # Guardar la cola actualizada
        controlador_archivos.guardar_cola_reproduccion(controlador_reproductor)
    # Verificar si la canción está en la lista de "Me gusta" y eliminarla manualmente
    if cancion.me_gusta:
        cancion.me_gusta = False
        if cancion in biblioteca.me_gusta:
            biblioteca.me_gusta.remove(cancion)
    # Verificar si la canción está en la lista de "Favoritos" y eliminarla manualmente
    if cancion.favorito:
        cancion.favorito = False
        if cancion in biblioteca.favorito:
            biblioteca.favorito.remove(cancion)
    # Verificar y eliminar de la colección de artistas
    for artista, lista_canciones in list(biblioteca.por_artista.items()):
        if cancion in lista_canciones:
            lista_canciones.remove(cancion)
            # Si quedó vacía, eliminar la clave
            if not lista_canciones:
                biblioteca.por_artista.pop(artista, None)
    # Verificar y eliminar de la colección de álbumes
    for album, lista_canciones in list(biblioteca.por_album.items()):
        if cancion in lista_canciones:
            lista_canciones.remove(cancion)
            # Si quedó vacía, eliminar la clave
            if not lista_canciones:
                biblioteca.por_album.pop(album, None)
    # Eliminar de la colección por título
    if cancion.titulo_cancion.lower() in biblioteca.por_titulo:
        biblioteca.por_titulo.pop(cancion.titulo_cancion.lower(), None)
    # Finalmente, eliminar la canción de la biblioteca principal
    try:
        if cancion in biblioteca.canciones:
            biblioteca.canciones.remove(cancion)
    except Exception as e:
        print(f"Error al eliminar la canción de la lista principal: {e}")
    # Guardar los cambios en los archivos
    guardar_biblioteca()
    # Limpiar la referencia del botón de esta canción si existe
    if cancion in botones_canciones:
        # Destruir el botón físicamente
        if botones_canciones[cancion].winfo_exists():
            botones_canciones[cancion].destroy()
        # Eliminar la referencia del diccionario
        del botones_canciones[cancion]
    # Marcar todas las pestañas como no cargadas para forzar su reconstrucción
    for pestana in pestanas_cargadas:
        pestanas_cargadas[pestana] = False
    # Obtener la pestaña actual
    pestana_actual = paginas_canciones.get()
    # Reconstruir completamente la vista actual
    if pestana_actual == "Canciones":
        # Limpiar el panel de canciones
        for widget in panel_botones_canciones.winfo_children():
            widget.destroy()
        # Reconstruir la vista
        actualizar_vista_canciones(panel_botones_canciones)
    elif pestana_actual == "Me gusta":
        # Recrear el panel de Me gusta
        configurar_interfaz_pestania("Me gusta")
    elif pestana_actual == "Favoritos":
        # Recrear el panel de Favoritos
        configurar_interfaz_pestania("Favoritos")
    elif pestana_actual == "Álbumes":
        # Recrear el panel de Álbumes
        configurar_interfaz_albumes()
    elif pestana_actual == "Artistas":
        # Recrear el panel de Artistas
        configurar_interfaz_artistas()
    # Mostrar mensaje de confirmación
    print(f"Se ha eliminado de la biblioteca: {cancion.titulo_cancion}")


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


# Función para verificar el estado de reproducción
def verificar_estado_reproduccion():
    global ESTADO_REPRODUCCION
    # Verificar si la reproducción ha terminado naturalmente
    if ESTADO_REPRODUCCION and not controlador_reproductor.reproduciendo:
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
    # Llamar a esta función nuevamente después de un breve retraso
    ventana_principal.after(500, verificar_estado_reproduccion)


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


# Función para guardar la biblioteca cuando ocurren cambios
def guardar_biblioteca():
    global controlador_archivos, biblioteca, controlador_reproductor
    controlador_archivos.guardar_biblioteca(biblioteca, controlador_reproductor)


# Función para cargar la biblioteca al iniciar
def cargar_biblioteca_vista():
    if controlador_archivos.cargar_biblioteca(biblioteca):
        # Cargar ajustes primero para tener el tema correcto
        cargar_todos_ajustes()
        # Reinicializar la estructura de artistas para separar colaboraciones
        biblioteca.reinicializar_artistas()
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
    controlador_archivos.cargar_cola_reproduccion(controlador_reproductor, biblioteca)
    # Si hay canciones en la cola, actualizar la interfaz
    if controlador_reproductor.lista_reproduccion:
        # Establecer la canción actual sin reproducirla automáticamente
        indice = controlador_reproductor.indice_actual
        if 0 <= indice < len(controlador_reproductor.lista_reproduccion):
            controlador_reproductor.cancion_actual = controlador_reproductor.lista_reproduccion[indice]
            controlador_reproductor.actualizar_informacion_interfaz()
            # Actualizar estado de los botones de me gusta/favorito
            actualizar_estado_botones_gustos()
    # También podemos cargar la información de la última canción reproducida
    cargar_ultima_cancion_reproducida()


# Función para iniciar el desplazamiento del texto
def iniciar_desplazamiento_boton(boton):
    # Verificar si el botón tiene el atributo timer_id usando hasattr
    if hasattr(boton, "timer_id") and getattr(boton, "timer_id"):
        boton.after_cancel(getattr(boton, "timer_id"))
    # Reiniciar la posición
    setattr(boton, "pos_marquee", 0)
    animar_texto_boton(boton)


# Función para detener el desplazamiento del texto
def detener_desplazamiento_boton(boton, longitud_maxima=50):
    if hasattr(boton, "timer_id") and getattr(boton, "timer_id"):
        boton.after_cancel(getattr(boton, "timer_id"))
    # Mostrar texto truncado al detener
    texto_completo = getattr(boton, "texto_completo", "")
    boton.configure(text=texto_completo[:longitud_maxima] + "...")


# Función para animar el texto del botón
def animar_texto_boton(boton, longitud_maxima=50):
    # Verificar si tiene el atributo texto_completo
    if not hasattr(boton, "texto_completo"):
        return
    texto_completo = getattr(boton, "texto_completo")
    pos = getattr(boton, "pos_marquee", 0)
    # Control de la posición de desplazamiento
    if pos == 0:
        # Al inicio, pausa
        if not hasattr(boton, "pausa_inicio"):
            setattr(boton, "pausa_inicio", 0)
        pausa_actual = getattr(boton, "pausa_inicio")
        if pausa_actual < 8:  # Pausa de 1 segundo (8 * 125ms)
            setattr(boton, "pausa_inicio", pausa_actual + 1)
            texto_visible = texto_completo[:longitud_maxima]
            boton.configure(text=texto_visible + "...")
            timer_id = boton.after(125, lambda: animar_texto_boton(boton, longitud_maxima))
            setattr(boton, "timer_id", timer_id)
            return
        else:
            setattr(boton, "pausa_inicio", 0)
    # Si el texto llega al final, reiniciar
    if pos >= len(texto_completo) - longitud_maxima:
        # Pausa al final
        if not hasattr(boton, "pausa_final"):
            setattr(boton, "pausa_final", 0)
        pausa_actual = getattr(boton, "pausa_final")
        if pausa_actual < 8:  # Pausa de 1 segundo (8 * 125ms)
            setattr(boton, "pausa_final", pausa_actual + 1)
            texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
            boton.configure(text=texto_visible)
            timer_id = boton.after(125, lambda: animar_texto_boton(boton, longitud_maxima))
            setattr(boton, "timer_id", timer_id)
            return
        else:
            setattr(boton, "pausa_final", 0)
            setattr(boton, "pos_marquee", 0)
            texto_visible = texto_completo[:longitud_maxima]
            boton.configure(text=texto_visible + "...")
            timer_id = boton.after(125, lambda: animar_texto_boton(boton, longitud_maxima))
            setattr(boton, "timer_id", timer_id)
            return
    # Desplazamiento normal
    texto_visible = texto_completo[pos : pos + longitud_maxima]
    boton.configure(text=texto_visible)
    setattr(boton, "pos_marquee", pos + 1)
    timer_id = boton.after(125, lambda: animar_texto_boton(boton, longitud_maxima))
    setattr(boton, "timer_id", timer_id)


# Función para configurar el desplazamiento de texto en botones
def configurar_desplazamiento_texto(boton, texto_completo, longitud_maxima=55):
    # Si el texto es más corto que el límite, simplemente mostrarlo
    if len(texto_completo) <= longitud_maxima:
        boton.configure(text=texto_completo)
        return
    # Almacenar el texto completo como atributo del botón usando setattr
    setattr(boton, "texto_completo", texto_completo)
    setattr(boton, "pos_marquee", 0)
    setattr(boton, "timer_id", None)
    # Vincular eventos de ratón para activar/desactivar el desplazamiento
    boton.bind("<Enter>", lambda event: iniciar_desplazamiento_boton(boton))
    boton.bind("<Leave>", lambda event: detener_desplazamiento_boton(boton, longitud_maxima))
    # Mostrar inicialmente el texto truncado con elipsis
    boton.configure(text=texto_completo[:longitud_maxima] + "...")


# Función para crear botones para cada canción en la biblioteca
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
        width=ANCHO_BOTON + 8,
        height=ALTO_BOTON + 8,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text=texto_cancion,
        command=lambda c=cancion: reproducir_cancion_desde_lista(c),
    )
    boton_cancion.pack(side="left", fill="both", expand=True)
    # -------------------------------------------------------------------------------------------

    # ------------------------------------ Boton de opciones ------------------------------------
    # Cargar icono de opciones
    icono_opcion = cargar_icono_personalizado("opcion", controlador_tema.tema_iconos, (15, 20))
    # Botón de opciones
    boton_opciones = ctk.CTkButton(
        panel_lista_cancion,
        width=ANCHO_BOTON + 8,
        height=ALTO_BOTON + 8,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text="",
        image=icono_opcion,
        command=lambda c=cancion: mostrar_menu_cancion(c, panel_lista_cancion),
    )
    boton_opciones.pack(side="right", padx=(1, 0))
    crear_tooltip(boton_opciones, "Opciones")
    # -------------------------------------------------------------------------------------------

    # Registrar botones en el controlador de tema
    controlador_tema.registrar_botones(f"cancion_{cancion.titulo_cancion}", boton_cancion)
    controlador_tema.registrar_botones(f"opciones_{cancion.titulo_cancion}", boton_opciones)
    botones_canciones[cancion] = boton_cancion
    # Configurar desplazamiento si el texto es largo
    configurar_desplazamiento_texto(boton_cancion, texto_cancion)
    # Vincular clic derecho al botón principal para mostrar el menú
    boton_cancion.bind("<Button-3>", lambda event, c=cancion: mostrar_menu_cancion(c, panel_lista_cancion))
    return panel_lista_cancion


# Función para crear una opción de menú en un menú contextual
def crear_opcion_menu(panel_menu_opciones, texto, comando, tiene_separador=False):
    if tiene_separador:
        # -------------------------..--- Separador entre opciones -------------------------------
        separador = ctk.CTkFrame(
            panel_menu_opciones,
            fg_color=controlador_tema.color_hover,
            height=1,
        )
        separador.pack(fill="x", padx=5, pady=3)
        # ---------------------------------------------------------------------------------------
    # ------------------------------------ Botón de opción --------------------------------------
    boton_opcion = ctk.CTkButton(
        panel_menu_opciones,
        width=ANCHO_BOTON + 5,
        height=ALTO_BOTON + 5,
        fg_color="transparent",
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text=texto,
        anchor="w",
        command=lambda: [comando(), panel_menu_opciones.master.destroy()],
    )
    boton_opcion.pack(fill="x", padx=2, pady=1)
    # -------------------------------------------------------------------------------------------


# Función para cerrar el menú cuando pierde el foco
def cerrar_menu_al_desenfocar(menu_ventana, _event=None):
    # Verificar si el menú sigue existiendo
    if not menu_ventana.winfo_exists():
        return
    # Obtener el widget que tiene el foco ahora
    focused_widget = menu_ventana.focus_get()
    # Si nada tiene el foco o el foco no está en el menú o sus hijos
    if not focused_widget or not str(focused_widget).startswith(str(menu_ventana)):
        try:
            # Limpiar el binding adicional antes de destruir
            ventana_principal.unbind("<Button-1>")
            menu_ventana.destroy()
        except Exception as e:
            print(f"Error al cerrar menú: {e}")


# Función para mostrar el menú contextual personalizado de una canción
def mostrar_menu_cancion(cancion, panel_padre):
    # Verificar si ya existe un menú abierto y cerrarlo
    for widget in ventana_principal.winfo_children():
        if isinstance(widget, ctk.CTkToplevel) and hasattr(widget, "menu_opciones"):
            widget.destroy()
    # Obtener colores actuales del tema
    controlador_tema.colores()
    # Crear una ventana de nivel superior para el menú
    menu_ventana = ctk.CTkToplevel(ventana_principal)
    # Marcar esta ventana como un menú contextual
    menu_ventana.menu_opciones = True
    menu_ventana.title("")
    menu_ventana.geometry("175x0")
    menu_ventana.overrideredirect(True)
    menu_ventana.configure(fg_color=controlador_tema.color_fondo)
    menu_ventana.attributes("-topmost", True)
    # ----------------------------------- Panel menu opciones -----------------------------------
    # Contenedor principal del menú
    panel_menu_opciones = ctk.CTkFrame(
        menu_ventana, corner_radius=BORDES_REDONDEADOS_PANEL, fg_color=controlador_tema.color_fondo
    )
    panel_menu_opciones.pack(fill="both", expand=True)
    # -------------------------------------------------------------------------------------------
    # Agregar opciones al menú
    crear_opcion_menu(
        panel_menu_opciones, "Reproducir ahora", lambda: reproducir_cancion_desde_lista(cancion)
    )
    crear_opcion_menu(panel_menu_opciones, "Agregar a la cola", lambda: agregar_a_cola_vista(cancion))
    # Separador antes de opciones de Me gusta/Favorito
    texto_me_gusta = "Quitar de Me gusta" if cancion.me_gusta else "Agregar a Me gusta"
    crear_opcion_menu(panel_menu_opciones, texto_me_gusta, lambda: cambiar_me_gusta_menu(cancion), True)
    texto_favorito = "Quitar de Favoritos" if cancion.favorito else "Agregar a Favoritos"
    crear_opcion_menu(panel_menu_opciones, texto_favorito, lambda: cambiar_favorito_menu(cancion))
    # Separador antes de opciones adicionales
    crear_opcion_menu(
        panel_menu_opciones, "Ver información", lambda: print(f"Ver info de: {cancion.titulo_cancion}"), True
    )
    crear_opcion_menu(
        panel_menu_opciones, "Eliminar de la biblioteca", lambda: eliminar_cancion_vista(cancion)
    )
    # Actualizar el panel para obtener su altura real
    panel_menu_opciones.update_idletasks()
    altura_real = panel_menu_opciones.winfo_reqheight()
    # Posicionar el menú junto al botón
    x = panel_padre.winfo_rootx() + panel_padre.winfo_width() - 200
    y = panel_padre.winfo_rooty()
    # Asegurar que el menú no salga de la pantalla
    screen_width = menu_ventana.winfo_screenwidth()
    if x + 200 > screen_width:
        x = screen_width - 210
    # Establecer la geometría con la altura exacta del contenido
    menu_ventana.geometry(f"175x{altura_real}+{x}+{y}")
    # Vincular eventos para cerrar el menú
    menu_ventana.bind("<FocusOut>", lambda event: cerrar_menu_al_desenfocar(menu_ventana, event))
    menu_ventana.bind("<Button-1>", lambda e: menu_ventana.destroy())
    # Vincular clic en cualquier parte de la pantalla para cerrar el menú
    ventana_principal.bind("<Button-1>", lambda e: menu_ventana.destroy(), add="+")

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


# Función para actualizar la vista de las canciones en la biblioteca
def actualizar_vista_canciones(panel):
    # Limpiar botones existentes
    for cancion, boton in botones_canciones.items():
        try:
            # Eliminar el botón del controlador_tema de tema
            nombre_boton = f"cancion_{cancion.titulo_cancion}"
            nombre_opciones = f"opciones_{cancion.titulo_cancion}"
            controlador_tema.eliminar_boton(nombre_boton)
            controlador_tema.eliminar_boton(nombre_opciones)
            # Destruir el frame contenedor (que contiene el botón)
            if boton and boton.winfo_exists():
                frame_padre = boton.winfo_parent()
                if frame_padre:
                    frame = boton.nametowidget(frame_padre)
                    if frame and frame.winfo_exists():
                        frame.destroy()
        except Exception as e:
            print(f"Error al destruir el botón {cancion.titulo_cancion}: {e}")
            pass
    botones_canciones.clear()
    # Crear nuevos botones para cada canción
    for cancion in biblioteca.canciones:
        crear_boton_cancion(cancion, panel)
    # Forzar actualización del layout
    panel.update_idletasks()
    # Asegurar que el canvas se actualice correctamente y volver al inicio
    canvas_canciones.yview_moveto(0)
    canvas_canciones.configure(scrollregion=canvas_canciones.bbox("all"))


# Función para reestablecer el scroll en una pestaña
def restablecer_scroll_pestania(canvas, panel, ventana_canvas):
    # Limpiar cualquier binding anterior
    canvas.unbind_all("<MouseWheel>")
    # Crear una nueva instancia de GestorScroll
    gestor = GestorScroll(canvas, panel, ventana_canvas)
    # Forzar la actualización de la región de scroll
    panel.update_idletasks()
    canvas.yview_moveto(0)
    canvas.configure(scrollregion=canvas.bbox("all"))
    # Vincular el evento de rueda del ratón
    canvas.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas, e))
    return gestor


# Función para manejar cambios de pestaña
def actualizar_pestana_seleccionada():
    # Obtener nombre de la pestaña activa
    pestana_actual = paginas_canciones.get()
    # Desvincular el scroll wheel de todos los canvas para evitar conflictos
    canvas_canciones.unbind_all("<MouseWheel>")
    # Actualizar solo si no se ha cargado previamente
    if pestana_actual == "Me gusta" and not pestanas_cargadas["Me gusta"]:
        actualizar_vista_me_gusta()
        pestanas_cargadas["Me gusta"] = True
    elif pestana_actual == "Favoritos" and not pestanas_cargadas["Favoritos"]:
        actualizar_vista_favoritos()
        pestanas_cargadas["Favoritos"] = True
    elif pestana_actual == "Álbumes" and not pestanas_cargadas["Álbumes"]:
        actualizar_vista_albumes()
        pestanas_cargadas["Álbumes"] = True
    elif pestana_actual == "Artistas" and not pestanas_cargadas["Artistas"]:
        actualizar_vista_artistas()
        pestanas_cargadas["Artistas"] = True
    elif pestana_actual == "Listas" and not pestanas_cargadas["Listas"]:
        # Implementar cuando sea necesario
        pestanas_cargadas["Listas"] = True
    # Restaurar el binding correcto dependiendo de la pestaña activa
    if pestana_actual == "Canciones":
        canvas_canciones.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e))
    elif pestana_actual == "Me gusta":
        tab_me_gusta = paginas_canciones.tab("Me gusta")
        for widget in tab_me_gusta.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.bind_all(
                    "<MouseWheel>", lambda e, canvas=widget: GestorScroll.scroll_simple(canvas, e)
                )
    elif pestana_actual == "Favoritos":
        tab_favoritos = paginas_canciones.tab("Favoritos")
        for widget in tab_favoritos.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.bind_all(
                    "<MouseWheel>", lambda e, canvas=widget: GestorScroll.scroll_simple(canvas, e)
                )
    elif pestana_actual == "Álbumes":
        tab_albumes = paginas_canciones.tab("Álbumes")
        for widget in tab_albumes.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.bind_all(
                    "<MouseWheel>", lambda e, canvas=widget: GestorScroll.scroll_simple(canvas, e)
                )
    elif pestana_actual == "Artistas":
        tab_artistas = paginas_canciones.tab("Artistas")
        for widget in tab_artistas.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.bind_all(
                    "<MouseWheel>", lambda e, canvas=widget: GestorScroll.scroll_simple(canvas, e)
                )


# Función para actualizar todas las vistas de las canciones
def actualizar_todas_vistas_canciones():
    pestana_actual = paginas_canciones.get()
    # Actualizar la vista de canciones
    actualizar_vista_canciones(panel_botones_canciones)
    # Actualizar las demás vistas pero marcarlas como no cargadas
    pestanas_cargadas["Me gusta"] = False
    pestanas_cargadas["Favoritos"] = False
    pestanas_cargadas["Álbumes"] = False
    pestanas_cargadas["Artistas"] = False
    # Reestablecer el scroll para la pestaña actual
    if pestana_actual == "Canciones":
        canvas_canciones.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e))
    # Guardar la biblioteca después de las actualizaciones
    guardar_biblioteca()


# Función para mostrar los detalles de las canciones
def mostrar_canciones_detalle(tipo, elemento, funcion_volver):
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña correspondiente
    tab = paginas_canciones.tab(tipo)
    # Limpiar la pestaña
    for widget in tab.winfo_children():
        widget.destroy()
    # Crear contenedor para la visualización del detalle
    contenedor_detalles = ctk.CTkFrame(tab, fg_color="transparent")
    contenedor_detalles.pack(fill="both", expand=True)
    # Panel superior con botón volver y título
    panel_superior = ctk.CTkFrame(contenedor_detalles, fg_color="transparent")
    panel_superior.pack(fill="x", pady=(5, 10))
    # Icono de regrear
    icono_regresar = cargar_icono_personalizado("regresar", controlador_tema.tema_iconos, (12, 12))
    # Botón para volver a la lista
    boton_volver = ctk.CTkButton(
        panel_superior,
        width=ANCHO_BOTON + 4,
        height=ALTO_BOTON + 4,
        fg_color=controlador_tema.color_boton,
        hover_color=controlador_tema.color_hover,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text="Regresar",
        image=icono_regresar,
        command=funcion_volver,
    )
    boton_volver.pack(side="left")
    controlador_tema.registrar_botones(f"volver_{tipo.lower()}", boton_volver)
    crear_tooltip(boton_volver, "Regresar a la lista")
    # Título del elemento
    etiqueta_elemento = ctk.CTkLabel(
        panel_superior,
        fg_color="transparent",
        font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
        text_color=controlador_tema.color_texto,
        text=elemento,
        anchor="center",
    )
    etiqueta_elemento.pack(side="top", fill="x", expand=True)
    controlador_tema.registrar_etiqueta(etiqueta_elemento)
    # Usar la función existente para crear el canvas con scroll
    canvas_canciones_general, panel_canciones, _ = crear_canvas_con_scroll(
        contenedor_detalles, True, paginas_canciones
    )
    # Mostrar las canciones del elemento
    if tipo == "Álbumes":
        canciones = biblioteca.por_album.get(elemento, [])
    else:  # "Artistas"
        canciones = biblioteca.por_artista.get(elemento, [])
    for cancion in canciones:
        crear_boton_cancion(cancion, panel_canciones)
    # Actualizar la vista del canvas
    panel_canciones.update_idletasks()
    canvas_canciones_general.yview_moveto(0)
    canvas_canciones_general.configure(scrollregion=canvas_canciones_general.bbox("all"))
    return canvas_canciones_general, panel_canciones


# Función para crear un canvas con scroll y panel de botones
def crear_canvas_con_scroll(contenedor_padre, estabview=True, tabviewparent=None):
    canvas = tk.Canvas(contenedor_padre, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.configure(bg=paginas_canciones.cget("fg_color") if estabview else controlador_tema.color_fondo)
    controlador_tema.registrar_canvas(canvas, es_tabview=estabview, tabview_parent=tabviewparent)
    # Crear panel para el contenido
    panel_botones = ctk.CTkFrame(canvas, fg_color="transparent", corner_radius=0)
    panel_botones.pack(fill="both")
    controlador_tema.registrar_panel(panel_botones)
    # Crear ventana en el canvas para el panel
    canvas_ventana_general = canvas.create_window((0, 0), window=panel_botones)
    # Configurar scroll
    GestorScroll(canvas, panel_botones, canvas_ventana_general)
    return canvas, panel_botones, canvas_ventana_general


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
    # Actualizar la vista del canvas
    panel_botones.update_idletasks()
    canvas.yview_moveto(0)
    canvas.configure(scrollregion=canvas.bbox("all"))
    return canvas, panel_botones


# Función genérica para configurar la interfaz de cualquier pestaña
def configurar_interfaz_pestania(nombre_pestania):
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña
    tab = paginas_canciones.tab(nombre_pestania)
    # Limpiar la pestaña
    for widget in tab.winfo_children():
        widget.destroy()
    # Crear canvas con scroll
    canvas, panel_botones, _ = crear_canvas_con_scroll(tab, True, paginas_canciones)
    return canvas, panel_botones


# Función para configurar la interfaz de albumes
def configurar_interfaz_albumes():
    return configurar_interfaz_pestania("Álbumes")


# Función auxiliar para crear botones de álbumes
def crear_botones_albumes(albumes, canvas_albumes, panel_botones_albumes):
    # Crear botones para cada álbum
    for album in sorted(albumes):
        # Ignorar álbumes vacíos o sin nombre
        if album == "" or album == "Unknown Album" or album.lower() == "desconocido":
            continue
        boton_album = ctk.CTkButton(
            panel_botones_albumes,
            width=ANCHO_BOTON + 8,
            height=ALTO_BOTON + 8,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=album,
            command=lambda a=album: mostrar_canciones_album(a),
        )
        boton_album.pack(fill="both", pady=(0, 2), expand=True)
        controlador_tema.registrar_botones(f"album_{album}", boton_album)
        # Configurar desplazamiento si el texto es largo
        configurar_desplazamiento_texto(boton_album, album)
    panel_botones_albumes.update_idletasks()
    canvas_albumes.yview_moveto(0)
    canvas_albumes.configure(scrollregion=canvas_albumes.bbox("all"))


# Función para actualizar la vista de álbumes
def actualizar_vista_albumes():
    canvas_albumes, panel_botones_albumes = configurar_interfaz_albumes()
    # Obtener todos los álbumes
    albumes = biblioteca.por_album.keys()
    crear_botones_albumes(albumes, canvas_albumes, panel_botones_albumes)


# Función para mostrar las canciones de un álbum
def mostrar_canciones_album(album):
    return mostrar_canciones_detalle("Álbumes", album, actualizar_vista_albumes)


# Función para actualizar la vista de albunes filtrados
def mostrar_albumes_filtrados(texto_busqueda):
    canvas_albumes, panel_botones_albumes = configurar_interfaz_albumes()
    # Filtrar álbumes
    albumes_filtrados = [
        album for album in biblioteca.por_album.keys() if texto_busqueda.lower() in album.lower()
    ]
    crear_botones_albumes(albumes_filtrados, canvas_albumes, panel_botones_albumes)


# Función para configurar la interfaz artistas
def configurar_interfaz_artistas():
    return configurar_interfaz_pestania("Artistas")


# Función auxiliar para crear botones de artistas
def crear_botones_artistas(artistas, canvas_artistas, panel_botones_artistas):
    # Crear botones para cada artista
    for artista in sorted(artistas):
        # Ignorar artistas sin nombre o desconocidos
        if artista == "" or artista == "Unknown Artist" or artista.lower() == "desconocido":
            continue
        boton_artista = ctk.CTkButton(
            panel_botones_artistas,
            width=ANCHO_BOTON + 8,
            height=ALTO_BOTON + 8,
            fg_color=controlador_tema.color_boton,
            hover_color=controlador_tema.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=artista,
            command=lambda a=artista: mostrar_canciones_artista(a),
        )
        boton_artista.pack(fill="both", pady=(0, 2), expand=True)
        controlador_tema.registrar_botones(f"artista_{artista}", boton_artista)
        # Configurar desplazamiento si el texto es largo
        configurar_desplazamiento_texto(boton_artista, artista)
    panel_botones_artistas.update_idletasks()
    canvas_artistas.yview_moveto(0)
    canvas_artistas.configure(scrollregion=canvas_artistas.bbox("all"))


# Función para actualizar la vista de artistas
def actualizar_vista_artistas():
    canvas_artistas, panel_botones_artistas = configurar_interfaz_artistas()
    # Obtener todos los artistas
    artistas = biblioteca.por_artista.keys()
    # Usar la función auxiliar para crear botones
    crear_botones_artistas(artistas, canvas_artistas, panel_botones_artistas)


# Función para mostrar las canciones de un artista
def mostrar_canciones_artista(artista):
    return mostrar_canciones_detalle("Artistas", artista, actualizar_vista_artistas)


# Función para mostrar artistas filtrados
def mostrar_artistas_filtrados(texto_busqueda):
    canvas_artistas, panel_botones_artistas = configurar_interfaz_artistas()
    # Filtrar artistas
    artistas_filtrados = [
        artista for artista in biblioteca.por_artista.keys() if texto_busqueda.lower() in artista.lower()
    ]
    # Usar la función auxiliar para crear botones
    crear_botones_artistas(artistas_filtrados, canvas_artistas, panel_botones_artistas)


# Función para actualizar la vista de Me gusta
def actualizar_vista_me_gusta():
    configurar_vista_lista_canciones("Me gusta", biblioteca.me_gusta)


# Función para mostrar las canciones de Me gusta filtradas
def mostrar_me_gusta_filtrados(texto_busqueda):
    configurar_vista_lista_canciones("Me gusta", biblioteca.me_gusta, texto_busqueda)


# Función para actualizar la vista de favoritos
def actualizar_vista_favoritos():
    configurar_vista_lista_canciones("Favoritos", biblioteca.favorito)


# Función para mostrar las canciones de favoritos filtradas
def mostrar_favoritos_filtrados(texto_busqueda):
    configurar_vista_lista_canciones("Favoritos", biblioteca.favorito, texto_busqueda)


# Función para mostrar las canciones filtradas en la vista de canciones
def mostrar_canciones_filtradas(texto_busqueda):
    # Limpiar el panel de canciones
    for widget in panel_botones_canciones.winfo_children():
        widget.destroy()
    # Obtener las canciones filtradas
    canciones_filtradas = [
        cancion
        for cancion in biblioteca.canciones
        if texto_busqueda.lower() in cancion.titulo_cancion.lower()
        or texto_busqueda.lower() in cancion.artista.lower()
        or texto_busqueda.lower() in cancion.album.lower()
    ]
    # Mostrar las canciones filtradas
    for cancion in canciones_filtradas:
        crear_boton_cancion(cancion, panel_botones_canciones)
    # Forzar actualización de layout
    panel_botones_canciones.update_idletasks()
    # Restaurar la posición del scroll a la parte superior
    canvas_canciones.yview_moveto(0)
    # Actualizar la región de desplazamiento
    canvas_canciones.configure(scrollregion=canvas_canciones.bbox("all"))
    # Reestablecer el scroll
    canvas_canciones.bind_all("<MouseWheel>", lambda e: GestorScroll.scroll_simple(canvas_canciones, e))


# Función para buscar canciones según el texto introducido
def buscar_canciones(_event=None):
    # Obtener el texto de búsqueda
    texto_busqueda = entrada_busqueda.get().strip().lower()
    # Obtener la pestaña actual
    pestana_actual = paginas_canciones.get()
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


# Función para crear las barras iniciales
def crear_barras_espectro():
    global barras_espectro
    controlador_tema.colores()
    # Limpiar barras existentes
    for barra in barras_espectro:
        try:
            canvas_espectro.delete(barra)
        except Exception as e:
            # Error cuando el widget del canvas ha sido destruido o no está disponible
            print(f"Error al eliminar la barra del espectro: {e}")
            return
    barras_espectro.clear()
    # Obtener dimensiones del canvas
    ancho_canvas = canvas_espectro.winfo_width()
    alto_canvas = canvas_espectro.winfo_height()
    # Calcular ancho de barra y espacio entre barras dinámicamente
    espacio_total = ancho_canvas
    ancho_barra = max(2, (espacio_total / NUMERO_BARRA) * 0.7)  # 70% para la barra
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
        y2 = alto_canvas - alturas_barras[i]
        barra = canvas_espectro.create_rectangle(x1, y1, x2, y2, fill=controlador_tema.color_barras, width=0)
        barras_espectro.append(barra)


# Función para actualizar la animación del espectro
def actualizar_espectro():
    if not canvas_espectro.winfo_exists():  # Verificar si el canvas existe
        return
    alto_canvas = canvas_espectro.winfo_height()
    # Generar alturas aleatorias para simular el espectro
    for i in range(min(NUMERO_BARRA, len(barras_espectro))):
        # Calcular nueva altura con suavizado (70% actual + 30% objetivo)
        altura_objetivo = random.randint(10, int(alto_canvas * 0.9))  # Limitar al 90% de altura
        alturas_barras[i] = int(alturas_barras[i] * 0.7 + altura_objetivo * 0.3)
        # Actualizar altura de la barra
        try:
            x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
            canvas_espectro.coords(barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i])
        except Exception as e:
            # Error cuando el widget del canvas ha sido destruido o no está disponible
            print(f"Error al actualizar la barra del espectro: {e}")
            return
    # Llamar a la función nuevamente después de un delay
    if ESTADO_REPRODUCCION:
        ventana_principal.after(85, actualizar_espectro)


# Función para establecer el icono del tema
def cambiar_icono_tema(tema="claro"):
    establecer_icono_tema(ventana_principal, tema)


# Función para abrir la ventana de configuración
def abrir_configuracion():
    try:
        configuracion.mostrar_ventana_configuracion()
    except Exception as e:
        print(f"Error al abrir la configuración: {e}")


# Función para minimizar la ventana
def abrir_minireproductor():
    try:
        mini_reproductor.mostrar_ventana_mini_reproductor()
    except Exception as e:
        print(f"Error al abrir el mini reproductor: {e}")


# Función para reproducir una canción desde la lista de canciones
def abrir_estadisticas():
    try:
        estadisticas.mostrar_ventana_estadisticas()
    except Exception as e:
        print(f"Error al abrir las estadísticas: {e}")


# Función para abrir la ventana de cola de reproducción
def abrir_cola_reproduccion():
    try:
        cola_reproduccion.mostrar_ventana_cola()
    except Exception as e:
        print(f"Error al abrir la cola de reproducción: {e}")


# ************************************** Ventana principal **************************************
# Crear ventana
ventana_principal = ctk.CTk()

# Biblioteca de canciones
biblioteca = Biblioteca()

# Controlador_tema de tema
controlador_tema = ControladorTema()

# Controlador de la biblioteca
controlador_biblioteca = ControladorBiblioteca(biblioteca)

# Controlador del reproductor
controlador_reproductor = ControladorReproductor()

# Controlador de archivos
controlador_archivos = ControladorArchivos()

# Primero, cargar configuración (antes de establecer apariencia)
configuracion = controlador_archivos.cargar_ajustes()

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

# Mini reproductor
mini_reproductor = MiniReproductor(ventana_principal, controlador_tema)

# Configuración
configuracion = Configuracion(ventana_principal, controlador_tema)

# Estadísticas
estadisticas = Estadisticas(ventana_principal, controlador_tema, controlador_archivos, controlador_biblioteca)

# Cola de reproducción
cola_reproduccion = ColaReproduccion(
    ventana_principal,
    controlador_tema,
    controlador_reproductor,
    lambda: actualizar_estado_reproduccion_desde_cola(),
)

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana_principal.winfo_screenwidth()
alto_pantalla = ventana_principal.winfo_screenheight()

# Calcular la posición x,y para la ventana
posicion_ancho = (ancho_pantalla - ANCHO_PRINCIPAL) // 2
posicion_alto = (alto_pantalla - ALTO_PRINCIPAL) // 3

# Establecer la geometría de la ventana
ventana_principal.geometry(f"{ANCHO_PRINCIPAL}x{ALTO_PRINCIPAL}+{posicion_ancho}+{posicion_alto}")

# Título de la ventana
ventana_principal.title("Reproductor de música")

# ***********************************************************************************************

# ==================================== Contenedor principal =====================================
# Contenedor principal
conenedor_principal = tk.Frame(ventana_principal)
conenedor_principal.configure(
    bg=FONDO_PRINCIPAL_CLARO,
    padx=5,
    pady=5,
)
conenedor_principal.pack(fill="both", expand=True)
controlador_tema.registrar_panel(conenedor_principal, es_principal=True)

# ===============================================================================================

# ======================================= Panel izquierda =======================================
# Contenedor izquierdo hecho con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    conenedor_principal, fg_color=FONDO_CLARO, corner_radius=BORDES_REDONDEADOS_PANEL
)
contenedor_izquierda.pack(side="left", fill="both", expand=True)
controlador_tema.registrar_panel(contenedor_izquierda, es_ctk=True)

# ------------------------------- Seccion de controles superiores --------------------------------
# Contenedor superior
contenedor_superior = ctk.CTkFrame(contenedor_izquierda, fg_color="transparent")
contenedor_superior.pack(fill="both", padx=10, pady=(10, 3))

# Botones de la parte superior
boton_ajustes = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=abrir_configuracion,
)
boton_ajustes.pack(side=tk.RIGHT, padx=(5, 0))
controlador_tema.registrar_botones("ajustes", boton_ajustes)
crear_tooltip(boton_ajustes, "Configuración")

boton_tema = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=cambiar_tema_vista,
)
boton_tema.pack(side=tk.RIGHT, padx=(5, 0))
controlador_tema.registrar_botones("modo_oscuro", boton_tema)
crear_tooltip(boton_tema, "Cambiar a oscuro")

boton_visibilidad = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=cambiar_visibilidad_vista,
)
boton_visibilidad.pack(side=tk.RIGHT, padx=(5, 0))
controlador_tema.registrar_botones("ocultar", boton_visibilidad)
crear_tooltip(boton_visibilidad, "Ocultar lateral")


# En el contenedor_superior, junto a los otros botones
boton_estadisticas = ctk.CTkButton(
    contenedor_superior,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=abrir_estadisticas,
)
boton_estadisticas.pack(side=tk.RIGHT)
controlador_tema.registrar_botones("estadistica", boton_estadisticas)
crear_tooltip(boton_estadisticas, "Estadísticas de reproducción")
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
    font=(LETRA, TAMANIO_LETRA_VOLUMEN),
    text_color=TEXTO_CLARO,
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
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="",
)
etiqueta_nombre_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_nombre_cancion)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="",
)
etiqueta_artista_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_artista_cancion)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="",
)
etiqueta_album_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_album_cancion)

etiqueta_anio_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="",
)
etiqueta_anio_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_anio_cancion)

controlador_reproductor.establecer_informacion_interfaz(
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=cambiar_me_gusta_vista,
)
boton_me_gusta.pack(side="left", padx=(5, 0))
controlador_tema.registrar_botones("me_gusta", boton_me_gusta)
crear_tooltip(boton_me_gusta, "Agregar a Me Gusta")

boton_favorito = ctk.CTkButton(
    panel_botones_gustos,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=cambiar_favorito_vista,
)
boton_favorito.pack(side="left", padx=(5, 0))
controlador_tema.registrar_botones("favorito", boton_favorito)
crear_tooltip(boton_favorito, "Agregar a Favoritos")

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de espectro de audio ----------------------------------
# Contenedor de espectro de audio
contenedor_espectro = ctk.CTkFrame(contenedor_izquierda, height=100, fg_color="transparent")
contenedor_espectro.pack(fill="both", padx=10, pady=3)
contenedor_espectro.pack_propagate(False)

# Canvas para el espectro
canvas_espectro = tk.Canvas(contenedor_espectro, bg=FONDO_CLARO, highlightthickness=0)
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
    panel_progreso, height=5, progress_color=controlador_tema.color_barra_progreso
)
barra_progreso.pack(fill="x", padx=6, pady=(0, 3))
barra_progreso.set(0)
barra_progreso.bind("<Button-1>", iniciar_arrastre_progreso)
barra_progreso.bind("<B1-Motion>", durante_arrastre_progreso)
barra_progreso.bind("<ButtonRelease-1>", finalizar_arrastre_progreso)
controlador_tema.registrar_progress_bar(barra_progreso)

controlador_reproductor.establecer_barra_progreso(barra_progreso)

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
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_actual.pack(side="left")
controlador_tema.registrar_etiqueta(etiqueta_tiempo_actual)

# Etiqueta de tiempo total
etiqueta_tiempo_total = ctk.CTkLabel(
    panel_tiempo,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_TIEMPO),
    text_color=TEXTO_CLARO,
    text="00:00",
)
etiqueta_tiempo_total.pack(side=tk.RIGHT)
controlador_tema.registrar_etiqueta(etiqueta_tiempo_total)

controlador_reproductor.establecer_etiquetas_tiempo(etiqueta_tiempo_actual, etiqueta_tiempo_total)

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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    command=reproducir_anterior_vista,
)
boton_anterior.pack(side="left", padx=5)
controlador_tema.registrar_botones("anterior", boton_anterior)
crear_tooltip(boton_anterior, "Reproucir anterior")

boton_retroceder = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
#     fg_color=BOTON_CLARO,
#     hover_color=HOVER_CLARO,
#     font=(LETRA, TAMANIO_LETRA_BOTON),
#     text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
barra_volumen = ctk.CTkSlider(panel_elementos_volumen)
barra_volumen.configure(
    progress_color=FONDO_OSCURO,
    fg_color=HOVER_CLARO,
    button_color=FONDO_OSCURO,
    button_hover_color=HOVER_OSCURO,
    number_of_steps=100,
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
    font=(LETRA, TAMANIO_LETRA_VOLUMEN),
    text_color=TEXTO_CLARO,
    text=f"{NIVEL_VOLUMEN}%",
)
etiqueta_porcentaje_volumen.pack(side="left")
controlador_tema.registrar_etiqueta(etiqueta_porcentaje_volumen)


# -----------------------------------------------------------------------------------------------
# =============================================================================s==================

# ======================================== Panel derecha ========================================
# Contenedor principal de panel derecho
contenedor_derecha_principal = ctk.CTkFrame(
    conenedor_principal,
    width=ANCHO_PANEL_DERECHA + 5 if PANEL_LATERAL_VISIBLE else 0,
    fg_color=FONDO_CLARO,
    corner_radius=BORDES_REDONDEADOS_PANEL,
)
contenedor_derecha_principal.pack(side="left", fill="both", padx=(5, 0))
contenedor_derecha_principal.pack_propagate(False)
controlador_tema.registrar_panel(contenedor_derecha_principal, es_ctk=True)

# Contentedor de panel derecho interno
contenedor_derecha = ctk.CTkFrame(
    contenedor_derecha_principal,
    fg_color="transparent",
)
contenedor_derecha.pack(side="left", fill="both", expand=True, padx=3, pady=3)

# ------------------------------ Seccion de busqueda y ordenamiento -----------------------------
# Contenedor de busqueda y ordenamiento
contenedor_busqueda_ordenamiento = ctk.CTkFrame(contenedor_derecha, fg_color="transparent")
contenedor_busqueda_ordenamiento.pack(fill="both", padx=5, pady=(5, 0))

# Panel de busqueda y ordenamiento
panel_elementos = ctk.CTkFrame(contenedor_busqueda_ordenamiento, fg_color="transparent")
panel_elementos.pack(fill="x", expand=True)

# Entrada de busqueda
entrada_busqueda = ctk.CTkEntry(
    panel_elementos,
    fg_color=FONDO_CLARO,
    border_width=1,
    border_color=FONDO_OSCURO,
    font=(LETRA, TAMANIO_LETRA_ENTRADA),
    placeholder_text="Buscar cancion...",
    placeholder_text_color=TEXTO_CLARO,
    text_color=TEXTO_CLARO,
)
entrada_busqueda.pack(side="left", fill="x", expand=True)
controlador_tema.registrar_entrada(entrada_busqueda)

# Vincular el evento de liberación de tecla con la función de búsqueda
entrada_busqueda.bind("<KeyRelease>", lambda _event: buscar_canciones())

# Opciones de ordenamiento en combobox
opciones_ordenamiento = ["Nombre", "Artista", "Álbum", "Año", "Duración"]

# Combobox de ordenamiento
combo_ordenamiento = ctk.CTkComboBox(
    panel_elementos,
    fg_color=FONDO_CLARO,
    border_width=1,
    border_color=FONDO_OSCURO,
    button_color=FONDO_CLARO,
    button_hover_color=HOVER_CLARO,
    dropdown_fg_color=FONDO_CLARO,
    dropdown_hover_color=HOVER_CLARO,
    dropdown_text_color=TEXTO_CLARO,
    font=(LETRA, TAMANIO_LETRA_COMBOBOX),
    text_color=TEXTO_CLARO,
    values=opciones_ordenamiento,
    state="readonly",
)
combo_ordenamiento.set("Elija una opcion")
combo_ordenamiento.pack(side="left", padx=(5, 0))
controlador_tema.registrar_combobox(combo_ordenamiento)

# -----------------------------------------------------------------------------------------------

# ------------------------------- Seccion de lista de canciones --------------------------------
# Contenedor de lista de canciones
contenedor_lista_canciones = ctk.CTkFrame(
    contenedor_derecha,
    height=ALTO_TABVIEW,
    fg_color="transparent",
)
contenedor_lista_canciones.pack(fill="both", expand=True, padx=3)
contenedor_lista_canciones.pack_propagate(False)

# Lista de canciones
paginas_canciones = ctk.CTkTabview(
    contenedor_lista_canciones,
    fg_color=CLARO,
    segmented_button_fg_color=CLARO_SEGUNDARIO,
    segmented_button_selected_color=FONDO_CLARO,
    segmented_button_selected_hover_color=HOVER_CLARO,
    segmented_button_unselected_color=HOVER_CLARO,
    segmented_button_unselected_hover_color=FONDO_CLARO,
    text_color=TEXTO_CLARO,
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
tab_canciones = paginas_canciones.tab("Canciones")

# Usar la función para crear canvas con scroll
canvas_canciones, panel_botones_canciones, canvas_window = crear_canvas_con_scroll(
    tab_canciones, True, paginas_canciones
)
# Vincular eventos
gestion_scroll = GestorScroll(canvas_canciones, panel_botones_canciones, canvas_window)

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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
    fg_color=BOTON_CLARO,
    hover_color=HOVER_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
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
controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN if not ESTADO_SILENCIO else 0)

# Muestre el icono del volumen actual de la barra de volumen
# cambiar_volumen_vista(None)

# Actualizar los botones de la interfaz al iniciar la ejecución
actualizar_iconos()

# Verificar el estado de la reproducción
verificar_estado_reproduccion()

# Cargar las canciones de biblioteca al iniciar
cargar_biblioteca_vista()

# Cargar la cola de reproducción al iniciar
cargar_cola_vista()

# Mostrar la ventana
ventana_principal.mainloop()
