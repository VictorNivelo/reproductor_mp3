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
        self.componente_etiqueta_animada = None

    # Método para configurar el desplazamiento automático de etiquetas
    def configurar_desplazamiento_etiqueta(self, componente_etiqueta, textos_dict, longitud_maxima):
        self.detener_desplazamiento_etiqueta()
        if not componente_etiqueta or not componente_etiqueta.winfo_exists():
            return
        self.componente_etiqueta_animada = componente_etiqueta
        # Reinicializar estados para la nueva animación
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.textos_animados = textos_dict.copy()
        self.pausa_inicio = {}
        self.pausa_final = {}
        longitud_letra_dict = {}
        for clave, (texto, etiqueta_actual) in self.textos_animados.items():
            # Asegurarse de que la etiqueta actual (del diccionario) existe
            if not etiqueta_actual or not etiqueta_actual.winfo_exists():
                self.desplazamiento_activo[clave] = False
                continue
            # Obtener la fuente del componente
            font = letra.Font(font=etiqueta_actual.cget("font"))
            # Calcular cuántos caracteres caben en el ancho dado
            longitud_letra_calculada = len(texto)
            for i in range(1, len(texto) + 1):
                if font.measure(texto[:i]) > longitud_maxima:
                    longitud_letra_calculada = i - 1
                    break
            longitud_letra_dict[clave] = longitud_letra_calculada
            if len(texto) > longitud_letra_calculada:
                self.desplazamiento_activo[clave] = True
                self.posicion_desplazamiento[clave] = 0
                self.direccion_desplazamiento[clave] = (
                    1  # Asumo que siempre es 1, no se usa en el código provisto
                )
                etiqueta_actual.configure(text=texto[:longitud_letra_calculada] + "...")
            else:
                self.desplazamiento_activo[clave] = False
                etiqueta_actual.configure(text=texto)
        # Iniciar animación automática si hay textos largos
        if any(self.desplazamiento_activo.values()):
            # Filtrar claves que realmente están activas y tienen longitud_letra_dict
            claves_activas = [
                k for k, v in self.desplazamiento_activo.items() if v and k in longitud_letra_dict
            ]
            if claves_activas:
                min_longitud_letra = min(longitud_letra_dict[clave] for clave in claves_activas)
                self.iniciar_desplazamiento_etiqueta(min_longitud_letra)

    # Método para iniciar desplazamiento de textos largos (llama a animar)
    def iniciar_desplazamiento_etiqueta(self, longitud_maxima):
        if not self.componente_etiqueta_animada or not self.componente_etiqueta_animada.winfo_exists():
            return
        # Cancelar explícitamente aquí también por si acaso, usando el componente guardado
        if self.id_marcador_tiempo:
            try:
                self.componente_etiqueta_animada.after_cancel(self.id_marcador_tiempo)
            except Exception as e:
                print(f"Error al cancelar el temporizador: {e}")
                pass
            self.id_marcador_tiempo = None
        if any(self.desplazamiento_activo.values()):
            self.animar_desplazamiento_etiqueta(longitud_maxima)

    # Método para detener la animación
    def detener_desplazamiento_etiqueta(self):  # Ya no necesita argumento componente_etiqueta
        if self.id_marcador_tiempo and self.componente_etiqueta_animada:
            if self.componente_etiqueta_animada.winfo_exists():
                try:
                    self.componente_etiqueta_animada.after_cancel(self.id_marcador_tiempo)
                except Exception as e:
                    print(f"Error al cancelar el temporizador: {e}")
                    pass
        self.id_marcador_tiempo = None
        self.componente_etiqueta_animada = None  # Olvidar el componente
        # Resetear todos los estados de la animación de etiquetas
        self.desplazamiento_activo = {}
        self.posicion_desplazamiento = {}
        self.direccion_desplazamiento = {}
        self.textos_animados = {}
        self.pausa_inicio = {}
        self.pausa_final = {}

    # Método para animar el desplazamiento del texto
    def animar_desplazamiento_etiqueta(self, longitud_maxima, intervalo=125, reproduciendo=True):
        # Comprobación robusta al inicio
        if (
            not self.componente_etiqueta_animada
            or not self.componente_etiqueta_animada.winfo_exists()
            or not self.textos_animados
            or not any(self.desplazamiento_activo.values())
        ):
            self.id_marcador_tiempo = None  # Asegurar que no quede un ID colgado si salimos
            return
        # Si la reproducción está pausada, no animamos el desplazamiento
        if not reproduciendo:
            if self.componente_etiqueta_animada.winfo_exists():  # Comprobar antes de .after
                self.id_marcador_tiempo = self.componente_etiqueta_animada.after(
                    400,
                    lambda: self.animar_desplazamiento_etiqueta(longitud_maxima, intervalo, reproduciendo),
                )
            return
        algo_que_animar_restante = False
        for clave, (texto_completo, etiqueta) in list(self.textos_animados.items()):  # Iterar sobre copia
            if not self.desplazamiento_activo.get(clave, False):
                continue
            if not etiqueta or not etiqueta.winfo_exists():  # Si la etiqueta individual ya no existe
                self.desplazamiento_activo.pop(clave, None)  # Eliminar de activos
                continue
            algo_que_animar_restante = True  # Todavía hay al menos una etiqueta activa
            posicion = self.posicion_desplazamiento[clave]
            # Control de pausa al inicio
            if posicion == 0:
                self.pausa_inicio.setdefault(clave, 0)
                if self.pausa_inicio[clave] < 8:  # 8 * 125ms = 1 segundo de pausa
                    self.pausa_inicio[clave] += 1
                    texto_visible = texto_completo[:longitud_maxima]
                    if etiqueta.winfo_exists():
                        etiqueta.configure(text=texto_visible)
                    continue
                else:
                    self.pausa_inicio[clave] = 0  # Resetear pausa para la próxima vez
            # Control de pausa al final
            if posicion >= len(texto_completo) - longitud_maxima:
                self.pausa_final.setdefault(clave, 0)
                if self.pausa_final[clave] < 8:  # 1 segundo de pausa
                    texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                    if etiqueta.winfo_exists():
                        etiqueta.configure(text=texto_visible)
                    self.pausa_final[clave] += 1
                    continue
                else:
                    self.posicion_desplazamiento[clave] = 0  # Reiniciar posición
                    texto_visible = texto_completo[:longitud_maxima]
                    self.pausa_final[clave] = 0  # Resetear pausa
                    if etiqueta.winfo_exists():
                        etiqueta.configure(text=texto_visible)
                    continue
            # Desplazamiento normal
            texto_visible = texto_completo[posicion : posicion + longitud_maxima]
            self.posicion_desplazamiento[clave] += 1
            if etiqueta.winfo_exists():
                etiqueta.configure(text=texto_visible)
        # Programar próxima actualización solo si el componente principal existe y hay algo que animar
        if (
            algo_que_animar_restante
            and self.componente_etiqueta_animada
            and self.componente_etiqueta_animada.winfo_exists()
        ):
            self.id_marcador_tiempo = self.componente_etiqueta_animada.after(
                intervalo,
                lambda: self.animar_desplazamiento_etiqueta(longitud_maxima, intervalo, reproduciendo),
            )
        else:
            # No hay más animación o el componente principal se fue
            self.id_marcador_tiempo = None

    # Método para configurar el desplazamiento de un botón
    def configurar_desplazamiento_boton(self, componente_boton, texto_completo, longitud_maxima):
        if len(texto_completo) <= longitud_maxima:
            componente_boton.configure(text=texto_completo)
            return
        setattr(componente_boton, "texto_completo", texto_completo)
        setattr(componente_boton, "posicion_desplazamiento", 0)
        setattr(componente_boton, "id_temporizador", None)
        componente_boton.bind("<Enter>", lambda event: self.iniciar_desplazamiento_boton(componente_boton))
        componente_boton.bind(
            "<Leave>", lambda event: self.detener_desplazamiento_boton(componente_boton, longitud_maxima)
        )
        componente_boton.configure(text=texto_completo[:longitud_maxima] + "...")

    # Método para iniciar el desplazamiento del texto en un botón
    def iniciar_desplazamiento_boton(self, componente_boton):
        if hasattr(componente_boton, "id_temporizador") and getattr(componente_boton, "id_temporizador"):
            componente_boton.after_cancel(getattr(componente_boton, "id_temporizador"))
        setattr(componente_boton, "posicion_desplazamiento", 0)
        self.animar_desplazamiento_boton(componente_boton)

    # Método para detener el desplazamiento del texto en un botón
    @staticmethod
    def detener_desplazamiento_boton(componente_boton, longitud_maxima=50):
        if hasattr(componente_boton, "id_temporizador") and getattr(componente_boton, "id_temporizador"):
            componente_boton.after_cancel(getattr(componente_boton, "id_temporizador"))
        texto_completo = getattr(componente_boton, "texto_completo", "")
        componente_boton.configure(text=texto_completo[:longitud_maxima] + "...")

    # Método para animar el texto en un botón
    def animar_desplazamiento_boton(self, componente_boton, longitud_maxima=50):
        if not hasattr(componente_boton, "texto_completo"):
            return
        texto_completo = getattr(componente_boton, "texto_completo")
        pos = getattr(componente_boton, "posicion_desplazamiento", 0)
        if pos == 0:
            if not hasattr(componente_boton, "pausa_inicio"):
                setattr(componente_boton, "pausa_inicio", 0)
            pausa_actual = getattr(componente_boton, "pausa_inicio")
            if pausa_actual < 8:
                setattr(componente_boton, "pausa_inicio", pausa_actual + 1)
                texto_visible = texto_completo[:longitud_maxima]
                componente_boton.configure(text=texto_visible + "...")
                id_temporizador = componente_boton.after(
                    125, lambda: self.animar_desplazamiento_boton(componente_boton, longitud_maxima)
                )
                setattr(componente_boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(componente_boton, "pausa_inicio", 0)
        if pos >= len(texto_completo) - longitud_maxima:
            if not hasattr(componente_boton, "pausa_final"):
                setattr(componente_boton, "pausa_final", 0)
            pausa_actual = getattr(componente_boton, "pausa_final")
            if pausa_actual < 8:
                setattr(componente_boton, "pausa_final", pausa_actual + 1)
                texto_visible = texto_completo[len(texto_completo) - longitud_maxima :]
                componente_boton.configure(text=texto_visible)
                id_temporizador = componente_boton.after(
                    125, lambda: self.animar_desplazamiento_boton(componente_boton, longitud_maxima)
                )
                setattr(componente_boton, "id_temporizador", id_temporizador)
                return
            else:
                setattr(componente_boton, "pausa_final", 0)
                setattr(componente_boton, "posicion_desplazamiento", 0)
                texto_visible = texto_completo[:longitud_maxima]
                componente_boton.configure(text=texto_visible + "...")
                id_temporizador = componente_boton.after(
                    125, lambda: self.animar_desplazamiento_boton(componente_boton, longitud_maxima)
                )
                setattr(componente_boton, "id_temporizador", id_temporizador)
                return
        texto_visible = texto_completo[pos : pos + longitud_maxima]
        componente_boton.configure(text=texto_visible)
        setattr(componente_boton, "posicion_desplazamiento", pos + 1)
        id_temporizador = componente_boton.after(
            125, lambda: self.animar_desplazamiento_boton(componente_boton, longitud_maxima)
        )
        setattr(componente_boton, "id_temporizador", id_temporizador)
