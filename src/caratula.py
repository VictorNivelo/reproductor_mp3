import io


from PIL import Image, ImageDraw, ImageTk, ImageFont
from customtkinter import CTkImage
from constantes import *


class CaratulaGeneral:

    # Método que verifica si hay carátula
    @staticmethod
    def tiene_caratula(caratula_bytes) -> bool:
        try:
            if caratula_bytes is None or len(caratula_bytes) == 0:
                return False
            # Intentar abrir la imagen para verificar que es válida
            imagen_bytes = io.BytesIO(caratula_bytes)
            imagen_pil = Image.open(imagen_bytes)
            # Verificar que tiene dimensiones válidas
            return imagen_pil.width > 0 and imagen_pil.height > 0
        except Exception as e:
            print(f"Error al verificar carátula: {e}")
            return False

    # Método que obtiene información básica de la carátula
    @staticmethod
    def obtener_informacion_caratula(caratula_bytes) -> dict:
        info = {"tiene_caratula": False, "ancho": 0, "alto": 0, "formato": "Desconocido", "tamanio_bytes": 0}
        try:
            if CaratulaGeneral.tiene_caratula(caratula_bytes):
                imagen_bytes = io.BytesIO(caratula_bytes)
                imagen_pil = Image.open(imagen_bytes)
                info.update(
                    {
                        "tiene_caratula": True,
                        "ancho": imagen_pil.width,
                        "alto": imagen_pil.height,
                        "formato": imagen_pil.format or "Desconocido",
                        "tamanio_bytes": len(caratula_bytes),
                    }
                )
        except Exception as e:
            print(f"Error al obtener información de carátula: {e}")
        return info

    # Método que determina la calidad del audio basado en formato y bitrate
    @staticmethod
    def determinar_calidad_audio(formato, bitrate, sample_rate=0):
        try:
            formato_upper = formato.upper()
            # Convertir bitrate de bps a kbps si es necesario
            if bitrate > 1000:
                bitrate_kbps = round(bitrate / 1000)
            else:
                bitrate_kbps = bitrate
            # Hi-Res: FLAC/WAV 24-bit 96kHz+
            if formato_upper in ["FLAC", "WAV"] and sample_rate >= 96000:
                return "Hi-Res"
            # Hi-Fi: FLAC 16-bit 44.1kHz (cualquier FLAC que no sea Hi-Res)
            if formato_upper == "FLAC":
                return "Hi-Fi"
            # Para formatos con pérdida (MP3, AAC, etc.)
            if bitrate_kbps > 0:
                if bitrate_kbps >= 320:
                    return "HD"
                elif bitrate_kbps >= 192:
                    return "High Quality"
                else:
                    return "Estándar"
            # Casos especiales para otros formatos sin bitrate específico
            if formato_upper in ["OGG VORBIS", "OGG OPUS"]:
                return "High Quality"
            return "Estándar"
        except Exception as e:
            print(f"Error al determinar calidad: {e}")
            return "Estándar"

    # Método que crea un estandarte de calidad
    @staticmethod
    def crear_estandarte_calidad(etiqueta_calidad):
        try:
            # Configurar fuente con mejor calidad
            try:
                fuente = ImageFont.truetype("arial.ttf", 10)
            except (OSError, IOError):
                try:
                    fuente = ImageFont.truetype("segoeui.ttf", 10)
                except (OSError, IOError):
                    try:
                        fuente = ImageFont.truetype("calibri.ttf", 10)
                    except (OSError, IOError):
                        try:
                            fuente = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 10)
                        except (OSError, IOError):
                            fuente = ImageFont.load_default()
            # Crear imagen temporal transparente para medir texto
            img_temp = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
            draw_temp = ImageDraw.Draw(img_temp)
            # Obtener dimensiones del texto
            bbox = draw_temp.textbbox((0, 0), etiqueta_calidad, font=fuente)
            texto_ancho = bbox[2] - bbox[0]
            texto_alto = bbox[3] - bbox[1]
            # Padding para el estandarte
            padding_x = 8
            padding_y = 6
            # Calcular dimensiones del estandarte
            ancho_estandarte = texto_ancho + (padding_x * 2)
            alto_estandarte = texto_alto + (padding_y * 2)
            # Dimensiones mínimas
            ancho_estandarte = max(ancho_estandarte, 40)
            alto_estandarte = max(alto_estandarte, 16)
            # Crear imagen del estandarte con alta resolución
            escala = 2
            ancho_alta_res = int(ancho_estandarte * escala)
            alto_alta_res = int(alto_estandarte * escala)
            # Crear imagen transparente
            estandarte_hd = Image.new("RGBA", (ancho_alta_res, alto_alta_res), (0, 0, 0, 0))
            draw_hd = ImageDraw.Draw(estandarte_hd)
            # Fuente escalada
            try:
                fuente_hd = ImageFont.truetype("arial.ttf", 10 * escala)
            except (OSError, IOError):
                try:
                    fuente_hd = ImageFont.truetype("segoeui.ttf", 10 * escala)
                except (OSError, IOError):
                    try:
                        fuente_hd = ImageFont.truetype("calibri.ttf", 10 * escala)
                    except (OSError, IOError):
                        fuente_hd = ImageFont.load_default()
            # Color de fondo gris semi-transparente
            color_fondo = (80, 80, 80, 200)
            # Radio de borde escalado
            radio_borde_hd = 6 * escala
            # Dibujar rectángulo redondeado
            draw_hd.rounded_rectangle(
                [(0, 0), (ancho_alta_res, alto_alta_res)], radius=radio_borde_hd, fill=color_fondo
            )
            # Medir texto en alta resolución
            bbox_hd = draw_hd.textbbox((0, 0), etiqueta_calidad, font=fuente_hd)
            texto_ancho_hd = bbox_hd[2] - bbox_hd[0]
            texto_alto_hd = bbox_hd[3] - bbox_hd[1]
            # Calcular posición centrada
            texto_x_hd = (ancho_alta_res - texto_ancho_hd) // 2
            texto_y_hd = (alto_alta_res - texto_alto_hd) // 2
            # Ajuste fino para centrado
            ajuste_y = bbox_hd[1]
            texto_y_hd = texto_y_hd - ajuste_y
            # Dibujar texto en blanco
            draw_hd.text(
                (texto_x_hd, texto_y_hd), etiqueta_calidad, fill=(255, 255, 255, 255), font=fuente_hd
            )
            # Redimensionar a tamaño final
            estandarte = estandarte_hd.resize((ancho_estandarte, alto_estandarte), Image.Resampling.LANCZOS)
            return estandarte
        except Exception as e:
            print(f"Error al crear estandarte para '{etiqueta_calidad}': {e}")
            return None

    # Método que superpone el estandarte en la carátula
    @staticmethod
    def superponer_estandarte_calidad(imagen_pil, etiqueta_calidad, posicion="inf_izq"):
        try:
            if not etiqueta_calidad:
                return imagen_pil
            # Crear el estandarte
            estandarte = CaratulaGeneral.crear_estandarte_calidad(etiqueta_calidad)
            if not estandarte:
                return imagen_pil
            # Crear una copia de la imagen para no modificar la original
            imagen_con_estandarte = imagen_pil.copy()
            # Obtener dimensiones
            img_ancho, img_alto = imagen_con_estandarte.size
            est_ancho, est_alto = estandarte.size
            # Margen ajustado para bordes redondeados
            margen_base = 8
            factor_ajuste = min(img_ancho, img_alto) / 300
            margen_ajustado = max(margen_base, int(margen_base * factor_ajuste))
            # Calcular posición según parámetro
            if posicion == "sup_der":
                x = img_ancho - est_ancho - margen_ajustado
                y = margen_ajustado
            elif posicion == "sup_izq":
                x = margen_ajustado
                y = margen_ajustado
            elif posicion == "inf_der":
                x = img_ancho - est_ancho - margen_ajustado
                y = img_alto - est_alto - margen_ajustado
            elif posicion == "inf_izq":
                x = margen_ajustado
                y = img_alto - est_alto - margen_ajustado
            else:
                # Por defecto: inferior izquierda
                x = margen_ajustado
                y = img_alto - est_alto - margen_ajustado
            # Asegurar que la imagen esté en modo RGBA para transparencia
            if imagen_con_estandarte.mode != "RGBA":
                imagen_con_estandarte = imagen_con_estandarte.convert("RGBA")
            # Superponer el estandarte usando la transparencia
            imagen_con_estandarte.paste(estandarte, (x, y), estandarte)
            return imagen_con_estandarte
        except Exception as e:
            print(f"Error al superponer estandarte: {e}")
            return imagen_pil

    # Método que procesa la carátula y la devuelve en el formato solicitado
    @staticmethod
    def extraer_caratula(
        caratula_bytes,
        formato="bytes",
        ancho=None,
        alto=None,
        bordes_redondeados=False,
        radio_borde=None,
        etiqueta_calidad=None,
        posicion_estandarte="inf_izq",
    ):
        if not caratula_bytes:
            return None
        try:
            if formato == "bytes":
                return caratula_bytes
            # Convertir bytes a imagen PIL
            imagen_bytes = io.BytesIO(caratula_bytes)
            imagen_pil = Image.open(imagen_bytes)
            # Redimensionar si se especifican dimensiones
            if ancho or alto:
                if ancho and not alto:
                    proporcion = ancho / imagen_pil.width
                    alto = int(imagen_pil.height * proporcion)
                elif alto and not ancho:
                    proporcion = alto / imagen_pil.height
                    ancho = int(imagen_pil.width * proporcion)
                imagen_pil = imagen_pil.resize((ancho, alto), Image.Resampling.LANCZOS)
            # Aplicar bordes redondeados si se solicita
            if bordes_redondeados:
                imagen_pil = CaratulaGeneral.aplicar_bordes_redondeados(imagen_pil, radio_borde)
            # Superponer estandarte de calidad si se especifica
            if etiqueta_calidad:
                imagen_pil = CaratulaGeneral.superponer_estandarte_calidad(
                    imagen_pil, etiqueta_calidad, posicion_estandarte
                )
            # Devolver el formato solicitado
            if formato == "PIL":
                return imagen_pil
            elif formato == "ctk":
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
                return ImageTk.PhotoImage(imagen_pil)
            else:
                raise ValueError(f"Formato '{formato}' no soportado. Usa 'bytes', 'PIL', 'ctk' o 'tk'")
        except Exception as e:
            print(f"Error al procesar la carátula: {e}")
            return None

    # Método que crea una caratula vacia
    @staticmethod
    def crear_caratula_vacia(ancho=None, alto=None, etiqueta_calidad=None):
        try:
            # Usar las constantes de carátula por defecto si no se especifican dimensiones
            if ancho is None:
                ancho = ANCHO_CARATULA
            if alto is None:
                alto = ALTO_CARATULA
            # Crear imagen con fondo transparente
            img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
            dibujo = ImageDraw.Draw(img)
            # Dibujar rectángulo redondeado con fondo y borde
            color_fondo = (240, 240, 240, 50)  # Gris muy claro y transparente
            color_borde = (0, 0, 0, 30)  # Negro muy transparente (color de sombra)
            # Usar radio de bordes redondeados de las constantes
            radio = BORDES_REDONDEADOS_CARATULA
            borde_grosor = 1
            # Ajustar coordenadas para que todos los bordes sean visibles
            mitad_borde = borde_grosor / 2
            # Dibujar rectángulo redondeado
            dibujo.rounded_rectangle(
                [(mitad_borde, mitad_borde), (ancho - mitad_borde, alto - mitad_borde)],
                radius=radio,
                fill=color_fondo,
                outline=color_borde,
                width=borde_grosor,
            )
            # Superponer estandarte de calidad si se especifica
            if etiqueta_calidad:
                img = CaratulaGeneral.superponer_estandarte_calidad(img, etiqueta_calidad, "inf_izq")
            return CTkImage(light_image=img, dark_image=img, size=(ancho, alto))
        except Exception as e:
            print(f"Error al crear imagen vacía: {e}")
            return None

    # Método privado para aplicar bordes redondeados
    @staticmethod
    def aplicar_bordes_redondeados(imagen, radio):
        try:
            # Asegurar que la imagen esté en modo RGBA
            if imagen.mode != "RGBA":
                imagen = imagen.convert("RGBA")
            # Crear una máscara con mayor resolución para antialiasing
            ancho, alto = imagen.size
            factor_escala = 4  # Factor de escalado para suavizar bordes
            ancho_escalado = ancho * factor_escala
            alto_escalado = alto * factor_escala
            radio_escalado = radio * factor_escala
            # Crear máscara escalada
            mascara_escalada = Image.new("L", (ancho_escalado, alto_escalado), 0)
            draw = ImageDraw.Draw(mascara_escalada)
            # Dibujar rectángulo redondeado en la máscara escalada
            draw.rounded_rectangle([(0, 0), (ancho_escalado, alto_escalado)], radius=radio_escalado, fill=255)
            # Redimensionar la máscara al tamaño original con suavizado
            mascara = mascara_escalada.resize((ancho, alto), Image.Resampling.LANCZOS)
            # Crear imagen final con transparencia
            imagen_redondeada = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
            imagen_redondeada.paste(imagen, (0, 0))
            imagen_redondeada.putalpha(mascara)
            return imagen_redondeada
        except Exception as e:
            print(f"Error al aplicar bordes redondeados: {e}")
            return imagen
