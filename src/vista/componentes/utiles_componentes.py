from constantes import *


class UtilesComponentes:
    def __init__(self, controlador):
        self.controlador = controlador
        self.color_fondo_principal = None
        self.color_fondo = None
        self.color_texto = None
        self.color_boton = None
        self.color_hover = None
        self.color_progreso = None

    def colores(self):
        # Colores base
        self.color_fondo_principal = (
            FONDO_PRINCIPAL_OSCURO
            if self.controlador.tema_interfaz == "oscuro"
            else FONDO_PRINCIPAL_CLARO
        )
        self.color_fondo = (
            FONDO_OSCURO if self.controlador.tema_interfaz == "oscuro" else FONDO_CLARO
        )
        self.color_texto = (
            TEXTO_OSCURO if self.controlador.tema_interfaz == "oscuro" else TEXTO_CLARO
        )
        self.color_boton = (
            BOTON_OSCURO if self.controlador.tema_interfaz == "oscuro" else BOTON_CLARO
        )
        self.color_hover = (
            HOVER_OSCURO if self.controlador.tema_interfaz == "oscuro" else HOVER_CLARO
        )
        self.color_progreso = (
            TEXTO_OSCURO if self.controlador.tema_interfaz == "oscuro" else FONDO_OSCURO
        )
