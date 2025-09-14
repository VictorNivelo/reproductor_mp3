from modelo.metadatos import Metadatos
from caratula import CaratulaGeneral
from datetime import datetime
from pathlib import Path
from constantes import *

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
        genero: str = "Desconocido",
        caratula: bytes = None,
    ):
        self.ruta_cancion = ruta
        self.titulo_cancion = titulo
        self.artista_cancion = artista
        self.artista_album_cancion = artista_album
        self.album_cancion = album
        self.duracion_cancion = duracion
        self.anio_cancion = anio
        self.numero_pista_cancion = numero_pista
        self.genero_cancion = genero
        self.caratula_cancion = caratula
        self.fecha_agregado_cancion = datetime.now()
        self.me_gusta = False
        self.favorito = False

    # Convertir a cadena para mostrar en la consola
    def __str__(self):
        return f"\n{self.titulo_cancion} - {self.artista_cancion}"

    # Convertir en cadena un objeto Cancion
    def __repr__(self):
        return self.__str__()

    # Método que crea una instancia de Cancion a partir de un archivo de audio
    @classmethod
    def cargar_cancion(cls, ruta_archivo: Path):
        metadatos = Metadatos.cargar_metadatos_completos(ruta_archivo)
        return cls(**metadatos)

    # Método que devuelve la ruta de la canción como objeto Path
    @property
    def obtener_ruta_path(self) -> Path:
        try:
            return self.ruta_cancion
        except Exception as e:
            print(f"Error al obtener ruta como Path: {e}")
            return Path()

    # Método que devuelve la ruta de la canción
    @property
    def obtener_ruta(self) -> str:
        try:
            return str(self.ruta_cancion)
        except Exception as e:
            print(f"Error al obtener ruta: {e}")
            return "Desconocido"

    # Propiedad que devuelve el nombre de la canción sin extensión
    @property
    def obtener_nombre(self) -> str:
        try:
            return self.ruta_cancion.stem
        except Exception as e:
            print(f"Error al obtener nombre del archivo: {e}")
            return "Desconocido"

    # Propiedad que devuelve solo la extensión del archivo
    @property
    def obtener_extension(self) -> str:
        try:
            return self.ruta_cancion.suffix.lower()
        except Exception as e:
            print(f"Error al obtener extensión del archivo: {e}")
            return ""

    # Propiedad que devuelve el formato/códec del archivo
    @property
    def obtener_formato(self) -> str:
        try:
            if self.ruta_cancion.exists():
                audio = mutagen.File(self.ruta_cancion)
                if audio:
                    # Obtener el tipo de archivo desde mutagen
                    tipo_archivo = type(audio).__name__
                    # Mapear tipos de mutagen a nombres más amigables
                    mapeo_formatos = {
                        "MP3": "MP3",
                        "FLAC": "FLAC",
                        "MP4": "MP4/AAC",
                        "OggVorbis": "OGG Vorbis",
                        "OggOpus": "OGG Opus",
                        "ASF": "WMA",
                        "APEv2File": "APE",
                        "WavPack": "WavPack",
                        "TrueAudio": "TTA",
                    }
                    return mapeo_formatos.get(tipo_archivo, tipo_archivo)
                else:
                    # Si mutagen no puede identificar, usar extensión
                    extension = self.ruta_cancion.suffix.upper().lstrip(".")
                    return extension if extension else "Desconocido"
            return "Desconocido"
        except Exception as e:
            print(f"Error al obtener formato: {e}")
            # Fallback a extensión del archivo
            try:
                extension = self.ruta_cancion.suffix.upper().lstrip(".")
                return extension if extension else "Desconocido"
            except Exception as e:
                print(f"Error al obtener extensión en fallback: {e}")
                return "Desconocido"

    # Propiedad que devuelve el tamaño del archivo en bytes
    @property
    def obtener_tamanio(self) -> int:
        try:
            if self.ruta_cancion.exists():
                return self.ruta_cancion.stat().st_size
            return 0
        except Exception as e:
            print(f"Error al obtener tamaño: {e}")
            return 0

    # Propiedad que devuelve el tamaño formateado (KB, MB, GB)
    @property
    def obtener_tamanio_formateado(self) -> str:
        try:
            tamanio = self.obtener_tamanio
            if tamanio == 0:
                return "0 B"
            unidades = ["B", "KB", "MB", "GB"]
            i = 0
            while tamanio >= 1024 and i < len(unidades) - 1:
                tamanio /= 1024.0
                i += 1
            return f"{tamanio:.1f} {unidades[i]}"
        except Exception as e:
            print(f"Error al formatear tamaño: {e}")
            return "Desconocido"

    # Propiedad que devuelve la duración de la canción en formato MM:SS
    @property
    def obtener_duracion_formateada(self) -> str:
        minutos = int(self.duracion_cancion // 60)
        segundos = int(self.duracion_cancion % 60)
        return f"{minutos:02d}:{segundos:02d}"

    # Propiedad que devuelve la tasa de bits en kbps
    @property
    def obtener_tasa_bits(self) -> int:
        try:
            if self.ruta_cancion.exists():
                audio = mutagen.File(self.ruta_cancion)
                if audio and hasattr(audio, "info") and hasattr(audio.info, "bitrate"):
                    return audio.info.bitrate
            return 0
        except Exception as e:
            print(f"Error al obtener tasa de bits: {e}")
            return 0

    # Propiedad que devuelve la tasa de bits formateada
    @property
    def obtener_tasa_bits_formateada(self) -> str:
        try:
            bitrate = self.obtener_tasa_bits
            if bitrate == 0:
                return "Desconocido"
            return f"{bitrate} kbps"
        except Exception as e:
            print(f"Error al formatear tasa de bits: {e}")
            return "Desconocido"

    # Propiedad que devuelve la frecuencia de muestreo en Hz
    @property
    def obtener_frecuencia_muestreo(self) -> int:
        try:
            if self.ruta_cancion.exists():
                audio = mutagen.File(self.ruta_cancion)
                if audio and hasattr(audio, "info") and hasattr(audio.info, "sample_rate"):
                    return audio.info.sample_rate
            return 0
        except Exception as e:
            print(f"Error al obtener frecuencia de muestreo: {e}")
            return 0

    # Propiedad que devuelve la frecuencia de muestreo formateada
    @property
    def obtener_frecuencia_muestreo_formateada(self) -> str:
        try:
            sample_rate = self.obtener_frecuencia_muestreo
            if sample_rate == 0:
                return "Desconocido"
            # Convertir a kHz si es mayor a 1000 Hz
            if sample_rate >= 1000:
                return f"{sample_rate / 1000:.1f} kHz"
            else:
                return f"{sample_rate} Hz"
        except Exception as e:
            print(f"Error al formatear frecuencia de muestreo: {e}")
            return "Desconocido"

    # Propiedad que devuelve la fecha de la canción en formato DD/MM/YYYY
    @property
    def obtener_lanzamiento_formateada(self) -> str:
        try:
            if self.anio_cancion == "Desconocido":
                return "Desconocido"
            formatos = ["%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]
            for formato in formatos:
                try:
                    fecha = datetime.strptime(str(self.anio_cancion), formato)
                    return fecha.strftime("%d/%m/%Y")
                except ValueError:
                    continue
            return self.anio_cancion
        except Exception as e:
            print(f"Error al formatear fecha: {e}")
            return "Desconocido"

    # Propiedad que devuelve el año de la canción
    @property
    def obtener_lanzamiento_anio(self) -> str:
        try:
            if self.anio_cancion == "Desconocido":
                return "Desconocido"
            if str(self.anio_cancion).isdigit() and len(str(self.anio_cancion)) == 4:
                return str(self.anio_cancion)
            partes_fecha = str(self.anio_cancion).split("-")[0]
            if partes_fecha.isdigit() and len(partes_fecha) == 4:
                return partes_fecha
            return "Desconocido"
        except Exception as e:
            print(f"Error al obtener año: {e}")
            return "Desconocido"

    # Propiedad que devuelve la fecha de creación de la canción
    @property
    def obtener_fecha_creacion(self) -> datetime | None:
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
    def obtener_fecha_creacion_formateada(self) -> str:
        try:
            fecha = self.obtener_fecha_creacion
            if fecha:
                return fecha.strftime("%d/%m/%Y %H:%M:%S")
            return "Desconocido"
        except Exception as e:
            print(f"Error al formatear fecha de creación: {e}")
            return "Desconocido"

    # Propiedad que devuelve la fecha cuando se agregó a la biblioteca
    @property
    def obtener_fecha_agregado_formateada(self) -> str:
        try:
            return self.fecha_agregado_cancion.strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            print(f"Error al formatear fecha de agregado: {e}")
            return "Desconocido"

    # Método estático para separar artistas
    @staticmethod
    def separar_artistas_cancion(texto_artista: str) -> list:
        try:
            # Si el texto está vacío o es None, devolver lista vacía
            if not texto_artista or texto_artista.strip() == "":
                return []
            # Lista de separadores comunes para artistas (sin coma inicialmente)
            separadores_primarios = SEPARADORES
            # Convertir a minúsculas para búsqueda insensible a mayúsculas
            texto_lower = texto_artista.lower()
            # Primero separar por separadores primarios (no comas)
            artistas = [texto_artista]
            for sep in separadores_primarios:
                if sep in texto_lower:
                    nuevos_artistas = []
                    for artista in artistas:
                        partes = []
                        texto_temp = artista
                        sep_lower = sep.lower()
                        while sep_lower in texto_temp.lower():
                            indice = texto_temp.lower().find(sep_lower)
                            if indice != -1:
                                partes.append(texto_temp[:indice])
                                texto_temp = texto_temp[indice + len(sep) :]
                            else:
                                break
                        if texto_temp:
                            partes.append(texto_temp)
                        for parte in partes:
                            if parte.strip():
                                nuevos_artistas.append(parte.strip())
                    if nuevos_artistas:
                        artistas = nuevos_artistas
            # Ahora procesar comas de manera inteligente para cada artista
            artistas_finales = []
            for artista in artistas:
                if "," in artista:
                    # Palabras que indican que es parte de un nombre de artista
                    palabras_nombre = ["the", "a", "an", "de", "la", "el", "los", "las"]
                    # Separar por comas para analizar
                    partes_coma = [p.strip() for p in artista.split(",") if p.strip()]
                    # Si solo hay 2 partes, verificar si la segunda es parte del nombre
                    if len(partes_coma) == 2:
                        segunda_parte_lower = partes_coma[1].lower().strip()
                        # Si la segunda parte empieza con una palabra común de nombres de artistas
                        if any(segunda_parte_lower.startswith(palabra) for palabra in palabras_nombre):
                            # Es probable que sea un solo artista
                            artistas_finales.append(artista.strip())
                        else:
                            artistas_finales.extend(partes_coma)
                    else:
                        # Más de 2 partes, separar todas por comas
                        artistas_finales.extend(partes_coma)
                else:
                    # No hay comas, agregar tal como está
                    artistas_finales.append(artista.strip())
            # Eliminar duplicados manteniendo el orden
            artistas_unicos = []
            for artista in artistas_finales:
                artista_limpio = artista.strip()
                if artista_limpio and artista_limpio not in artistas_unicos:
                    artistas_unicos.append(artista_limpio)
            return artistas_unicos
        except Exception as e:
            print(f"Error al separar artistas: {e}")
            return [texto_artista] if texto_artista else []

    # Método que devuelve el artista principal (el primero en la lista)
    @property
    def obtener_artista_principal(self) -> str:
        try:
            # Usar el método estático para separar artistas
            artistas = self.separar_artistas_cancion(self.artista_cancion)
            # Devolver el primer artista (principal)
            if artistas:
                return artistas[0].strip()
            else:
                return self.artista_cancion.strip()
        except Exception as e:
            print(f"Error al obtener artista principal: {e}")
            return self.artista_cancion

    # Método que devuelve todos los artistas separados
    @property
    def obtener_todos_artistas_separados(self) -> list:
        try:
            return self.separar_artistas_cancion(self.artista_cancion)
        except Exception as e:
            print(f"Error al separar artistas: {e}")
            return [self.artista_cancion]

    # Método que devuelve la carátula en el formato solicitado
    def obtener_caratula_general_cancion(
        self, formato="bytes", ancho=None, alto=None, bordes_redondeados=False, radio_borde=None
    ):
        return CaratulaGeneral.extraer_caratula(
            self.caratula_cancion, formato, ancho, alto, bordes_redondeados, radio_borde
        )

    # Método que devuelve toda la información de la canción
    def obtener_informacion_cancion(self) -> dict:
        return {
            "duracion": self.duracion_cancion,
            "duracion_formateada": self.obtener_duracion_formateada,
            "ruta": str(self.ruta_cancion),
            "nombre_archivo": self.obtener_nombre,
            "extension_archivo": self.obtener_extension,
            "titulo": self.titulo_cancion,
            "artista": self.artista_cancion,
            "artista_album": self.artista_album_cancion,
            "album": self.album_cancion,
            "anio": self.anio_cancion,
            "numero_pista": self.numero_pista_cancion,
            "genero": self.genero_cancion,
            "tamanio_archivo": self.obtener_tamanio,
            "tamanio_formateado": self.obtener_tamanio_formateado,
            "fecha_creacion": self.obtener_fecha_creacion_formateada,
            "fecha_agregado": self.obtener_fecha_agregado_formateada,
            "tiene_caratula": self.caratula_cancion is not None,
            "me_gusta": self.me_gusta,
            "favorito": self.favorito,
            "formato_archivo": self.obtener_formato,
            "tasa_bits": self.obtener_tasa_bits,
            "tasa_bits_formateada": self.obtener_tasa_bits_formateada,
            "frecuencia_muestreo": self.obtener_frecuencia_muestreo,
            "frecuencia_muestreo_formateada": self.obtener_frecuencia_muestreo_formateada,
        }


# # Ejemplo de uso
# cancion = Cancion.cargar_cancion(Path("C:/Users/Victor/Music/M/DÁKITI.mp3"))
# print("--------------------------------------------------------------------------------")
# print(f"Ruta como Path: {cancion.obtener_ruta_path}")
# print(f"Ruta del archivo: {cancion.obtener_ruta}")
# print(f"Nombre del archivo: {cancion.obtener_nombre}")
# print(f"Extensión del archivo: {cancion.obtener_extension}")
# print(f"Formato: {cancion.obtener_formato}")
# print(f"Tamaño del archivo: {cancion.obtener_tamanio_formateado}")
# print(f"Título: {cancion.titulo_cancion}")
# print(f"Artista: {cancion.artista_cancion}")
# print(f"Artista del Álbum: {cancion.artista_album_cancion}")
# print(f"Álbum: {cancion.album_cancion}")
# print(f"Género: {cancion.genero_cancion}")
# print(f"Año de lanzamiento: {cancion.obtener_lanzamiento_anio}")
# print(f"Fecha de lanzamiento: {cancion.anio_cancion}")
# print(f"Fecha de lanzamiento formateada: {cancion.obtener_lanzamiento_formateada}")
# print(f"Número de pista: {cancion.numero_pista_cancion}")
# print(f"Duración en segundos: {cancion.duracion_cancion} segundos")
# print(f"Duración formateada: {cancion.obtener_duracion_formateada}")
# print(f"Tiene carátula: {cancion.caratula_cancion is not None}")
# print(f"Informacion de la carátula: {CaratulaGeneral.obtener_informacion_caratula(cancion.caratula_cancion)}")
# print(f"Fecha de creación: {cancion.obtener_fecha_creacion_formateada}")
# print(f"Fecha de agregado: {cancion.obtener_fecha_agregado_formateada}")
# print(f"Artistas separados: {cancion.obtener_todos_artistas_separados}")
# print(f"Artista principal: {cancion.obtener_artista_principal}")
# print(f"Tasa de bits: {cancion.obtener_tasa_bits_formateada}")
# print(f"Frecuencia: {cancion.obtener_frecuencia_muestreo_formateada}")
# print("--------------------------------------------------------------------------------")
