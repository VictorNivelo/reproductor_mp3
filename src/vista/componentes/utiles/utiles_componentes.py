from vista.utiles.utiles_vista import establecer_icono_tema


# Metodo para configurar la ventana modal
def configurar_ventana_modal(
    ventana_principal, ventana_modal, ancho, alto, titulo, color_fondo, funcion_cierre, controlador
):
    # Establecer el título de la ventana modal
    ventana_modal.title(titulo)
    # Establecer el tamaño y posición de la ventana modal
    posicion_ancho = ventana_principal.winfo_x() + (ventana_principal.winfo_width() - ancho) // 2
    posicion_alto = ventana_principal.winfo_y() + (ventana_principal.winfo_height() - alto) // 2
    # Tamaño de la ventana modal
    tamanio_ventana = f"{ancho}x{alto}+{posicion_ancho}+{posicion_alto}"
    # Establecer la geometría de la ventana modal
    ventana_modal.geometry(tamanio_ventana)
    # Establecer el color de fondo de la ventana modal
    ventana_modal.configure(fg_color=color_fondo)
    # Configuración de la ventana como un modal
    ventana_modal.grab_set()
    # Evento para cerrar la ventana modal
    ventana_modal.protocol("WM_DELETE_WINDOW", funcion_cierre)
    # Establecer el icono de la ventana modal
    establecer_icono_tema(ventana_modal, controlador.tema_interfaz)


# Metodo para cerrar la ventana modal
def cerrar_ventana_modal(ventana, componentes, controlador):
    try:
        # Eliminar referencias de los componentes en el controlador
        for widget in componentes:
            if widget in controlador.paneles:
                controlador.paneles.remove(widget)
            if widget in controlador.etiquetas:
                controlador.etiquetas.remove(widget)
            for nombre in list(controlador.botones.keys()):
                if controlador.botones[nombre] == widget:
                    del controlador.botones[nombre]
        # Limpiar lista de componentes
        componentes.clear()
        # Liberar el modo modal
        ventana.grab_release()
        # Destruir la ventana
        ventana.destroy()
    except Exception as e:
        print(f"Error durante la limpieza: {e}")
