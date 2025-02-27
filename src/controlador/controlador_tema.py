from controlador.utiles.utiles_contolador import UtilesControlador
from vista.utiles.utiles_vista import cargar_iconos
import customtkinter as ctk


class ControladorTema(UtilesControlador):
    def __init__(self):
        super().__init__()
        # Iconos de la interfaz
        self.iconos = cargar_iconos(self.tema_iconos)
        # Diccionario de botones
        self.botones = {}
        self.frames = []
        self.etiquetas = []
        self.entradas = []
        self.comboboxes = []
        self.sliders = []
        self.progress_bars = []
        self.tabviews = []
        self.canvas = []
        # Establecer apariencia global
        self.establecer_apariencia_global()

    # Registrar botones
    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.mostrar_icono_boton(nombre)

    # Registrar frames
    def registrar_frame(self, frame, es_ctk=False, es_principal=False):
        self.frames.append((frame, es_ctk, es_principal))

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
    def registrar_canvas(self, canvas, es_tabview=False):
        self.canvas.append((canvas, es_tabview))

    # Mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        if nombre in self.botones:
            boton = self.botones[nombre]
            nombre_icono = nombre.replace("_mini", "")
            if nombre_icono in self.iconos and self.iconos[nombre_icono]:
                boton.configure(image=self.iconos[nombre_icono], compound="left")

    # Actualizar colores de los frames
    def actualizar_colores_frames(self):
        for frame, es_ctk, es_principal in self.frames:
            try:
                if frame.winfo_exists():
                    if es_principal:
                        frame.configure(bg=self.color_principal)
                    elif es_ctk:
                        frame.configure(fg_color=self.color_fondo)
                    else:
                        frame.configure(bg=self.color_fondo)
            except Exception as e:
                print(f"Error al configurar el color del frame: {e}")

    # Actualizar colores de las etiquetas
    def actualizar_colores_etiquetas(self):
        for etiqueta in self.etiquetas:
            try:
                etiqueta.configure(fg_color=self.color_fondo, text_color=self.color_texto)
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
                progress_bar.configure(fg_color=self.barra_progreso, progress_color=self.color_slider)
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
        for canvas, es_tabview in self.canvas:
            try:
                if es_tabview:
                    canvas.configure(bg=self.color_segundario)
                else:
                    canvas.configure(bg=self.color_fondo)
            except Exception as e:
                print(f"Error al configurar el canvas: {e}")

    # Eliminar botones del diccionario
    def eliminar_boton(self, nombre):
        if nombre in self.botones:
            del self.botones[nombre]

    # Establecer tema global
    def establecer_apariencia_global(self):
        ctk.set_appearance_mode("dark" if self.tema_interfaz == "oscuro" else "light")

    # Cambiar tema
    def cambiar_tema(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.establecer_apariencia_global()
        self.colores()
        # Actualizar iconos de botones
        for nombre in self.botones:
            try:
                self.mostrar_icono_boton(nombre)
            except Exception as e:
                print(f"Error al mostrar el icono del botón {nombre}: {e}")
        try:
            # Actualizar colores de frames
            self.actualizar_colores_frames()
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
