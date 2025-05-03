import tkinter.font as letra


class AnimacionGeneral:
    def __init__(self):
        # Animaciones
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.id_marcador_tiempo = None
        self.textos_animados = {}
        self.pausa_inicio = {}
        self.pausa_final = {}

    # Método para configurar el desplazamiento automático de etiquetas
    def configurar_desplazamiento_etiqueta(self, textos_dict, componente_principal, longitud_maxima):
        # Cancelar cualquier animación anterior
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            componente_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.textos_animados = textos_dict
        longitud_letra_dict = {}
        for clave, (texto, etiqueta) in textos_dict.items():
            # Obtener la fuente del componente
            font = letra.Font(font=etiqueta.cget("font"))
            # Calcular cuántos caracteres caben en el ancho dado
            longitud_letra = len(texto)
            for i in range(1, len(texto) + 1):
                if font.measure(texto[:i]) > longitud_maxima:
                    longitud_letra = i - 1
                    break
            longitud_letra_dict[clave] = longitud_letra
            if len(texto) > longitud_letra:
                self.desplazamiento_activo[clave] = True
                self.posicion_desplazamiento[clave] = 0
                self.direccion_desplazamiento[clave] = 1
                etiqueta.configure(text=texto[:longitud_letra] + "...")
            else:
                self.desplazamiento_activo[clave] = False
                etiqueta.configure(text=texto)
        # Iniciar animación automática si hay textos largos
        if any(self.desplazamiento_activo.values()):
            min_longitud_letra = min(
                longitud_letra_dict[clave]
                for clave in self.desplazamiento_activo
                if self.desplazamiento_activo[clave]
            )
            self.iniciar_desplazamiento_etiqueta(componente_principal, min_longitud_letra)

    # Método para iniciar desplazamiento de textos largos (llama a animar)
    def iniciar_desplazamiento_etiqueta(self, componente_principal, longitud_maxima):
        # Cancelar cualquier animación anterior
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            componente_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None
        # Ya están configurados los diccionarios, solo animar
        if any(self.desplazamiento_activo.values()):
            self.animar_desplazamiento_etiqueta(componente_principal, longitud_maxima)

    # Método para detener la animación
    def detener_desplazamiento_etiqueta(self, componente_principal):
        if hasattr(self, "id_marcador_tiempo") and self.id_marcador_tiempo:
            componente_principal.after_cancel(self.id_marcador_tiempo)
            self.id_marcador_tiempo = None

    # Método para animar el desplazamiento del texto
    def animar_desplazamiento_etiqueta(
        self, componente_principal, longitud_maxima, intervalo=125, reproduciendo=True
    ):
        if not hasattr(self, "desplazamiento_activo") or not self.textos_animados:
            return
        # Si la reproducción está pausada, no animamos el desplazamiento
        if not reproduciendo:
            self.id_marcador_tiempo = componente_principal.after(
                400,
                lambda: self.animar_desplazamiento_etiqueta(
                    componente_principal, longitud_maxima, intervalo, reproduciendo
                ),
            )
            return
        for clave, (texto_completo, etiqueta) in self.textos_animados.items():
            if not self.desplazamiento_activo.get(clave, False):
                continue
            posicion = self.posicion_desplazamiento[clave]
            # Control de pausa al inicio
            if posicion == 0:
                self.pausa_inicio.setdefault(clave, 0)
                if self.pausa_inicio[clave] < 8:
                    self.pausa_inicio[clave] += 1
                    texto_visible = texto_completo[:longitud_maxima]
                    etiqueta.configure(text=texto_visible)
                    continue
                else:
                    self.pausa_inicio[clave] = 0
            if posicion >= len(texto_completo) - longitud_maxima:
                self.pausa_final.setdefault(clave, 0)
                if self.pausa_final[clave] < 8:
                    texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                    etiqueta.configure(text=texto_visible)
                    self.pausa_final[clave] += 1
                    continue
                else:
                    self.posicion_desplazamiento[clave] = 0
                    texto_visible = texto_completo[:longitud_maxima]
                    self.pausa_final[clave] = 0
                    etiqueta.configure(text=texto_visible)
                    continue
            # Desplazamiento normal
            texto_visible = texto_completo[posicion : posicion + longitud_maxima]
            self.posicion_desplazamiento[clave] += 1
            etiqueta.configure(text=texto_visible)
        # Programar próxima actualización
        self.id_marcador_tiempo = componente_principal.after(
            intervalo,
            lambda: self.animar_desplazamiento_etiqueta(
                componente_principal, longitud_maxima, intervalo, reproduciendo
            ),
        )

    # Método para configurar el desplazamiento de un botón
    def configurar_desplazamiento_boton(self, boton, texto_completo, longitud_maxima):
        if len(texto_completo) <= longitud_maxima:
            boton.configure(text=texto_completo)
            return
        setattr(boton, "texto_completo", texto_completo)
        setattr(boton, "posicion_desplazamiento", 0)
        setattr(boton, "id_temporizador", None)
        boton.bind("<Enter>", lambda event: self.iniciar_desplazamiento_boton(boton))
        boton.bind("<Leave>", lambda event: self.detener_desplazamiento_boton(boton, longitud_maxima))
        boton.configure(text=texto_completo[:longitud_maxima] + "...")

    # Método para iniciar el desplazamiento del texto en un botón
    def iniciar_desplazamiento_boton(self, boton):
        if hasattr(boton, "id_temporizador") and getattr(boton, "id_temporizador"):
            boton.after_cancel(getattr(boton, "id_temporizador"))
        setattr(boton, "posicion_desplazamiento", 0)
        self.animar_desplazamiento_boton(boton)

    # Método para detener el desplazamiento del texto en un botón
    @staticmethod
    def detener_desplazamiento_boton(boton, longitud_maxima=55):
        if hasattr(boton, "id_temporizador") and getattr(boton, "id_temporizador"):
            boton.after_cancel(getattr(boton, "id_temporizador"))
        texto_completo = getattr(boton, "texto_completo", "")
        boton.configure(text=texto_completo[:longitud_maxima] + "...")

    # Método para animar el texto en un botón
    def animar_desplazamiento_boton(self, boton, longitud_maxima=55):
        if not hasattr(boton, "texto_completo"):
            return
        texto_completo = getattr(boton, "texto_completo")
        pos = getattr(boton, "posicion_desplazamiento", 0)
        if pos == 0:
            if not hasattr(boton, "pausa_inicio"):
                setattr(boton, "pausa_inicio", 0)
            pausa_actual = getattr(boton, "pausa_inicio")
            if pausa_actual < 8:
                setattr(boton, "pausa_inicio", pausa_actual + 1)
                texto_visible = texto_completo[:longitud_maxima]
                boton.configure(text=texto_visible + "...")
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(boton, "pausa_inicio", 0)
        if pos >= len(texto_completo) - longitud_maxima:
            if not hasattr(boton, "pausa_final"):
                setattr(boton, "pausa_final", 0)
            pausa_actual = getattr(boton, "pausa_final")
            if pausa_actual < 8:
                setattr(boton, "pausa_final", pausa_actual + 1)
                texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                boton.configure(text=texto_visible)
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(boton, "pausa_final", 0)
                setattr(boton, "posicion_desplazamiento", 0)
                texto_visible = texto_completo[:longitud_maxima]
                boton.configure(text=texto_visible + "...")
                id_temporizador = boton.after(
                    125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima)
                )
                setattr(boton, "id_temporizador", id_temporizador)
                return
        texto_visible = texto_completo[pos : pos + longitud_maxima]
        boton.configure(text=texto_visible)
        setattr(boton, "posicion_desplazamiento", pos + 1)
        id_temporizador = boton.after(125, lambda: self.animar_desplazamiento_boton(boton, longitud_maxima))
        setattr(boton, "id_temporizador", id_temporizador)
