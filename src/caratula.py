from PIL import Image, ImageDraw, ImageTk
from customtkinter import CTkImage

import io


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
        except Exception:
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

    # Método que procesa la carátula y la devuelve en el formato solicitado
    @staticmethod
    def procesar_caratula(
        caratula_bytes, formato="bytes", ancho=None, alto=None, bordes_redondeados=False, radio_borde=None
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
                    # Mantener proporciones si solo se especifica el ancho
                    proporcion = ancho / imagen_pil.width
                    alto = int(imagen_pil.height * proporcion)
                elif alto and not ancho:
                    # Mantener proporciones si solo se especifica el alto
                    proporcion = alto / imagen_pil.height
                    ancho = int(imagen_pil.width * proporcion)
                imagen_pil = imagen_pil.resize((ancho, alto), Image.Resampling.LANCZOS)
            # Aplicar bordes redondeados si se solicita
            if bordes_redondeados:
                imagen_pil = CaratulaGeneral.aplicar_bordes_redondeados(imagen_pil, radio_borde)
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

    # Método que crea una caratula vacia
    @staticmethod
    def crear_caratula_vacia():
        try:
            img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            return CTkImage(light_image=img, dark_image=img, size=(1, 1))
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
