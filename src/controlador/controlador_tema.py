from vista.utiles import cargar_iconos


class Controlador_tema:
    def __init__(self):
        self.tema_interfaz = "claro"
        self.tema_iconos = "oscuro"
        self.colores = {
            "claro": {
                "fondo": "#f0f0f0",
                "texto": "#333333"
            },
            "oscuro": {
                "fondo": "#333333",
                "texto": "#f0f0f0"
            }
        }
        self.iconos = cargar_iconos(self.tema_iconos)
        self.botones = {}

    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.actualizar_boton(nombre)

    def actualizar_boton(self, nombre):
        if nombre in self.botones:
            boton = self.botones[nombre]
            colores = self.colores[self.tema_interfaz]
            boton.configure(
                bg=colores["fondo"],
                fg=colores["texto"],
                activebackground=colores["fondo"],
                activeforeground=colores["texto"],
            )
            if nombre in self.iconos and self.iconos[nombre]:
                boton.configure(image=self.iconos[nombre], compound="left")

    def cambiar_tema(self):
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.actualizar_botones()

    def actualizar_botones(self):
        for nombre in self.botones:
            self.actualizar_boton(nombre)
