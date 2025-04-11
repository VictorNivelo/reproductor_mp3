import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.modelo.cancion import Cancion
from PIL import Image, ImageTk
from pathlib import Path
import unittest
import io


class TestCancionObtenerCaratula(unittest.TestCase):
    def setUp(self):
        # Create a mock image for testing
        self.test_image_bytes = self._crear_imagen_test()

        # Create a test song with a cover
        self.cancion_con_caratula = Cancion(
            ruta=Path("C:\\Users\\Victor\\Music\\Musica\\444..mp3"),
            titulo="Canción de prueba",
            artista="Artista de prueba",
            album="Álbum de prueba",
            caratula=self.test_image_bytes,
        )

        # Create a test song without a cover
        self.cancion_sin_caratula = Cancion(
            ruta=Path("C:\\Users\\Victor\\Music\\Musica\\444..mp3"),
            titulo="Canción sin caratula",
            artista="Artista de prueba",
            album="Álbum de prueba",
        )

    def _crear_imagen_test(self, ancho=100, alto=100):
        image = Image.new("RGB", (ancho, alto), color="red")
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        return img_bytes.getvalue()

    def test_obtener_caratula_formato_bytes(self):
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(formato="bytes")
        self.assertEqual(resultado, self.test_image_bytes)
        self.assertIsInstance(resultado, bytes)

    def test_obtener_caratula_formato_pil(self):
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(formato="PIL")
        self.assertIsInstance(resultado, Image.Image)
        self.assertEqual(resultado.width, 100)
        self.assertEqual(resultado.height, 100)

    def test_obtener_caratula_formato_tk(self):
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(formato="tk")
        self.assertIsInstance(resultado, ImageTk.PhotoImage)
        self.assertEqual(resultado.width(), 100)
        self.assertEqual(resultado.height(), 100)

    def test_obtener_caratula_redimensionar_ancho(self):
        ancho_deseado = 50
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(formato="PIL", ancho=ancho_deseado)
        self.assertEqual(resultado.width, ancho_deseado)
        # Height should be proportionally reduced
        self.assertEqual(resultado.height, 50)  # Since original is 100x100, 50% reduction

    def test_obtener_caratula_redimensionar_alto(self):
        alto_deseado = 50
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(formato="PIL", alto=alto_deseado)
        self.assertEqual(resultado.height, alto_deseado)
        # Width should be proportionally reduced
        self.assertEqual(resultado.width, 50)  # Since original is 100x100, 50% reduction

    def test_obtener_caratula_redimensionar_ambos(self):
        ancho_deseado = 75
        alto_deseado = 50
        resultado = self.cancion_con_caratula.obtener_caratula_cancion(
            formato="PIL", ancho=ancho_deseado, alto=alto_deseado
        )
        self.assertEqual(resultado.width, ancho_deseado)
        self.assertEqual(resultado.height, alto_deseado)

    def test_obtener_caratula_formato_invalido(self):
        with self.assertRaises(ValueError):
            self.cancion_con_caratula.obtener_caratula_cancion(formato="formato_inexistente")

    def test_obtener_caratula_sin_caratula(self):
        resultado = self.cancion_sin_caratula.obtener_caratula_cancion()
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
