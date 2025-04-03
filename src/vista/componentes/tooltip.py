import customtkinter as ctk
from constantes import *


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self._text = text
        self.tooltip = None
        self.timer_id = None
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
            widget_x = self.widget.winfo_rootx()
            widget_y = self.widget.winfo_rooty()
            widget_width = self.widget.winfo_width()
            widget_height = self.widget.winfo_height()
            if ctk.get_appearance_mode().lower() == "dark":
                bg_color = OSCURO
                fg_color = TEXTO_OSCURO
            else:
                bg_color = CLARO
                fg_color = TEXTO_CLARO
            x = widget_x + widget_width // 2
            y = widget_y + widget_height + 5
            self.tooltip = ctk.CTkToplevel()
            self.tooltip.wm_overrideredirect(True)
            etiqueta_tooltip = ctk.CTkLabel(
                self.tooltip,
                fg_color=bg_color,
                corner_radius=5,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text=self.text,
                text_color=fg_color,
                padx=3,
                pady=3,
            )
            etiqueta_tooltip.pack()
            self.tooltip.update_idletasks()
            tooltip_width = etiqueta_tooltip.winfo_reqwidth()
            tooltip_height = etiqueta_tooltip.winfo_reqheight()
            x = x - tooltip_width // 2
            screen_width = self.widget.winfo_screenwidth()
            screen_height = self.widget.winfo_screenheight()
            if x + tooltip_width > screen_width:
                x = screen_width - tooltip_width
            if x < 0:
                x = 0
            if y + tooltip_height > screen_height:
                y = widget_y - tooltip_height - 5
            self.tooltip.wm_geometry(f"+{x}+{y}")
            self.tooltip.lift()
            self.tooltip.update_idletasks()

    # Ocultar tooltip al quitar el cursor del widget
    def ocultar_tooltip(self, _event=None):
        self.cancelar_temporizador()
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
