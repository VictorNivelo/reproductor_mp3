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
            widget_x = self.componente.winfo_rootx()
            widget_y = self.componente.winfo_rooty()
            widget_width = self.componente.winfo_width()
            widget_height = self.componente.winfo_height()
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
            self.tooltip.attributes("-alpha", 0.0)
            etiqueta_tooltip = ctk.CTkLabel(
                self.tooltip,
                fg_color=bg_color,
                corner_radius=5,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text=self.texto_componente,
                text_color=fg_color,
                padx=2,
                pady=2,
            )
            etiqueta_tooltip.pack()
            self.tooltip.update_idletasks()
            tooltip_width = etiqueta_tooltip.winfo_reqwidth()
            tooltip_height = etiqueta_tooltip.winfo_reqheight()
            x = x - tooltip_width // 2
            screen_width = self.componente.winfo_screenwidth()
            screen_height = self.componente.winfo_screenheight()
            if x + tooltip_width > screen_width:
                x = screen_width - tooltip_width
            if x < 0:
                x = 0
            if y + tooltip_height > screen_height:
                y = widget_y - tooltip_height - 5
            self.tooltip.wm_geometry(f"+{x}+{y}")
            self.tooltip.lift()
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
