import tkinter as tk
import customtkinter as ctk

ventana = tk.Tk()
ventana.title("Ventana de prueba")

# Configuramos tamaño específico para el panel rojo
panel = ctk.CTkFrame(ventana, fg_color="red", width=200, height=200)
panel.pack(padx=10, pady=10)
panel.pack_propagate(False)  # Evita que el frame se ajuste al contenido

# Configuramos tamaño específico para el panel azul
paneltk = tk.Frame(panel, bg="blue", width=190, height=190)
paneltk.pack(padx=5, pady=5)
paneltk.pack_propagate(False)  # Evita que el frame se ajuste al contenido

# Añadimos una etiqueta para ver mejor el contenido
etiqueta = tk.Label(paneltk, text="Panel Azul", bg="blue", fg="white")
etiqueta.pack(expand=True)

ventana.mainloop()