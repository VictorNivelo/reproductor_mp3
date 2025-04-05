import customtkinter as ctk
from constantes import *


class ToolTip:
    def __init__(self, componente, texto_componente):
        self.componente = componente
        self.texto = texto_componente
        self.tooltip = None
        self.id_temporizador = None
        self.temporizador_animacion = None
        self.pasos_desvanecimiento = 10
        self.intervalo_desvanecimiento = 15
        self.componente.bind("<Enter>", self.iniciar_temporizador)
        self.componente.bind("<Leave>", self.ocultar_tooltip)

    # Obtener el texto del tooltip
    @property
    def texto_componente(self):
        return self.texto

    # Actualizar el texto del tooltip
    @texto_componente.setter
    def texto_componente(self, valor):
        self.texto = valor
        if self.tooltip:
            self.ocultar_tooltip()
            self.mostrar_tooltip()

    # Método para iniciar el temporizador
    def iniciar_temporizador(self, _event=None):
        self.cancelar_temporizador()
        self.id_temporizador = self.componente.after(1000, self.mostrar_tooltip)

    # Método para cancelar el temporizador
    def cancelar_temporizador(self):
        if self.id_temporizador:
            self.componente.after_cancel(self.id_temporizador)
            self.id_temporizador = None
        if self.temporizador_animacion:
            self.componente.after_cancel(self.temporizador_animacion)
            self.temporizador_animacion = None

    # Método para mostrar el tooltip
    def mostrar_tooltip(self, _event=None):
        if not self.tooltip:
            # Obtener la posición del componente
            componente_posicion_x = self.componente.winfo_rootx()
            componente_posicion_y = self.componente.winfo_rooty()
            # Obtener el ancho y alto del componente
            ancho_componente = self.componente.winfo_width()
            alto_componente = self.componente.winfo_height()
            # Obtener el modo de apariencia actual
            modo_apariencia = ctk.get_appearance_mode().lower()
            # Definir colores según el modo de apariencia
            if modo_apariencia == "dark":
                color_fondo = OSCURO
                texto_color = TEXTO_OSCURO
            else:
                color_fondo = CLARO
                texto_color = TEXTO_CLARO
            # Calcular la posición del tooltip
            posicion_x = componente_posicion_x + ancho_componente // 2
            posicion_y = componente_posicion_y + alto_componente + 5
            # --------------------------------- Crear el tooltip --------------------------------
            # Crear el tooltip como un Toplevel
            self.tooltip = ctk.CTkToplevel(fg_color="red")
            self.tooltip.title("")
            # -----------------------------------------------------------------------------------
            # Eliminar bordes de la ventana
            self.tooltip.wm_overrideredirect(True)
            # Configurar la ventana para que este siempre encima
            self.tooltip.wm_attributes("-topmost", True)
            # Establece la opacidad inicial del tooltip
            self.tooltip.attributes("-alpha", 0.0)
            # Convierte el fondo del tooltip en transparente
            self.tooltip.attributes("-transparentcolor", "red")
            # ---------------------------------- Etiqueta texto ---------------------------------
            # Etiqueta del tooltip con el texto
            self.etiqueta_tooltip = ctk.CTkLabel(
                self.tooltip,
                corner_radius=10,
                fg_color=color_fondo,
                font=(LETRA, TAMANIO_LETRA_ETIQUETA),
                text_color=texto_color,
                text=self.texto_componente,
            )
            self.etiqueta_tooltip.pack()
            # -------------------------------------------------------------------------------------
            self.tooltip.update_idletasks()
            # Obtener el ancho y alto del tooltip
            ancho_tooltip = self.etiqueta_tooltip.winfo_reqwidth()
            alto_tooltip = self.etiqueta_tooltip.winfo_reqheight()
            # Calcular la posición del tooltip
            posicion_x = posicion_x - ancho_tooltip // 2
            # Obtenemos la posición de la pantalla
            ancho_pantalla = self.componente.winfo_screenwidth()
            alto_pantalla = self.componente.winfo_screenheight()
            # Si el tooltip se sale por la derecha lo ajusta al borde
            if posicion_x + ancho_tooltip > ancho_pantalla:
                posicion_x = ancho_pantalla - ancho_tooltip
            # Si el tooltip se sale por la izquierda lo ajusta al borde
            if posicion_x < 0:
                posicion_x = 0
            # Si el tooltip se sale por la parte inferior lo ajusta al borde
            if posicion_y + alto_tooltip > alto_pantalla:
                posicion_y = componente_posicion_y - alto_tooltip - 5
            # Posicionamos el tooltip
            self.tooltip.wm_geometry(f"+{posicion_x}+{posicion_y}")
            # Asegurar que el tooltip esté por encima de otros elementos
            self.tooltip.lift()
            # Actualizar el tooltip para que tome el tamaño correcto
            self.tooltip.update_idletasks()
            # Iniciar animación de aparición
            self.animar_aparicion(0)

    # Método para animar la aparición del tooltip
    def animar_aparicion(self, paso):
        if self.tooltip:
            if paso <= self.pasos_desvanecimiento:
                opacidad = paso / self.pasos_desvanecimiento
                self.tooltip.attributes("-alpha", opacidad)
                self.temporizador_animacion = self.componente.after(
                    self.intervalo_desvanecimiento, lambda: self.animar_aparicion(paso + 1)
                )

    # Método para animar la desaparición del tooltip
    def animar_desaparicion(self, paso):
        if self.tooltip:
            if paso <= self.pasos_desvanecimiento:
                opacidad = 1.0 - (paso / self.pasos_desvanecimiento)
                self.tooltip.attributes("-alpha", opacidad)
                self.temporizador_animacion = self.componente.after(
                    self.intervalo_desvanecimiento, lambda: self.animar_desaparicion(paso + 1)
                )
            else:
                # Destruir el tooltip al finalizar la animación
                self.tooltip.destroy()
                self.tooltip = None
                self.temporizador_animacion = None

    # Método para ocultar el tooltip
    def ocultar_tooltip(self, _event=None):
        self.cancelar_temporizador()
        if self.tooltip:
            # Iniciar animación de desaparición
            self.animar_desaparicion(0)
