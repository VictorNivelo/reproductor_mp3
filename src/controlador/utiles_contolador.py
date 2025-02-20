from constantes import *


class UtilesControlador:
    def __init__(self):
        self.tema_interfaz = "claro"
        self.color_principal = None
        self.color_base = None
        self.color_fondo = None
        self.color_texto = None
        self.color_borde = None
        self.color_boton = None
        self.color_hover = None
        self.color_slider = None
        self.color_hover_oscuro = None
        self.barra_progreso = None
        self.color_segundario = None

    def colores(self):
        # colores base
        self.color_principal = (
            FONDO_PRINCIPAL_OSCURO if self.tema_interfaz == "oscuro" else FONDO_PRINCIPAL_CLARO
        )
        self.color_base = OSCURO if self.tema_interfaz == "oscuro" else CLARO
        self.color_fondo = FONDO_OSCURO if self.tema_interfaz == "oscuro" else FONDO_CLARO
        self.color_texto = TEXTO_OSCURO if self.tema_interfaz == "oscuro" else TEXTO_CLARO
        self.color_borde = FONDO_CLARO if self.tema_interfaz == "oscuro" else FONDO_OSCURO
        self.color_boton = BOTON_OSCURO if self.tema_interfaz == "oscuro" else BOTON_CLARO
        self.color_hover = HOVER_OSCURO if self.tema_interfaz == "oscuro" else HOVER_CLARO
        self.color_slider = TEXTO_OSCURO if self.tema_interfaz == "oscuro" else FONDO_OSCURO
        self.color_hover_oscuro = HOVER_OSCURO if self.tema_interfaz == "oscuro" else HOVER_OSCURO
        self.barra_progreso = HOVER_OSCURO if self.tema_interfaz == "oscuro" else "lightgray"
        self.color_segundario = (
            OSCURO_SEGUNDARIO if self.tema_interfaz == "oscuro" else CLARO_SEGUNDARIO
        )
