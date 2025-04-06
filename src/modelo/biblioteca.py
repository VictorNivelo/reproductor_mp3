from modelo.cancion import Cancion
from typing import List, Dict
from pathlib import Path
from constantes import *


class Biblioteca:
    def __init__(self):
        self.canciones = []
        self.por_titulo = {}
        self.por_artista = {}
        self.por_album = {}
        self.me_gusta = []
        self.favorito = []

    # Verificar si una canción ya existe en la biblioteca
    def existe_cancion(self, ruta: Path) -> bool:
        return any(cancion.ruta_cancion == ruta for cancion in self.canciones)

    # Método adicional para detectar posibles duplicados (mismo título y artista)
    def detectar_duplicado(self, ruta: Path) -> list:
        try:
            # Crear una canción temporal para extraer metadatos
            cancion_temp = Cancion.desde_archivo(ruta)
            # Buscar canciones con el mismo título y artista
            duplicados = [
                cancion
                for cancion in self.canciones
                if cancion.titulo_cancion.lower() == cancion_temp.titulo_cancion.lower()
                and cancion.artista.lower() == cancion_temp.artista.lower()
            ]
            return duplicados
        except Exception as e:
            print(f"Error al detectar duplicado: {str(e)}")
            return []

    # Metodo para agregar una canción a la biblioteca
    def agregar_cancion(self, ruta: Path) -> Cancion | None:
        try:
            # Verificar si el archivo existe
            if not ruta.exists():
                print(f"No se encontró el archivo: {ruta}")
                return None
            # Verificar si el formato es soportado
            if ruta.suffix.lower() not in FORMATOS_SOPORTADOS:
                print(f"Formato no soportado: {ruta.suffix}")
                return None
            # Verificar si la canción ya existe por ruta
            if self.existe_cancion(ruta):
                print(f"La canción ya existe en la biblioteca: {ruta.name}")
                return None
            # Crear canción temporal para verificar duplicados por metadatos
            cancion_temp = Cancion.desde_archivo(ruta)
            duplicados = [
                cancion
                for cancion in self.canciones
                if cancion.titulo_cancion.lower() == cancion_temp.titulo_cancion.lower()
                and cancion.artista.lower() == cancion_temp.artista.lower()
                and cancion.album.lower() == cancion_temp.album.lower()
            ]
            # Si hay duplicados, no agregar la canción
            if duplicados:
                print(
                    f"Ya existe una canción con el mismo título, artista y álbum: {cancion_temp.titulo_cancion}"
                )
                return None
            # Crear nueva canción
            cancion = cancion_temp
            # Agregar a las colecciones principales
            self.canciones.append(cancion)
            self.por_titulo[cancion.titulo_cancion] = cancion
            # Procesar y separar múltiples artistas
            artistas = self.separar_artistas(cancion.artista)
            # Agregar a la colección de artistas, para cada uno de los artistas detectados
            for artista in artistas:
                if artista not in self.por_artista:
                    self.por_artista[artista] = []
                self.por_artista[artista].append(cancion)
            # Agregar a la colección de álbumes
            if cancion.album not in self.por_album:
                self.por_album[cancion.album] = []
            self.por_album[cancion.album].append(cancion)
            # Ordenar canciones por título después de agregar
            self.ordenar_colecciones()
            return cancion
        except Exception as e:
            print(f"Error al procesar la canción {ruta.name}: {str(e)}")
            return None

    # Metodo para agregar un directorio de canciones a la biblioteca
    def agregar_directorio(self, ruta: Path) -> List[Cancion]:
        if not ruta.is_dir():
            raise NotADirectoryError(f"No es un directorio: {ruta}")
        canciones_agregadas = []
        for archivo in ruta.rglob("*"):
            if archivo.suffix.lower() in FORMATOS_SOPORTADOS:
                try:
                    cancion = self.agregar_cancion(archivo)
                    if cancion is not None:
                        canciones_agregadas.append(cancion)
                except Exception as e:
                    print(f"Error al agregar {archivo}: {e}")
        return canciones_agregadas

    # Método para eliminar una canción de la biblioteca (en la clase Biblioteca)
    def eliminar_cancion(self, cancion: Cancion) -> bool:
        try:
            # Eliminar de la lista principal de canciones
            self.canciones.remove(cancion)
            # Primero, eliminar del diccionario de títulos
            if cancion.titulo_cancion.lower() in self.por_titulo:
                self.por_titulo.pop(cancion.titulo_cancion.lower(), None)
            # Eliminar del diccionario por artista
            if cancion.artista in self.por_artista:
                if cancion in self.por_artista[cancion.artista]:
                    self.por_artista[cancion.artista].remove(cancion)
                    # Si quedó vacía, eliminar la clave
                    if not self.por_artista[cancion.artista]:
                        self.por_artista.pop(cancion.artista, None)
            # Eliminar del diccionario por álbum
            if cancion.album in self.por_album:
                if cancion in self.por_album[cancion.album]:
                    self.por_album[cancion.album].remove(cancion)
                    # Si quedó vacía, eliminar la clave
                    if not self.por_album[cancion.album]:
                        self.por_album.pop(cancion.album, None)
            # Eliminar de la lista de "Me gusta" si está presente
            if cancion in self.me_gusta:
                self.me_gusta.remove(cancion)
            # Eliminar de la lista de "Favoritos" si está presente
            if cancion in self.favorito:
                self.favorito.remove(cancion)
            return True
        except ValueError:
            return False

    # Metodo para eliminar todas las canciones de un directorio
    def eliminar_directorio(self, ruta: Path) -> List[Cancion]:
        if not ruta.is_dir():
            raise NotADirectoryError(f"No es un directorio: {ruta}")
        canciones_eliminadas = []
        # Encontrar todas las canciones del directorio
        for cancion in self.canciones[:]:  # Creamos una copia para iterar
            if str(ruta) in str(cancion.ruta_cancion):
                if self.eliminar_cancion(cancion):
                    canciones_eliminadas.append(cancion)
        return canciones_eliminadas

    # Método para obtener la carátula de una canción
    def obtener_caratula_album(self, nombre_album, formato="bytes", ancho=None, alto=None):
        if nombre_album in self.por_album:
            for cancion in self.por_album[nombre_album]:
                if cancion.caratula_cancion:
                    return cancion.obtener_caratula(formato, ancho, alto)
        return None

    # Método para obtener la carátula de un artista
    def obtener_caratula_artista(self, nombre_artista, formato="bytes", ancho=None, alto=None):
        if nombre_artista in self.por_artista:
            for cancion in self.por_artista[nombre_artista]:
                if cancion.caratula_cancion:
                    return cancion.obtener_caratula(formato, ancho, alto)
        return None

    # Método para obtener todas las carátulas de un álbum
    def obtener_caratulas_album(self, nombre_album, formato="bytes", ancho=None, alto=None):
        caratulas = []
        if nombre_album in self.por_album:
            for cancion in self.por_album[nombre_album]:
                if cancion.caratula_cancion:
                    caratula = cancion.obtener_caratula(formato, ancho, alto)
                    if caratula and caratula not in caratulas:
                        caratulas.append(caratula)
        return caratulas

    # Método para agregar una canción a la lista de "me gusta"
    def marcar_me_gusta(self, cancion: Cancion):
        if cancion not in self.canciones:
            raise ValueError("La canción no existe en la biblioteca")
        cancion.me_gusta = not cancion.me_gusta
        if cancion.me_gusta:
            self.me_gusta.append(cancion)
        else:
            self.me_gusta.remove(cancion)

    # Método para agregar una canción a la lista de "favoritos"
    def marcar_favorito(self, cancion: Cancion):
        if cancion not in self.canciones:
            raise ValueError("La canción no existe en la biblioteca")
        cancion.favorito = not cancion.favorito
        if cancion.favorito:
            self.favorito.append(cancion)
        else:
            self.favorito.remove(cancion)

    # Método para obtener una lista de canciones por titulo, artista o álbum
    def buscar(self, texto: str) -> List[Cancion]:
        texto = texto.lower()
        return [
            cancion
            for cancion in self.canciones
            if texto in cancion.titulo_cancion.lower()
            or texto in cancion.artista.lower()
            or texto in cancion.album.lower()
        ]

    # Metodo para ordenar las canciones por un criterio
    def ordenar_por(self, criterio: str) -> List[Cancion]:
        if criterio == "titulo":
            return sorted(self.canciones, key=lambda x: x.titulo_cancion)
        elif criterio == "artista":
            return sorted(self.canciones, key=lambda x: x.artista)
        elif criterio == "album":
            return sorted(self.canciones, key=lambda x: x.album)
        elif criterio == "duracion":
            return sorted(self.canciones, key=lambda x: x.duracion)
        return self.canciones

    # Metodo que convierte la biblioteca a un diccionario
    def convertir_diccionario(self) -> dict:
        return {
            "canciones": [cancion.convertir_diccionario() for cancion in self.canciones],
            "estadisticas": self.obtener_estadisticas(),
        }

    # Método para separar múltiples artistas de una cadena
    @staticmethod
    def separar_artistas(texto_artista: str) -> list:
        # Lista de separadores comunes para artistas
        separadores = SEPARADORES
        # Convertir a minúsculas para búsqueda insensible a mayúsculas
        texto_lower = texto_artista.lower()
        # Identificar separadores presentes
        separadores_encontrados = []
        for sep in separadores:
            if sep in texto_lower:
                separadores_encontrados.append(sep)
        # Si no hay separadores, devolver el artista original
        if not separadores_encontrados:
            return [texto_artista.strip()]
        # Separar artistas según los separadores encontrados
        artistas = [texto_artista]
        for sep in separadores_encontrados:
            nuevos_artistas = []
            for artista in artistas:
                partes = artista.split(sep)
                for parte in partes:
                    # Solo agregar si no está vacío
                    if parte.strip():
                        nuevos_artistas.append(parte.strip())
            artistas = nuevos_artistas
        # Eliminar duplicados y devolver lista limpia
        return list(set(artistas))

    # Método para reconstruir la organización de artistas
    def reinicializar_artistas(self):
        # Guardar todas las canciones actuales
        canciones_actuales = self.canciones.copy()
        # Limpiar la estructura de artistas
        self.por_artista.clear()
        # Volver a procesar cada canción para actualizar la estructura de artistas
        for cancion in canciones_actuales:
            # Procesar y separar múltiples artistas
            artistas = self.separar_artistas(cancion.artista)
            # Agregar a la colección de artistas actualizada
            for artista in artistas:
                if artista not in self.por_artista:
                    self.por_artista[artista] = []
                self.por_artista[artista].append(cancion)
        return True

    # Método para ordenar las colecciones de canciones
    def ordenar_colecciones(self):
        # Ordenar la lista principal de canciones
        self.canciones.sort(key=lambda x: x.titulo_cancion.lower())
        # Ordenar las listas por artistas
        for artista in self.por_artista:
            self.por_artista[artista].sort(key=lambda x: x.titulo_cancion.lower())
        # Ordenar las listas por álbumes
        for album in self.por_album:
            self.por_album[album].sort(key=lambda x: x.titulo_cancion.lower())
        # Ordenar listas especiales
        if hasattr(self, "me_gusta") and self.me_gusta:
            self.me_gusta.sort(key=lambda x: x.titulo_cancion.lower())
        if hasattr(self, "favorito") and self.favorito:
            self.favorito.sort(key=lambda x: x.titulo_cancion.lower())

    # Método para obtener estadísticas de la biblioteca
    def obtener_estadisticas(self) -> Dict[str, int]:
        return {
            "total_canciones": len(self.canciones),
            "total_artistas": len(self.por_artista),
            "total_albumes": len(self.por_album),
            "me_gusta": len(self.me_gusta),
            "favorito": len(self.favorito),
        }

    # Método para limpiar la biblioteca
    def limpiar_biblioteca(self):
        self.canciones.clear()
        self.por_titulo.clear()
        self.por_artista.clear()
        self.por_album.clear()
        self.me_gusta.clear()
        self.favorito.clear()
