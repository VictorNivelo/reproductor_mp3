from vista.utiles import cargar_iconos
from vista.constantes import *


class Controlador_tema:
    def __init__(self):
        self.tema_interfaz = "claro"
        self.tema_iconos = "oscuro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.botones = {}
        self.frames = []
        self.etiquetas = []
        self.entradas = []
        self.comboboxes = []
        self.sliders = []
        self.progress_bars = []
        self.tabviews = []

    # registrar botones
    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.mostrar_icono_boton(nombre)

    # registrar frames
    def registrar_frame(self, frame, es_ctk=False):
        self.frames.append((frame, es_ctk))

    def registrar_etiqueta(self, etiqueta):
        self.etiquetas.append(etiqueta)

    # registrar entradas
    def registrar_entrada(self, entrada):
        self.entradas.append(entrada)

    # registrar comboboxes
    def registrar_combobox(self, combobox):
        self.comboboxes.append(combobox)

    # registrar sliders
    def registrar_slider(self, slider):
        self.sliders.append(slider)

    # registrar progress bars
    def registrar_progress_bar(self, progress_bar):
        self.progress_bars.append(progress_bar)

    # registrar tabviews
    def registrar_tabview(self, tabview):
        self.tabviews.append(tabview)

    # mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        if nombre in self.botones and nombre in self.iconos:
            boton = self.botones[nombre]
            if self.iconos[nombre]:
                boton.configure(image=self.iconos[nombre], compound="left")

    # actualizar colores de los frames
    def actualizar_colores_frames(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        for frame, es_ctk in self.frames:
            if es_ctk:
                frame.configure(fg_color=color_fondo)
            else:
                frame.configure(bg=color_fondo)

    # actualizar colores de las etiquetas
    def actualizar_colores_etiquetas(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        for etiqueta in self.etiquetas:
            etiqueta.configure(fg_color=color_fondo, text_color=color_texto)

    def actualizar_colores_entradas(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        color_borde = fondo_claro if self.tema_interfaz == "oscuro" else fondo_oscuro
        for entrada in self.entradas:
            entrada.configure(
                fg_color=color_fondo,
                text_color=color_texto,
                placeholder_text_color=color_texto,
                border_color=color_borde,
            )

    # actualizar colores de los comboboxes
    def actualizar_colores_comboboxes(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        color_borde = fondo_claro if self.tema_interfaz == "oscuro" else fondo_oscuro
        color_hover = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        for combobox in self.comboboxes:
            combobox.configure(
                fg_color=color_fondo,
                text_color=color_texto,
                border_color=color_borde,
                button_color=color_fondo,
                button_hover_color=color_hover,
                dropdown_fg_color=color_fondo,
                dropdown_hover_color=color_hover,
                dropdown_text_color=color_texto,
            )

    # actualizar colores de los botones
    def actualizar_colores_botones(self):
        color_fondo = boton_oscuro if self.tema_interfaz == "oscuro" else boton_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        color_hover = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        for boton in self.botones.values():
            boton.configure(fg_color=color_fondo, text_color=color_texto, hover_color=color_hover)

    def actualizar_colores_sliders(self):
        color_fondo = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        color_progreso = texto_oscuro if self.tema_interfaz == "oscuro" else fondo_oscuro
        color_boton = texto_oscuro if self.tema_interfaz == "oscuro" else fondo_oscuro
        color_boton_hover = hover_oscuro if self.tema_interfaz == "oscuro" else hover_oscuro
        for slider in self.sliders:
            slider.configure(
                fg_color=color_fondo,
                progress_color=color_progreso,
                button_color=color_boton,
                button_hover_color=color_boton_hover,
            )

    # actualizar colores de las progress bars
    def actualizar_colores_progress_bars(self):
        color_fondo = hover_oscuro if self.tema_interfaz == "oscuro" else "lightgray"
        color_progreso = texto_oscuro if self.tema_interfaz == "oscuro" else fondo_oscuro
        for progress_bar in self.progress_bars:
            progress_bar.configure(fg_color=color_fondo, progress_color=color_progreso)

    def actualizar_colores_tabviews(self):
        color_fondo = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        color_boton = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_boton_seleccionado = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        for tabview in self.tabviews:
            tabview.configure(
                fg_color=color_fondo,
                segmented_button_fg_color=color_boton,
                segmented_button_selected_color=color_boton_seleccionado,
                segmented_button_selected_hover_color=color_boton_seleccionado,
                segmented_button_unselected_color=color_boton,
                segmented_button_unselected_hover_color=color_boton_seleccionado,
                text_color=color_texto,
            )

    # cambiar tema
    def cambiar_tema(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_iconos(self.tema_iconos)

        # Actualizar iconos de botones
        for nombre in self.botones:
            self.mostrar_icono_boton(nombre)

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
