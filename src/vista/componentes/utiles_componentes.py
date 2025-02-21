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
        # Tema de la interfaz
        tema_componentes = self.controlador.tema_componentes_interfaz == "oscuro"
        # Colores base
        self.color_fondo_principal = FONDO_PRINCIPAL_OSCURO if tema_componentes else FONDO_PRINCIPAL_CLARO
        self.color_fondo = FONDO_OSCURO if tema_componentes else FONDO_CLARO
        self.color_texto = TEXTO_OSCURO if tema_componentes else TEXTO_CLARO
        self.color_boton = BOTON_OSCURO if tema_componentes else BOTON_CLARO
        self.color_hover = HOVER_OSCURO if tema_componentes else HOVER_CLARO
        self.color_progreso = TEXTO_OSCURO if tema_componentes else FONDO_OSCURO
