import customtkinter as ctk
from constantes import *


class ToolTip:
    def __init__(self, componente, texto_componente):
        self.componente = componente
        self.texto = texto_componente
        self.tooltip = None
        self.etiqueta_tooltip = None
        self.id_temporizador = None
        self.temporizador_animacion = None
        self.pasos_desvanecimiento = 10
        self.intervalo_desvanecimiento = 15
        # Asociar eventos de entrada y salida al componente
        self.componente.bind("<Enter>", self.iniciar_temporizador)
        self.componente.bind("<Leave>", self.ocultar_tooltip)
        # Asociar evento de destrucción del componente para ocultar el tooltip
        self.componente.bind("<Destroy>", self.ocultar_tooltip_forzado)

    # Obtener el texto del tooltip
    @property
    def texto_componente(self):
        return self.texto

    # Actualizar el texto del tooltip
    @texto_componente.setter
    def texto_componente(self, valor):
        self.texto = valor
        # Si el tooltip está visible, actualizarlo en tiempo real
        if self.tooltip and self.tooltip.winfo_exists():
            # Actualizar el texto de la etiqueta
            self.etiqueta_tooltip.configure(text=valor)
            # Actualizar dimensiones y posición para adaptarse al nuevo texto
            self.tooltip.update_idletasks()
            self.actualizar_posicion_tooltip()

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
        if not self.tooltip or not self.tooltip.winfo_exists():
            # Obtener el modo de apariencia actual
            modo_apariencia = ctk.get_appearance_mode().lower()
            # Definir colores según el modo de apariencia
            if modo_apariencia == "dark":
                color_fondo = FONDO_OSCURO
                color_etiqueta = OSCURO
                texto_color = TEXTO_OSCURO
            else:
                color_fondo = FONDO_CLARO
                color_etiqueta = CLARO
                texto_color = TEXTO_CLARO
            # --------------------------------- Crear el tooltip --------------------------------
            # Crear el tooltip como un Toplevel
            self.tooltip = ctk.CTkToplevel(fg_color=color_fondo)
            self.tooltip.title("")
            # -----------------------------------------------------------------------------------
            # Eliminar bordes de la ventana
            self.tooltip.overrideredirect(True)
            # Configurar la ventana para que este siempre encima
            self.tooltip.attributes("-topmost", True)
            # Evitar que el tooltip se muestre en la barra de tareas
            self.tooltip.attributes("-toolwindow", True)
            # Establece la opacidad inicial del tooltip
            self.tooltip.attributes("-alpha", 0.0)
            # Convierte el fondo del tooltip en transparente
            self.tooltip.attributes("-transparentcolor", color_fondo)
            # ---------------------------------- Etiqueta texto ---------------------------------
            # Etiqueta del tooltip con el texto
            self.etiqueta_tooltip = ctk.CTkLabel(
                self.tooltip,
                corner_radius=7,
                fg_color=color_etiqueta,
                font=(LETRA, TAMANIO_LETRA_ETIQUETA),
                text_color=texto_color,
                text=self.texto_componente,
            )
            self.etiqueta_tooltip.pack()
            # -------------------------------------------------------------------------------------
            self.tooltip.update_idletasks()
            # Actualizar la posición
            self.actualizar_posicion_tooltip()
            # Asegurar que el tooltip esté por encima de otros elementos
            self.tooltip.lift()
            # Actualizar el tooltip para que tome el tamaño correcto
            self.tooltip.update_idletasks()
            # Iniciar animación de aparición
            self.animar_aparicion(0)
        else:
            # Si ya existe, actualizar colores y texto por si han cambiado
            self.actualizar_colores_tooltip()

    # Método para actualizar la posición del tooltip
    def actualizar_posicion_tooltip(self):
        if not self.tooltip or not self.tooltip.winfo_exists():
            return
        # Obtener la posición del componente
        componente_posicion_x = self.componente.winfo_rootx()
        componente_posicion_y = self.componente.winfo_rooty()
        # Obtener el ancho y alto del componente
        ancho_componente = self.componente.winfo_width()
        alto_componente = self.componente.winfo_height()
        # Obtener el ancho y alto del tooltip
        ancho_tooltip = self.etiqueta_tooltip.winfo_reqwidth()
        alto_tooltip = self.etiqueta_tooltip.winfo_reqheight()
        # Calcular la posición del tooltip
        posicion_x = componente_posicion_x + ancho_componente // 2 - ancho_tooltip // 2
        posicion_y = componente_posicion_y + alto_componente + 5
        # Obtenemos la posición de la pantalla
        ancho_pantalla = self.componente.winfo_screenwidth()
        alto_pantalla = self.componente.winfo_screenheight()
        # Ajustar posición si se sale de los bordes
        if posicion_x + ancho_tooltip > ancho_pantalla:
            posicion_x = ancho_pantalla - ancho_tooltip
        if posicion_x < 0:
            posicion_x = 0
        if posicion_y + alto_tooltip > alto_pantalla:
            posicion_y = componente_posicion_y - alto_tooltip - 5
        # Posicionamos el tooltip
        self.tooltip.wm_geometry(f"+{posicion_x}+{posicion_y}")

    # Método para actualizar los colores del tooltip según el tema actual
    def actualizar_colores_tooltip(self):
        if not self.tooltip or not self.tooltip.winfo_exists():
            return
        # Obtener el modo de apariencia actual
        modo_apariencia = ctk.get_appearance_mode().lower()
        # Definir colores según el modo de apariencia
        if modo_apariencia == "dark":
            color_fondo = FONDO_OSCURO
            color_etiqueta = OSCURO
            texto_color = TEXTO_OSCURO
        else:
            color_fondo = FONDO_CLARO
            color_etiqueta = CLARO
            texto_color = TEXTO_CLARO
        # Actualizar los colores
        self.tooltip.configure(fg_color=color_fondo)
        self.etiqueta_tooltip.configure(fg_color=color_etiqueta, text_color=texto_color)
        self.tooltip.attributes("-transparentcolor", color_fondo)

    # Método para animar la aparición del tooltip
    def animar_aparicion(self, paso):
        if self.tooltip and self.tooltip.winfo_exists():
            if paso <= self.pasos_desvanecimiento:
                opacidad = paso / self.pasos_desvanecimiento
                self.tooltip.attributes("-alpha", opacidad)
                self.temporizador_animacion = self.componente.after(
                    self.intervalo_desvanecimiento, lambda: self.animar_aparicion(paso + 1)
                )

    # Método para animar la desaparición del tooltip
    def animar_desaparicion(self, paso):
        if self.tooltip and self.tooltip.winfo_exists():
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
        if self.tooltip and self.tooltip.winfo_exists():
            # Iniciar animación de desaparición
            self.animar_desaparicion(0)

    # Método para ocultar el tooltip forzado (sin animación)
    def ocultar_tooltip_forzado(self, _event=None):
        self.cancelar_temporizador()
        if self.tooltip and self.tooltip.winfo_exists():
            try:
                self.tooltip.destroy()
                self.tooltip = None
            except Exception as e:
                print(f"Error al ocultar el tooltip forzado: {e}")
                pass
