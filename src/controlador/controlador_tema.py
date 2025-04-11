from vista.utiles.utiles_vista import cargar_icono_personalizado, cargar_iconos
import customtkinter as ctk
from utiles import Utiles


class ControladorTema(Utiles):
    def __init__(self):
        super().__init__()
        # Iconos de la interfaz
        self.iconos = cargar_iconos(self.tema_iconos)
        # Diccionario de botones
        self.botones = {}
        self.paneles = []
        self.etiquetas = []
        self.entradas = []
        self.comboboxes = []
        self.sliders = []
        self.progress_bars = []
        self.tabviews = []
        self.canvas = []
        # Establecer apariencia global
        self.establecer_apariencia_global_controlador()

    # Registrar botones
    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.mostrar_icono_boton(nombre)

    # Registrar botones con iconos de tamaño personalizado
    def registrar_botones_con_tamano(self, nombre, boton, tamano=None):
        self.botones[nombre] = boton
        if tamano:
            # Cargar icono con tamaño personalizado
            icono = cargar_icono_personalizado(nombre, self.tema_iconos, tamano)
            if icono:
                boton.configure(image=icono)
                # Guardar referencia para evitar el recolector de basura
                boton._icono_personalizado = icono
        else:
            # Usar el método estándar para mostrar iconos
            self.mostrar_icono_boton(nombre)

    # Registrar paneles
    def registrar_panel(self, panel, es_ctk=False, es_principal=False):
        # Verificar si el panel no está ya en la lista
        for f, _, _ in self.paneles:
            if f == panel:
                return
        self.paneles.append((panel, es_ctk, es_principal))

    # Registrar etiquetas
    def registrar_etiqueta(self, etiqueta):
        self.etiquetas.append(etiqueta)

    # Registrar entradas
    def registrar_entrada(self, entrada):
        self.entradas.append(entrada)

    # Registrar comboboxes
    def registrar_combobox(self, combobox):
        self.comboboxes.append(combobox)

    # Registrar sliders
    def registrar_slider(self, slider):
        self.sliders.append(slider)

    # Registrar progress bars
    def registrar_progress_bar(self, progress_bar):
        self.progress_bars.append(progress_bar)

    # Registrar tabviews
    def registrar_tabview(self, tabview):
        self.tabviews.append(tabview)

    # Registrar canvas
    def registrar_canvas(self, canvas, es_tabview=False, tabview_parent=None):
        self.canvas.append((canvas, es_tabview, tabview_parent))

    # Mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        if nombre in self.botones:
            boton = self.botones[nombre]
            nombre_icono = nombre.replace("_mini", "")
            if nombre_icono in self.iconos and self.iconos[nombre_icono]:
                boton.configure(image=self.iconos[nombre_icono], compound="left")

    # Actualizar colores de los paneles
    def actualizar_colores_paneles(self):
        for panel, es_ctk, es_principal in self.paneles:
            try:
                if panel.winfo_exists():
                    if es_principal:
                        panel.configure(bg=self.color_fondo_principal)
                    elif es_ctk:
                        panel.configure(fg_color=self.color_fondo)
                    else:
                        panel.configure(fg_color=self.color_base)
            except Exception as e:
                print(f"Error al configurar el color del panel: {e}")

    # Actualizar colores de las etiquetas
    def actualizar_colores_etiquetas(self):
        for etiqueta in self.etiquetas:
            try:
                etiqueta.configure(text_color=self.color_texto)
            except Exception as e:
                print(f"Error al configurar la etiqueta: {e}")

    # Actualizar colores de las entradas
    def actualizar_colores_entradas(self):
        for entrada in self.entradas:
            try:
                entrada.configure(
                    fg_color=self.color_fondo,
                    text_color=self.color_texto,
                    placeholder_text_color=self.color_texto,
                    border_color=self.color_borde,
                )
            except Exception as e:
                print(f"Error al configurar la entrada: {e}")

    # Actualizar colores de los comboboxes
    def actualizar_colores_comboboxes(self):
        for combobox in self.comboboxes:
            try:
                combobox.configure(
                    fg_color=self.color_fondo,
                    text_color=self.color_texto,
                    border_color=self.color_borde,
                    button_color=self.color_fondo,
                    button_hover_color=self.color_hover,
                    dropdown_fg_color=self.color_fondo,
                    dropdown_hover_color=self.color_hover,
                    dropdown_text_color=self.color_texto,
                )
            except Exception as e:
                print(f"Error al configurar el combobox: {e}")

    # Actualizar colores de los botones
    def actualizar_colores_botones(self):
        botones_a_eliminar = []
        for nombre, boton in self.botones.items():
            try:
                if boton.winfo_exists():
                    boton.configure(
                        fg_color=self.color_boton, text_color=self.color_texto, hover_color=self.color_hover
                    )
                else:
                    botones_a_eliminar.append(nombre)
            except Exception as e:
                print(f"Error al configurar el botón {nombre}: {e}")
                botones_a_eliminar.append(nombre)
        # Eliminar los botones que ya no existen
        for nombre in botones_a_eliminar:
            if nombre in self.botones:
                del self.botones[nombre]

    # Actualizar colores de los sliders
    def actualizar_colores_sliders(self):
        for slider in self.sliders:
            try:
                slider.configure(
                    fg_color=self.color_hover,
                    progress_color=self.color_slider,
                    button_color=self.color_slider,
                    button_hover_color=self.color_hover_oscuro,
                )
            except Exception as e:
                print(f"Error al configurar el slider: {e}")

    # Actualizar colores de las progress bars
    def actualizar_colores_progress_bars(self):
        for progress_bar in self.progress_bars:
            try:
                progress_bar.configure(progress_color=self.color_barra_progreso)
            except Exception as e:
                print(f"Error al configurar la progress bar: {e}")

    # Actualizar colores de los tabviews
    def actualizar_colores_tabviews(self):
        for tabview in self.tabviews:
            try:
                tabview.configure(
                    fg_color=self.color_base,
                    segmented_button_fg_color=self.color_segundario,
                    segmented_button_selected_color=self.color_fondo,
                    segmented_button_selected_hover_color=self.color_hover,
                    segmented_button_unselected_color=self.color_hover,
                    segmented_button_unselected_hover_color=self.color_fondo,
                    text_color=self.color_texto,
                )
            except Exception as e:
                print(f"Error al configurar el tabview: {e}")

    # Actualizar colores de los canvas
    def actualizar_colores_canvas(self):
        for canvas_info in self.canvas:
            try:
                canvas = canvas_info[0]
                es_tabview = canvas_info[1]
                tabview_parent = canvas_info[2] if len(canvas_info) > 2 else None
                if es_tabview and tabview_parent and tabview_parent.winfo_exists():
                    # Obtener el color directamente del tabview padre
                    canvas.configure(bg=tabview_parent.cget("fg_color"))
                elif es_tabview:
                    canvas.configure(bg=self.color_base)
                else:
                    canvas.configure(bg=self.color_fondo)
            except Exception as e:
                print(f"Error al configurar el canvas: {e}")

    # Eliminar botones del diccionario
    def eliminar_boton(self, nombre):
        if nombre in self.botones:
            try:
                # Eliminar la referencia al botón sin intentar acceder a él
                del self.botones[nombre]
                return True
            except Exception as e:
                print(f"Error al eliminar el botón {nombre} del controlador: {e}")
                return False
        return False

    # Establecer tema global
    def establecer_apariencia_global_controlador(self):
        ctk.set_appearance_mode("dark" if self.tema_interfaz == "oscuro" else "light")

    # Cambiar tema
    def cambiar_tema_controlador(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.establecer_apariencia_global_controlador()
        self.colores()
        # Limpiar widgets destruidos antes de actualizar
        self.limpiar_widgets_destruidos()
        # Actualizar iconos de botones
        for nombre in list(self.botones.keys()):
            try:
                self.mostrar_icono_boton(nombre)
            except Exception as e:
                print(f"Error al mostrar el icono del botón {nombre}: {e}")
                if nombre in self.botones:
                    del self.botones[nombre]
        try:
            # Actualizar colores de paneles
            self.actualizar_colores_paneles()
            # Actualizar colores de etiquetas
            self.actualizar_colores_etiquetas()
            # Actualizar colores de entradas
            self.actualizar_colores_entradas()
            # Actualizar colores de comboboxes
            self.actualizar_colores_comboboxes()
            # Actualizar colores de botones
            self.actualizar_colores_botones()
            # Actualizar colores de sliders
            self.actualizar_colores_sliders()
            # Actualizar colores de progress bars
            self.actualizar_colores_progress_bars()
            # Actualizar colores de tabviews
            self.actualizar_colores_tabviews()
            # Actualizar colores de canvas
            self.actualizar_colores_canvas()
        except Exception as e:
            print(f"Error al cambiar el tema: {e}")

    # Limpiar widgets destruidos
    def limpiar_widgets_destruidos(self):
        # Limpiar botones destruidos
        botones_a_eliminar = []
        for nombre, boton in self.botones.items():
            try:
                if not boton.winfo_exists():
                    botones_a_eliminar.append(nombre)
            except Exception as e:
                print(f"Error al verificar si el botón {nombre} existe: {e}")
                botones_a_eliminar.append(nombre)
        for nombre in botones_a_eliminar:
            if nombre in self.botones:
                del self.botones[nombre]
        # Limpiar paneles destruidos
        self.paneles = [
            (panel, es_ctk, es_principal)
            for panel, es_ctk, es_principal in self.paneles
            if self.widget_existe(panel)
        ]
        # Limpiar etiquetas destruidas
        self.etiquetas = [etiqueta for etiqueta in self.etiquetas if self.widget_existe(etiqueta)]
        # Limpiar entradas destruidas
        self.entradas = [entrada for entrada in self.entradas if self.widget_existe(entrada)]
        # Limpiar comboboxes destruidos
        self.comboboxes = [combobox for combobox in self.comboboxes if self.widget_existe(combobox)]
        # Limpiar sliders destruidos
        self.sliders = [slider for slider in self.sliders if self.widget_existe(slider)]
        # Limpiar progress_bars destruidas
        self.progress_bars = [bar for bar in self.progress_bars if self.widget_existe(bar)]
        # Limpiar tabviews destruidos
        self.tabviews = [tabview for tabview in self.tabviews if self.widget_existe(tabview)]
        # Limpiar canvas destruidos
        self.canvas = [canvas_info for canvas_info in self.canvas if self.widget_existe(canvas_info[0])]

    # Método auxiliar para verificar si un widget existe
    @staticmethod
    def widget_existe(widget):
        try:
            if widget is None:
                return False
            return widget.winfo_exists()
        except Exception as e:
            print(f"Error al verificar si el widget existe: {e}")
            return False
