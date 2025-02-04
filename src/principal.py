from controlador.controlador_tema import Controlador_tema
from vista import vista_principal


def main():
    controlador = Controlador_tema()
    vista = vista_principal(controlador)
    vista.iniciar()


if __name__ == "__main__":
    main()
