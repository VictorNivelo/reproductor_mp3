from modelo.biblioteca import Biblioteca
from modelo.cancion import Cancion
from pathlib import Path


class ControladorBiblioteca:
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.cancion_actual = None

    # Método que agregan canciones a la biblioteca
    def agregar_cancion_controlador(self, ruta: Path) -> Cancion:
        try:
            return self.biblioteca.agregar_cancion_biblioteca(ruta)
        except Exception as e:
            raise ValueError(f"Error al agregar la canción: {e}")

    # Método que agregan directorios de canciones a la biblioteca
    def agregar_directorio_controlador(self, ruta: Path) -> list:
        try:
            return self.biblioteca.agregar_directorio_biblioteca(ruta)
        except Exception as e:
            print(f"Error al agregar el directorio: {e}")
            return []

    # Método para eliminar una canción específica
    def eliminar_cancion_controlador(self, cancion: Cancion) -> bool:
        try:
            if cancion is None:
                print("Error: Canción no válida")
                return False
            # Verificar si la canción existe en la biblioteca
            if cancion not in self.biblioteca.canciones:
                print("Error: La canción no existe en la biblioteca")
                return False
            # Si es la canción actual, limpiar la referencia
            if self.cancion_actual == cancion:
                self.cancion_actual = None
            # Eliminar la canción de la biblioteca
            resultado = self.biblioteca.eliminar_cancion_biblioteca(cancion)
            if resultado:
                print(f"Canción eliminada exitosamente: {cancion.titulo_cancion}")
            else:
                print(f"Error al eliminar la canción: {cancion.titulo_cancion}")
            return resultado
        except Exception as e:
            print(f"Error al eliminar la canción: {e}")
            return False
        
    # Método para eliminar un artista completo
    def eliminar_artista_controlador(self, nombre_artista: str):
        try:
            return self.biblioteca.eliminar_artista_biblioteca(nombre_artista)
        except Exception as e:
            print(f"Error al eliminar artista: {e}")
            return False

    # Método para eliminar un álbum completo
    def eliminar_album_controlador(self, nombre_album: str):
        try:
            return self.biblioteca.eliminar_album_biblioteca(nombre_album)
        except Exception as e:
            print(f"Error al eliminar álbum: {e}")
            return False

    # Método para eliminar todas las canciones de un directorio
    def eliminar_directorio_controlador(self, ruta: Path) -> bool:
        try:
            if not isinstance(ruta, Path):
                ruta = Path(ruta)
            if not ruta.exists():
                print(f"Error: El directorio no existe: {ruta}")
                return False
            if not ruta.is_dir():
                print(f"Error: La ruta no es un directorio: {ruta}")
                return False
            # Obtener canciones eliminadas antes de la eliminación
            canciones_eliminadas = self.biblioteca.eliminar_directorio_biblioteca(ruta)
            # Si alguna de las canciones eliminadas era la canción actual, limpiar la referencia
            if self.cancion_actual in canciones_eliminadas:
                self.cancion_actual = None
            print(f"Se eliminaron {len(canciones_eliminadas)} canciones del directorio: {ruta}")
            # Mostrar las canciones eliminadas
            for cancion in canciones_eliminadas:
                print(f"  - {cancion.titulo_cancion} - {cancion.artista}")
            return len(canciones_eliminadas) > 0
        except NotADirectoryError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Error al eliminar directorio: {e}")
            return False

    # Método para obtener todas las canciones de un álbum específico
    def obtener_canciones_album_controlador(self, nombre_album):
        try:
            if nombre_album in self.biblioteca.por_album:
                return self.biblioteca.por_album[nombre_album]
            return []
        except Exception as e:
            print(f"Error al obtener canciones del álbum: {e}")
            return []

    # Método para obtener el artista de un álbum
    def obtener_artista_album_controlador(self, nombre_album: str):
        try:
            return self.biblioteca.obtener_artista_album_biblioteca(nombre_album)
        except Exception as e:
            print(f"Error al obtener artista del álbum: {e}")
            return None

    # Método para obtener todas las canciones de un artista específico
    def obtener_canciones_artista_controlador(self, nombre_artista):
        try:
            if nombre_artista in self.biblioteca.por_artista:
                return self.biblioteca.por_artista[nombre_artista]
            return []
        except Exception as e:
            print(f"Error al obtener canciones del artista: {e}")
            return []

    # Método para obtener todos los álbumes de un artista
    def obtener_albumes_artista_controlador(self, nombre_artista: str):
        try:
            return self.biblioteca.obtener_albumes_artista_biblioteca(nombre_artista)
        except Exception as e:
            print(f"Error al obtener álbumes del artista: {e}")
            return []

    # Método que verifica si una canción está marcada como "Me gusta"
    def verificar_me_gusta_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.me_gusta
        except Exception as e:
            print(f"Error al verificar me gusta: {e}")
            return False

    # Método que agrega canciones como me gusta
    def agregar_cancion_me_gusta_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_me_gusta_biblioteca(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como me gusta: {e}")
            return False

    def agregar_album_me_gusta_controlador(self, nombre_album: str):
        try:
            self.biblioteca.agregar_album_me_gusta_biblioteca(nombre_album)
            return True
        except Exception as e:
            print(f"Error al agregar álbum a me gusta: {e}")
            return False

    # Método para agregar un artista completo a "me gusta"
    def agregar_artista_me_gusta_controlador(self, nombre_artista: str):
        try:
            self.biblioteca.agregar_artista_me_gusta_biblioteca(nombre_artista)
            return True
        except Exception as e:
            print(f"Error al agregar artista a me gusta: {e}")
            return False

    # Método que verifica si una canción está marcada como favorita
    def verificar_favorito_controlador(self, cancion):
        try:
            if cancion is None:
                return False
            return cancion in self.biblioteca.favorito
        except Exception as e:
            print(f"Error al verificar favorito: {e}")
            return False

    # Método que agrega canciones como favoritas
    def agregar_cancion_favorito_controlador(self, cancion):
        try:
            self.biblioteca.agregar_cancion_favorito_biblioteca(cancion)
            return True
        except Exception as e:
            print(f"Error al marcar como favorito: {e}")
            return False

    # Método para agregar un álbum completo a "favoritos"
    def agregar_album_favorito_controlador(self, nombre_album: str):
        try:
            self.biblioteca.agregar_album_favorito_biblioteca(nombre_album)
            return True
        except Exception as e:
            print(f"Error al agregar álbum a favoritos: {e}")
            return False

    # Método para agregar un artista completo a "favoritos"
    def agregar_artista_favorito_controlador(self, nombre_artista: str):
        try:
            self.biblioteca.agregar_artista_favorito_biblioteca(nombre_artista)
            return True
        except Exception as e:
            print(f"Error al agregar artista a favoritos: {e}")
            return False

    # Método para obtener la caratula de un album
    def obtener_caratula_album_controlador(self, nombre_album, formato="bytes", ancho=None, alto=None):
        try:
            return self.biblioteca.obtener_caratula_album_biblioteca(nombre_album, formato, ancho, alto)
        except Exception as e:
            print(f"Error al obtener carátula del álbum: {e}")
            return None

    # Método para obtener la caratula de un artista
    def obtener_caratula_artista_controlador(self, nombre_artista, formato="bytes", ancho=None, alto=None):
        try:
            return self.biblioteca.obtener_caratula_artista_biblioteca(nombre_artista, formato, ancho, alto)
        except Exception as e:
            print(f"Error al obtener carátula del artista: {e}")
            return None
