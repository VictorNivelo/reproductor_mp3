import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from vista.vista_principal import ventana_principal


def main():
    ventana = ventana_principal
    ventana.mainloop()


if __name__ == "__main__":
    main()
