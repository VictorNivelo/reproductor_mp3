# Pone el directorio padre en el path para poder importar src.constantes
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from src.constantes import *
import unittest
import sys
import os


# Clase de pruebas unitarias
class TestConstantes(unittest.TestCase):
    # Método que se ejecuta antes de cada prueba
    def setUp(self):
        self.ruta_test = os.path.dirname(os.path.dirname(__file__))

    # Metodo que testea si los directorios existen
    def test_directorios_existen(self):
        self.assertTrue(os.path.exists(RUTA_BASE), "RUTA_BASE no existe")
        self.assertTrue(os.path.exists(RUTA_RECURSOS), "RUTA_RECURSOS no existe")
        self.assertTrue(os.path.exists(RUTA_ICONOS), "RUTA_ICONOS no existe")
        self.assertTrue(os.path.exists(RUTA_IMAGENES), "RUTA_IMAGENES no existe")

    # Método que testea si las rutas de los iconos de la aplicación existen
    def test_obtener_ruta_iconos_especiales(self):
        ruta_esperada = os.path.join(RUTA_ICONOS, "me_gusta_rojo.png")
        ruta_actual = obtener_ruta_iconos("me_gusta_rojo", "claro")
        self.assertEqual(ruta_actual, ruta_esperada)
        ruta_esperada = os.path.join(RUTA_ICONOS, "favorito_amarillo.png")
        ruta_actual = obtener_ruta_iconos("favorito_amarillo", "oscuro")
        self.assertEqual(ruta_actual, ruta_esperada)

    # Método que testea si las rutas de los iconos de los temas existen
    def test_obtener_ruta_iconos_temas(self):
        ruta_esperada = os.path.join(RUTA_ICONOS, "claro", "reproducir_claro.png")
        ruta_actual = obtener_ruta_iconos("reproducir", "claro")
        self.assertEqual(ruta_actual, ruta_esperada)
        ruta_esperada = os.path.join(RUTA_ICONOS, "oscuro", "reproducir_oscuro.png")
        ruta_actual = obtener_ruta_iconos("reproducir", "oscuro")
        self.assertEqual(ruta_actual, ruta_esperada)

    # Método que testea si las rutas de los iconos de los botones existen
    def test_constantes_dimensiones(self):
        self.assertEqual(ANCHO_PRINCIPAL, 1200)
        self.assertEqual(ALTO_PRINCIPAL, 720)
        self.assertEqual(ANCHO_CONFIGURACION, 400)
        self.assertEqual(ALTO_CONFIGURACION, 500)
        self.assertEqual(ANCHO_MINI_REPRODUCTOR, 355)
        self.assertEqual(ALTO_MINI_REPRODUCTOR, 125)
        self.assertEqual(ANCHO_PANEL_DERECHA, 435)
        self.assertEqual(ALTO_TABVIEW, 400)

    # Método que testea si las rutas de los iconos de los botones existen
    def test_constantes_colores(self):
        colores = [
            CLARO,
            CLARO_SEGUNDARIO,
            FONDO_PRINCIPAL_CLARO,
            FONDO_CLARO,
            TEXTO_CLARO,
            BOTON_CLARO,
            HOVER_CLARO,
            OSCURO,
            OSCURO_SEGUNDARIO,
            FONDO_PRINCIPAL_OSCURO,
            FONDO_OSCURO,
            TEXTO_OSCURO,
            BOTON_OSCURO,
            HOVER_OSCURO,
        ]
        for color in colores:
            self.assertTrue(color.startswith("#"))
            self.assertTrue(len(color) == 7)
            self.assertTrue(all(c in "0123456789abcdefABCDEF" for c in color[1:]))

    # Método que testea si las rutas de los iconos de los botones existen
    def test_variables_estado_inicial(self):
        self.assertEqual(TEMA_ACTUAL, "claro")
        self.assertFalse(REPRODUCIENDO)
        self.assertFalse(SILENCIADO)
        self.assertTrue(PANEL_VISIBLE)
        self.assertTrue(ORDEN)
        self.assertEqual(REPETICION, 0)
        self.assertEqual(VOLUMEN, 100)
        self.assertFalse(ME_GUSTA)
        self.assertFalse(FAVORITO)
        self.assertFalse(ARRASTRANDO_PROGRESO)
        self.assertEqual(DURACION_TOTAL, 0)
        self.assertEqual(TIEMPO_ACTUAL, 0)


if __name__ == "__main__":
    unittest.main()
