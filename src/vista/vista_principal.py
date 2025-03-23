from controlador.controlador_reproductor import ControladorReproductor
from controlador.controlador_biblioteca import ControladorBiblioteca
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

# Diccionario para almacenar los botones de canciones
botones_canciones = {}
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
        actualizar_tooltip(boton_tema, "Cambiar a claro")
    else:
        cambiar_icono_tema("oscuro")
        controlador_tema.registrar_botones("modo_claro", boton_tema)
        actualizar_tooltip(boton_tema, "Cambiar a oscuro")
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
    # Actualizar el porcentaje de volumen
    etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")


# Función para guardar todos los ajustes
def guardar_todos_ajustes():
    configuracion = {
        "apariencia": APARIENCIA,
        "nivel_volumen": NIVEL_VOLUMEN,
        "modo_aleatorio": MODO_ALEATORIO,
        "modo_repeticion": MODO_REPETICION,
        "estado_silenciado": ESTADO_SILENCIO,
        "panel_lateral_visible": PANEL_LATERAL_VISIBLE,
    }
    controlador_archivos.guardar_ajustes(configuracion)


# Función para cargar todos los ajustes
def cargar_todos_ajustes():
    global APARIENCIA, NIVEL_VOLUMEN, MODO_ALEATORIO, MODO_REPETICION, ESTADO_SILENCIO, PANEL_LATERAL_VISIBLE
    # Cargar configuración desde archivo
    configuracion = controlador_archivos.cargar_ajustes()
    # Aplicar valores a las variables globales
    APARIENCIA = configuracion.get("apariencia", "claro")
    NIVEL_VOLUMEN = configuracion.get("nivel_volumen", 100)
    MODO_ALEATORIO = configuracion.get("modo_aleatorio", False)
    MODO_REPETICION = configuracion.get("modo_repeticion", 0)
    ESTADO_SILENCIO = configuracion.get("estado_silenciado", False)
    PANEL_LATERAL_VISIBLE = configuracion.get("panel_lateral_visible", True)
    # Ajustar tema
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


# Función para reproducir o pausar la canción
def reproducir_vista():
    global ESTADO_REPRODUCCION
    if not ESTADO_REPRODUCCION:
        # Iniciar reproducción
        ESTADO_REPRODUCCION = True
        controlador_tema.registrar_botones("pausa", boton_reproducir)
        controlador_reproductor.reanudar_reproduccion()
        actualizar_tooltip(boton_reproducir, "Pausar")
        actualizar_espectro()
    else:
        # Pausar reproducción
        ESTADO_REPRODUCCION = False
        controlador_tema.registrar_botones("reproducir", boton_reproducir)
        controlador_reproductor.pausar_reproduccion()
        actualizar_tooltip(boton_reproducir, "Repoducir")


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
        contenedor_derecha_principal.configure(width=ANCHO_PANEL_DERECHA)
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
        pestana_actual = paginas_canciones.get()
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
        pestana_actual = paginas_canciones.get()
        actualizar_todas_vistas_canciones()
        guardar_biblioteca()
        # Restaurar el binding de scroll según la pestaña actual
        actualizar_pestana_seleccionada()


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
    controlador_archivos.guardar_biblioteca(biblioteca)


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


# Función para crear botones para cada canción en la biblioteca
def crear_boton_cancion(cancion, panel_botones_canciones):
    # Obtener colores del tema actual
    controlador_tema.colores()
    boton = ctk.CTkButton(
        panel_botones_canciones,
        height=28,
        fg_color=controlador_tema.color_boton,
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        text=f"{cancion.titulo_cancion} - {cancion.artista}",
        hover_color=controlador_tema.color_hover,
        command=lambda c=cancion: reproducir_cancion_desde_lista(c),
    )
    boton.pack(fill="both", pady=(0, 2), expand=True)
    controlador_tema.registrar_botones(f"cancion_{cancion.titulo_cancion}", boton)
    botones_canciones[cancion] = boton


# Función para actualizar la vista de las canciones en la biblioteca
def actualizar_vista_canciones(panel_botones_canciones):
    # Limpiar botones existentes
    for cancion, boton in botones_canciones.items():
        try:
            # Eliminar el botón del controlador_tema de tema
            nombre_boton = f"cancion_{cancion.titulo_cancion}"
            controlador_tema.eliminar_boton(nombre_boton)
            # Destruir el botón
            boton.destroy()
        except Exception as e:
            print(f"Error al destruir el botón {cancion.titulo_cancion}: {e}")
            pass
    botones_canciones.clear()
    # Crear nuevos botones para cada canción
    for cancion in biblioteca.canciones:
        crear_boton_cancion(cancion, panel_botones_canciones)


# Función para reestablecer el scroll en una pestaña
def restablecer_scroll_pestaña(canvas, panel, ventana_canvas):
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


# Función para configurar la interfaz de albumes
def configurar_interfaz_albumes():
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña de álbumes
    tab_albumes = paginas_canciones.tab("Álbumes")
    # Limpiar la pestaña
    for widget in tab_albumes.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible
    canvas_albumes = tk.Canvas(tab_albumes, highlightthickness=0)
    canvas_albumes.pack(fill="both", expand=True)
    canvas_albumes.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_albumes, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_albumes = ctk.CTkFrame(canvas_albumes, fg_color="transparent", corner_radius=0)
    panel_botones_albumes.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_albumes)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_albumes.create_window((0, 0), window=panel_botones_albumes)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_albumes, panel_botones_albumes, canvas_window)
    return canvas_albumes, panel_botones_albumes


# Función auxiliar para crear botones de álbumes
def crear_botones_albumes(albumes, canvas_albumes, panel_botones_albumes):
    # Crear botones para cada álbum
    for album in sorted(albumes):
        # Ignorar álbumes vacíos o sin nombre
        if album == "" or album == "Unknown Album" or album.lower() == "desconocido":
            continue
        boton_album = ctk.CTkButton(
            panel_botones_albumes,
            height=28,
            fg_color=controlador_tema.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=album,
            hover_color=controlador_tema.color_hover,
            command=lambda a=album: mostrar_canciones_album(a),
        )
        boton_album.pack(fill="both", pady=(0, 2), expand=True)
        controlador_tema.registrar_botones(f"album_{album}", boton_album)
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
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña de álbumes
    tab_albumes = paginas_canciones.tab("Álbumes")
    # Limpiar la pestaña
    for widget in tab_albumes.winfo_children():
        widget.destroy()
    # Crear contenedor para la visualización del álbum
    contenedor_detalles_album = ctk.CTkFrame(tab_albumes, fg_color="transparent")
    contenedor_detalles_album.pack(fill="both", expand=True)
    # Panel superior con botón volver y título
    panel_superior = ctk.CTkFrame(contenedor_detalles_album, fg_color="transparent")
    panel_superior.pack(fill="x", pady=(5, 10))
    # Botón para volver a la lista de álbumes
    boton_volver = ctk.CTkButton(
        panel_superior,
        width=50,
        height=28,
        fg_color=controlador_tema.color_boton,
        text="Volver",
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        hover_color=controlador_tema.color_hover,
        command=lambda: actualizar_vista_albumes(),
    )
    boton_volver.pack(side="left")
    controlador_tema.registrar_botones("volver_albumes", boton_volver)
    # Título del álbum
    etiqueta_album = ctk.CTkLabel(
        panel_superior,
        fg_color="transparent",
        text=album,
        font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
        text_color=controlador_tema.color_texto,
        anchor="center",
    )
    etiqueta_album.pack(side="top", fill="x", expand=True)
    controlador_tema.registrar_etiqueta(etiqueta_album)
    # Crear canvas sin scrollbar visible
    canvas_canciones_album = tk.Canvas(contenedor_detalles_album, highlightthickness=0)
    canvas_canciones_album.pack(fill="both", expand=True)
    canvas_canciones_album.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(
        canvas_canciones_album, es_tabview=True, tabview_parent=paginas_canciones
    )
    # Crear panel para los botones dentro del canvas
    panel_canciones_album = ctk.CTkFrame(canvas_canciones_album, fg_color="transparent", corner_radius=0)
    panel_canciones_album.pack(fill="both")
    controlador_tema.registrar_frame(panel_canciones_album)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_canciones_album.create_window((0, 0), window=panel_canciones_album)
    # Vincular eventos con GestorScroll
    GestorScroll(canvas_canciones_album, panel_canciones_album, canvas_window)
    # Mostrar las canciones del álbum
    for cancion in biblioteca.por_album.get(album, []):
        crear_boton_cancion(cancion, panel_canciones_album)
    panel_canciones_album.update_idletasks()
    canvas_canciones_album.yview_moveto(0)
    canvas_canciones_album.configure(scrollregion=canvas_canciones_album.bbox("all"))


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
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña de artistas
    tab_artistas = paginas_canciones.tab("Artistas")
    # Limpiar la pestaña
    for widget in tab_artistas.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible
    canvas_artistas = tk.Canvas(tab_artistas, highlightthickness=0)
    canvas_artistas.pack(fill="both", expand=True)
    canvas_artistas.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_artistas, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_artistas = ctk.CTkFrame(canvas_artistas, fg_color="transparent", corner_radius=0)
    panel_botones_artistas.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_artistas)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_artistas.create_window((0, 0), window=panel_botones_artistas)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_artistas, panel_botones_artistas, canvas_window)
    return canvas_artistas, panel_botones_artistas


# Función auxiliar para crear botones de artistas
def crear_botones_artistas(artistas, canvas_artistas, panel_botones_artistas):
    # Crear botones para cada artista
    for artista in sorted(artistas):
        # Ignorar artistas sin nombre o desconocidos
        if artista == "" or artista == "Unknown Artist" or artista.lower() == "desconocido":
            continue
        boton_artista = ctk.CTkButton(
            panel_botones_artistas,
            height=28,
            fg_color=controlador_tema.color_boton,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=controlador_tema.color_texto,
            text=artista,
            hover_color=controlador_tema.color_hover,
            command=lambda a=artista: mostrar_canciones_artista(a),
        )
        boton_artista.pack(fill="both", pady=(0, 2), expand=True)
        controlador_tema.registrar_botones(f"artista_{artista}", boton_artista)
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
    # Obtener colores actualizados del tema
    controlador_tema.colores()
    # Obtener la pestaña de artistas
    tab_artistas = paginas_canciones.tab("Artistas")
    # Limpiar la pestaña
    for widget in tab_artistas.winfo_children():
        widget.destroy()
    # Crear contenedor para la visualización del artista
    contenedor_detalles_artista = ctk.CTkFrame(tab_artistas, fg_color="transparent")
    contenedor_detalles_artista.pack(fill="both", expand=True)
    # Panel superior con botón volver y título
    panel_superior = ctk.CTkFrame(contenedor_detalles_artista, fg_color="transparent")
    panel_superior.pack(fill="x", pady=(5, 10))
    # Botón para volver a la lista de artistas
    boton_volver = ctk.CTkButton(
        panel_superior,
        width=50,
        height=28,
        fg_color=controlador_tema.color_boton,
        text="Volver",
        font=(LETRA, TAMANIO_LETRA_BOTON),
        text_color=controlador_tema.color_texto,
        hover_color=controlador_tema.color_hover,
        command=lambda: actualizar_vista_artistas(),
    )
    boton_volver.pack(side="left")
    controlador_tema.registrar_botones("volver_artistas", boton_volver)
    # Título del artista
    etiqueta_artista = ctk.CTkLabel(
        panel_superior,
        fg_color="transparent",
        text=artista,
        font=(LETRA, TAMANIO_LETRA_ETIQUETA, "bold"),
        text_color=controlador_tema.color_texto,
        anchor="center",
    )
    etiqueta_artista.pack(side="top", fill="x", expand=True)
    controlador_tema.registrar_etiqueta(etiqueta_artista)
    # Crear canvas sin scrollbar visible
    canvas_canciones_artista = tk.Canvas(contenedor_detalles_artista, highlightthickness=0)
    canvas_canciones_artista.pack(fill="both", expand=True)
    canvas_canciones_artista.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(
        canvas_canciones_artista, es_tabview=True, tabview_parent=paginas_canciones
    )
    # Crear panel para las canciones dentro del canvas
    panel_canciones_artista = ctk.CTkFrame(canvas_canciones_artista, fg_color="transparent", corner_radius=0)
    panel_canciones_artista.pack(fill="both")
    controlador_tema.registrar_frame(panel_canciones_artista)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_canciones_artista.create_window((0, 0), window=panel_canciones_artista)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_canciones_artista, panel_canciones_artista, canvas_window)
    # Mostrar las canciones del artista
    for cancion in biblioteca.por_artista.get(artista, []):
        crear_boton_cancion(cancion, panel_canciones_artista)
    panel_canciones_artista.update_idletasks()
    canvas_canciones_artista.yview_moveto(0)
    canvas_canciones_artista.configure(scrollregion=canvas_canciones_artista.bbox("all"))


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
    # Obtener la pestaña de me gusta
    tab_me_gusta = paginas_canciones.tab("Me gusta")
    # Limpiar la pestaña
    for widget in tab_me_gusta.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible (consistente con otras vistas)
    canvas_me_gusta = tk.Canvas(tab_me_gusta, highlightthickness=0)
    canvas_me_gusta.pack(fill="both", expand=True)
    canvas_me_gusta.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_me_gusta, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_me_gusta = ctk.CTkFrame(canvas_me_gusta, fg_color="transparent", corner_radius=0)
    panel_botones_me_gusta.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_me_gusta)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_me_gusta.create_window((0, 0), window=panel_botones_me_gusta)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_me_gusta, panel_botones_me_gusta, canvas_window)
    # Crear botones para cada canción en Me gusta
    for cancion in biblioteca.me_gusta:
        crear_boton_cancion(cancion, panel_botones_me_gusta)
    panel_botones_me_gusta.update_idletasks()
    canvas_me_gusta.yview_moveto(0)
    canvas_me_gusta.configure(scrollregion=canvas_me_gusta.bbox("all"))


# Función para mostrar las canciones de Me gusta filtradas
def mostrar_me_gusta_filtrados(texto_busqueda):
    # Obtener la pestaña de me gusta
    tab_me_gusta = paginas_canciones.tab("Me gusta")
    # Limpiar la pestaña
    for widget in tab_me_gusta.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible
    canvas_me_gusta = tk.Canvas(tab_me_gusta, highlightthickness=0)
    canvas_me_gusta.pack(fill="both", expand=True)
    canvas_me_gusta.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_me_gusta, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_me_gusta = ctk.CTkFrame(canvas_me_gusta, fg_color="transparent", corner_radius=0)
    panel_botones_me_gusta.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_me_gusta)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_me_gusta.create_window((0, 0), window=panel_botones_me_gusta)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_me_gusta, panel_botones_me_gusta, canvas_window)
    # Filtrar y mostrar canciones
    canciones_filtradas = [
        c
        for c in biblioteca.me_gusta
        if texto_busqueda.lower() in c.titulo_cancion.lower()
        or texto_busqueda.lower() in c.artista.lower()
        or texto_busqueda.lower() in c.album.lower()
    ]
    for cancion in canciones_filtradas:
        crear_boton_cancion(cancion, panel_botones_me_gusta)
    # Actualizar la vista del canvas
    panel_botones_me_gusta.update_idletasks()
    canvas_me_gusta.yview_moveto(0)
    canvas_me_gusta.configure(scrollregion=canvas_me_gusta.bbox("all"))


# Función para actualizar la vista de favoritos
def actualizar_vista_favoritos():
    # Obtener la pestaña de favoritos
    tab_favoritos = paginas_canciones.tab("Favoritos")
    # Limpiar la pestaña
    for widget in tab_favoritos.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible
    canvas_favoritos = tk.Canvas(tab_favoritos, highlightthickness=0)
    canvas_favoritos.pack(fill="both", expand=True)
    canvas_favoritos.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_favoritos, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_favoritos = ctk.CTkFrame(canvas_favoritos, fg_color="transparent", corner_radius=0)
    panel_botones_favoritos.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_favoritos)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_favoritos.create_window((0, 0), window=panel_botones_favoritos)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_favoritos, panel_botones_favoritos, canvas_window)
    # Crear botones para cada canción en favoritos
    for cancion in biblioteca.favorito:
        crear_boton_cancion(cancion, panel_botones_favoritos)
    panel_botones_favoritos.update_idletasks()
    canvas_favoritos.yview_moveto(0)
    canvas_favoritos.configure(scrollregion=canvas_favoritos.bbox("all"))


# Función para mostrar las canciones de favoritos filtradas
def mostrar_favoritos_filtrados(texto_busqueda):
    # Obtener la pestaña de favoritos
    tab_favoritos = paginas_canciones.tab("Favoritos")
    # Limpiar la pestaña
    for widget in tab_favoritos.winfo_children():
        widget.destroy()
    # Crear canvas sin scrollbar visible
    canvas_favoritos = tk.Canvas(tab_favoritos, highlightthickness=0)
    canvas_favoritos.pack(fill="both", expand=True)
    canvas_favoritos.configure(bg=paginas_canciones.cget("fg_color"))
    controlador_tema.registrar_canvas(canvas_favoritos, es_tabview=True, tabview_parent=paginas_canciones)
    # Crear panel para los botones dentro del canvas
    panel_botones_favoritos = ctk.CTkFrame(canvas_favoritos, fg_color="transparent", corner_radius=0)
    panel_botones_favoritos.pack(fill="both")
    controlador_tema.registrar_frame(panel_botones_favoritos)
    # Crear ventana en el canvas para el panel
    canvas_window = canvas_favoritos.create_window((0, 0), window=panel_botones_favoritos)
    # Usar GestorScroll para manejar el scrolling
    GestorScroll(canvas_favoritos, panel_botones_favoritos, canvas_window)
    # Filtrar y mostrar canciones
    canciones_filtradas = [
        c
        for c in biblioteca.favorito
        if texto_busqueda.lower() in c.titulo_cancion.lower()
        or texto_busqueda.lower() in c.artista.lower()
        or texto_busqueda.lower() in c.album.lower()
    ]
    for cancion in canciones_filtradas:
        crear_boton_cancion(cancion, panel_botones_favoritos)
    # Actualizar la vista del canvas
    panel_botones_favoritos.update_idletasks()
    canvas_favoritos.yview_moveto(0)
    canvas_favoritos.configure(scrollregion=canvas_favoritos.bbox("all"))


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
    global barras_espectro, ANCHO_BARRA, ESPACIO_ENTRE_BARRA
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
    espacio_total = ancho_canvas  # Usar 90% del ancho para dejar márgenes
    ANCHO_BARRA = max(2, (espacio_total / NUMERO_BARRA) * 0.7)  # 70% para la barra
    ESPACIO_ENTRE_BARRA = (espacio_total / NUMERO_BARRA) * 0.3  # 30% para el espacio
    # Calcular posición inicial para centrar las barras
    x_inicial = (
        ancho_canvas - (NUMERO_BARRA * (ANCHO_BARRA + ESPACIO_ENTRE_BARRA) - ESPACIO_ENTRE_BARRA)
    ) // 2
    # Color según el tema
    color_barra = HOVER_CLARO if APARIENCIA == "claro" else HOVER_OSCURO
    # Crear barras
    for i in range(NUMERO_BARRA):
        x1 = x_inicial + i * (ANCHO_BARRA + ESPACIO_ENTRE_BARRA)
        x2 = x1 + ANCHO_BARRA
        y1 = alto_canvas
        y2 = alto_canvas - alturas_barras[i]
        barra = canvas_espectro.create_rectangle(x1, y1, x2, y2, fill=color_barra, width=0)
        barras_espectro.append(barra)


# Función para actualizar la animación del espectro
def actualizar_espectro():
    if not canvas_espectro.winfo_exists():  # Verificar si el canvas existe
        return
    alto_canvas = canvas_espectro.winfo_height()
    # Generar alturas aleatorias para simular el espectro
    for i in range(NUMERO_BARRA):
        if i < len(barras_espectro):  # Verificar que la barra existe
            altura_objetivo = random.randint(10, int(alto_canvas))
            alturas_barras[i] = int(alturas_barras[i] * 0.7 + altura_objetivo * 0.3)
            # Actualizar altura de la barra
            try:
                x1, _, x2, _ = canvas_espectro.coords(barras_espectro[i])
                canvas_espectro.coords(
                    barras_espectro[i], x1, alto_canvas, x2, alto_canvas - alturas_barras[i]
                )
            except Exception as e:
                # Error cuando el widget del canvas ha sido destruido o no está disponible
                print(f"Error al actualizar la barra del espectro: {e}")
                return
            except IndexError:
                # Error cuando se intenta acceder a una barra que no existe
                print(f"Error: No se encontró la barra {i} en el espectro")
                return
    # Llamar a la función nuevamente después de un delay
    if ESTADO_REPRODUCCION:
        ventana_principal.after(75, actualizar_espectro)


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


# ************************************** Ventana principal **************************************
# Crear ventana
ventana_principal = ctk.CTk()

# Apariencia de la interfaz por defecto es claro
ctk.set_appearance_mode("light")

# Icono de la ventana
cambiar_icono_tema()

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

# Mini reproductor
mini_reproductor = MiniReproductor(ventana_principal, controlador_tema)

# Configuración
configuracion = Configuracion(ventana_principal, controlador_tema)

# Estadísticas
estadisticas = Estadisticas(ventana_principal, controlador_tema, controlador_archivos)

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
controlador_tema.registrar_frame(conenedor_principal, es_principal=True)

# ===============================================================================================

# ======================================= Panel izquierda =======================================
# Contenedor izquierdo hecho con customtkinter
contenedor_izquierda = ctk.CTkFrame(
    conenedor_principal, fg_color=FONDO_CLARO, corner_radius=BORDES_REDONDEADOS_PANEL
)
contenedor_izquierda.pack(side="left", fill="both", expand=True)
controlador_tema.registrar_frame(contenedor_izquierda, es_ctk=True)

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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    text="Nombre de la Canción",
)
etiqueta_nombre_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_nombre_cancion)

etiqueta_artista_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Artista de la Canción",
)
etiqueta_artista_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_artista_cancion)

etiqueta_album_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Álbum de la Canción",
)
etiqueta_album_cancion.pack(expand=True)
controlador_tema.registrar_etiqueta(etiqueta_album_cancion)

etiqueta_anio_cancion = ctk.CTkLabel(
    contenedor_informacion,
    height=23,
    fg_color="transparent",
    font=(LETRA, TAMANIO_LETRA_ETIQUETA),
    text_color=TEXTO_CLARO,
    text="Lanzamiento de la Canción",
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
barra_progreso = ctk.CTkProgressBar(panel_progreso)
barra_progreso.configure(height=5, progress_color=FONDO_OSCURO, fg_color="lightgray")
barra_progreso.pack(fill="x", padx=12, pady=(0, 3))
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=cambiar_repeticion_vista,
)
boton_repetir.pack(side="left", padx=5)
controlador_tema.registrar_botones("no_repetir", boton_repetir)
crear_tooltip(boton_repetir, "No repetir")

boton_retroceder = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=retroceder_reproduccion_vista,
)
boton_retroceder.pack(side="left", padx=5)
controlador_tema.registrar_botones("retroceder", boton_retroceder)
crear_tooltip(boton_retroceder, f"Retrocede {TIEMPO_AJUSTE} segundos")

boton_anterior = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=reproducir_anterior_vista,
)
boton_anterior.pack(side="left", padx=5)
controlador_tema.registrar_botones("anterior", boton_anterior)
crear_tooltip(boton_anterior, "Reproucir anterior")

boton_reproducir = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=reproducir_vista,
)
boton_reproducir.pack(side="left", padx=5)
controlador_tema.registrar_botones("reproducir", boton_reproducir)
crear_tooltip(boton_reproducir, "Reproducir")

boton_siguiente = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=reproducir_siguiente_vista,
)
boton_siguiente.pack(side="left", padx=5)
controlador_tema.registrar_botones("siguiente", boton_siguiente)
crear_tooltip(boton_siguiente, "Reproducir siguiente")

boton_adelantar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
    command=adelantar_reproduccion_vista,
)
boton_adelantar.pack(side="left", padx=5)
controlador_tema.registrar_botones("adelantar", boton_adelantar)
crear_tooltip(boton_adelantar, f"Adelanta {TIEMPO_AJUSTE} segundos")

boton_mostrar_cola = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_mostrar_cola.pack(side="left", padx=5)
controlador_tema.registrar_botones("mostrar_cola", boton_mostrar_cola)
crear_tooltip(boton_mostrar_cola, "Mostrar la cola")

boton_agregar_cola = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
)
boton_agregar_cola.pack(side="left", padx=5)
controlador_tema.registrar_botones("agregar_cola", boton_agregar_cola)
crear_tooltip(boton_agregar_cola, "Agregar a la cola")

boton_minimizar = ctk.CTkButton(
    panel_controles_reproduccion,
    width=ANCHO_BOTON,
    height=ALTO_BOTON,
    corner_radius=BORDES_REDONDEADOS_BOTON,
    fg_color=BOTON_CLARO,
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="",
    hover_color=HOVER_CLARO,
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
controlador_tema.registrar_frame(contenedor_derecha_principal, es_ctk=True)

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
    height=ALTO_TABVIEW + 5,
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

# Crear canvas sin scrollbar visible
canvas_canciones = tk.Canvas(tab_canciones, highlightthickness=0)
canvas_canciones.pack(fill="both", expand=True)
canvas_canciones.configure(bg=paginas_canciones.cget("fg_color"))
controlador_tema.registrar_canvas(canvas_canciones, es_tabview=True, tabview_parent=paginas_canciones)

# Crear panel para los botones dentro del canvas
panel_botones_canciones = ctk.CTkFrame(canvas_canciones, fg_color="transparent", corner_radius=0)
panel_botones_canciones.pack(fill="both")
controlador_tema.registrar_frame(panel_botones_canciones)

# Crear ventana en el canvas para el panel
canvas_window = canvas_canciones.create_window((0, 0), window=panel_botones_canciones)

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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Canción",
    hover_color=HOVER_CLARO,
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
    font=(LETRA, TAMANIO_LETRA_BOTON),
    text_color=TEXTO_CLARO,
    text="Agregar Carpeta",
    hover_color=HOVER_CLARO,
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

# Mostrar la ventana
ventana_principal.mainloop()
