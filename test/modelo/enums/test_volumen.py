import sys
import os
import unittest

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.modelo.enums.enum_volumen import Volumen


class TestVolumen(unittest.TestCase):

    def test_valores_enum(self):
        self.assertEqual(Volumen.SILENCIADO.value, 0)
        self.assertEqual(Volumen.SIN_VOLUMEN.value, 0)
        self.assertEqual(Volumen.BAJO.value, 33)
        self.assertEqual(Volumen.MEDIO.value, 66)
        self.assertEqual(Volumen.ALTO.value, 100)

    def test_silenciado_sin_volumen_son_aliases(self):
        self.assertIs(Volumen.SILENCIADO, Volumen.SIN_VOLUMEN)

    def test_nombre_silenciado(self):
        self.assertEqual(Volumen.SILENCIADO.nombre, "Silenciado")

    def test_nombre_bajo(self):
        self.assertEqual(Volumen.BAJO.nombre, "Volumen Medio")

    def test_nombre_medio(self):
        self.assertEqual(Volumen.MEDIO.nombre, "Volumen Alto")

    def test_nombre_alto(self):
        self.assertEqual(Volumen.ALTO.nombre, "Volumen Alto")

    def test_todos_los_miembros_existen(self):
        miembros = [e.name for e in Volumen]
        self.assertIn("SILENCIADO", miembros)
        self.assertIn("BAJO", miembros)
        self.assertIn("MEDIO", miembros)
        self.assertIn("ALTO", miembros)

    def test_cantidad_miembros(self):
        # Solo cuenta miembros únicos, no aliases
        self.assertEqual(len(list(Volumen)), 4)


if __name__ == "__main__":
    unittest.main()
