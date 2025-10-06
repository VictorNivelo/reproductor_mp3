import mutagen

from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pathlib import Path


class Metadatos:

    # Método que valida si el archivo es de un formato de audio soportado
    @staticmethod
    def validar_archivo(ruta_archivo: Path) -> bool:
        try:
            if not ruta_archivo.exists():
                print(f"Error: El archivo no existe: {ruta_archivo}")
                return False
            if not ruta_archivo.is_file():
                print(f"Error: La ruta no es un archivo: {ruta_archivo}")
                return False
            extensiones_validas = {".mp3", ".flac", ".m4a", ".mp4", ".ogg", ".wav"}
            extension = ruta_archivo.suffix.lower()
            if extension not in extensiones_validas:
                print(f"Error: Extensión '{extension}' no soportada para: {ruta_archivo}")
                return False
            return True
        except Exception as e:
            print(f"Error al validar archivo {ruta_archivo}: {e}")
            return False

    # Método que carga metadatos completos de un archivo de audio
    @staticmethod
    def obtener_metadatos(ruta_archivo: Path) -> dict:
        if not Metadatos.validar_archivo(ruta_archivo):
            return {"ruta": ruta_archivo, "titulo": ruta_archivo.stem}
        try:
            audio = mutagen.File(ruta_archivo)
            if audio is None:
                return {"ruta": ruta_archivo, "titulo": ruta_archivo.stem}
            informacion = Metadatos.obtener_metadatos_base(ruta_archivo)
            if isinstance(audio, MP3):
                informacion.update(Metadatos.obtener_metadatos_mp3(ruta_archivo))
            elif isinstance(audio, FLAC):
                informacion.update(Metadatos.obtener_metadatos_flac(audio))
            elif isinstance(audio, MP4):
                informacion.update(Metadatos.obtener_metadatos_mp4(audio))
            informacion["ruta"] = ruta_archivo
            return informacion
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_archivo}: {str(e)}")
            return {"ruta": ruta_archivo, "titulo": ruta_archivo.stem}

    # Método que obtiene la información base de la canción
    @staticmethod
    def obtener_metadatos_base(ruta_archivo: Path) -> dict:
        return {
            "duracion": 0.0,
            "titulo": ruta_archivo.stem,
            "artista": "Artista desconocido",
            "artista_album": "Album desconocido",
            "album": "Álbum desconocido",
            "anio": "Año desconocido",
            "numero_pista": "0",
            "genero": "Género desconocido",
            "caratula": None,
        }

    # Método que obtiene la información de un archivo MP3
    @staticmethod
    def obtener_metadatos_mp3(ruta_archivo: Path) -> dict:
        try:
            tags = ID3(ruta_archivo)
            audio = MP3(ruta_archivo)
            informacion = {
                "duracion": audio.info.length,
                "titulo": str(tags.get("TIT2", ruta_archivo.stem)),
                "artista": str(tags.get("TPE1", "Artista desconocido")),
                "artista_album": str(tags.get("TPE2", "Artista desconocido")),
                "album": str(tags.get("TALB", "Album desconocido")),
                "anio": str(tags.get("TDRC", "Año desconocido")),
                "numero_pista": str(tags.get("TRCK", "0")),
                "genero": str(tags.get("TCON", "Género desconocido")),
                "caratula": tags["APIC:"].data if "APIC:" in tags else None,
            }
            return informacion
        except Exception as e:
            print(f"Error al leer metadatos MP3: {e}")
            return {}

    # Método que obtiene la información de un archivo FLAC
    @staticmethod
    def obtener_metadatos_flac(audio: FLAC) -> dict:
        try:
            informacion = {
                "duracion": audio.info.length,
                "titulo": str(audio.get("title", [""])[0] or audio.filename),
                "artista": str(audio.get("artist", ["Artista desconocido"])[0]),
                "artista_album": str(audio.get("albumartist", ["Artista desconocido"])[0]),
                "album": str(audio.get("album", ["Album desconocido"])[0]),
                "anio": str(audio.get("date", ["Año desconocido"])[0]),
                "numero_pista": str(audio.get("tracknumber", ["0"])[0]),
                "genero": str(audio.get("genre", ["Género desconocido"])[0]),
                "caratula": audio.pictures[0].data if audio.pictures else None,
            }
            return informacion
        except Exception as e:
            print(f"Error al leer metadatos FLAC: {e}")
            return {}

    # Método que obtiene la información de un archivo MP4
    @staticmethod
    def obtener_metadatos_mp4(audio: MP4) -> dict:
        try:
            informacion = {
                "duracion": audio.info.length,
                "titulo": str(audio.get("\xa9nam", [""])[0] or audio.filename),
                "artista": str(audio.get("\xa9ART", ["Artista desconocido"])[0]),
                "artista_album": str(audio.get("aART", ["Artista desconocido"])[0]),
                "album": str(audio.get("\xa9alb", ["Album desconocido"])[0]),
                "anio": str(audio.get("\xa9day", ["Año desconocido"])[0]),
                "numero_pista": str(audio.get("trkn", [[0, 0]])[0][0]),
                "genero": str(audio.get("\xa9gen", ["Género desconocido"])[0]),
                "caratula": audio["covr"][0] if "covr" in audio else None,
            }
            return informacion
        except Exception as e:
            print(f"Error al leer metadatos MP4: {e}")
            return {}
