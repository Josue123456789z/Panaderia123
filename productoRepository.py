import json
from producto import Producto
from generarCodigoBarra import GenerarCodigoBarra
import os

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")
        
class ProductoRepository:
    def __init__(self, archivo="productos.json"):
        self.archivo = archivo
        self.productos = []
        self.read()

    def read(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as contenido:
                data_json = json.load(contenido)
            self.productos = []

            for line in data_json:
                prod = Producto(
                    line['producto_id'], line['nombre'], line['precio'],
                    line['codigo'], line['stock'], line['categoria_id'], line['descripcion']
                )
                self.productos.append(prod)

        except FileNotFoundError:
            print("No existe productos.json, se creará uno nuevo.")
            self.save()

    def save(self):
        datos = [item.convertir() for item in self.productos]
        with open(self.archivo, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)

    def select_all(self):
        return self.productos

    def select_by_id(self, id):
        for item in self.productos:
            if item.producto_id == id:
                return item
        return None

    def add(self, producto):
        self.productos.append(producto)
        self.save()

    def get_id(self):
        return max([item.producto_id for item in self.productos], default=0)

    def agregar_producto(self):
        while True:
            limpiar_pantalla()
            print("\n--- AGREGAR NUEVO PRODUCTO ---")
            nuevo_id = self.get_id() + 1
            nombre = input("Nombre del producto: ").strip()
            precio = float(input("Precio: "))
            stock = int(input("Stock disponible: "))
            categoria_id = int(input("ID de categoría: "))
            descripcion = input("Descripción: ").strip()

            generador = GenerarCodigoBarra()
            codigo_barra = generador.generar(nuevo_id, categoria_id)

            if input("¿Generar imagen del código de barras? (s/n): ").lower() == 's':
                generador.generar_imagen(codigo_barra, f"producto_{nuevo_id}_{nombre.replace(' ', '_')}")

            producto = Producto(nuevo_id, nombre, precio, codigo_barra, stock, categoria_id, descripcion)
            self.add(producto)
            print(f"\nProducto '{nombre}' agregado correctamente.")
            print(f"Código de barras: {codigo_barra}")

            opcion = input("\n¿Desea agregar otro producto? (s/n): ").lower()
            if opcion != 's':
                break

    def eliminar_producto(self):
        while True:
            limpiar_pantalla()
            codigo_eliminar = input("Ingrese el código del producto a eliminar: ")
            for p in self.productos:
                if p.codigo == codigo_eliminar:
                    self.productos.remove(p)
                    self.save()
                    print(f"Producto '{p.nombre}' eliminado correctamente.")
                    break
            else:
                print("No se encontró un producto con ese código.")

            opcion = input("\n¿Desea eliminar otro producto? (s/n): ").lower()
            if opcion != 's':
                break

    def buscar_producto(self):
        while True:
            limpiar_pantalla()
            codigo_buscar = input("Ingrese el código del producto a buscar: ")
            producto = None
            for p in self.productos:
                if p.codigo == codigo_buscar:
                    producto = p
                    break

            if producto:
                print(f"Producto encontrado: ID {producto.producto_id}")
                print(f"Nombre: {producto.nombre}")
                print(f"Precio: {producto.precio}")
                print(f"Stock: {producto.stock}")
                print(f"Categoría ID: {producto.categoria_id}")
                print(f"Descripción: {producto.descripcion}")
            else:
                print("No se encontró un producto con ese código.")

            opcion = input("\n¿Desea buscar otro producto? (s/n): ").lower()
            if opcion != 's':
                break

    def mostrar_productos(self):
        limpiar_pantalla()
        if not self.productos:
            print("No hay productos disponibles.")
        else:
            print("\n--- LISTA DE PRODUCTOS ---")
            for p in self.productos:
                print(f"ID: {p.producto_id} | Nombre: {p.nombre} | Precio: ${p.precio:.2f} | Stock: {p.stock} | Código: {p.codigo}")
        input("\nPresiona Enter para continuar...")

def menu():
    repo = ProductoRepository()

    while True:
        limpiar_pantalla()
        print("\n====== MENÚ DE PRODUCTOS ======")
        print("1. Agregar Producto")
        print("2. Mostrar Productos")
        print("3. Eliminar Producto")
        print("4. Buscar Producto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            repo.agregar_producto()
        elif opcion == "2":
            repo.mostrar_productos()
        elif opcion == "3":
            repo.eliminar_producto()
        elif opcion == "4":
            repo.buscar_producto()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intenta otra vez.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    menu()
