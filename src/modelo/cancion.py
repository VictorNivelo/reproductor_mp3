from customtkinter import CTkImage
from PIL.Image import Resampling
from PIL import Image, ImageTk
from datetime import datetime
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pathlib import Path
import mutagen
import io


class Cancion:
    def __init__(
        self,
        ruta: Path,
        titulo: str,
        artista: str = "Desconocido",
        artista_album: str = "Desconocido",
        album: str = "Desconocido",
        duracion: float = 0.0,
        anio: str = "Desconocido",
        numero_pista: str = "0",
        genero: str = "Desconocido",
        caratula: bytes = None,
    ):
        self.ruta_cancion = ruta
        self.titulo_cancion = titulo
        self.artista = artista
        self.artista_album = artista_album
        self.album = album
        self.duracion = duracion
        self.anio = anio
        self.numero_pista = numero_pista
        self.genero = genero
        self.fecha_agregado = datetime.now()
        self.me_gusta = False
        self.favorito = False
        self.caratula_cancion = caratula

    # Convertir a cadena para mostrar en la consola
    def __str__(self):
        return f"\n{self.titulo_cancion} - {self.artista}"

    # Convertir en cadena un objeto Cancion
    def __repr__(self):
        return self.__str__()

    # Método que devuelve la ruta del archivo de la canción
    @property
    def ruta_archivo(self) -> str:
        return str(self.ruta_cancion)

    # Método que devuelve la ruta del archivo de la canción como objeto Path
    @property
    def ruta_path(self) -> Path:
        return self.ruta_cancion

    # Propiedad que devuelve el tamaño del archivo en bytes
    @property
    def tamano_archivo(self) -> int:
        try:
            if self.ruta_cancion.exists():
                return self.ruta_cancion.stat().st_size
            return 0
        except Exception as e:
            print(f"Error al obtener tamaño: {e}")
            return 0

    # Propiedad que devuelve el tamaño formateado (KB, MB, GB)
    @property
    def tamano_formateado(self) -> str:
        try:
            tamano = self.tamano_archivo
            if tamano == 0:
                return "0 B"
            unidades = ["B", "KB", "MB", "GB"]
            i = 0
            while tamano >= 1024 and i < len(unidades) - 1:
                tamano /= 1024.0
                i += 1
            return f"{tamano:.1f} {unidades[i]}"
        except Exception as e:
            print(f"Error al formatear tamaño: {e}")
            return "Desconocido"

    # Propiedad que devuelve la fecha de creación del archivo
    @property
    def fecha_creacion_archivo(self) -> datetime:
        try:
            if self.ruta_cancion.exists():
                timestamp = self.ruta_cancion.stat().st_ctime
                return datetime.fromtimestamp(timestamp)
            return None
        except Exception as e:
            print(f"Error al obtener fecha de creación: {e}")
            return None

    # Propiedad que devuelve la fecha de creación formateada
    @property
    def fecha_creacion_formateada(self) -> str:
        try:
            fecha = self.fecha_creacion_archivo
            if fecha:
                return fecha.strftime("%d/%m/%Y %H:%M:%S")
            return "Desconocido"
        except Exception as e:
            print(f"Error al formatear fecha de creación: {e}")
            return "Desconocido"

    # Propiedad que devuelve la fecha cuando se agregó a la biblioteca
    @property
    def fecha_agregado_formateada(self) -> str:
        try:
            return self.fecha_agregado.strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            print(f"Error al formatear fecha de agregado: {e}")
            return "Desconocido"

    # Propiedad que devuelve la duración de la canción en formato MM:SS
    @property
    def duracion_formateada(self) -> str:
        minutos = int(self.duracion // 60)
        segundos = int(self.duracion % 60)
        return f"{minutos:02d}:{segundos:02d}"

    # Propiedad que devuelve la fecha de la canción en formato DD/MM/YYYY
    @property
    def fecha_formateada(self) -> str:
        try:
            if self.anio == "Desconocido":
                return "Desconocido"
            formatos = ["%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]
            for formato in formatos:
                try:
                    fecha = datetime.strptime(str(self.anio), formato)
                    return fecha.strftime("%d/%m/%Y")
                except ValueError:
                    continue
            return self.anio
        except Exception as e:
            print(f"Error al formatear fecha: {e}")
            return "Desconocido"

    # Propiedad que devuelve el año de la canción
    @property
    def fecha_formateada_anio(self) -> str:
        try:
            if self.anio == "Desconocido":
                return "Desconocido"
            if str(self.anio).isdigit() and len(str(self.anio)) == 4:
                return str(self.anio)
            partes_fecha = str(self.anio).split("-")[0]
            if partes_fecha.isdigit() and len(partes_fecha) == 4:
                return partes_fecha
            return "Desconocido"
        except Exception as e:
            print(f"Error al obtener año: {e}")
            return "Desconocido"

    # Método que crea una instancia de Cancion a partir de un archivo de audio
    @classmethod
    def cargar_cancion(cls, ruta_archivo: Path):
        try:
            audio = mutagen.File(ruta_archivo)
            if audio is None:
                return cls(ruta=ruta_archivo, titulo=ruta_archivo.stem)
            info = cls.obtener_informacion_base_cancion(ruta_archivo)
            if isinstance(audio, MP3):
                info.update(cls.obtener_informacion_mp3(ruta_archivo))
            elif isinstance(audio, FLAC):
                info.update(cls.obtener_informacion_flac(audio))
            elif isinstance(audio, MP4):
                info.update(cls.obtener_informacion_mp4(audio))
            return cls(ruta=ruta_archivo, **info)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_archivo}: {str(e)}")
            return cls(ruta=ruta_archivo, titulo=ruta_archivo.stem)

    # Método que crea una imagen vacía para la carátula
    @staticmethod
    def crear_imagen_vacia():
        try:
            img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            return CTkImage(light_image=img, dark_image=img, size=(1, 1))
        except Exception as e:
            print(f"Error al crear imagen vacía: {e}")
            return None

    # Método para obtener la carátula de la canción
    def obtener_caratula_general_cancion(self, formato="bytes", ancho=None, alto=None):
        if not self.caratula_cancion:
            return None
        try:
            if formato == "bytes":
                return self.caratula_cancion
            # Convertir bytes a imagen PIL
            imagen_bytes = io.BytesIO(self.caratula_cancion)
            imagen_pil = Image.open(imagen_bytes)
            # Redimensionar si se especifican dimensiones
            if ancho or alto:
                if ancho and not alto:
                    # Mantener proporciones si solo se especifica el ancho
                    proporcion = ancho / imagen_pil.width
                    alto = int(imagen_pil.height * proporcion)
                elif alto and not ancho:
                    # Mantener proporciones si solo se especifica el alto
                    proporcion = alto / imagen_pil.height
                    ancho = int(imagen_pil.width * proporcion)
                imagen_pil = imagen_pil.resize((ancho, alto), Resampling.LANCZOS)
            # Devolver el formato solicitado
            if formato == "PIL":
                return imagen_pil
            elif formato == "ctk":
                # Opción específica para CustomTkinter
                try:
                    return CTkImage(
                        light_image=imagen_pil,
                        dark_image=imagen_pil,
                        size=(ancho or imagen_pil.width, alto or imagen_pil.height),
                    )
                except ImportError:
                    raise ImportError(
                        "No se puede importar CTkImage. Asegúrate de tener CustomTkinter instalado."
                    )
            elif formato == "tk":
                # Opción específica para Tkinter estándar
                return ImageTk.PhotoImage(imagen_pil)
            else:
                raise ValueError(f"Formato '{formato}' no soportado. Usa 'bytes', 'PIL', 'ctk' o 'tk'")
        except Exception as e:
            print(f"Error al procesar la carátula: {e}")
            return None

    # Método que obtiene la información base de la canción
    @staticmethod
    def obtener_informacion_base_cancion(ruta_archivo: Path) -> dict:
        return {
            "duracion": 0.0,
            "titulo": ruta_archivo.stem,
            "artista": "Desconocido",
            "artista_album": "Desconocido",
            "album": "Desconocido",
            "anio": "Desconocido",
            "numero_pista": "0",
            "genero": "Desconocido",
            "caratula": None,
        }

    # Método que obtiene la información de un archivo MP3
    @staticmethod
    def obtener_informacion_mp3(ruta_archivo: Path) -> dict:
        tags = ID3(ruta_archivo)
        audio = MP3(ruta_archivo)
        info = {
            "duracion": audio.info.length,
            "titulo": str(tags.get("TIT2", ruta_archivo.stem)),
            "artista": str(tags.get("TPE1", "Desconocido")),
            "artista_album": str(tags.get("TPE2", "Desconocido")),
            "album": str(tags.get("TALB", "Desconocido")),
            "anio": str(tags.get("TDRC", "Desconocido")),
            "numero_pista": str(tags.get("TRCK", "0")),
            "genero": str(tags.get("TCON", "Desconocido")),
            "caratula": tags["APIC:"].data if "APIC:" in tags else None,
        }
        return info

    # Método que obtiene la información de un archivo FLAC
    @staticmethod
    def obtener_informacion_flac(audio: FLAC) -> dict:
        info = {
            "duracion": audio.info.length,
            "titulo": str(audio.get("title", [""])[0] or audio.filename),
            "artista": str(audio.get("artist", ["Desconocido"])[0]),
            "artista_album": str(audio.get("albumartist", ["Desconocido"])[0]),
            "album": str(audio.get("album", ["Desconocido"])[0]),
            "anio": str(audio.get("date", ["Desconocido"])[0]),
            "numero_pista": str(audio.get("tracknumber", ["0"])[0]),
            "genero": str(audio.get("genre", ["Desconocido"])[0]),
            "caratula": audio.pictures[0].data if audio.pictures else None,
        }
        return info

    # Método que obtiene la información de un archivo MP4
    @staticmethod
    def obtener_informacion_mp4(audio: MP4) -> dict:
        info = {
            "duracion": audio.info.length,
            "titulo": str(audio.get("\xa9nam", [""])[0] or audio.filename),
            "artista": str(audio.get("\xa9ART", ["Desconocido"])[0]),
            "artista_album": str(audio.get("aART", ["Desconocido"])[0]),
            "album": str(audio.get("\xa9alb", ["Desconocido"])[0]),
            "anio": str(audio.get("\xa9day", ["Desconocido"])[0]),
            "numero_pista": str(audio.get("trkn", [[0, 0]])[0][0]),
            "genero": str(audio.get("\xa9gen", ["Desconocido"])[0]),
            "caratula": audio["covr"][0] if "covr" in audio else None,
        }
        return info

    # Método que convierte la canción a un diccionario
    def convertir_diccionario_cancion(self) -> dict:
        return {
            "duracion": self.duracion,
            "duracion_formateada": self.duracion_formateada,
            "ruta": str(self.ruta_cancion),
            "titulo": self.titulo_cancion,
            "artista": self.artista,
            "artista_album": self.artista_album,
            "album": self.album,
            "anio": self.anio,
            "numero_pista": self.numero_pista,
            "genero": self.genero,
            "tamano_archivo": self.tamano_archivo,
            "tamano_formateado": self.tamano_formateado,
            "fecha_creacion": self.fecha_creacion_formateada,
            "fecha_agregado": self.fecha_agregado_formateada,
            "tiene_caratula": self.caratula_cancion is not None,
            "me_gusta": self.me_gusta,
            "favorito": self.favorito,
        }


# # Ejemplo de uso
# cancion = Cancion.cargar_cancion(Path("C:/Users/Victor/Music/M/DÁKITI.mp3"))
# print(f"Título: {cancion.titulo_cancion}")
# print(f"Artista: {cancion.artista}")
# print(f"Artista del Álbum: {cancion.artista_album}")
# print(f"Álbum: {cancion.album}")
# print(f"Género: {cancion.genero}")
# print(f"Año: {cancion.fecha_formateada_anio}")
# print(f"Lanzamiento: {cancion.anio}")
# print(f"Fecha formateada: {cancion.fecha_formateada}")
# print(f"Número de pista: {cancion.numero_pista}")
# print(f"Duración: {cancion.duracion} segundos")
# print(f"Duración formateada: {cancion.duracion_formateada}")
# print(f"Tiene carátula: {cancion.caratula_cancion is not None}")
# print(f"Tamaño del archivo: {cancion.tamano_formateado}")
# print(f"Fecha de creación: {cancion.fecha_creacion_formateada}")
# print(f"Fecha de agregado: {cancion.fecha_agregado_formateada}")
