class GestorScroll:
    def __init__(self, canvas, panel, ventana_canvas):
        self.canvas = canvas
        self.panel = panel
        self.ventana_canvas = ventana_canvas
        # Configurar eventos
        self.panel.bind("<Configure>", self.scroll_frame_configuracion)
        self.canvas.bind("<Configure>", self.scroll_canvas_configuracion)

    # Configurar el scroll del frame
    def scroll_frame_configuracion(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Obtener dimensiones
        contenido_altura = self.panel.winfo_reqheight()
        canvas_altura = self.canvas.winfo_height()
        # Habilitar o deshabilitar el scroll
        if contenido_altura <= canvas_altura:
            self.canvas.unbind_all("<MouseWheel>")
        else:
            self.canvas.bind_all("<MouseWheel>", self.scroll_raton_configuracion)

    # Configurar el scroll del canvas
    def scroll_canvas_configuracion(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.ventana_canvas, width=canvas_width)
        # Verificar scroll después de redimensionar
        self.scroll_frame_configuracion(None)

    # Desplazar el canvas con la rueda del ratón
    def scroll_raton_configuracion(self, event):
        contenido_altura = self.panel.winfo_reqheight()
        canvas_altura = self.canvas.winfo_height()
        # Solo permitir scroll si el contenido es mayor que el canvas
        if contenido_altura > canvas_altura:
            # Obtener la posición actual (fracciones entre 0 y 1)
            posicion_actual = self.canvas.yview()
            # Calcular la dirección (positivo = hacia abajo, negativo = hacia arriba)
            direccion = -1 * (event.delta / 120)
            # Evitar scroll hacia arriba si ya estamos al inicio
            if direccion < 0 and posicion_actual[0] <= 0:
                return
            # Evitar scroll hacia abajo si ya estamos al final
            if direccion > 0 and posicion_actual[1] >= 1:
                return
            # Aplicar el scroll si está dentro de los límites
            self.canvas.yview_scroll(int(direccion), "units")

    # Método estático para usar en binds directos sin una instancia específica
    @staticmethod
    def scroll_simple(canvas, event):
        # Obtener la posición actual
        posicion_actual = canvas.yview()
        # Calcular la dirección
        direccion = -1 * (event.delta / 120)
        # Evitar scroll fuera de límites
        if (direccion < 0 and posicion_actual[0] <= 0) or (direccion > 0 and posicion_actual[1] >= 1):
            return
        canvas.yview_scroll(int(direccion), "units")
