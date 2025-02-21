from pathlib import Path
import mutagen


class Cancion:
    def __init__(
        self,
        ruta: Path,
        titulo: str,
        artista: str = "Desconocido",
        album: str = "Desconocido",
        duracion: float = 0.0,
    ):
        self.ruta_cancion = ruta
        self.titulo_cancion = titulo
        self.artista = artista
        self.album = album
        self.duracion = duracion
        self.caratula_cancion = None
        self.me_gusta = False
        self.favorita = False

    # crea una cancion desde un archivo de audio
    @classmethod
    def desde_archivo(cls, ruta_archivo: Path):
        try:
            audio = mutagen.File(ruta_archivo)
            if audio is None:
                return ruta_archivo, ruta_archivo.stem
            # Extraer metadatos
            titulo = audio.get("title", [ruta_archivo.stem])[0]
            artista = audio.get("artist", ["Desconocido"])[0]
            album = audio.get("album", ["Desconocido"])[0]
            duracion = audio.info.length
            return cls(
                ruta=ruta_archivo, titulo=titulo, artista=artista, album=album, duracion=duracion
            )
        except (mutagen.MutagenError, OSError) as e:
            print(f"Error al procesar el archivo {ruta_archivo}: {str(e)}")
            return cls(ruta=ruta_archivo, titulo=ruta_archivo.stem)
