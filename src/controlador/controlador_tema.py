from vista.utiles import cargar_iconos
from vista.constantes import *
import customtkinter as ctk


class ControladorTema:
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
        self.canvas = []
        self.establecer_tema_global()

    # registrar botones
    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.mostrar_icono_boton(nombre)

    # registrar frames
    def registrar_frame(self, frame, es_ctk=False, es_principal=False):
        self.frames.append((frame, es_ctk, es_principal))

    # registrar etiquetas
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

    # registrar canvas
    def registrar_canvas(self, canvas, es_tabview=False):
        self.canvas.append((canvas, es_tabview))

    # mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        if nombre in self.botones:
            boton = self.botones[nombre]
            nombre_icono = nombre.replace("_mini", "")
            if nombre_icono in self.iconos and self.iconos[nombre_icono]:
                boton.configure(image=self.iconos[nombre_icono], compound="left")

    # actualizar colores de los frames
    def actualizar_colores_frames(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_principal = (
            fondo_principal_oscuro if self.tema_interfaz == "oscuro" else fondo_principal_claro
        )
        for frame, es_ctk, es_principal in self.frames:
            if es_principal:
                frame.configure(bg=color_principal)
            elif es_ctk:
                frame.configure(fg_color=color_fondo)
            else:
                frame.configure(bg=color_fondo)

    # actualizar colores de las etiquetas
    def actualizar_colores_etiquetas(self):
        color_fondo = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        for etiqueta in self.etiquetas:
            etiqueta.configure(fg_color=color_fondo, text_color=color_texto)

    # actualizar colores de las entradas
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

    # actualizar colores de los sliders
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

    # actualizar colores de los tabviews
    def actualizar_colores_tabviews(self):
        color_fondo = oscuro if self.tema_interfaz == "oscuro" else claro
        color_barra = oscuro_segundario if self.tema_interfaz == "oscuro" else claro_segundario
        color_pestania = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        color_hover = hover_oscuro if self.tema_interfaz == "oscuro" else hover_claro
        color_texto = texto_oscuro if self.tema_interfaz == "oscuro" else texto_claro
        for tabview in self.tabviews:
            tabview.configure(
                fg_color=color_fondo,
                segmented_button_fg_color=color_barra,
                segmented_button_selected_color=color_pestania,
                segmented_button_selected_hover_color=color_hover,
                segmented_button_unselected_color=color_hover,
                segmented_button_unselected_hover_color=color_pestania,
                text_color=color_texto,
            )

    # actualizar colores de los canvas
    def actualizar_colores_canvas(self):
        color_tabview = oscuro_segundario if self.tema_interfaz == "oscuro" else claro_segundario
        color_normal = fondo_oscuro if self.tema_interfaz == "oscuro" else fondo_claro
        for canvas, es_tabview in self.canvas:
            if es_tabview:
                canvas.configure(bg=color_tabview)
            else:
                canvas.configure(bg=color_normal)

    # establecer tema global
    def establecer_tema_global(self):
        ctk.set_appearance_mode("dark" if self.tema_interfaz == "oscuro" else "light")

    # cambiar tema
    def cambiar_tema(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.establecer_tema_global()
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
        # Actualizar colores de canvas
        self.actualizar_colores_canvas()
