import customtkinter as ctk

from vista.componentes.utiles.utiles_componentes import *
from vista.utiles.utiles_atajos import GestorAtajos
from vista.utiles.utiles_vista import *
from utiles import UtilesGeneral
from constantes import *


class Atajos(UtilesGeneral):
    def __init__(self, ventana_principal, controlador_tema):
        super().__init__(controlador_externo=controlador_tema)
        self.ventana_atajos = None
        self.ventana_principal = ventana_principal
        self.controlador_tema = controlador_tema
        self.componentes = []
        self.gestor_atajos = GestorAtajos()
        self.entradas_atajos = {}
        self.botones_editar = {}
        self.botones_restablecer = {}

    # Método para crear la ventana de atajos
    def crear_ventana_atajos(self):
        # Establecer los colores de la interfaz
        self.colores()
        # ======================================= Ventana principal =======================================
        # Crear el panel principal de la ventana de atajos
        self.ventana_atajos = ctk.CTkToplevel(self.ventana_principal)
        # Configurar la ventana para que no se pueda maximizar ni minimizar
        self.ventana_atajos.resizable(False, False)
        # Configurar la ventana de atajos
        crear_ventana_modal(
            ventana_principal=self.ventana_principal,
            ventana_modal=self.ventana_atajos,
            ancho=ANCHO_ATAJOS,
            alto=ALTO_ATAJOS,
            titulo="Atajos",
            color_fondo=self.color_fondo_principal,
            funcion_cierre=self.cerrar_ventana_atajos,
            controlador=self.controlador_tema,
        )
        # =================================================================================================

        # ======================================== Panel principal ========================================

        # **************************************** Panel de atajos ****************************************
        # Crear el panel de atajos
        panel_atajos_general = ctk.CTkFrame(
            self.ventana_atajos,
            fg_color=self.color_fondo,
            corner_radius=BORDES_REDONDEADOS_PANEL,
        )
        panel_atajos_general.pack(fill="both", expand=True, padx=3, pady=3)

        # -------------------------------------- Etiqueta de título ---------------------------------------
        # Crear etiqueta de título
        etiqueta_titulo_atajos = ctk.CTkLabel(
            panel_atajos_general,
            height=15,
            fg_color="transparent",
            font=(LETRA, TAMANIO_LETRA_TITULO, "bold"),
            text_color=self.color_texto,
            text="Atajos de teclado",
        )
        etiqueta_titulo_atajos.pack()
        self.componentes.append(etiqueta_titulo_atajos)
        self.controlador_tema.registrar_etiqueta(etiqueta_titulo_atajos)
        # -------------------------------------------------------------------------------------------------

        # ----------------------------------- Panel contenedor de atajos ----------------------------------
        # Panel que contendrá todos los atajos con scroll
        contenedor_scroll = ctk.CTkFrame(panel_atajos_general, fg_color="transparent")
        contenedor_scroll.pack(fill="both", expand=True, padx=(3, 0), pady=5)
        self.componentes.append(contenedor_scroll)
        # -------------------------------------------------------------------------------------------------

        # Crear los atajos individuales
        self.crear_atajos_individuales(contenedor_scroll)

        # ----------------------------------- Panel de botones --------------------------------------------
        # Panel para los botones de acción
        panel_botones = ctk.CTkFrame(
            panel_atajos_general,
            fg_color="transparent",
        )
        panel_botones.pack(fill="both", expand=True, padx=3, pady=3)
        self.componentes.append(panel_botones)
        # -------------------------------------------------------------------------------------------------

        # -------------------------------------- Botón para guardar cambios -------------------------------
        # Botón para restablecer todos los predeterminados
        boton_restablecer_todos = ctk.CTkButton(
            panel_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Restablecer todos",
            command=self.restablecer_todos_predeterminados,
        )
        boton_restablecer_todos.pack(side="left")
        self.componentes.append(boton_restablecer_todos)
        crear_tooltip(boton_restablecer_todos, "Restablecer todos los atajos")
        # -------------------------------------------------------------------------------------------------

        # -------------------------------------- Botón para cerrar la ventana -----------------------------
        # Botón cerrar
        boton_cerrar_atajos = ctk.CTkButton(
            panel_botones,
            width=ANCHO_BOTON,
            height=ALTO_BOTON,
            corner_radius=BORDES_REDONDEADOS_BOTON,
            fg_color=self.color_boton,
            hover_color=self.color_hover,
            font=(LETRA, TAMANIO_LETRA_BOTON),
            text_color=self.color_texto,
            text="Cerrar",
            command=self.cerrar_ventana_atajos,
        )
        boton_cerrar_atajos.pack(side="right")
        self.componentes.append(boton_cerrar_atajos)
        crear_tooltip(boton_cerrar_atajos, "Cerrar ventana de atajos")
        # -------------------------------------------------------------------------------------------------

    # Método para crear los atajos individuales
    def crear_atajos_individuales(self, panel_padre):
        # Obtener los nombres de atajos y los atajos actuales
        nombres_atajos = self.gestor_atajos.obtener_nombres_atajos()
        atajos_actuales = self.gestor_atajos.obtener_atajos_actuales()
        for accion, nombre in nombres_atajos.items():
            # --------------------------------------- Panel para cada atajo -------------------------------
            # Panel para cada atajo
            panel_atajos = ctk.CTkFrame(
                panel_padre, fg_color="transparent", corner_radius=BORDES_REDONDEADOS_BOTON, height=31
            )
            panel_atajos.pack(fill="x")
            panel_atajos.pack_propagate(False)
            self.componentes.append(panel_atajos)
            # ---------------------------------------------------------------------------------------------

            # ----------------------------------- Etiqueta con el icono del atajo -------------------------
            # Etiqueta con el nombre del atajo
            etiqueta_nombre = ctk.CTkLabel(
                panel_atajos,
                width=130,
                fg_color="transparent",
                font=(LETRA, TAMANIO_LETRA_ETIQUETA_INFORMACION),
                text_color=self.color_texto,
                text=nombre,
                anchor="w",
            )
            etiqueta_nombre.pack(side="left", pady=(0, 2))
            self.componentes.append(etiqueta_nombre)
            self.controlador_tema.registrar_etiqueta(etiqueta_nombre)
            # ---------------------------------------------------------------------------------------------

            # ---------------------------------- Entrada para el atajo ------------------------------------
            # Entry para mostrar/editar el atajo (inicialmente deshabilitado)
            entrada_atajos = ctk.CTkEntry(
                panel_atajos,
                width=150,
                height=28,
                corner_radius=BORDES_REDONDEADOS_ENTRADAS,
                font=(LETRA, TAMANIO_LETRA_ENTRADA),
                fg_color=self.color_fondo,
                text_color=self.color_texto,
                border_color=self.color_borde,
                border_width=1,
                justify="center",
                state="normal",
            )
            entrada_atajos.pack(side="left", pady=(0, 2))

            # Insertar el valor actual del atajo
            valor_actual = atajos_actuales.get(accion, "")
            entrada_atajos.delete(0, "end")
            entrada_atajos.insert(0, valor_actual)
            entrada_atajos.configure(state="disabled")
            self.componentes.append(entrada_atajos)
            # Configurar eventos para el entry
            entrada_atajos.bind("<KeyPress>", lambda e, acc=accion: self.capturar_tecla(e, acc))
            entrada_atajos.bind("<FocusIn>", lambda e, acc=accion: self.seleccionar_texto(e, acc))
            # Guardar referencia al entry
            self.entradas_atajos[accion] = entrada_atajos
            # ---------------------------------------------------------------------------------------------

            icono_editar_atajo = cargar_icono_con_tamanio(
                "editar", self.controlador_tema.tema_iconos, (16, 16)
            )

            # ------------------------------ Botón para editar atajo --------------------------------------
            # Botón para editar/guardar
            boton_editar = ctk.CTkButton(
                panel_atajos,
                width=ANCHO_BOTON,
                height=ALTO_BOTON,
                corner_radius=BORDES_REDONDEADOS_BOTON,
                fg_color=self.color_boton,
                hover_color=self.color_hover,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text_color=self.color_texto,
                text="",
                image=icono_editar_atajo,
                command=lambda acc=accion: self.alternar_modo_edicion(acc),
            )
            boton_editar.pack(side="right", pady=(0, 2))
            self.componentes.append(boton_editar)
            crear_tooltip(boton_editar, f"Editar atajo para {nombre}")
            self.botones_editar[accion] = boton_editar
            # ---------------------------------------------------------------------------------------------

            icono_restablecer = cargar_icono_con_tamanio(
                "restaurar", self.controlador_tema.tema_iconos, (16, 16)
            )

            # -------------------------------- Botón para restablecer atajo -------------------------------
            # Botón para restablecer individual
            boton_restablecer = ctk.CTkButton(
                panel_atajos,
                width=ANCHO_BOTON,
                height=ALTO_BOTON,
                corner_radius=BORDES_REDONDEADOS_BOTON,
                fg_color=self.color_boton,
                hover_color=self.color_hover,
                font=(LETRA, TAMANIO_LETRA_BOTON),
                text_color=self.color_texto,
                text="",
                image=icono_restablecer,
                command=lambda acc=accion: self.restablecer_atajo_individual(acc),
            )
            boton_restablecer.pack(side="right", pady=(0, 2))
            self.componentes.append(boton_restablecer)
            crear_tooltip(boton_restablecer, f"Restablecer predeterminado")
            self.botones_restablecer[accion] = boton_restablecer
            # ---------------------------------------------------------------------------------------------

    # Método para alternar entre modo edición y modo normal
    def alternar_modo_edicion(self, accion):
        entry = self.entradas_atajos[accion]
        boton = self.botones_editar[accion]
        if entry.cget("state") == "disabled":
            # Activar modo edición
            entry.configure(state="normal")
            # Cambiar icono a guardar (sin texto)
            icono_guardar = cargar_icono_con_tamanio("guardar", self.controlador_tema.tema_iconos, (16, 16))
            boton.configure(text="", image=icono_guardar)
            # Actualizar tooltip
            actualizar_texto_tooltip(boton, "Guardar atajo")
            entry.focus_set()
            entry.select_range(0, "end")
        else:
            # Guardar y desactivar modo edición
            self.guardar_atajo_individual(accion)
            entry.configure(state="disabled")
            # Cambiar icono de vuelta a editar
            icono_editar = cargar_icono_con_tamanio("editar", self.controlador_tema.tema_iconos, (16, 16))
            boton.configure(text="", image=icono_editar)
            # Restaurar tooltip original
            nombres_atajos = self.gestor_atajos.obtener_nombres_atajos()
            nombre_accion = nombres_atajos.get(accion, accion)
            actualizar_texto_tooltip(boton, f"Editar atajo para {nombre_accion}")

    # Método para guardar un atajo individual
    def guardar_atajo_individual(self, accion):
        try:
            entry = self.entradas_atajos[accion]
            nueva_tecla = entry.get().strip()
            if nueva_tecla:
                # Verificar si la tecla ya está en uso por otro atajo
                for otra_accion, otra_entry in self.entradas_atajos.items():
                    if otra_accion != accion and otra_entry.get().strip() == nueva_tecla:
                        print(f"La tecla '{nueva_tecla}' ya está en uso por '{otra_accion}'")
                        # Restaurar valor anterior
                        entry.delete(0, "end")
                        entry.insert(0, self.gestor_atajos.obtener_atajo(accion))
                        return
                # Guardar el nuevo atajo
                exito, mensaje = self.gestor_atajos.establecer_atajo(accion, nueva_tecla)
                if exito:
                    print(f"Atajo para '{accion}' guardado correctamente")
                else:
                    print(mensaje)
                    # Restaurar valor anterior
                    entry.delete(0, "end")
                    entry.insert(0, self.gestor_atajos.obtener_atajo(accion))
            else:
                # Si está vacío, usar el predeterminado
                valor_predeterminado = self.gestor_atajos.atajos_por_defecto.get(accion, "")
                entry.delete(0, "end")
                entry.insert(0, valor_predeterminado)
                self.gestor_atajos.establecer_atajo(accion, valor_predeterminado)
        except Exception as e:
            print(f"Error al guardar atajo: {e}")

    # Método para restablecer un atajo individual
    def restablecer_atajo_individual(self, accion):
        try:
            entry = self.entradas_atajos[accion]
            valor_predeterminado = self.gestor_atajos.atajos_por_defecto.get(accion, "")
            # Actualizar la entrada
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, valor_predeterminado)
            entry.configure(state="disabled")
            # Actualizar el botón de edición
            boton = self.botones_editar[accion]
            icono_editar = cargar_icono_con_tamanio("editar", self.controlador_tema.tema_iconos, (16, 16))
            boton.configure(text="", image=icono_editar)
            # Restaurar tooltip original
            nombres_atajos = self.gestor_atajos.obtener_nombres_atajos()
            nombre_accion = nombres_atajos.get(accion, accion)
            actualizar_texto_tooltip(boton, f"Editar atajo para {nombre_accion}")
            # Guardar el cambio
            self.gestor_atajos.establecer_atajo(accion, valor_predeterminado)
            print(f"Atajo para '{accion}' restablecido al valor predeterminado")
        except Exception as e:
            print(f"Error al restablecer atajo: {e}")

    # Método para restablecer todos los atajos predeterminados
    def restablecer_todos_predeterminados(self):
        try:
            exito, mensaje = self.gestor_atajos.restaurar_atajos_predeterminados()
            if exito:
                nombres_atajos = self.gestor_atajos.obtener_nombres_atajos()
                # Actualizar todas las entradas con los valores predeterminados
                for accion, entry in self.entradas_atajos.items():
                    entry.configure(state="normal")
                    entry.delete(0, "end")
                    entry.insert(0, self.gestor_atajos.atajos_por_defecto.get(accion, ""))
                    entry.configure(state="disabled")
                    # Actualizar botones de edición
                    boton = self.botones_editar[accion]
                    icono_editar = cargar_icono_con_tamanio(
                        "editar", self.controlador_tema.tema_iconos, (16, 16)
                    )
                    boton.configure(text="", image=icono_editar)
                    # Restaurar tooltip original
                    nombre_accion = nombres_atajos.get(accion, accion)
                    actualizar_texto_tooltip(boton, f"Editar atajo para {nombre_accion}")
                print("Todos los atajos han sido restablecidos")
            else:
                print("Error al restablecer todos los atajos")
        except Exception as e:
            print(f"Error al restablecer atajos: {e}")

    # Método para capturar teclas presionadas
    def capturar_tecla(self, evento, accion):
        # Solo procesar si el entry está habilitado
        if self.entradas_atajos[accion].cget("state") == "disabled":
            return "break"
        # Prevenir la entrada normal
        evento.widget.delete(0, "end")
        # Construir la combinación de teclas
        teclas = []
        # Modificadores - usar valores más específicos
        if evento.state & 0x4:  # Control
            teclas.append("Control")
        if evento.state & 0x20000:  # Alt (AltGr puede interferir)
            teclas.append("Alt")
        if evento.state & 0x1:  # Shift
            teclas.append("Shift")
        # Tecla principal
        keysym = evento.keysym
        # Mapear teclas especiales
        mapeo_teclas = {
            "Return": "Enter",
            "BackSpace": "BackSpace",
            "Tab": "Tab",
            "Escape": "Escape",
            "Delete": "Delete",
            "Insert": "Insert",
            "Home": "Home",
            "End": "End",
            "Page_Up": "Page_Up",
            "Page_Down": "Page_Down",
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right",
            "space": "space",
        }
        # Teclas de función
        if keysym.startswith("F") and keysym[1:].isdigit():
            tecla_final = keysym
        else:
            tecla_final = mapeo_teclas.get(keysym, keysym)
        # No agregar modificadores duplicados ni teclas de modificadores solas
        teclas_modificadores = [
            "Control_L",
            "Control_R",
            "Alt_L",
            "Alt_R",
            "Shift_L",
            "Shift_R",
            "ISO_Level3_Shift",
        ]
        if tecla_final not in teclas_modificadores:
            # Solo agregar la tecla si no es un modificador solo
            if not (keysym in teclas_modificadores):
                teclas.append(tecla_final)
        # Crear la combinación final solo si hay teclas válidas
        if teclas:
            combinacion = "-".join(teclas) if len(teclas) > 1 else teclas[0]
            # Mostrar en el entry
            evento.widget.insert(0, combinacion)
        return "break"

    # Método para seleccionar todo el texto al hacer foco
    def seleccionar_texto(self, evento, accion):
        if self.entradas_atajos[accion].cget("state") != "disabled":
            evento.widget.select_range(0, "end")

    # Método para mostrar la ventana de atajos
    def mostrar_ventana_atajos(self):
        if not hasattr(self, "ventana_atajos") or self.ventana_atajos is None:
            self.crear_ventana_atajos()
        else:
            try:
                if self.ventana_atajos.winfo_exists():
                    self.colores()
                    establecer_icono_tema(self.ventana_atajos, self.controlador_tema.tema_interfaz)
                    self.ventana_atajos.deiconify()
                else:
                    self.ventana_atajos = None
                    self.crear_ventana_atajos()
            except Exception as e:
                print(f"Error al mostrar la ventana de atajos: {e}")
                self.ventana_atajos = None
                self.crear_ventana_atajos()

    # Método para cerrar la ventana de atajos
    def cerrar_ventana_atajos(self):
        # Limpiar referencias
        self.entradas_atajos.clear()
        self.botones_editar.clear()
        self.botones_restablecer.clear()
        cerrar_ventana_modal(self.ventana_atajos, self.componentes, self.controlador_tema)
