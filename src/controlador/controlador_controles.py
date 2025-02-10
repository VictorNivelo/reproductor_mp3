class Controlador_botones:
    def __init__(self, vista, controlador_tema):
        self.vista = vista
        self.controlador_tema = controlador_tema
        # Estados
        self.tema_actual = "claro"
        self.reproduciendo = False
        self.silenciado = False
        self.orden = False
        self.repeticion = 0  # 0: no repetir, 1: repetir actual, 2: repetir todo
        self.volumen = 50

    def cambiar_tema(self):
        self.tema_actual = "oscuro" if self.tema_actual == "claro" else "claro"
        self.controlador_tema.cambiar_tema()
        self._actualizar_iconos_tema()

    def _actualizar_iconos_tema(self):
        # Actualizar icono del botón de tema
        icono_tema = "modo_claro" if self.tema_actual == "oscuro" else "modo_oscuro"
        self.controlador_tema.registrar_botones(icono_tema, self.vista.boton_tema)

        # Actualizar otros iconos
        self._actualizar_icono_reproduccion()
        self._actualizar_icono_orden()
        self._actualizar_icono_repeticion()
        self._actualizar_icono_volumen()

    def _actualizar_icono_reproduccion(self):
        icono = "pausa" if self.reproduciendo else "reproducir"
        self.controlador_tema.registrar_botones(icono, self.vista.boton_reproducir)

    def _actualizar_icono_orden(self):
        icono = "aleatorio" if self.orden else "orden"
        self.controlador_tema.registrar_botones(icono, self.vista.boton_aleatorio)

    def _actualizar_icono_repeticion(self):
        if self.repeticion == 0:
            icono = "no_repetir"
        elif self.repeticion == 1:
            icono = "repetir_actual"
        else:
            icono = "repetir_todo"
        self.controlador_tema.registrar_botones(icono, self.vista.boton_repetir)

    def _actualizar_icono_volumen(self):
        if self.silenciado:
            icono = "silencio"
        else:
            if self.volumen == 0:
                icono = "sin_volumen"
            elif self.volumen <= 33:
                icono = "volumen_bajo"
            elif self.volumen <= 66:
                icono = "volumen_medio"
            else:
                icono = "volumen_alto"
        self.controlador_tema.registrar_botones(icono, self.vista.boton_silenciar)

    def cambiar_estado_reproduccion(self):
        self.reproduciendo = not self.reproduciendo
        self._actualizar_icono_reproduccion()

    def cambiar_volumen(self, event=None):
        if not self.silenciado:
            self.volumen = int(self.vista.barra_volumen.get())
            self.vista.etiqueta_porcentaje_volumen.configure(text=f"{self.volumen}%")
            self._actualizar_icono_volumen()

    def cambiar_silencio(self):
        self.silenciado = not self.silenciado
        if self.silenciado:
            self.controlador_tema.registrar_botones("silencio", self.vista.boton_silenciar)
        else:
            self.cambiar_volumen()

    def cambiar_orden(self):
        self.orden = not self.orden
        self._actualizar_icono_orden()

    def cambiar_repeticion(self):
        self.repeticion = (self.repeticion + 1) % 3
        self._actualizar_icono_repeticion()
