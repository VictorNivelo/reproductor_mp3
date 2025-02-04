from vista.utiles import cargar_iconos


class Controlador_tema:
    def __init__(self):
        self.tema_interfaz = "claro"
        self.tema_iconos = "oscuro"
        self.iconos = cargar_iconos(self.tema_iconos)
        self.botones = {}

    # registrar botones
    def registrar_botones(self, nombre, boton):
        self.botones[nombre] = boton
        self.mostrar_icono_boton(nombre)

    # mostrar icono de botones
    def mostrar_icono_boton(self, nombre):
        # si el nombre del boton esta en la lista de botones y en la lista de iconos
        if nombre in self.botones and nombre in self.iconos:
            # se obtiene el boton
            boton = self.botones[nombre]
            # si el boton no esta deshabilitado
            if self.iconos[nombre]:
                # se configura el boton con el icono
                boton.configure(image=self.iconos[nombre], compound="left")

    # cambiar tema
    def cambiar_tema(self):
        # se cambia el tema de la interfaz
        self.tema_interfaz = "oscuro" if self.tema_interfaz == "claro" else "claro"
        self.tema_iconos = "oscuro" if self.tema_interfaz == "claro" else "claro"
        # se cargan los iconos
        self.iconos = cargar_iconos(self.tema_iconos)
        # por cada nombre en la lista de botones se actualiza el boton
        for nombre in self.botones:
            # se actualiza el boton con el nombre
            self.mostrar_icono_boton(nombre)
