from vista.utiles.utiles_vista import *
from constantes import *


class ControladorBotones:
    def __init__(self, controlador, ventana_principal):
        self.controlador = controlador  # ControladorTema
        self.ventana_principal = ventana_principal
        self.controlador_reproductor = None
        # Botones
        self.boton_aleatorio = None
        self.boton_repetir = None
        self.boton_silenciar = None
        self.boton_visibilidad = None
        # Elementos adicionales
        self.contenedor_derecha = None
        self.barra_volumen = None
        self.etiqueta_porcentaje_volumen = None

    def establecer_controlador_reproductor(self, controlador_reproductor):
        self.controlador_reproductor = controlador_reproductor

    def establecer_botones(
        self, boton_aleatorio, boton_repetir=None, boton_silenciar=None, boton_visibilidad=None
    ):
        self.boton_aleatorio = boton_aleatorio
        self.boton_repetir = boton_repetir
        self.boton_silenciar = boton_silenciar
        self.boton_visibilidad = boton_visibilidad

    def establecer_elementos_interfaz(
        self, contenedor_derecha=None, barra_volumen=None, etiqueta_porcentaje_volumen=None
    ):
        self.contenedor_derecha = contenedor_derecha
        self.barra_volumen = barra_volumen
        self.etiqueta_porcentaje_volumen = etiqueta_porcentaje_volumen

    def cambiar_orden(self):
        global MODO_ALEATORIO
        MODO_ALEATORIO = not MODO_ALEATORIO
        # Informar al controlador sobre el cambio en el modo de reproducción
        self.controlador_reproductor.establecer_modo_aleatorio(MODO_ALEATORIO)
        if MODO_ALEATORIO:
            self.controlador.registrar_botones("aleatorio", self.boton_aleatorio)
            actualizar_tooltip(self.boton_aleatorio, "Reproducción aleatoria")
        else:
            self.controlador.registrar_botones("orden", self.boton_aleatorio)
            actualizar_tooltip(self.boton_aleatorio, "Reproducción en orden")
        return MODO_ALEATORIO

    def cambiar_repeticion(self):
        global MODO_REPETICION
        MODO_REPETICION = (MODO_REPETICION + 1) % 3
        self.controlador_reproductor.establecer_modo_repeticion(MODO_REPETICION)
        # Icono de no repetir
        if MODO_REPETICION == 0:
            self.controlador.registrar_botones("no_repetir", self.boton_repetir)
            actualizar_tooltip(self.boton_repetir, "No repetir")
        # Icono de repetir actual
        elif MODO_REPETICION == 1:
            self.controlador.registrar_botones("repetir_actual", self.boton_repetir)
            actualizar_tooltip(self.boton_repetir, "Repetir actual")
        # Icono de repetir todo
        else:
            self.controlador.registrar_botones("repetir_todo", self.boton_repetir)
            actualizar_tooltip(self.boton_repetir, "Repetir todo")
        return MODO_REPETICION

    def cambiar_visibilidad(self):
        global PANEL_LATERAL_VISIBLE
        PANEL_LATERAL_VISIBLE = not PANEL_LATERAL_VISIBLE
        if PANEL_LATERAL_VISIBLE:
            # Mostrar el panel
            self.contenedor_derecha.configure(width=ANCHO_PANEL_DERECHA)
            self.contenedor_derecha.pack(side="left", fill="both", padx=(5, 0))
            self.controlador.registrar_botones("ocultar", self.boton_visibilidad)
            actualizar_tooltip(self.boton_visibilidad, "Ocultar lateral")
        else:
            # Ocultar el panel
            self.contenedor_derecha.configure(width=0)
            self.contenedor_derecha.pack_forget()
            self.controlador.registrar_botones("mostrar", self.boton_visibilidad)
            actualizar_tooltip(self.boton_visibilidad, "Mostrar lateral")
        return PANEL_LATERAL_VISIBLE

    def cambiar_volumen(self, _event=None):
        global NIVEL_VOLUMEN, ESTADO_SILENCIO
        if not ESTADO_SILENCIO:
            nuevo_volumen = int(self.barra_volumen.get())
            NIVEL_VOLUMEN = nuevo_volumen
            self.etiqueta_porcentaje_volumen.configure(text=f"{NIVEL_VOLUMEN}%")
            # Aplicar el cambio de volumen al reproductor
            self.controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN)
            # Actualizar el icono según el nivel de volumen
            if NIVEL_VOLUMEN == 0:
                self.controlador.registrar_botones("sin_volumen", self.boton_silenciar)
            elif NIVEL_VOLUMEN <= 33:
                self.controlador.registrar_botones("volumen_bajo", self.boton_silenciar)
            elif NIVEL_VOLUMEN <= 66:
                self.controlador.registrar_botones("volumen_medio", self.boton_silenciar)
            else:
                self.controlador.registrar_botones("volumen_alto", self.boton_silenciar)
        return NIVEL_VOLUMEN

    def cambiar_silencio(self):
        global ESTADO_SILENCIO
        ESTADO_SILENCIO = not ESTADO_SILENCIO
        if ESTADO_SILENCIO:
            # Guardar volumen actual y silenciar
            self.controlador_reproductor.ajustar_volumen(0)
            self.controlador.registrar_botones("silencio", self.boton_silenciar)
            actualizar_tooltip(self.boton_silenciar, "Quitar silencio")
        else:
            # Restaurar volumen anterior
            self.controlador_reproductor.ajustar_volumen(NIVEL_VOLUMEN)
            actualizar_tooltip(self.boton_silenciar, "Silenciar")
            self.cambiar_volumen()
        return ESTADO_SILENCIO
