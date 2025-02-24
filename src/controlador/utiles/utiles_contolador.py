from constantes import *


class UtilesControlador:
    def __init__(self):
        # Tema de la interfaz y de los iconos
        self.tema_interfaz = "claro"
        self.tema_iconos = "oscuro"
        # Initializar colores
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
        # Tema de la interfaz
        tema_controlador = self.tema_interfaz == "oscuro"
        # Colores base
        self.color_principal = FONDO_PRINCIPAL_OSCURO if tema_controlador else FONDO_PRINCIPAL_CLARO
        self.color_base = OSCURO if tema_controlador else CLARO
        self.color_fondo = FONDO_OSCURO if tema_controlador else FONDO_CLARO
        self.color_texto = TEXTO_OSCURO if tema_controlador else TEXTO_CLARO
        self.color_borde = FONDO_CLARO if tema_controlador else FONDO_OSCURO
        self.color_boton = BOTON_OSCURO if tema_controlador else BOTON_CLARO
        self.color_hover = HOVER_OSCURO if tema_controlador else HOVER_CLARO
        self.color_slider = TEXTO_OSCURO if tema_controlador else FONDO_OSCURO
        self.color_hover_oscuro = HOVER_OSCURO if tema_controlador else HOVER_OSCURO
        self.barra_progreso = HOVER_OSCURO if tema_controlador else "lightgray"
        self.color_segundario = OSCURO_SEGUNDARIO if tema_controlador else CLARO_SEGUNDARIO
