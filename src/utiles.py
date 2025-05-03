from constantes import *
import tracemalloc


# Método decorador para medir el consumo de memoria de una función
def medir_consumo_memoria(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        resultado = func(*args, **kwargs)
        actual, pico = tracemalloc.get_traced_memory()
        print(f"{func.__name__} - Memoria actual: {actual / 1024:.2f} KB")
        print(f"{func.__name__} - Pico de memoria: {pico / 1024:.2f} KB")
        tracemalloc.stop()
        return resultado

    return wrapper


class UtilesGeneral:
    def __init__(self, controlador_externo=None):
        # Si no hay controlador externo, esta instancia actúa como controlador
        self.es_controlador = controlador_externo is None
        # Almacena la referencia al controlador (self si es controlador)
        self.controlador = self if self.es_controlador else controlador_externo
        # Tema de la interfaz y de los iconos (solo inicializa si es controlador)
        if self.es_controlador:
            self.tema_interfaz = "claro"
            self.tema_iconos = "oscuro"
        # Inicializar todos los colores
        self.color_fondo_principal = None
        self.color_fondo = None
        self.color_texto = None
        self.color_boton = None
        self.color_hover = None
        self.color_base = None
        self.color_barras = None
        self.color_borde = None
        self.color_slider = None
        self.color_hover_oscuro = None
        self.color_barra_progreso = None
        self.color_segundario = None

    # Método para obtener los colores de la interfaz
    def colores(self):
        # Obtiene el tema del controlador (propio o externo)
        tema = self.controlador.tema_interfaz == "oscuro"
        # Colores base compartidos
        self.color_fondo_principal = FONDO_PRINCIPAL_OSCURO if tema else FONDO_PRINCIPAL_CLARO
        self.color_fondo = FONDO_OSCURO if tema else FONDO_CLARO
        self.color_texto = TEXTO_OSCURO if tema else TEXTO_CLARO
        self.color_boton = BOTON_OSCURO if tema else BOTON_CLARO
        self.color_hover, self.color_hover_oscuro = (
            (HOVER_OSCURO, HOVER_CLARO) if tema else (HOVER_CLARO, HOVER_OSCURO)
        )
        # Colores exclusivos de UtilesControlador
        self.color_base = OSCURO if tema else CLARO
        self.color_segundario = OSCURO_SEGUNDARIO if tema else CLARO_SEGUNDARIO
        self.color_borde = FONDO_CLARO if tema else FONDO_OSCURO
        self.color_barras = BARRA_OSCURO if tema else BARRA_CLARO
        self.color_slider = TEXTO_OSCURO if tema else FONDO_OSCURO
        self.color_barra_progreso = BARRA_PROGRESO_CLARO if tema else BARRA_PROGRESO_OSCURO

    # Método para obtener el ancho de un componente
    @staticmethod
    def obtener_ancho_componente(componente):
        componente.update_idletasks()
        ancho = componente.winfo_width()
        # Si el ancho es 1 o menor, intentamos obtener el tamaño de la ventana padre si existe
        if ancho <= 1 and componente.master is not None:
            componente.master.update_idletasks()
            ancho = componente.master.winfo_width()
        return ancho

    # Método para obtener el alto de un componente
    @staticmethod
    def obtener_alto_componente(componente):
        componente.update_idletasks()
        alto = componente.winfo_height()
        # Si el alto es 1 o menor, intentamos obtener el tamaño de la ventana padre si existe
        if alto <= 1 and componente.master is not None:
            componente.master.update_idletasks()
            alto = componente.master.winfo_height()
        return alto

    # Método para mostrar las dimensiones de un componente
    def mostrar_dimensiones_componente(self, componente):
        def _mostrar():
            ancho = self.obtener_ancho_componente(componente)
            alto = self.obtener_alto_componente(componente)
            if ancho <= 1 or alto <= 1:
                componente.after(100, _mostrar)
            else:
                print(f"Ancho real: {ancho}, Alto real: {alto}")

        componente.after(100, _mostrar)
