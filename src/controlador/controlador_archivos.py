from datetime import datetime
from pathlib import Path
from constantes import *
import json
import os


class ControladorArchivos:
    def __init__(self):
        # Directorios base
        self.ruta_carpeta_datos = RUTA_CARPETA_DATOS
        self.ruta_carpeta_listas = RUTA_CARPETA_LISTAS
        self.ruta_carpeta_me_gusta = RUTA_CARPETA_ME_GUSTA
        self.ruta_carpeta_favoritos = RUTA_CARPETA_FAVORITOS
        self.ruta_carpeta_estadisticas = RUTA_CARPETA_ESTADISTICAS
        self.ruta_carpeta_configuracion = RUTA_CARPETA_CONFIGURACION
        # Rutas de archivos
        self.ruta_canciones = RUTA_CANCIONES
        self.ruta_favoritos = RUTA_FAVORITOS
        self.ruta_me_gusta = RUTA_ME_GUSTA
        self.ruta_reproduccion = RUTA_REPRODUCCION
        self.ruta_configuracion = RUTA_CONFIGURACION
        self.ruta_cola = RUTA_COLA
        # Crear la estructura de directorios
        self.crear_estructura_directorios()

    # Verificar y crear un archivo JSON con estructura predeterminada
    @staticmethod
    def verificar_archivo_json(ruta, estructura_predeterminada):
        try:
            # Verificar si el directorio existe
            directorio = os.path.dirname(ruta)
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            # Si el archivo no existe o está vacío, crear la estructura básica
            if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
                contenido = json.dumps(estructura_predeterminada, ensure_ascii=False, indent=4)
                with open(ruta, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)
            # Intentar cargar el archivo para verificar que es JSON válido
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:
                    json.load(archivo)
            except json.JSONDecodeError:
                # Sí hay un error al decodificar, sobrescribir con la estructura predeterminada
                contenido = json.dumps(estructura_predeterminada, ensure_ascii=False, indent=4)
                with open(ruta, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)
        except Exception as e:
            print(f"Error al verificar/crear archivo JSON {ruta}: {e}")

    # Crear la estructura de directorios necesaria
    def crear_estructura_directorios(self):
        directorios = [
            self.ruta_carpeta_datos,
            self.ruta_carpeta_estadisticas,
            self.ruta_carpeta_listas,
            self.ruta_carpeta_me_gusta,
            self.ruta_carpeta_favoritos,
            self.ruta_carpeta_configuracion,
        ]
        for directorio in directorios:
            if not os.path.exists(directorio):
                os.makedirs(directorio)

    # Guardar la biblioteca en archivos JSON
    def guardar_biblioteca_json_controlador(self, biblioteca, reproductor=None):
        try:
            # Guardar todas las canciones
            self.guardar_cancion_json_controlador(biblioteca)
            # Guardar listas especiales
            self.guardar_me_gusta_json_controlador(biblioteca)
            self.guardar_favorito_json_controlador(biblioteca)
            # Guardar la cola de reproducción si se proporciona el reproductor
            if reproductor is not None:
                self.guardar_cola_reproduccion_json_controlador(reproductor)
            return True
        except Exception as e:
            print(f"Error al guardar biblioteca: {str(e)}")
            return False

    # Guardar las canciones en un archivo JSON
    def guardar_cancion_json_controlador(self, biblioteca):
        datos = {
            "estadisticas": biblioteca.obtener_estadisticas_biblioteca(),
            "canciones": [cancion.convertir_diccionario_cancion() for cancion in biblioteca.canciones],
        }
        contenido = json.dumps(datos, ensure_ascii=False, indent=4)
        with open(self.ruta_canciones, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    # Guardar la cola de reproducción en un archivo JSON
    def guardar_cola_reproduccion_json_controlador(self, reproductor):
        try:
            if not reproductor.lista_reproduccion:
                # Si la cola está vacía, crear un JSON con lista vacía
                datos_cola = {"indice_actual": -1, "canciones": [], "ultima_cancion": None}
            else:
                # Guardar la lista de reproducción con el índice actual y la última canción
                ultima_cancion_info = None
                if 0 <= reproductor.indice_actual < len(reproductor.lista_reproduccion):
                    cancion_actual = reproductor.lista_reproduccion[reproductor.indice_actual]
                    ultima_cancion_info = {
                        "ruta": str(cancion_actual.ruta_cancion),
                        "titulo": cancion_actual.titulo_cancion,
                        "artista": cancion_actual.artista,
                        "album": cancion_actual.album,
                        "timestamp": datetime.now().isoformat(),
                    }
                # Modificación: Guardar las rutas y las posiciones en la cola
                canciones_en_cola = []
                for cancion in reproductor.lista_reproduccion:
                    canciones_en_cola.append(str(cancion.ruta_cancion))
                datos_cola = {
                    "indice_actual": reproductor.indice_actual,
                    "canciones": canciones_en_cola,
                    "ultima_cancion": ultima_cancion_info,
                }
            contenido = json.dumps(datos_cola, ensure_ascii=False, indent=4)
            with open(self.ruta_cola, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"Error al guardar la cola de reproducción: {str(e)}")
            return False

    # Guardar la lista de me gusta en un archivo JSON
    def guardar_me_gusta_json_controlador(self, biblioteca):
        datos = {"me_gusta": [cancion.convertir_diccionario_cancion() for cancion in biblioteca.me_gusta]}
        contenido = json.dumps(datos, ensure_ascii=False, indent=4)
        with open(self.ruta_me_gusta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    # Guardar la lista de favoritos en un archivo JSON
    def guardar_favorito_json_controlador(self, biblioteca):
        datos = {"favoritos": [cancion.convertir_diccionario_cancion() for cancion in biblioteca.favorito]}
        contenido = json.dumps(datos, ensure_ascii=False, indent=4)
        with open(self.ruta_favoritos, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    # Cargar la biblioteca desde los archivos JSON
    def cargar_biblioteca_json_controlador(self, biblioteca):
        # Estructuras predeterminadas
        estructura_canciones = {
            "estadisticas": {
                "total_canciones": 0,
                "total_artistas": 0,
                "total_albumes": 0,
                "me_gusta": 0,
                "favorito": 0,
            },
            "canciones": [],
        }
        estructura_me_gusta = {"me_gusta": []}
        estructura_favoritos = {"favoritos": []}
        # Verificar y preparar archivos
        self.verificar_archivo_json(self.ruta_canciones, estructura_canciones)
        self.verificar_archivo_json(self.ruta_me_gusta, estructura_me_gusta)
        self.verificar_archivo_json(self.ruta_favoritos, estructura_favoritos)
        try:
            # Limpiar la biblioteca actual
            biblioteca.limpiar_biblioteca()
            # Cargar las canciones principales
            canciones_cargadas = self.cargar_cancion_json_controlador(biblioteca)
            # Actualizar estado me gusta y favoritos
            self.actualizar_estados_listas_json_controlador(biblioteca)
            # print(f"Se cargaron {canciones_cargadas} canciones)
            return canciones_cargadas > 0
        except Exception as e:
            print(f"Error al cargar la biblioteca: {str(e)}")
            return False

    # Cargar las canciones desde un archivo JSON
    def cargar_cancion_json_controlador(self, biblioteca):
        canciones_cargadas = 0
        with open(self.ruta_canciones, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for cancion_dict in datos.get("canciones", []):
            try:
                ruta_cancion = Path(cancion_dict.get("ruta"))
                if ruta_cancion.exists():
                    cancion = biblioteca.agregar_cancion_biblioteca(ruta_cancion)
                    if cancion:
                        canciones_cargadas += 1
                else:
                    print(f"No se encontró el archivo: {ruta_cancion}")
            except Exception as e:
                print(f"Error al cargar canción: {str(e)}")
        # Ordenar todas las colecciones después de cargar
        biblioteca.ordenar_canciones_biblioteca()
        return canciones_cargadas

    # Cargar la cola de reproducción desde un archivo JSON
    def cargar_cola_reproduccion_json_controlador(self, reproductor, biblioteca):
        estructura_cola = {"indice_actual": -1, "canciones": [], "ultima_cancion": None}
        # Verificar archivo de cola
        self.verificar_archivo_json(self.ruta_cola, estructura_cola)
        try:
            with open(self.ruta_cola, "r", encoding="utf-8") as archivo:
                datos_cola = json.load(archivo)
            # Limpiar la cola actual
            reproductor.lista_reproduccion = []
            reproductor.indice_actual = -1
            # Guardar información de la última canción reproducida
            reproductor.ultima_cancion = datos_cola.get("ultima_cancion")
            # Si no hay canciones en el archivo, salir
            if not datos_cola["canciones"]:
                return True
            # Modificación: Reconstruir la lista de reproducción permitiendo duplicados
            lista_reconstruida = []
            for ruta_str in datos_cola["canciones"]:
                ruta = Path(ruta_str)
                # Buscar la canción en la biblioteca
                for cancion in biblioteca.canciones:
                    if cancion.ruta_cancion == ruta:
                        # Añadir la canción a la lista aunque ya esté presente
                        lista_reconstruida.append(cancion)
                        break
            # Establecer la lista reconstruida y el índice actual
            if lista_reconstruida:
                reproductor.lista_reproduccion = lista_reconstruida
                # Asegurarse que el índice esté dentro de los límites
                indice = datos_cola["indice_actual"]
                if 0 <= indice < len(lista_reconstruida):
                    reproductor.indice_actual = indice
                else:
                    reproductor.indice_actual = 0
            return True
        except Exception as e:
            print(f"Error al cargar la cola de reproducción: {str(e)}")
            return False

    # Método para obtener la última canción reproducida con verificación adicional
    def ultima_reproducida_json_controlador(self):
        estructura_reproduccion = {
            "artistas": {},
            "albumes": {},
            "tiempo_total": 0.0,
            "canciones_escuchadas": 0,
            "ultima_cancion": None,
            "canciones": {},
        }
        # Verificar archivo de estadísticas
        self.verificar_archivo_json(self.ruta_reproduccion, estructura_reproduccion)
        try:
            with open(self.ruta_reproduccion, "r", encoding="utf-8") as archivo:
                estadisticas = json.load(archivo)
            ultima_cancion = estadisticas.get("ultima_cancion")
            if ultima_cancion and "ruta" in ultima_cancion:
                # Verificar que el archivo existe
                ruta_cancion = Path(ultima_cancion["ruta"])
                if ruta_cancion.exists():
                    return ultima_cancion
                else:
                    print(f"El archivo de la última canción no existe: {ruta_cancion}")
            return None
        except Exception as e:
            print(f"Error al obtener la última canción reproducida: {str(e)}")
            return None

    # Actualizar los estados me gusta y favoritos desde los archivos JSON
    def actualizar_estados_listas_json_controlador(self, biblioteca):
        try:
            # Actualizar me gusta
            if os.path.exists(self.ruta_me_gusta):
                with open(self.ruta_me_gusta, "r", encoding="utf-8") as archivo:
                    datos_me_gusta = json.load(archivo)
                for cancion_dict in datos_me_gusta.get("me_gusta", []):
                    try:
                        ruta = Path(cancion_dict.get("ruta"))
                        for cancion in biblioteca.canciones:
                            if cancion.ruta_cancion == ruta:
                                biblioteca.agregar_me_gusta_biblioteca(cancion)
                                break
                    except Exception as e:
                        print(f"Error al actualizar me gusta: {str(e)}")
            # Actualizar favoritos
            if os.path.exists(self.ruta_favoritos):
                with open(self.ruta_favoritos, "r", encoding="utf-8") as archivo:
                    datos_favoritos = json.load(archivo)
                for cancion_dict in datos_favoritos.get("favoritos", []):
                    try:
                        ruta = Path(cancion_dict.get("ruta"))
                        for cancion in biblioteca.canciones:
                            if cancion.ruta_cancion == ruta:
                                biblioteca.agregar_favorito_biblioteca(cancion)
                                break
                    except Exception as e:
                        print(f"Error al actualizar favoritos: {str(e)}")
        except Exception as e:
            print(f"Error al actualizar estados: {str(e)}")

    # Guardar la lista de me gusta en un archivo JSON
    def registrar_reproduccion_json_controlador(self, cancion):
        estructura_reproduccion = {
            "artistas": {},
            "albumes": {},
            "tiempo_total": 0.0,
            "canciones_escuchadas": 0,
            "ultima_cancion": None,
            "canciones": {},
        }
        # Verificar archivo de estadísticas de reproducción
        self.verificar_archivo_json(self.ruta_reproduccion, estructura_reproduccion)
        try:
            # Cargar las estadísticas actuales
            with open(self.ruta_reproduccion, "r", encoding="utf-8") as archivo:
                estadisticas = json.load(archivo)
            # Actualizar estadísticas generales
            estadisticas["tiempo_total"] += cancion.duracion
            estadisticas["canciones_escuchadas"] += 1
            # Registrar última canción reproducida
            estadisticas["ultima_cancion"] = {
                "ruta": str(cancion.ruta_cancion),
                "titulo": cancion.titulo_cancion,
                "artista": cancion.artista,
                "album": cancion.album,
                "timestamp": datetime.now().isoformat(),
            }
            # Actualizar contador de la canción
            ruta_str = str(cancion.ruta_cancion)
            if ruta_str not in estadisticas["canciones"]:
                estadisticas["canciones"][ruta_str] = {
                    "contador": 0,
                    "titulo": cancion.titulo_cancion,
                    "artista": cancion.artista,
                    "album": cancion.album,
                }
            estadisticas["canciones"][ruta_str]["contador"] += 1
            # Actualizar contador del artista
            if cancion.artista not in estadisticas["artistas"]:
                estadisticas["artistas"][cancion.artista] = 0
            estadisticas["artistas"][cancion.artista] += 1
            # Actualizar contador del álbum
            if cancion.album not in estadisticas["albumes"]:
                estadisticas["albumes"][cancion.album] = 0
            estadisticas["albumes"][cancion.album] += 1
            # Guardar las estadísticas
            contenido = json.dumps(estadisticas, ensure_ascii=False, indent=4)
            with open(self.ruta_reproduccion, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"Error al registrar reproducción: {str(e)}")
            return False

    # Guardar los atajos en un archivo JSON
    @staticmethod
    def guardar_atajos_json_controlador(atajos):
        try:
            # Asegurarse de que exista el directorio
            directorio = os.path.dirname(RUTA_ATAJOS)
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            # Guardar los atajos
            contenido = json.dumps(atajos, ensure_ascii=False, indent=4)
            with open(RUTA_ATAJOS, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"Error al guardar los atajos: {str(e)}")
            return False

    # Cargar los atajos desde un archivo JSON
    def cargar_atajos_json_controlador(self):
        # Estructura con atajos predeterminados
        atajos_por_defecto = {
            "reproducir_pausar": "space",
            "siguiente": "Control-Right",
            "anterior": "Control-Left",
            "aumentar_volumen": "Up",
            "disminuir_volumen": "Down",
            "silenciar": "m",
            "modo_aleatorio": "s",
            "repeticion": "r",
            "visibilidad_panel": "l",
            "me_gusta": "g",
            "favorito": "f",
            "cola": "c",
            "mini_reproductor": "p",
            "adelantar": "Right",
            "retroceder": "Left",
        }
        try:
            # Verificar que exista el archivo
            self.verificar_archivo_json(RUTA_ATAJOS, atajos_por_defecto)
            # Cargar los atajos
            with open(RUTA_ATAJOS, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error al cargar los atajos: {str(e)}")
            return atajos_por_defecto

    # Obtener las estadísticas de reproducción
    def obtener_estadisticas_json_controlador(self):
        estructura_reproduccion = {
            "tiempo_total": 0.0,
            "canciones_escuchadas": 0,
            "artistas": {},
            "albumes": {},
            "ultima_cancion": None,
            "canciones": {},
        }
        # Verificar archivo de estadísticas
        self.verificar_archivo_json(self.ruta_reproduccion, estructura_reproduccion)
        try:
            with open(self.ruta_reproduccion, "r", encoding="utf-8") as archivo:
                estadisticas = json.load(archivo)
            # Convertir tiempo total a formato legible
            tiempo_total = estadisticas["tiempo_total"]
            horas = int(tiempo_total // 3600)
            minutos = int((tiempo_total % 3600) // 60)
            segundos = int(tiempo_total % 60)
            tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            # Encontrar la canción más reproducida
            cancion_mas_reproducida = None
            reproducciones_max = 0
            for ruta, datos in estadisticas["canciones"].items():
                if datos["contador"] > reproducciones_max:
                    reproducciones_max = datos["contador"]
                    cancion_mas_reproducida = {
                        "titulo": datos["titulo"],
                        "artista": datos["artista"],
                        "album": datos["album"],
                        "reproducciones": datos["contador"],
                    }
            # Encontrar el artista más escuchado
            artista_mas_escuchado = None
            max_artista = 0
            for artista, contador in estadisticas["artistas"].items():
                if contador > max_artista:
                    max_artista = contador
                    artista_mas_escuchado = {"nombre": artista, "reproducciones": contador}
            # Encontrar el álbum más escuchado
            album_mas_escuchado = None
            max_album = 0
            for album, contador in estadisticas["albumes"].items():
                if contador > max_album:
                    max_album = contador
                    album_mas_escuchado = {"nombre": album, "reproducciones": contador}
            # Compilar resumen de estadísticas
            resumen = {
                "tiempo_total_reproduccion": tiempo_formateado,
                "canciones_escuchadas": estadisticas["canciones_escuchadas"],
                "cancion_mas_reproducida": cancion_mas_reproducida,
                "artista_mas_escuchado": artista_mas_escuchado,
                "album_mas_escuchado": album_mas_escuchado,
                "ultima_cancion": estadisticas["ultima_cancion"],
            }
            return resumen
        except Exception as e:
            print(f"Error al obtener estadísticas de reproducción: {str(e)}")
            return None

    # Guardar la configuración en un archivo JSON
    def guardar_ajustes_json_controlador(self, configuracion):
        try:
            # Asegurarse de que exista el directorio
            if not os.path.exists(self.ruta_carpeta_configuracion):
                os.makedirs(self.ruta_carpeta_configuracion)
            # Crear o actualizar el archivo de configuración
            if os.path.exists(self.ruta_configuracion):
                # Sí existe, cargar la configuración actual y actualizar
                try:
                    with open(self.ruta_configuracion, "r", encoding="utf-8") as archivo:
                        datos = json.load(archivo)
                        # Actualizar todos los valores proporcionados
                        for clave, valor in configuracion.items():
                            datos[clave] = valor
                        configuracion = datos
                except Exception as e:
                    print(f"Error al leer la configuración existente: {str(e)}")
            # Guardar la configuración
            contenido = json.dumps(configuracion, ensure_ascii=False, indent=4)
            with open(self.ruta_configuracion, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")
            return False

    # Cargar la configuración desde un archivo JSON
    def cargar_ajustes_json_controlador(self):
        # Estructura predeterminada con valores por defecto
        configuracion_por_defecto = {
            "apariencia": "claro",
            "nivel_volumen": 100,
            "modo_aleatorio": False,
            "modo_repeticion": 0,
            "estado_silenciado": False,
            "panel_lateral_visible": True,
        }
        try:
            # Verificar que exista el archivo
            self.verificar_archivo_json(self.ruta_configuracion, configuracion_por_defecto)
            # Cargar la configuración
            with open(self.ruta_configuracion, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
            return configuracion_por_defecto
