import json
import os
from categoria import Categoria

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

class CategoriaRepository:
    def __init__(self, archivo="categoria.json"):
        self.archivo = archivo
        self.categorias = []
        self.read()

    def read(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as contenido:
                data_json = json.load(contenido)

            self.categorias = []
            
            for line in data_json:
                cat = Categoria(line['categoria_id'], line['nombre'])
                self.categorias.append(cat)
                
        except FileNotFoundError:
            print("No existe el archivo categoria.json, se creará vacío.")
            self.categorias = []
            self.save()

    def save(self):
        data = []
        for c in self.categorias:
            categoria_diccionario = {
                "categoria_id": c.categoria_id,
                "nombre": c.nombre
            }
            data.append(categoria_diccionario)

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def mostrar_categorias(self):
        limpiar_pantalla()
        if not self.categorias:
            print("No hay categorías registradas.")
        else:
            print("\nLISTA DE CATEGORÍAS:")
            for c in self.categorias:
                print(f"- {c.categoria_id} | {c.nombre}")

    def agregar_categoria(self):
        while True:
            limpiar_pantalla()
            try:
                nuevo_id = int(input("Ingrese el ID de la nueva categoría: "))
                nombre = input("Ingrese el nombre de la categoría: ")

                for c in self.categorias:
                    if c.categoria_id == nuevo_id:
                        print("Ya existe una categoría con ese ID.")
                        break
                else:
                    self.categorias.append(Categoria(nuevo_id, nombre))
                    self.save()
                    print("Categoría agregada exitosamente.")

            except ValueError:
                print("El ID debe ser un número entero.")

            opcion = input("\n¿Desea ingresar otra categoría? (s/n): ").lower()
            if opcion != "s":
                break

    def eliminar_categoria(self):
        while True:
            limpiar_pantalla()
            try:
                id_eliminar = int(input("Ingrese el ID de la categoría a eliminar: "))
                for c in self.categorias:
                    if c.categoria_id == id_eliminar:
                        self.categorias.remove(c)
                        self.save()
                        print("Categoría eliminada correctamente.")
                        break
                else:
                    print("No se encontró una categoría con ese ID.")

            except ValueError:
                print("El ID debe ser un número entero.")

            opcion = input("\n¿Desea eliminar otra categoría? (s/n): ").lower()
            if opcion != "s":
                break


def menu_categorias():
    repo = CategoriaRepository()

    while True:
        limpiar_pantalla()
        print("\n===== MENÚ DE CATEGORÍAS =====")
        print("1. Ver categorías")
        print("2. Ingresar nueva categoría")
        print("3. Eliminar categoría")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            repo.mostrar_categorias()
            input("\nPresione Enter para volver al menú.")
        elif opcion == "2":
            repo.agregar_categoria()
        elif opcion == "3":
            repo.eliminar_categoria()
        elif opcion == "4":
            limpiar_pantalla()
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu_categorias()
