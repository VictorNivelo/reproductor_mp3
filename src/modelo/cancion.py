from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pathlib import Path
import mutagen


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
        self.caratula_cancion = caratula
        self.me_gusta = False
        self.favorito = False

    # Propiedad que devuelve la duración de la canción en formato MM:SS
    @property
    def duracion_formato(self) -> str:
        minutos = int(self.duracion // 60)
        segundos = int(self.duracion % 60)
        return f"{minutos:02d}:{segundos:02d}"

    # Método que crea una instancia de Cancion a partir de un archivo de audio
    @classmethod
    def desde_archivo(cls, ruta_archivo: Path):
        try:
            audio = mutagen.File(ruta_archivo)
            if audio is None:
                return cls(ruta=ruta_archivo, titulo=ruta_archivo.stem)
            info = cls.obtener_info_base(ruta_archivo)
            if isinstance(audio, MP3):
                info.update(cls.obtener_info_mp3(ruta_archivo))
            elif isinstance(audio, FLAC):
                info.update(cls.obtener_info_flac(audio))
            elif isinstance(audio, MP4):
                info.update(cls.obtener_info_mp4(audio))
            return cls(ruta=ruta_archivo, **info)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_archivo}: {str(e)}")
            return cls(ruta=ruta_archivo, titulo=ruta_archivo.stem)

    # Método que obtiene la información base de la canción
    @staticmethod
    def obtener_info_base(ruta_archivo: Path) -> dict:
        return {
            "titulo": ruta_archivo.stem,
            "artista": "Desconocido",
            "artista_album": "Desconocido",
            "album": "Desconocido",
            "anio": "Desconocido",
            "numero_pista": "0",
            "caratula": None,
            "duracion": 0.0,
        }

    # Método que obtiene la información de un archivo MP3
    @staticmethod
    def obtener_info_mp3(ruta_archivo: Path) -> dict:
        tags = ID3(ruta_archivo)
        audio = MP3(ruta_archivo)
        info = {
            "titulo": str(tags.get("TIT2", ruta_archivo.stem)),
            "artista": str(tags.get("TPE1", "Desconocido")),
            "artista_album": str(tags.get("TPE2", "Desconocido")),
            "album": str(tags.get("TALB", "Desconocido")),
            "anio": str(tags.get("TDRC", "Desconocido")),
            "numero_pista": str(tags.get("TRCK", "0")),
            "duracion": audio.info.length,
            "caratula": tags["APIC:"].data if "APIC:" in tags else None,
        }
        return info

    # Método que obtiene la información de un archivo FLAC
    @staticmethod
    def obtener_info_flac(audio: FLAC) -> dict:
        info = {
            "titulo": str(audio.get("title", [""])[0] or audio.filename),
            "artista": str(audio.get("artist", ["Desconocido"])[0]),
            "artista_album": str(audio.get("albumartist", ["Desconocido"])[0]),
            "album": str(audio.get("album", ["Desconocido"])[0]),
            "anio": str(audio.get("date", ["Desconocido"])[0]),
            "numero_pista": str(audio.get("tracknumber", ["0"])[0]),
            "duracion": audio.info.length,
            "caratula": audio.pictures[0].data if audio.pictures else None,
        }
        return info

    # Método que obtiene la información de un archivo MP4
    @staticmethod
    def obtener_info_mp4(audio: MP4) -> dict:
        info = {
            "titulo": str(audio.get("\xa9nam", [""])[0] or audio.filename),
            "artista": str(audio.get("\xa9ART", ["Desconocido"])[0]),
            "artista_album": str(audio.get("aART", ["Desconocido"])[0]),
            "album": str(audio.get("\xa9alb", ["Desconocido"])[0]),
            "anio": str(audio.get("\xa9day", ["Desconocido"])[0]),
            "numero_pista": str(audio.get("trkn", [[0, 0]])[0][0]),
            "duracion": audio.info.length,
            "caratula": audio["covr"][0] if "covr" in audio else None,
        }
        return info


# # Ejemplo de uso
# cancion = Cancion.desde_archivo(Path("C:/Users/Victor/Music/Musica/3 Am.mp3"))
# print(f"Título: {cancion.titulo_cancion}")
# print(f"Artista: {cancion.artista}")
# print(f"Artista del Álbum: {cancion.artista_album}")
# print(f"Álbum: {cancion.album}")
# print(f"Año: {cancion.anio}")
# print(f"Número de pista: {cancion.numero_pista}")
# print(f"Duración: {cancion.duracion} segundos")
# print(f"Duración formateada: {cancion.duracion_formato}")
# print(f"Tiene carátula: {cancion.caratula_cancion is not None}")
