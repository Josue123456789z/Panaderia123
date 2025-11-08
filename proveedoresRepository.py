import json
import os
from proveedores import Proveedores  

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

class ProveedoresRepository:
    def __init__(self, archivo="proveedores.json"):
        self.archivo = archivo
        self.proveedores = []
        self.cargar_proveedores()

    def cargar_proveedores(self):
        if not os.path.exists(self.archivo):
            self.guardar_proveedores()
            return
        with open(self.archivo, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                self.proveedores = [Proveedores(**p) for p in data]
            except json.JSONDecodeError:
                self.proveedores = []

    def guardar_proveedores(self):
        with open(self.archivo, "w", encoding="utf-8") as file:
            json.dump([p.convertir() for p in self.proveedores], file, indent=4, ensure_ascii=False)

    def get_id(self):
        return max([p.proveedor_id for p in self.proveedores], default=0)

    def agregar_proveedor(self):
        limpiar_pantalla()
        print("\n--- AGREGAR NUEVO PROVEEDOR ---")

        nombre = input("Nombre del proveedor: ")
        contacto = input("Nombre de la persona de contacto: ")
        telefono = input("Teléfono: ")
        email = input("Correo electrónico: ")

        nuevo_id = self.get_id() + 1
        nuevo_proveedor = Proveedores(nuevo_id, nombre, contacto, telefono, email)
        self.proveedores.append(nuevo_proveedor)
        self.guardar_proveedores()

        print(f"\nProveedor '{nombre}' agregado correctamente.")
        input("\nPresione Enter para continuar...")

    def listar_proveedores(self):
        limpiar_pantalla()
        if not self.proveedores:
            print("No hay proveedores registrados.")
        else:
            print("\nLISTA DE PROVEEDORES:")
            for p in self.proveedores:
                print(p)
        input("\nPresione Enter para continuar...")

    def eliminar_proveedor(self):
        limpiar_pantalla()
        try:
            id_eliminar = int(input("Ingrese el ID del proveedor a eliminar: "))
            for p in self.proveedores:
                if p.proveedor_id == id_eliminar:
                    self.proveedores.remove(p)
                    self.guardar_proveedores()
                    print(f"\nProveedor '{p.nombre}' eliminado correctamente.")
                    break
            else:
                print("No se encontró un proveedor con ese ID.")
        except ValueError:
            print("El ID debe ser un número entero.")
        input("\nPresione Enter para continuar...")

    def buscar_por_id(self, proveedor_id):
        for p in self.proveedores:
            if p.proveedor_id == proveedor_id:
                return p
        return None


def menu_proveedores():
    repo = ProveedoresRepository()

    while True:
        limpiar_pantalla()
        print("\n===== MENÚ DE PROVEEDORES =====")
        print("1. Listar proveedores")
        print("2. Agregar proveedor")
        print("3. Eliminar proveedor")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            repo.listar_proveedores()
        elif opcion == "2":
            repo.agregar_proveedor()
        elif opcion == "3":
            repo.eliminar_proveedor()
        elif opcion == "4":
            print("Saliendo del menú de proveedores...")
            break
        else:
            print("Opción inválida, intente de nuevo.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu_proveedores()

