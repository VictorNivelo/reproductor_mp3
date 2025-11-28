import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

# Agregar el directorio src al path para importar módulos
proyecto_root = Path(__file__).parent.parent.parent
src_path = proyecto_root / "src"
sys.path.insert(0, str(src_path))

from controlador.controlador_reproductor_poo import ControladorReproductor
from modelo.cancion import Cancion
from modelo.cola_reproduccion import ColaReproduccion


class InterfazGraficaPrueba:
    def __init__(self):
        # Crear la cola de reproducción primero
        self.cola_reproduccion = ColaReproduccion()
        # Pasar la cola al controlador
        self.controlador = ControladorReproductor(self.cola_reproduccion)
        self.lista_canciones = []
        self.volumen_actual = 50
        self.silenciado = False
        self.volumen_antes_silenciar = 50
        
        # Configurar ventana principal
        self.root = tk.Tk()
        self.root.title("Reproductor MP3 - Interfaz de Prueba")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Variables de tkinter
        self.var_cancion_actual = tk.StringVar(value="Ninguna canción seleccionada")
        self.var_tiempo = tk.StringVar(value="00:00 / 00:00")
        self.var_estado = tk.StringVar(value="DETENIDO")
        self.var_modo_orden = tk.StringVar(value="ORDEN")
        self.var_modo_repeticion = tk.StringVar(value="NO_REPETIR")
        self.var_volumen = tk.IntVar(value=50)
        
        self.crear_interfaz()
        self.iniciar_actualizacion_tiempo()
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === SECCIÓN DE CARGA DE ARCHIVOS ===
        archivo_frame = ttk.LabelFrame(main_frame, text="Cargar Canciones", padding=10)
        archivo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(archivo_frame, text="Cargar Directorio", 
                  command=self.cargar_directorio).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(archivo_frame, text="Agregar Archivo", 
                  command=self.agregar_archivo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(archivo_frame, text="Limpiar Lista", 
                  command=self.limpiar_lista).pack(side=tk.LEFT)
        
        # === SECCIÓN DE LISTA DE CANCIONES ===
        lista_frame = ttk.LabelFrame(main_frame, text="Lista de Canciones", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Listbox con scrollbar
        list_container = ttk.Frame(lista_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_canciones = tk.Listbox(
            list_container, 
            yscrollcommand=scrollbar.set,
            bg='#404040',
            fg='white',
            selectbackground='#0078d4',
            font=('Arial', 10)
        )
        self.listbox_canciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_canciones.yview)
        
        # Doble clic para reproducir
        self.listbox_canciones.bind('<Double-1>', self.reproducir_seleccionada)
        
        # === SECCIÓN DE INFORMACIÓN ACTUAL ===
        info_frame = ttk.LabelFrame(main_frame, text="Información Actual", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="Canción:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.var_cancion_actual, 
                 foreground='blue').grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Tiempo:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.var_tiempo).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Estado:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        ttk.Label(info_frame, textvariable=self.var_estado, 
                 foreground='green').grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(info_frame, text="Orden:").grid(row=1, column=2, sticky=tk.W, padx=(20, 5))
        ttk.Label(info_frame, textvariable=self.var_modo_orden).grid(row=1, column=3, sticky=tk.W)
        
        ttk.Label(info_frame, text="Repetición:").grid(row=0, column=4, sticky=tk.W, padx=(20, 5))
        ttk.Label(info_frame, textvariable=self.var_modo_repeticion).grid(row=0, column=5, sticky=tk.W)
        
        # === SECCIÓN DE CONTROLES ===
        controles_frame = ttk.LabelFrame(main_frame, text="Controles de Reproducción", padding=10)
        controles_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones principales
        botones_frame = ttk.Frame(controles_frame)
        botones_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(botones_frame, text="▶ Reproducir", 
                  command=self.reproducir_seleccionada).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(botones_frame, text="⏸ Pausar", 
                  command=self.pausar).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(botones_frame, text="⏹ Detener", 
                  command=self.detener).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(botones_frame, text="🔄 Reiniciar", 
                  command=self.reiniciar).pack(side=tk.LEFT, padx=(0, 5))
        
        # Navegación
        nav_frame = ttk.Frame(controles_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="⏮ Anterior", 
                  command=self.cancion_anterior).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏭ Siguiente", 
                  command=self.cancion_siguiente).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏪ -10s", 
                  command=self.retroceder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="⏩ +10s", 
                  command=self.adelantar).pack(side=tk.LEFT, padx=(0, 5))
        
        # === SECCIÓN DE VOLUMEN ===
        volumen_frame = ttk.LabelFrame(main_frame, text="Control de Volumen", padding=10)
        volumen_frame.pack(fill=tk.X, pady=(0, 10))
        
        vol_container = ttk.Frame(volumen_frame)
        vol_container.pack(fill=tk.X)
        
        ttk.Label(vol_container, text="Volumen:").pack(side=tk.LEFT)
        
        self.scale_volumen = ttk.Scale(
            vol_container, 
            from_=0, 
            to=100, 
            variable=self.var_volumen,
            command=self.cambiar_volumen
        )
        self.scale_volumen.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.label_volumen = ttk.Label(vol_container, text="50%")
        self.label_volumen.pack(side=tk.RIGHT)
        
        ttk.Button(vol_container, text="🔇 Silenciar", 
                  command=self.toggle_silenciar).pack(side=tk.RIGHT, padx=(0, 10))
        
        # === SECCIÓN DE MODOS ===
        modos_frame = ttk.LabelFrame(main_frame, text="Modos de Reproducción", padding=10)
        modos_frame.pack(fill=tk.X)
        
        ttk.Button(modos_frame, text="Cambiar Orden", 
                  command=self.cambiar_orden).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(modos_frame, text="Cambiar Repetición", 
                  command=self.cambiar_repeticion).pack(side=tk.LEFT)
    
    def crear_cancion_desde_archivo(self, archivo_path):
        """Crea un objeto Cancion desde un archivo, manejando diferentes firmas del constructor"""
        try:
            # Intentar diferentes formas de crear la canción
            # Primero con los nombres más comunes
            try:
                return Cancion(
                    titulo=archivo_path.stem,
                    ruta=archivo_path,
                    duracion=180
                )
            except TypeError:
                pass
            
            # Probar con otros nombres posibles
            try:
                return Cancion(
                    nombre=archivo_path.stem,
                    archivo=archivo_path,
                    duracion=180
                )
            except TypeError:
                pass
            
            # Probar solo con la ruta
            try:
                return Cancion(str(archivo_path))
            except TypeError:
                pass
            
            # Probar con Path
            try:
                return Cancion(archivo_path)
            except TypeError:
                pass
            
            # Si todo falla, crear con parámetros por defecto
            return Cancion()
            
        except Exception as e:
            print(f"Error al crear canción: {e}")
            return None
    
    def obtener_titulo_cancion(self, cancion):
        """Obtiene el título de una canción, manejando diferentes atributos"""
        if hasattr(cancion, 'titulo_cancion'):
            return cancion.titulo_cancion
        elif hasattr(cancion, 'titulo'):
            return cancion.titulo
        elif hasattr(cancion, 'nombre'):
            return cancion.nombre
        elif hasattr(cancion, 'ruta_cancion'):
            return Path(cancion.ruta_cancion).stem
        elif hasattr(cancion, 'ruta'):
            return Path(cancion.ruta).stem
        elif hasattr(cancion, 'archivo'):
            return Path(cancion.archivo).stem
        else:
            return "Canción sin título"
    
    def obtener_duracion_cancion(self, cancion):
        """Obtiene la duración de una canción, manejando diferentes atributos"""
        if hasattr(cancion, 'duracion_cancion'):
            return cancion.duracion_cancion
        elif hasattr(cancion, 'duracion'):
            return cancion.duracion
        else:
            return 180  # Duración por defecto
        
    def cargar_directorio(self):
        """Cargar canciones desde un directorio"""
        directorio = filedialog.askdirectory(title="Seleccionar directorio con música")
        if directorio:
            try:
                directorio_path = Path(directorio)
                extensiones_audio = ['.mp3', '.wav', '.ogg', '.flac']
                archivos_audio = []
                
                for ext in extensiones_audio:
                    archivos_audio.extend(directorio_path.glob(f'*{ext}'))
                
                canciones_cargadas = 0
                for archivo in archivos_audio:
                    try:
                        cancion = self.crear_cancion_desde_archivo(archivo)
                        if cancion:
                            self.lista_canciones.append(cancion)
                            titulo = self.obtener_titulo_cancion(cancion)
                            self.listbox_canciones.insert(tk.END, titulo)
                            canciones_cargadas += 1
                    except Exception as e:
                        print(f"Error al cargar {archivo}: {e}")
                
                messagebox.showinfo("Éxito", f"Se cargaron {canciones_cargadas} canciones")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar directorio: {e}")
    
    def agregar_archivo(self):
        """Agregar un archivo individual"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos de audio", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3", "*.mp3"),
                ("WAV", "*.wav"),
                ("OGG", "*.ogg"),
                ("FLAC", "*.flac"),
                ("Todos los archivos", "*.*")
            ]
        )
        if archivo:
            try:
                archivo_path = Path(archivo)
                cancion = self.crear_cancion_desde_archivo(archivo_path)
                if cancion:
                    self.lista_canciones.append(cancion)
                    titulo = self.obtener_titulo_cancion(cancion)
                    self.listbox_canciones.insert(tk.END, titulo)
                    messagebox.showinfo("Éxito", f"Canción '{titulo}' agregada")
                else:
                    messagebox.showerror("Error", "No se pudo crear el objeto canción")
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar archivo: {e}")
    
    def limpiar_lista(self):
        """Limpiar la lista de canciones"""
        if messagebox.askyesno("Confirmar", "¿Limpiar toda la lista de canciones?"):
            self.detener()
            self.lista_canciones.clear()
            self.listbox_canciones.delete(0, tk.END)
            self.var_cancion_actual.set("Ninguna canción seleccionada")
    
    def reproducir_seleccionada(self, event=None):
        """Reproducir la canción seleccionada"""
        seleccion = self.listbox_canciones.curselection()
        if seleccion and self.lista_canciones:
            indice = seleccion[0]
            cancion = self.lista_canciones[indice]
            try:
                self.controlador.reproducir(cancion)
                titulo = self.obtener_titulo_cancion(cancion)
                self.var_cancion_actual.set(titulo)
                self.actualizar_listbox_actual()
            except Exception as e:
                messagebox.showerror("Error", f"Error al reproducir: {e}")
    
    def pausar(self):
        """Pausar la reproducción"""
        self.controlador.pausar()
    
    def detener(self):
        """Detener la reproducción"""
        self.controlador.detener()
        self.actualizar_listbox_actual()
    
    def reiniciar(self):
        """Reiniciar la canción actual"""
        self.controlador.reiniciar()
    
    def cancion_anterior(self):
        """Reproducir canción anterior"""
        self.controlador.reproducir_anterior()
        if self.controlador.cancion_actual:
            titulo = self.obtener_titulo_cancion(self.controlador.cancion_actual)
            self.var_cancion_actual.set(titulo)
            self.actualizar_listbox_actual()
    
    def cancion_siguiente(self):
        """Reproducir canción siguiente"""
        self.controlador.reproducir_siguiente()
        if self.controlador.cancion_actual:
            titulo = self.obtener_titulo_cancion(self.controlador.cancion_actual)
            self.var_cancion_actual.set(titulo)
            self.actualizar_listbox_actual()
    
    def retroceder(self):
        """Retroceder 10 segundos"""
        self.controlador.retroceder()
    
    def adelantar(self):
        """Adelantar 10 segundos"""
        self.controlador.adelantar()
    
    def cambiar_volumen(self, valor):
        """Cambiar el volumen"""
        volumen = int(float(valor))
        self.volumen_actual = volumen
        self.controlador.ajustar_volumen(volumen)
        self.label_volumen.config(text=f"{volumen}%")
        
        if volumen > 0 and self.silenciado:
            self.silenciado = False
    
    def toggle_silenciar(self):
        """Alternar silencio"""
        if self.silenciado:
            # Quitar silencio
            self.controlador.quitar_silencio(self.volumen_antes_silenciar)
            self.var_volumen.set(self.volumen_antes_silenciar)
            self.volumen_actual = self.volumen_antes_silenciar
            self.silenciado = False
        else:
            # Silenciar
            self.volumen_antes_silenciar = self.volumen_actual
            self.controlador.silenciar()
            self.silenciado = True
    
    def cambiar_orden(self):
        """Cambiar modo de orden"""
        self.controlador.cambiar_modo_orden()
        self.var_modo_orden.set(self.controlador.modo_orden.value)
    
    def cambiar_repeticion(self):
        """Cambiar modo de repetición"""
        self.controlador.cambiar_modo_repeticion()
        self.var_modo_repeticion.set(self.controlador.modo_repeticion.value)
    
    def actualizar_listbox_actual(self):
        """Actualizar la visualización de la canción actual en la lista"""
        # Limpiar todas las selecciones
        self.listbox_canciones.selection_clear(0, tk.END)
        
        # Marcar la canción actual
        if self.controlador.cancion_actual and self.lista_canciones:
            try:
                indice = self.lista_canciones.index(self.controlador.cancion_actual)
                self.listbox_canciones.selection_set(indice)
                self.listbox_canciones.see(indice)
            except ValueError:
                pass  # La canción actual no está en la lista
    
    def actualizar_tiempo(self):
        """Actualizar la información de tiempo y estado"""
        try:
            # Actualizar estado
            self.var_estado.set(self.controlador.estado_reproduccion.value)
            
            # Actualizar tiempo
            if self.controlador.cancion_actual:
                tiempo_actual = self.controlador.obtener_tiempo_actual()
                duracion = self.obtener_duracion_cancion(self.controlador.cancion_actual)
                
                min_actual, seg_actual = divmod(int(tiempo_actual), 60)
                min_total, seg_total = divmod(int(duracion), 60)
                
                tiempo_str = f"{min_actual:02d}:{seg_actual:02d} / {min_total:02d}:{seg_total:02d}"
                self.var_tiempo.set(tiempo_str)
            else:
                self.var_tiempo.set("00:00 / 00:00")
                
        except Exception as e:
            print(f"Error al actualizar tiempo: {e}")
    
    def iniciar_actualizacion_tiempo(self):
        """Iniciar el hilo de actualización de tiempo"""
        def actualizar():
            while True:
                try:
                    self.root.after(0, self.actualizar_tiempo)
                    time.sleep(1)
                except:
                    break
        
        hilo_tiempo = threading.Thread(target=actualizar, daemon=True)
        hilo_tiempo.start()
    
    def ejecutar(self):
        """Ejecutar la interfaz"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Manejar el cierre de la ventana"""
        try:
            self.controlador.detener()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    try:
        interfaz = InterfazGraficaPrueba()
        interfaz.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la interfaz: {e}")
        messagebox.showerror("Error", f"Error al iniciar la interfaz: {e}")