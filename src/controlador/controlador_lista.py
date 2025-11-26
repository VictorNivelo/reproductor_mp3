import json

from modelo.lista_reproduccion import ListaReproduccion
from modelo.cancion import Cancion
from typing import List, Dict


class ControladorLista:

    def __init__(self):
        self.listas_reproduccion = []
        self.lista_actual = None

    # Crear una nueva lista de reproducción
    def crear_lista(self, nombre: str) -> ListaReproduccion | None:
        try:
            if not nombre or nombre.strip() == "":
                print("El nombre de la lista no puede estar vacío")
                return None
            # Verificar si ya existe una lista con ese nombre
            if self.existe_lista(nombre):
                print(f"Ya existe una lista con el nombre: {nombre}")
                return None
            nueva_lista = ListaReproduccion(nombre)
            self.listas_reproduccion.append(nueva_lista)
            print(f"Lista de reproducción '{nombre}' creada exitosamente")
            return nueva_lista
        except Exception as e:
            print(f"Error al crear lista: {str(e)}")
            return None

    # Renombrar una lista de reproducción
    def renombrar_lista(self, lista: ListaReproduccion, nuevo_nombre: str) -> bool:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return False
            if not nuevo_nombre or nuevo_nombre.strip() == "":
                print("El nuevo nombre no puede estar vacío")
                return False
            # Verificar si ya existe una lista con el nuevo nombre
            if any(
                l.nombre_lista.lower() == nuevo_nombre.lower() and l != lista
                for l in self.listas_reproduccion
            ):
                print(f"Ya existe una lista con el nombre: {nuevo_nombre}")
                return False
            nombre_anterior = lista.nombre_lista
            lista.nombre_lista = nuevo_nombre
            lista.fecha_modificacion_lista = __import__("datetime").datetime.now()
            print(f"Lista renombrada de '{nombre_anterior}' a '{nuevo_nombre}'")
            return True
        except Exception as e:
            print(f"Error al renombrar lista: {str(e)}")
            return False

    # Eliminar una lista de reproducción
    def eliminar_lista(self, lista: ListaReproduccion) -> bool:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista '{lista.nombre_lista}' no existe")
                return False
            # Si es la lista actual, desvincularla
            if self.lista_actual == lista:
                self.lista_actual = None
            self.listas_reproduccion.remove(lista)
            print(f"Lista de reproducción '{lista.nombre_lista}' eliminada")
            return True
        except Exception as e:
            print(f"Error al eliminar lista: {str(e)}")
            return False

    # Eliminar una lista de reproducción por nombre
    def eliminar_lista_por_nombre(self, nombre: str) -> bool:
        try:
            lista = self.obtener_lista_por_nombre(nombre)
            if lista is None:
                print(f"No se encontró la lista: {nombre}")
                return False
            return self.eliminar_lista(lista)
        except Exception as e:
            print(f"Error al eliminar lista por nombre: {str(e)}")
            return False

    # Agregar una canción a una lista de reproducción
    def agregar_cancion_a_lista(self, lista: ListaReproduccion, cancion: Cancion) -> bool:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return False
            resultado = lista.agregar_cancion_lista(cancion)
            if resultado:
                print(f"Canción '{cancion.titulo_cancion}' agregada a la lista '{lista.nombre_lista}'")
            else:
                print(f"La canción ya existe en la lista '{lista.nombre_lista}'")
            return resultado
        except Exception as e:
            print(f"Error al agregar canción a la lista: {str(e)}")
            return False

    # Agregar múltiples canciones a una lista de reproducción
    def agregar_multiples_canciones_a_lista(self, lista: ListaReproduccion, canciones: List[Cancion]) -> int:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return 0
            agregadas = 0
            for cancion in canciones:
                if lista.agregar_cancion_lista(cancion):
                    agregadas += 1
            print(f"Se agregaron {agregadas} de {len(canciones)} canciones a la lista '{lista.nombre_lista}'")
            return agregadas
        except Exception as e:
            print(f"Error al agregar múltiples canciones: {str(e)}")
            return 0

    # Eliminar una canción de una lista de reproducción
    def eliminar_cancion_de_lista(self, lista: ListaReproduccion, cancion: Cancion) -> bool:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return False
            resultado = lista.eliminar_cancion_lista(cancion)
            if resultado:
                print(f"Canción '{cancion.titulo_cancion}' eliminada de la lista '{lista.nombre_lista}'")
            else:
                print(f"La canción no existe en la lista '{lista.nombre_lista}'")
            return resultado
        except Exception as e:
            print(f"Error al eliminar canción de la lista: {str(e)}")
            return False

    # Mover una canción a otra posición en la lista de reproducción
    def mover_cancion_en_lista(
        self, lista: ListaReproduccion, indice_origen: int, indice_destino: int
    ) -> bool:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return False
            resultado = lista.mover_cancion_lista(indice_origen, indice_destino)
            if resultado:
                print(f"Canción movida de posición {indice_origen} a {indice_destino}")
            else:
                print(f"No se pudo mover la canción. Verifica los índices")
            return resultado
        except Exception as e:
            print(f"Error al mover canción: {str(e)}")
            return False

    # Verificar si existe una lista de reproducción con ese nombre
    def existe_lista(self, nombre: str) -> bool:
        return any(lista.nombre_lista.lower() == nombre.lower() for lista in self.listas_reproduccion)

    # Obtener una lista de reproducción por nombre
    def obtener_lista_por_nombre(self, nombre: str) -> ListaReproduccion | None:
        for lista in self.listas_reproduccion:
            if lista.nombre_lista.lower() == nombre.lower():
                return lista
        return None

    # Obtener una lista de reproducción por ID
    def obtener_lista_por_id(self, id_lista: str) -> ListaReproduccion | None:
        for lista in self.listas_reproduccion:
            if lista.id_lista == id_lista:
                return lista
        return None

    # Obtener todas las listas de reproducción
    def obtener_todas_listas(self) -> List[ListaReproduccion]:
        return self.listas_reproduccion

    # Obtener la lista de reproducción actual
    def obtener_lista_actual(self) -> ListaReproduccion | None:
        return self.lista_actual

    # Obtener todas las canciones de una lista de reproducción
    def obtener_canciones_lista(self, lista: ListaReproduccion) -> List[Cancion]:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return []
            canciones = lista.obtener_lista_cancion()
            if not canciones:
                print(f"La lista '{lista.nombre_lista}' está vacía")
                return []
            return canciones
        except Exception as e:
            print(f"Error al obtener canciones: {str(e)}")
            return []

    # Obtener el total de canciones en una lista de reproducción
    def obtener_total_canciones_lista(self, lista: ListaReproduccion) -> int:
        try:
            if lista not in self.listas_reproduccion:
                return 0
            return len(lista.obtener_lista_cancion())
        except Exception as e:
            print(f"Error al obtener total de canciones: {str(e)}")
            return 0

    # Obtener todas las listas de reproducción como información
    def obtener_informacion_todas_listas(self) -> List[Dict]:
        try:
            return [
                {
                    "id": lista.id_lista,
                    "nombre": lista.nombre_lista,
                    "total_canciones": len(lista.lista_cancion),
                    "fecha_creacion": lista.fecha_creacion_lista.strftime("%d/%m/%Y %H:%M:%S"),
                }
                for lista in self.listas_reproduccion
            ]
        except Exception as e:
            print(f"Error al obtener información de listas: {str(e)}")
            return []

    # Imprimir todas las canciones de una lista de reproducción
    def imprimir_canciones_lista(self, lista: ListaReproduccion) -> None:
        try:
            if lista not in self.listas_reproduccion:
                print(f"La lista no existe")
                return
            informacion = lista.obtener_informacion_lista()
            canciones = informacion.get("canciones", [])
            print(f"----------------------- canciones en {lista.nombre_lista} -----------------------")
            print(json.dumps(canciones, indent=2, ensure_ascii=False))
            print("----------------------------------------------------------------------------------")
        except Exception as e:
            print(f"Error al imprimir canciones: {str(e)}")

    # Imprimir todas las listas de reproducción
    def imprimir_todas_listas(self) -> None:
        try:
            if not self.listas_reproduccion:
                print("No hay listas de reproducción creadas")
                return
            listas_info = self.obtener_informacion_todas_listas()
            print("-------------------- Listas de reproducción --------------------")
            print(json.dumps(listas_info, indent=2, ensure_ascii=False))
            print("----------------------------------------------------------------")
        except Exception as e:
            print(f"Error al imprimir listas: {str(e)}")

    # Imprimir todas las listas de reproducción con sus canciones
    def imprimir_listas_con_canciones(self) -> None:
        try:
            if not self.listas_reproduccion:
                print("No hay listas de reproducción creadas")
                return
            listas_completas = [lista.obtener_informacion_lista() for lista in self.listas_reproduccion]
            print("---------------- Listas de reproducción con canciones ----------------")
            print(json.dumps(listas_completas, indent=2, ensure_ascii=False))
            print("----------------------------------------------------------------------")
        except Exception as e:
            print(f"Error al imprimir listas con canciones: {str(e)}")
