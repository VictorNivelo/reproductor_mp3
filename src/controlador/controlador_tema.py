from vista.utiles.utiles_vista import cargar_icono_con_tamanio, cargar_icono
from utiles import UtilesGeneral
import customtkinter as ctk


class ControladorTema(UtilesGeneral):
    def __init__(self):
        super().__init__()
        # Iconos de la interfaz
        self.iconos = cargar_icono(self.tema_iconos)
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
        self.barras = []
        # Establecer apariencia global
        self.establecer_tema_global_controlador()

    # Establecer tema global
    def establecer_tema_global_controlador(self):
        ctk.set_appearance_mode("dark" if self.tema_interfaz == "oscuro" else "light")

    # Función para obtener el tema de iconos actual
    def obtener_tema_iconos_actual(self):
        return self.tema_iconos

    # Función para obtener el tema de la interfaz actual
    def obtener_apariencia_interfaz_actual(self):
        return self.tema_interfaz

    # Mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        if nombre in self.botones:
            boton = self.botones[nombre]
            nombre_icono = nombre.replace("_mini", "")
            if nombre_icono in self.iconos and self.iconos[nombre_icono]:
                boton.configure(image=self.iconos[nombre_icono], compound="left")

    # Registrar botones
    def registrar_botones(self, nombre, boton, tamanio=None):
        self.botones[nombre] = boton

        if tamanio:
            # Cargar icono con tamaño personalizado
            nombre_icono = nombre.replace("_mini", "")
            icono = cargar_icono_con_tamanio(nombre_icono, self.tema_iconos, tamanio)
            if icono:
                boton.configure(image=icono, compound="left")
                # Guardar referencia para evitar el recolector de basura
                boton._icono_personalizado = icono
        else:
            # Usar el método estándar para mostrar iconos con tamaño predeterminado
            self.mostrar_icono_boton(nombre)

    # Eliminar botones del diccionario
    def eliminar_boton(self, nombre):
        if nombre in self.botones:
            try:
                # Eliminar la referencia del botón del diccionario
                del self.botones[nombre]
                return True
            except Exception as e:
                print(f"Error al eliminar el botón {nombre} del controlador: {e}")
                return False
        else:
            return False

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

    def registrar_barras_espectro(self, canvas_espectro, barras_espectro):
        self.barras.append((canvas_espectro, barras_espectro))

    # Actualizar colores de los botones
    def actualizar_colores_botones(self):
        botones_a_eliminar = []
        for nombre, boton in self.botones.items():
            try:
                if boton.winfo_exists():
                    boton.configure(
                        fg_color=self.color_boton,
                        hover_color=self.color_hover,
                        text_color=self.color_texto,
                    )
                else:
                    botones_a_eliminar.append(nombre)
            except Exception as e:
                print(f"Error al configurar el botón {nombre}: {e}")
                botones_a_eliminar.append(nombre)
        # Eliminar los botones que ya no existen
        for nombre in botones_a_eliminar:
            self.eliminar_boton(nombre)

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

    # Actualizar colores de los sliders
    def actualizar_colores_sliders(self):
        for slider in self.sliders:
            try:
                slider.configure(
                    fg_color=self.color_hover,
                    progress_color=self.color_barra_progreso,
                    button_color=self.color_texto,
                )
            except Exception as e:
                print(f"Error al configurar el slider: {e}")

    # Actualizar colores de las progress bars
    def actualizar_colores_progress_bars(self):
        for progress_bar in self.progress_bars:
            try:
                progress_bar.configure(fg_color=self.color_hover, progress_color=self.color_barra_progreso)
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
                if es_tabview:
                    # Para canvas dentro de tabviews, usar color_base
                    canvas.configure(bg=self.color_base)
                else:
                    # Para otros canvas, usar color_fondo
                    canvas.configure(bg=self.color_fondo)
            except Exception as e:
                print(f"Error al configurar el canvas: {e}")

    # Actualizar color de las barras del espectro
    def actualizar_colores_barras_espectro(self):
        for canvas_espectro, barras_espectro in self.barras:
            try:
                if canvas_espectro.winfo_exists() and barras_espectro:
                    for barra in barras_espectro:
                        canvas_espectro.itemconfig(barra, fill=self.color_barras)
            except Exception as e:
                print(f"Error al actualizar espectro: {e}")

    # Cambiar tema
    def cambiar_tema_controlador(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_icono(self.tema_iconos)
        self.establecer_tema_global_controlador()
        self.colores()
        # Limpiar componentes destruidos antes de actualizar
        self.limpiar_componentes_destruidos()
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
            # Actualizar colores de barras del espectro
            self.actualizar_colores_barras_espectro()
        except Exception as e:
            print(f"Error al cambiar el tema: {e}")

    # Método auxiliar para verificar si un componente existe
    @staticmethod
    def existe_componente(componente):
        try:
            if componente is None:
                return False
            return componente.winfo_exists()
        except Exception as e:
            print(f"Error al verificar si el componente existe: {e}")
            return False

    # Limpiar componentes destruidos
    def limpiar_componentes_destruidos(self):
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
            if self.existe_componente(panel)
        ]
        # Limpiar etiquetas destruidas
        self.etiquetas = [etiqueta for etiqueta in self.etiquetas if self.existe_componente(etiqueta)]
        # Limpiar entradas destruidas
        self.entradas = [entrada for entrada in self.entradas if self.existe_componente(entrada)]
        # Limpiar comboboxes destruidos
        self.comboboxes = [combobox for combobox in self.comboboxes if self.existe_componente(combobox)]
        # Limpiar sliders destruidos
        self.sliders = [slider for slider in self.sliders if self.existe_componente(slider)]
        # Limpiar progress_bars destruidas
        self.progress_bars = [bar for bar in self.progress_bars if self.existe_componente(bar)]
        # Limpiar tabviews destruidos
        self.tabviews = [tabview for tabview in self.tabviews if self.existe_componente(tabview)]
        # Limpiar canvas destruidos
        self.canvas = [canvas_info for canvas_info in self.canvas if self.existe_componente(canvas_info[0])]
