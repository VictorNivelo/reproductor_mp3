import customtkinter as ctk
from constantes import *
from utiles import Utiles


class ToolTip:
    def __init__(self, widget, text, controlador_tema=None):
        self.widget = widget
        self._text = text
        self.tooltip = None
        self.timer_id = None
        self.utiles = Utiles(controlador_tema)
        self.widget.bind("<Enter>", self.iniciar_temporizador)
        self.widget.bind("<Leave>", self.ocultar_tooltip)

    # Obtener el texto del tooltip
    @property
    def text(self):
        return self._text

    # Actualizar el texto del tooltip
    @text.setter
    def text(self, value):
        self._text = value
        if self.tooltip:
            self.ocultar_tooltip()
            self.mostrar_tooltip()

    # Iniciar temporizador para mostrar el tooltip
    def iniciar_temporizador(self, _event=None):
        self.cancelar_temporizador()
        self.timer_id = self.widget.after(1000, self.mostrar_tooltip)

    # Cancelar temporizador para ocultar el tooltip
    def cancelar_temporizador(self):
        if self.timer_id:
            self.widget.after_cancel(self.timer_id)
            self.timer_id = None

    # Mostrar tooltip en la posición del widget
    def mostrar_tooltip(self, _event=None):
        if not self.tooltip:
            # Obtener las coordenadas del widget
            widget_x = self.widget.winfo_rootx()
            widget_y = self.widget.winfo_rooty()
            widget_width = self.widget.winfo_width()
            widget_height = self.widget.winfo_height()
            
            # Actualizar colores según el tema actual
            self.utiles.colores()
            bg_color = self.utiles.color_base
            fg_color = self.utiles.color_texto
            
            # Calcular posición inicial
            x = widget_x + widget_width // 2
            y = widget_y + widget_height + 5
            
            # Crear ventana de tooltip
            self.tooltip = ctk.CTkToplevel()
            self.tooltip.wm_overrideredirect(True)
            
            # Evitar que el tooltip aparezca en la barra de tareas
            self.tooltip.wm_attributes("-topmost", True)
            
            # Crear etiqueta con el texto del tooltip
            etiqueta_tooltip = ctk.CTkLabel(
                self.tooltip,
                fg_color=bg_color,
                corner_radius=5,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text=self.text,
                text_color=fg_color,
                padx=5,
                pady=5,
            )
            etiqueta_tooltip.pack()
            
            # Actualizar para obtener dimensiones reales
            self.tooltip.update_idletasks()
            tooltip_width = etiqueta_tooltip.winfo_reqwidth()
            tooltip_height = etiqueta_tooltip.winfo_reqheight()
            
            # Ajustar posición horizontal centrada
            x = x - tooltip_width // 2
            
            # Obtener dimensiones de la pantalla
            screen_width = self.widget.winfo_screenwidth()
            screen_height = self.widget.winfo_screenheight()
            
            # Evitar que el tooltip salga de los límites de la pantalla
            if x + tooltip_width > screen_width:
                x = screen_width - tooltip_width - 5
            if x < 0:
                x = 5
                
            # Si no hay espacio abajo, mostrar arriba del widget
            if y + tooltip_height > screen_height:
                y = widget_y - tooltip_height - 5
            
            # Establecer la posición final
            self.tooltip.wm_geometry(f"+{x}+{y}")
            self.tooltip.lift()
            self.tooltip.update_idletasks()

    # Ocultar tooltip al quitar el cursor del widget
    def ocultar_tooltip(self, _event=None):
        self.cancelar_temporizador()
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Función para crear tooltips fácilmente
def crear_tooltip(widget, texto, controlador_tema=None):
    """
    Crea un tooltip para el widget especificado.
    
    Args:
        widget: El widget al que se le agregará el tooltip
        texto: El texto que mostrará el tooltip
        controlador_tema: El controlador de tema para mantener consistencia visual
    
    Returns:
        Instancia de ToolTip
    """
    return ToolTip(widget, texto, controlador_tema)