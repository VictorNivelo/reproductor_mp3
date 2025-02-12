from vista.constantes import *
import customtkinter as ctk


ctk.set_appearance_mode("light")
tamanio_minireproductor = f"{ancho_minireproductor}x{alto_minireproductor}"


class MiniReproductor:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal_mini_reproductor = None

    def mostrar(self):
        if self.ventana_principal_mini_reproductor is None:
            self.crear_ventana()
        self.ventana_principal_mini_reproductor.deiconify()
        self.ventana_principal.withdraw()

    def ocultar(self):
        if self.ventana_principal_mini_reproductor:
            self.ventana_principal_mini_reproductor.withdraw()
            self.ventana_principal.deiconify()

    def crear_ventana(self):
        self.ventana_principal_mini_reproductor = ctk.CTk()
        self.ventana_principal_mini_reproductor.title("Minireproductor de música")
        self.ventana_principal_mini_reproductor.iconbitmap("recursos/iconos/reproductor.ico")
        self.ventana_principal_mini_reproductor.geometry(tamanio_minireproductor)
        self.ventana_principal_mini_reproductor.resizable(False, False)

        panel_principal_mini_reproductor = ctk.CTkFrame(
            self.ventana_principal_mini_reproductor, fg_color=fondo_principal
        )
        panel_principal_mini_reproductor.pack(fill="x", expand=True)

        panel_derecha = ctk.CTkFrame(
            panel_principal_mini_reproductor,
            fg_color=fondo_claro,
            width=300,
            height=165,
        )
        panel_derecha.pack(side="right", padx=(0, 5), pady=5)
        panel_derecha.pack_propagate(False)

        panel_informacion = ctk.CTkFrame(panel_derecha, fg_color=fondo_claro)
        panel_informacion.pack(fill="x", padx=5, pady=3)

        etiqueta_nombre_cancion = ctk.CTkLabel(
            panel_informacion,
            text="Nombre de la canción",
            font=(letra, tamanio_letra_etiqueta - 1),
            fg_color=fondo_claro,
        )
        etiqueta_nombre_cancion.pack()

        etiqueta_artista = ctk.CTkLabel(
            panel_informacion,
            text="Artista",
            font=(letra, tamanio_letra_etiqueta - 1),
            fg_color=fondo_claro,
        )
        etiqueta_artista.pack()

        etiqueta_album = ctk.CTkLabel(
            panel_informacion,
            text="Álbum",
            font=(letra, tamanio_letra_etiqueta - 1),
            fg_color=fondo_claro,
        )
        etiqueta_album.pack()

        panel_progreso = ctk.CTkFrame(panel_derecha, fg_color=fondo_claro)
        panel_progreso.pack(fill="x", padx=5)

        barra_progreso = ctk.CTkProgressBar(panel_progreso, height=5, fg_color=fondo_claro)
        barra_progreso.pack(fill="x")

        panel_tiempo = ctk.CTkFrame(panel_progreso, fg_color=fondo_claro)
        panel_tiempo.pack(fill="x")

        etiqueta_tiempo_inicio = ctk.CTkLabel(
            panel_tiempo, text="00:00", font=(letra, tamanio_letra_tiempo - 1), fg_color=fondo_claro
        )
        etiqueta_tiempo_inicio.pack(side="left")

        etiqueta_tiempo_final = ctk.CTkLabel(
            panel_tiempo, text="00:00", font=(letra, tamanio_letra_tiempo - 1), fg_color=fondo_claro
        )
        etiqueta_tiempo_final.pack(side="right")

        panel_botones = ctk.CTkFrame(panel_derecha, fg_color=fondo_claro)
        panel_botones.pack(fill="x", padx=5, pady=(0, 5))

        contenedor_botones = ctk.CTkFrame(panel_botones, fg_color=fondo_claro)
        contenedor_botones.pack(pady=(0, 3), expand=True)

        boton_anterior = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=boton_claro,
            font=(letra, tamanio_letra_boton),
            text_color=texto_claro,
            text="⏮",
            hover_color=hover_claro,
        )
        boton_anterior.pack(side="left", padx=5)
        # self.controlador.registrar_botones("anterior", boton_anterior)

        boton_reproducir = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=boton_claro,
            font=(letra, tamanio_letra_boton),
            text_color=texto_claro,
            text="▶",
            hover_color=hover_claro,
        )
        boton_reproducir.pack(side="left", padx=5)
        # self.controlador.registrar_botones("reproducir", boton_reproducir)

        boton_siguiente = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=boton_claro,
            font=(letra, tamanio_letra_boton),
            text_color=texto_claro,
            text="⏭",
            hover_color=hover_claro,
        )
        boton_siguiente.pack(side="left", padx=5)
        # self.controlador.registrar_botones("siguiente", boton_siguiente)

        boton_maximizar = ctk.CTkButton(
            contenedor_botones,
            width=ancho_boton,
            height=alto_boton,
            fg_color=boton_claro,
            font=(letra, tamanio_letra_boton),
            text_color=texto_claro,
            text="⬆",
            hover_color=hover_claro,
            command=self.ocultar,
        )
        boton_maximizar.pack(side="left", padx=5)
        # self.controlador.registrar_botones("maximizar", boton_maximizar)

        panel_izquierda = ctk.CTkFrame(
            panel_principal_mini_reproductor,
            fg_color=fondo_claro,
            width=135,
            height=165,
        )
        panel_izquierda.pack(side="left", padx=(5, 0), pady=5)
        panel_izquierda.pack_propagate(False)

        imagen_cancion = ctk.CTkLabel(panel_izquierda, text="img", fg_color=fondo_claro)
        imagen_cancion.pack(pady=5)

        self.ventana_principal_mini_reproductor.protocol("WM_DELETE_WINDOW", self.ocultar)

        # self.ventana_principal_mini_reproductor.mainloop()
