from constantes import *
import tracemalloc


# Método decorador para medir el consumo de memoria de una función
def medir_consumo_memoria(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        resultado = func(*args, **kwargs)
        actual, pico = tracemalloc.get_traced_memory()
        print("--------------------------------------------------------------")
        print("Consumo de memoria:")
        print(f"{func.__name__} - Memoria actual: {actual / 1024:.2f} KB")
        print(f"{func.__name__} - Pico de memoria: {pico / 1024:.2f} KB")
        print("--------------------------------------------------------------")
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

    @staticmethod
    def quitar_foco_evento(event, ventana_principal):
        widget_clickeado = event.widget
        # Verificar si el clic fue en una entrada de texto usando nombres de clase
        nombre_clase = widget_clickeado.__class__.__name__
        componentes_foco = ("CTkEntry", "Entry", "CTkTextbox", "Text")
        # Verificar si es un botón de opciones o menú
        widget_str = str(widget_clickeado)
        es_componente_menu = any(palabra in widget_str.lower() for palabra in ["opcion", "menu", "button"])
        # Solo quitar el foco si no es un componente de entrada ni un botón de menú
        if nombre_clase not in componentes_foco and not es_componente_menu:
            ventana_principal.focus_set()

    def configurar_quitar_foco_global(self, ventana_principal):
        # Componentes que mantienen el foco (usando nombres de clase)
        componentes_excluidos = ("CTkEntry", "Entry", "CTkTextbox", "Text")
        # Componentes que no soportan eventos de ratón
        componentes_sin_eventos = ("CTkTabview",)

        def aplicar_evento_recursivo(componente):
            # Aplicar evento al componente actual si es válido
            try:
                nombre_clase = componente.__class__.__name__
                if (
                    nombre_clase not in componentes_excluidos
                    and nombre_clase not in componentes_sin_eventos
                    and hasattr(componente, "bind")
                ):
                    componente.bind(
                        "<Button-1>", lambda event: self.quitar_foco_evento(event, ventana_principal), add="+"
                    )
            except Exception as e:
                print(f"Error al configurar evento de quitar foco en {componente}: {e}")
            # Aplicar recursivamente a todos los hijos
            try:
                for componente_hijo in componente.winfo_children():
                    aplicar_evento_recursivo(componente_hijo)
            except Exception as e:
                print(f"Error al acceder a los hijos de {componente}: {e}")

        # Aplicar a toda la ventana principal
        try:
            aplicar_evento_recursivo(ventana_principal)
        except Exception as e:
            print(f"Error al configurar eventos de quitar foco: {e}")

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
        def mostrar_dimensiones():
            ancho = self.obtener_ancho_componente(componente)
            alto = self.obtener_alto_componente(componente)
            if ancho <= 1 or alto <= 1:
                componente.after(100, mostrar_dimensiones)
            else:
                print("------------------------------------------")
                print("Dimensiones del componente:")
                print(f"Ancho: {ancho}, Alto: {alto} en px")
                print("------------------------------------------")

        componente.after(100, mostrar_dimensiones)

    # Método para obtener información completa de un componente (tamaño y posición)
    def obtener_informacion_componente(self, componente):
        componente.update_idletasks()
        # Obtener dimensiones
        ancho = self.obtener_ancho_componente(componente)
        alto = self.obtener_alto_componente(componente)
        # Obtener posición absoluta (en la pantalla)
        x_abs = componente.winfo_rootx()
        y_abs = componente.winfo_rooty()
        # Obtener posición relativa al contenedor padre
        x_rel = componente.winfo_x()
        y_rel = componente.winfo_y()
        return {
            "ancho": ancho,
            "alto": alto,
            "x_absoluta": x_abs,
            "y_absoluta": y_abs,
            "x_relativa": x_rel,
            "y_relativa": y_rel,
        }

    # Método para mostrar la información completa de un componente
    def mostrar_informacion_componente(self, componente, nombre_componente=None):
        def mostrar_info():
            info = self.obtener_informacion_componente(componente)
            # Si el componente aún no tiene dimensiones, intentamos de nuevo
            if info["ancho"] <= 1 or info["alto"] <= 1:
                componente.after(100, mostrar_info)
            else:
                print("------------------------------------------")
                print("Información del componente:")
                print(f"Nombre: {nombre_componente}")
                print(f"Dimensiones: {info['ancho']}x{info['alto']} px")
                print(f"Posición absoluta: ({info['x_absoluta']}, {info['y_absoluta']})")
                print(f"Posición relativa al padre: ({info['x_relativa']}, {info['y_relativa']})")
                print("------------------------------------------")

        componente.after(100, mostrar_info)
