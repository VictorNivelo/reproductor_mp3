from modelo.enums.enum_orden_cancion import Orden_Cancion
from modelo.cancion import Cancion
from typing import List, Dict
from pathlib import Path
from constantes import *


class Biblioteca:

    def __init__(self):
        self.canciones = []
        self.listas_reproduccion = []
        self.artistas = {}
        self.albums = {}
        self.me_gusta = []
        self.favorito = []
        self.cancion_actual = None

    # Método para validar si una canción puede ser agregada
    def validar_cancion_biblioteca(self, ruta: Path) -> bool:
        try:
            # Verificar si el archivo existe
            if not ruta.exists():
                print(f"No se encontró el archivo: {ruta}")
                return False
            # Verificar si el formato es soportado
            if ruta.suffix.lower() not in FORMATOS_SOPORTADOS:
                print(f"Formato no soportado: {ruta.suffix}")
                return False
            # Verificar si la canción ya existe por ruta
            if self.existe_cancion_biblioteca(ruta):
                print(f"La canción ya existe en la biblioteca: {ruta.name}")
                return False
            return True
        except Exception as e:
            print(f"Error al validar canción: {str(e)}")
            return False

    # Verificar si una canción ya existe en la biblioteca
    def existe_cancion_biblioteca(self, ruta: Path) -> bool:
        return any(cancion.ruta_cancion == ruta for cancion in self.canciones)

    # Método para verificar duplicados por metadatos
    def verificar_duplicados_biblioteca(self, cancion: Cancion) -> bool:
        try:
            duplicados = [
                cancion_temporal
                for cancion_temporal in self.canciones
                if cancion_temporal.titulo_cancion.lower() == cancion.titulo_cancion.lower()
                and cancion_temporal.artista_cancion.lower() == cancion.artista_cancion.lower()
                and cancion_temporal.album_cancion.lower() == cancion.album_cancion.lower()
            ]
            if duplicados:
                print(f"Ya existe una canción con el mismo título, artista y álbum: {cancion.titulo_cancion}")
                return True
            return False
        except Exception as e:
            print(f"Error al verificar duplicados: {str(e)}")
            return False

    # Método privado para ordenar automáticamente las canciones
    def ordenar_canciones_automaticamente(self):
        try:
            self.canciones.sort(key=lambda c: c.titulo_cancion.lower())
            # Actualizar y ordenar diccionario de artistas con separación
            self.artistas = {}
            for cancion in self.canciones:
                # Obtener todos los artistas separados de la canción
                artistas_separados = cancion.obtener_todos_artistas_separados
                # Agregar cada artista por separado
                for artista in artistas_separados:
                    artista_limpio = artista.strip()
                    if artista_limpio not in self.artistas:
                        self.artistas[artista_limpio] = []
                    # Solo agregar la canción si no está ya en la lista del artista
                    if cancion not in self.artistas[artista_limpio]:
                        self.artistas[artista_limpio].append(cancion)
            # Ordenar canciones dentro de cada artista
            for artista in self.artistas:
                self.artistas[artista].sort(key=lambda c: c.titulo_cancion.lower())
            # Actualizar y ordenar diccionario de álbumes
            self.albums = {}
            for cancion in self.canciones:
                if cancion.album_cancion not in self.albums:
                    self.albums[cancion.album_cancion] = []
                self.albums[cancion.album_cancion].append(cancion)
            # Ordenar canciones dentro de cada álbum
            for album in self.albums:
                self.albums[album].sort(key=lambda c: c.titulo_cancion.lower())
        except Exception as e:
            print(f"Error al ordenar canciones automáticamente: {str(e)}")

    # Método para agregar una canción a la biblioteca
    def agregar_cancion_biblioteca(self, ruta: Path) -> Cancion | None:
        try:
            # Validar la canción antes de agregar
            if not self.validar_cancion_biblioteca(ruta):
                return None
            # Cargar la canción y agregarla a la biblioteca
            nueva_cancion = Cancion.cargar_cancion(ruta)
            # Verificar duplicados por metadatos
            if self.verificar_duplicados_biblioteca(nueva_cancion):
                return None
            # Agregar la canción a la lista
            self.canciones.append(nueva_cancion)
            # Ordenar automáticamente las canciones
            self.ordenar_canciones_automaticamente()
            print(f"Canción agregada: {nueva_cancion.titulo_cancion} de {nueva_cancion.artista_cancion}")
            return nueva_cancion
        except Exception as e:
            print(f"Error al agregar canción: {str(e)}")
            return None

    # Método para cargar una canción guardada
    def cargar_cancion_guardada_biblioteca(self, ruta: Path) -> Cancion | None:
        try:
            # Verificar si el archivo existe
            if not ruta.exists():
                print(f"No se encontró el archivo: {ruta}")
                return None
            # Verificar si el formato es soportado
            if ruta.suffix.lower() not in FORMATOS_SOPORTADOS:
                print(f"Formato no soportado: {ruta.suffix}")
                return None
            # Cargar la canción directamente sin validaciones de duplicados
            cancion_cargada = Cancion.cargar_cancion(ruta)
            # Agregar la canción a la lista sin verificar duplicados
            self.canciones.append(cancion_cargada)
            print(f"Canción guardada: {cancion_cargada.titulo_cancion} de {cancion_cargada.artista_cancion}")
            return cancion_cargada
        except Exception as e:
            print(f"Error al cargar canción guardada: {str(e)}")
            return None

    # Método para agregar canciones solo de la carpeta actual (sin subcarpetas)
    def agregar_carpeta_canciones_biblioteca(self, ruta: Path) -> List[Cancion]:
        try:
            if not ruta.exists():
                print(f"No se encontró la carpeta: {ruta}")
                return []
            if not ruta.is_dir():
                print(f"La ruta no es una carpeta: {ruta}")
                return []
            canciones_agregadas = []
            # Iterar solo en los archivos de la carpeta actual
            for archivo in ruta.glob("*"):
                if archivo.is_file() and archivo.suffix.lower() in FORMATOS_SOPORTADOS:
                    cancion = self.agregar_cancion_biblioteca(archivo)
                    if cancion:
                        canciones_agregadas.append(cancion)
            # Ordenar automáticamente si se agregaron canciones
            if canciones_agregadas:
                self.ordenar_canciones_automaticamente()
            print(f"Se agregaron {len(canciones_agregadas)} canciones de la carpeta '{ruta.name}'")
            return canciones_agregadas
        except Exception as e:
            print(f"Error al agregar carpeta de canciones: {str(e)}")
            return []

    # Método para agregar canciones de la carpeta y todas sus subcarpetas
    def agregar_carpeta_canciones_recursivo_biblioteca(self, ruta: Path) -> List[Cancion]:
        try:
            if not ruta.exists():
                print(f"No se encontró la carpeta: {ruta}")
                return []
            if not ruta.is_dir():
                print(f"La ruta no es una carpeta: {ruta}")
                return []
            canciones_agregadas = []
            # Usar rglob para buscar recursivamente en todas las subcarpetas
            for archivo in ruta.rglob("*"):
                if archivo.is_file() and archivo.suffix.lower() in FORMATOS_SOPORTADOS:
                    cancion = self.agregar_cancion_biblioteca(archivo)
                    if cancion:
                        canciones_agregadas.append(cancion)
            # Ordenar automáticamente si se agregaron canciones
            if canciones_agregadas:
                self.ordenar_canciones_automaticamente()
            print(
                f"Se agregaron {len(canciones_agregadas)} canciones de la carpeta '{ruta.name}' y sus subcarpetas"
            )
            return canciones_agregadas
        except Exception as e:
            print(f"Error al agregar carpeta de canciones recursivamente: {str(e)}")
            return []

    # Método para eliminar una canción completamente de la biblioteca
    def eliminar_cancion_biblioteca(self, cancion: Cancion):
        try:
            if cancion not in self.canciones:
                print(f"La canción '{cancion.titulo_cancion}' no existe en la biblioteca.")
                return False
            # Desvincular si es la canción actual
            if self.cancion_actual and self.cancion_actual.ruta_cancion == cancion.ruta_cancion:
                self.cancion_actual = None
            # Eliminar de la lista principal de canciones
            self.canciones.remove(cancion)
            # Eliminar de "Me Gusta" si está presente
            if cancion in self.me_gusta:
                self.me_gusta.remove(cancion)
                cancion.me_gusta = False
            # Eliminar de "Favoritos" si está presente
            if cancion in self.favorito:
                self.favorito.remove(cancion)
                cancion.favorito = False
            # Limpiar de diccionarios de artistas
            artistas_a_limpiar = []
            for artista, canciones_artista in self.artistas.items():
                if cancion in canciones_artista:
                    canciones_artista.remove(cancion)
                    # Si el artista no tiene más canciones, marcarlo para eliminación
                    if not canciones_artista:
                        artistas_a_limpiar.append(artista)
            # Eliminar artistas que se quedaron sin canciones
            for artista in artistas_a_limpiar:
                del self.artistas[artista]
            # Limpiar de diccionarios de álbumes
            albums_a_limpiar = []
            for album, canciones_album in self.albums.items():
                if cancion in canciones_album:
                    canciones_album.remove(cancion)
                    # Si el álbum no tiene más canciones, marcarlo para eliminación
                    if not canciones_album:
                        albums_a_limpiar.append(album)
            # Eliminar álbumes que se quedaron sin canciones
            for album in albums_a_limpiar:
                del self.albums[album]
            # Reordenar todas las listas después de la eliminación
            self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
            self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canción '{cancion.titulo_cancion}' eliminada completamente de la biblioteca.")
            return True
        except Exception as e:
            print(f"Error al eliminar canción de la biblioteca: {str(e)}")
            return False

    # Método para eliminar todas las canciones de un álbum de la biblioteca
    def eliminar_album_biblioteca(self, album: str):
        try:
            # Usar el método existente para obtener canciones del álbum
            canciones_album = self.obtener_canciones_de_album_biblioteca(album)
            if not canciones_album:
                print(f"No se encontraron canciones del álbum: {album}")
                return False
            total_eliminadas = 0
            # Crear una copia de la lista para evitar problemas durante la iteración
            canciones_a_eliminar = canciones_album.copy()
            for cancion in canciones_a_eliminar:
                if self.eliminar_cancion_biblioteca(cancion):
                    total_eliminadas += 1
            print(f"Se eliminaron {total_eliminadas} canciones del álbum '{album}'")
            return total_eliminadas > 0
        except Exception as e:
            print(f"Error al eliminar canciones del álbum '{album}': {str(e)}")
            return False

    # Método para eliminar todas las canciones de un artista de la biblioteca
    def eliminar_artista_biblioteca(self, artista: str):
        try:
            # Obtener todas las canciones del artista (incluyendo colaboraciones)
            canciones_artista = self.obtener_canciones_de_artista_biblioteca(artista)
            if not canciones_artista:
                print(f"No se encontraron canciones del artista: {artista}")
                return False
            total_eliminadas = 0
            # Crear una copia de la lista para evitar problemas durante la iteración
            canciones_a_eliminar = canciones_artista.copy()
            for cancion in canciones_a_eliminar:
                if self.eliminar_cancion_biblioteca(cancion):
                    total_eliminadas += 1
            print(f"Se eliminaron {total_eliminadas} canciones del artista '{artista}'")
            return total_eliminadas > 0
        except Exception as e:
            print(f"Error al eliminar canciones del artista '{artista}': {str(e)}")
            return False

    # Método para eliminar todas las canciones de una carpeta de la biblioteca
    def eliminar_carpeta_canciones_biblioteca(self, ruta_carpeta: Path):
        try:
            if not ruta_carpeta.exists():
                print(f"No se encontró la carpeta: {ruta_carpeta}")
                return False
            if not ruta_carpeta.is_dir():
                print(f"La ruta no es una carpeta: {ruta_carpeta}")
                return False
            # Obtener todas las rutas de archivos de audio en la carpeta (recursivamente)
            rutas_archivos_carpeta = []
            for archivo in ruta_carpeta.rglob("*"):
                if archivo.suffix.lower() in FORMATOS_SOPORTADOS:
                    rutas_archivos_carpeta.append(archivo)
            if not rutas_archivos_carpeta:
                print(f"No se encontraron archivos de audio en la carpeta: {ruta_carpeta}")
                return False
            # Encontrar canciones en la biblioteca que estén en esta carpeta
            canciones_a_eliminar = []
            for cancion in self.canciones:
                if cancion.ruta_cancion in rutas_archivos_carpeta:
                    canciones_a_eliminar.append(cancion)
            if not canciones_a_eliminar:
                print(f"No se encontraron canciones de la carpeta '{ruta_carpeta}' en la biblioteca")
                return False
            total_eliminadas = 0
            # Crear una copia de la lista para evitar problemas durante la iteración
            canciones_copia = canciones_a_eliminar.copy()
            for cancion in canciones_copia:
                if self.eliminar_cancion_biblioteca(cancion):
                    total_eliminadas += 1
            print(f"Se eliminaron {total_eliminadas} canciones de la carpeta '{ruta_carpeta}'")
            return total_eliminadas > 0
        except Exception as e:
            print(f"Error al eliminar canciones de la carpeta '{ruta_carpeta}': {str(e)}")
            return False

    # Método para establecer la canción actual
    def establecer_cancion_actual_biblioteca(self, cancion: Cancion | None):
        self.cancion_actual = cancion

    # Método para obtener la canción actual
    def obtener_cancion_actual_biblioteca(self) -> Cancion | None:
        return self.cancion_actual

    # Método para obtener las canciones de la biblioteca
    def obtener_canciones_biblioteca(self) -> List[Cancion]:
        return self.canciones

    # Método para obtener los nombres únicos de las carpetas que contienen canciones
    def obtener_carpetas_biblioteca(self) -> List[str]:
        try:
            carpetas = set()
            for cancion in self.canciones:
                carpeta = cancion.ruta_cancion.parent.name
                carpetas.add(carpeta)
            return sorted(list(carpetas))
        except Exception as e:
            print(f"Error al obtener carpetas: {str(e)}")
            return []

    # Método para obtener los me gusta de la biblioteca
    def obtener_me_gusta_biblioteca(self) -> List[Cancion]:
        return self.me_gusta

    # Método para obtener los favoritos de la biblioteca
    def obtener_favorito_biblioteca(self) -> List[Cancion]:
        return self.favorito

    # Método para obtener los artistas de la biblioteca
    def obtener_artistas_biblioteca(self) -> Dict[str, List[Cancion]]:
        artistas = {}
        for cancion in self.canciones:
            # Obtener todos los artistas separados de la canción
            artistas_separados = cancion.obtener_todos_artistas_separados
            # Agregar cada artista por separado
            for artista in artistas_separados:
                artista_limpio = artista.strip()
                if artista_limpio not in artistas:
                    artistas[artista_limpio] = []
                # Solo agregar la canción si no está ya en la lista del artista
                if cancion not in artistas[artista_limpio]:
                    artistas[artista_limpio].append(cancion)
        # Ordenar las canciones dentro de cada artista
        for artista in artistas:
            artistas[artista].sort(key=lambda c: c.titulo_cancion.lower())
        return artistas

    # Método para obtener los albums de la biblioteca
    def obtener_albums_biblioteca(self) -> Dict[str, List[Cancion]]:
        albums = {}
        for cancion in self.canciones:
            if cancion.album_cancion not in albums:
                albums[cancion.album_cancion] = []
            albums[cancion.album_cancion].append(cancion)
        return albums

    # Método para obtener canciones de un artista
    def obtener_canciones_de_artista_biblioteca(self, artista: str) -> List[Cancion]:
        # Buscar tanto en artista principal como en artistas separados
        canciones_encontradas = []
        for cancion in self.canciones:
            artistas_separados = cancion.obtener_todos_artistas_separados
            if any(artista.lower() == a.strip().lower() for a in artistas_separados):
                canciones_encontradas.append(cancion)
        return canciones_encontradas

    # Método para obtener canciones de un album
    def obtener_canciones_de_album_biblioteca(self, album: str) -> List[Cancion]:
        return [c for c in self.canciones if c.album_cancion.lower() == album.lower()]

    # Método para obtener albums de un artista
    def obtener_albumes_de_artista_biblioteca(self, artista: str) -> List[str]:
        canciones_artista = self.obtener_canciones_de_artista_biblioteca(artista)
        return list({c.album_cancion for c in canciones_artista})

    # Método para obtener información de canciones por carpeta
    def obtener_canciones_por_carpeta_biblioteca(self, ruta_carpeta: Path) -> List[Cancion]:
        try:
            if not ruta_carpeta.exists() or not ruta_carpeta.is_dir():
                return []
            canciones_carpeta = []
            for cancion in self.canciones:
                try:
                    cancion.ruta_cancion.relative_to(ruta_carpeta)
                    canciones_carpeta.append(cancion)
                except ValueError:
                    continue
            return canciones_carpeta
        except Exception as e:
            print(f"Error al obtener canciones de la carpeta: {str(e)}")
            return []

    # Método para agregar una canción a la lista "Me Gusta"
    def agregar_cancion_me_gusta_biblioteca(self, cancion: Cancion):
        try:
            if cancion not in self.canciones:
                print("La canción no existe en la biblioteca.")
                return
            if not cancion.me_gusta and cancion not in self.me_gusta:
                cancion.me_gusta = True
                self.me_gusta.append(cancion)
                self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
                print(f"Canción '{cancion.titulo_cancion}' agregada a 'Me Gusta'")
            else:
                print(f"La canción '{cancion.titulo_cancion}' ya está en 'Me Gusta'")
        except Exception as e:
            print(f"Error al agregar canción a 'Me Gusta': {str(e)}")

    # Método para agregar todas las canciones de un álbum a "Me Gusta"
    def agregar_album_me_gusta_biblioteca(self, album: str):
        try:
            canciones_album = [c for c in self.canciones if c.album_cancion.lower() == album.lower()]
            if not canciones_album:
                print(f"No se encontraron canciones del álbum: {album}")
                return
            for cancion in canciones_album:
                if cancion not in self.me_gusta:
                    self.me_gusta.append(cancion)
                    cancion.me_gusta = True
            # Ordenar automáticamente la lista "Me Gusta"
            self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del álbum '{album}' agregadas a 'Me Gusta'")
        except Exception as e:
            print(f"Error al agregar canciones del álbum a 'Me Gusta': {str(e)}")

    # Método para agregar todas las canciones de un artista a "Me Gusta"
    def agregar_artista_me_gusta_biblioteca(self, artista: str):
        try:
            canciones_artista = [c for c in self.canciones if c.artista_cancion.lower() == artista.lower()]
            if not canciones_artista:
                print(f"No se encontraron canciones del artista: {artista}")
                return
            for cancion in canciones_artista:
                if cancion not in self.me_gusta:
                    self.me_gusta.append(cancion)
                    cancion.me_gusta = True
            # Ordenar automáticamente la lista "Me Gusta"
            self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del artista '{artista}' agregadas a 'Me Gusta'")
        except Exception as e:
            print(f"Error al agregar canciones del artista a 'Me Gusta': {str(e)}")

    # Método para agregar una canción a la lista "Favorito"
    def agregar_cancion_favorito_biblioteca(self, cancion: Cancion):
        try:
            if cancion not in self.canciones:
                print("La canción no existe en la biblioteca.")
                return
            if not cancion.favorito and cancion not in self.favorito:
                cancion.favorito = True
                self.favorito.append(cancion)
                self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
                print(f"Canción '{cancion.titulo_cancion}' agregada a 'Favorito'")
            else:
                print(f"La canción '{cancion.titulo_cancion}' ya está en 'Favorito'")
        except Exception as e:
            print(f"Error al agregar canción a 'Favorito': {str(e)}")

    # Método para agregar todas las canciones de un álbum a "Favorito"
    def agregar_album_favorito_biblioteca(self, album: str):
        try:
            canciones_album = [c for c in self.canciones if c.album_cancion.lower() == album.lower()]
            if not canciones_album:
                print(f"No se encontraron canciones del álbum: {album}")
                return
            for cancion in canciones_album:
                if cancion not in self.favorito:
                    self.favorito.append(cancion)
                    cancion.favorito = True
            # Ordenar automáticamente la lista "Favoritos"
            self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del álbum '{album}' agregadas a 'Favorito'")
        except Exception as e:
            print(f"Error al agregar canciones del álbum a 'Favorito': {str(e)}")

    # Método para agregar todas las canciones de un artista a "Favorito"
    def agregar_artista_favorito_biblioteca(self, artista: str):
        try:
            canciones_artista = [c for c in self.canciones if c.artista_cancion.lower() == artista.lower()]
            if not canciones_artista:
                print(f"No se encontraron canciones del artista: {artista}")
                return
            for cancion in canciones_artista:
                if cancion not in self.favorito:
                    self.favorito.append(cancion)
                    cancion.favorito = True
            # Ordenar automáticamente la lista "Favoritos"
            self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del artista '{artista}' agregadas a 'Favorito'")
        except Exception as e:
            print(f"Error al agregar canciones del artista a 'Favorito': {str(e)}")

    # Método para eliminar una canción de la lista "Me Gusta"
    def eliminar_cancion_me_gusta_biblioteca(self, cancion: Cancion):
        try:
            if cancion in self.me_gusta:
                self.me_gusta.remove(cancion)
                cancion.me_gusta = False
                # Ordenar automáticamente la lista "Me Gusta" después de eliminar
                self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
                print(f"Canción '{cancion.titulo_cancion}' eliminada de 'Me Gusta'")
            else:
                print(f"La canción '{cancion.titulo_cancion}' no está en 'Me Gusta'")
        except Exception as e:
            print(f"Error al eliminar canción de 'Me Gusta': {str(e)}")

    # Método para eliminar todas las canciones de un albúm de "Me Gusta"
    def eliminar_album_me_gusta_biblioteca(self, album: str):
        try:
            canciones_a_eliminar = [c for c in self.me_gusta if c.album_cancion.lower() == album.lower()]
            if not canciones_a_eliminar:
                print(f"No se encontraron canciones del álbum '{album}' en 'Me Gusta'")
                return
            for cancion in canciones_a_eliminar:
                self.me_gusta.remove(cancion)
                cancion.me_gusta = False
                # Ordenar automáticamente la lista "Me Gusta" después de eliminar
                self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del álbum '{album}' eliminadas de 'Me Gusta'")
        except Exception as e:
            print(f"Error al eliminar canciones del álbum de 'Me Gusta': {str(e)}")

    # Método para eliminar todas las canciones de un artista de "Me Gusta"
    def eliminar_artista_me_gusta_biblioteca(self, artista: str):
        try:
            canciones_a_eliminar = [c for c in self.me_gusta if c.artista_cancion.lower() == artista.lower()]
            if not canciones_a_eliminar:
                print(f"No se encontraron canciones del artista '{artista}' en 'Me Gusta'")
                return
            for cancion in canciones_a_eliminar:
                self.me_gusta.remove(cancion)
                cancion.me_gusta = False
                # Ordenar automáticamente la lista "Me Gusta" después de eliminar
                self.me_gusta.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del artista '{artista}' eliminadas de 'Me Gusta'")
        except Exception as e:
            print(f"Error al eliminar canciones del artista de 'Me Gusta': {str(e)}")

    # Método para eliminar una canción de la lista "Favorito"
    def eliminar_cancion_favorito_biblioteca(self, cancion: Cancion):
        try:
            if cancion in self.favorito:
                self.favorito.remove(cancion)
                cancion.favorito = False
                # Ordenar automáticamente la lista "Favoritos" después de eliminar
                self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
                print(f"Canción '{cancion.titulo_cancion}' eliminada de 'Favorito'")
            else:
                print(f"La canción '{cancion.titulo_cancion}' no está en 'Favorito'")
        except Exception as e:
            print(f"Error al eliminar canción de 'Favorito': {str(e)}")

    # Método para eliminar todas las canciones de un albúm de "Favorito"
    def eliminar_album_favorito_biblioteca(self, album: str):
        try:
            canciones_a_eliminar = [c for c in self.favorito if c.album_cancion.lower() == album.lower()]
            if not canciones_a_eliminar:
                print(f"No se encontraron canciones del álbum '{album}' en 'Favorito'")
                return
            for cancion in canciones_a_eliminar:
                self.favorito.remove(cancion)
                cancion.favorito = False
            # Ordenar automáticamente la lista "Favoritos" después de eliminar
            self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del álbum '{album}' eliminadas de 'Favorito'")
        except Exception as e:
            print(f"Error al eliminar canciones del álbum de 'Favorito': {str(e)}")

    # Método para eliminar todas las canciones de un artista de "Favorito"
    def eliminar_artista_favorito_biblioteca(self, artista: str):
        try:
            canciones_a_eliminar = [c for c in self.favorito if c.artista_cancion.lower() == artista.lower()]
            if not canciones_a_eliminar:
                print(f"No se encontraron canciones del artista '{artista}' en 'Favorito'")
                return
            for cancion in canciones_a_eliminar:
                self.favorito.remove(cancion)
                cancion.favorito = False
                # Ordenar automáticamente la lista "Favoritos" después de eliminar
                self.favorito.sort(key=lambda c: c.titulo_cancion.lower())
            print(f"Canciones del artista '{artista}' eliminadas de 'Favorito'")
        except Exception as e:
            print(f"Error al eliminar canciones del artista de 'Favorito': {str(e)}")

    # Método para buscar canciones en la biblioteca
    def buscar_cancion_biblioteca(self, busqueda: str) -> List[Cancion]:
        busqueda_lower = busqueda.lower()
        return [
            c
            for c in self.canciones
            if busqueda_lower in c.titulo_cancion.lower()
            or busqueda_lower in c.artista_cancion.lower()
            or busqueda_lower in c.album_cancion.lower()
        ]

    # Búsqueda avanzada con múltiples criterios
    def buscar_avanzado_biblioteca(
        self, titulo: str = "", artista: str = "", album: str = "", genero: str = "", anio: str = ""
    ) -> List[Cancion]:
        try:
            resultados = self.canciones.copy()
            if titulo:
                resultados = [c for c in resultados if titulo.lower() in c.titulo_cancion.lower()]
            if artista:
                resultados = [c for c in resultados if artista.lower() in c.artista_cancion.lower()]
            if album:
                resultados = [c for c in resultados if album.lower() in c.album_cancion.lower()]
            if genero:
                resultados = [c for c in resultados if genero.lower() in c.genero_cancion.lower()]
            if anio:
                resultados = [c for c in resultados if anio in str(c.anio_lanzamiento_cancion)]
            return resultados
        except Exception as e:
            print(f"Error en búsqueda avanzada: {str(e)}")
            return []

    # Método para ordenar canciones en la biblioteca
    def ordenar_canciones_biblioteca(self, criterio: Orden_Cancion, ascendente: bool = True) -> List[Cancion]:
        try:
            if criterio.es_orden_titulo():
                return sorted(self.canciones, key=lambda c: c.titulo_cancion.lower(), reverse=ascendente)
            elif criterio.es_orden_artista():
                return sorted(self.canciones, key=lambda c: c.artista_cancion.lower(), reverse=ascendente)
            elif criterio.es_orden_album():
                return sorted(self.canciones, key=lambda c: c.album_cancion.lower(), reverse=ascendente)
            elif criterio.es_orden_duracion():
                return sorted(self.canciones, key=lambda c: c.duracion_cancion, reverse=ascendente)
            elif criterio.es_orden_anio():
                return sorted(self.canciones, key=lambda c: c.anio_lanzamiento_cancion, reverse=ascendente)
            elif criterio.es_orden_fecha_agregado():
                return sorted(self.canciones, key=lambda c: c.fecha_agregado_cancion, reverse=ascendente)
            else:
                print(f"Criterio de ordenación no válido: {criterio}")
                return self.canciones
        except Exception as e:
            print(f"Error al ordenar canciones: {str(e)}")
            return self.canciones

    # ==========================================================================================
    # revisar

    # Método para obtener estadísticas de la biblioteca
    def obtener_estadisticas_biblioteca(self) -> Dict[str, int]:
        return {
            "total_canciones": len(self.canciones),
            "total_artistas": len(self.artistas),
            "total_albumes": len(self.albums),
            "me_gusta": len(self.me_gusta),
            "favorito": len(self.favorito),
        }

    # Método para limpiar la biblioteca
    def limpiar_biblioteca(self):
        self.canciones.clear()
        self.artistas.clear()
        self.albums.clear()
        self.me_gusta.clear()
        self.favorito.clear()

    # Método para obtener la carátula de una canción
    def obtener_caratula_album_biblioteca(self, nombre_album, formato="bytes", ancho=None, alto=None):
        if nombre_album in self.albums:
            for cancion in self.albums[nombre_album]:
                if cancion.caratula_cancion:
                    return cancion.obtener_caratula_general_cancion(
                        formato,
                        ancho,
                        alto,
                        bordes_redondeados=True,
                        radio_borde=5,
                        mostrar_calidad=False,
                    )
        return None
