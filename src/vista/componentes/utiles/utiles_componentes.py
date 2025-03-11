def cerrar_ventana_modal(ventana, componentes, controlador):
    try:
        # Eliminar referencias de los componentes en el controlador
        for widget in componentes:
            if widget in controlador.frames:
                controlador.frames.remove(widget)
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
