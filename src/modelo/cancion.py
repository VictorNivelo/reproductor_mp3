from pathlib import Path
import mutagen


class Cancion:
    ruta_cancion: Path
    caratula_cancion = None
    titulo_cancion: str
    artista: str = "Desconocido"
    album: str = "Desconocido"
    duracion: float = 0.0
    me_gusta: bool = False
    favorita: bool = False

    # crea una cancion desde un archivo de audio
    def desde_archivo(cls, ruta_archivo: Path):
        try:
            audio = mutagen.File(ruta_archivo)
            if audio is None:
                return (ruta_archivo, ruta_archivo.stem)
            # Extraer metadatos
            titulo = audio.get("title", [ruta_archivo.stem])[0]
            artista = audio.get("artist", ["Desconocido"])[0]
            album = audio.get("album", ["Desconocido"])[0]
            duracion = audio.info.length
            return cls(
                ruta=ruta_archivo, titulo=titulo, artista=artista, album=album, duracion=duracion
            )
        except Exception:
            return cls(ruta_archivo, ruta_archivo.stem)
