import json
import os

class Inventario:
    def __init__(self):
        self.productos = [] 

    def cargar_desde_archivo(self, ruta):
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as archivo:
                    self.productos = json.load(archivo)
                print("Inventario cargado correctamente.")
            except:
                print("Error en el archivo. Empezando vacío.")
        else:
            print("No se encontró productos.json, inventario vacío.")

    def guardar_en_archivo(self, ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(self.productos, archivo, indent=4)
        print("Inventario guardado correctamente.")
        
    def mostrar_inventario(self):
        if not self.productos:
            print("No hay productos en el inventario.")
        else:
            print("\nINVENTARIO:")
            for i in self.productos:
                print(f"Código: {i['codigo']} | Nombre: {i['nombre']} | "
                      f"Precio: ${i['precio']:.2f} | Stock: {i['stock']} | "
                      f"Categoría ID: {i['categoria_id']}")
        input("\nPresiona ENTER para continuar...")

    def añadir_producto(self):
        print("\n--- Añadir Producto ---")
        codigo = input("Código: ").strip()
        nombre = input("Nombre: ").strip()
        while True:
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                categoria_id = int(input("ID Categoría: "))
                break
            except:
                print("Solo números.")
        nuevo = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "stock": stock,
            "categoria_id": categoria_id
        }
        self.productos.append(nuevo)
        print("Producto añadido.")
        input("ENTER...")

    def eliminar_producto(self):
        codigo = input("\nCódigo a eliminar: ").strip()
        for i in self.productos:
            if i["codigo"] == codigo:
                self.productos.remove(i)
                print("Producto eliminado.")
                input("ENTER...")
                return
        print("No encontrado.")
        input("ENTER...")

    def buscar_por_codigo(self):
        codigo = input("\nBuscar código: ").strip()
        for i in self.productos:
            if i["codigo"] == codigo:
                print("Encontrado:")
                print(f"Código: {i['codigo']} | {i['nombre']} | ${i['precio']:.2f} | Stock: {i['stock']}")
                input("ENTER...")
                return
        print("No existe.")
        input("ENTER...")

def menu_inventario():
    inventario = Inventario()
    inventario.cargar_desde_archivo("productos.json")

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("""
==============================
     MENÚ INVENTARIO
==============================
1. Ver inventario
2. Añadir producto
3. Eliminar producto
4. Buscar por código
5. Guardar y salir
""")
        opcion = input("Elige: ").strip()

        if opcion == "1":
            inventario.mostrar_inventario()
        elif opcion == "2":
            inventario.añadir_producto()
        elif opcion == "3":
            inventario.eliminar_producto()
        elif opcion == "4":
            inventario.buscar_por_codigo()
        elif opcion == "5":
            inventario.guardar_en_archivo("productos.json")
            print("Guardado")
            break
        else:
            print("Opción inválida.")
            input("ENTER...")


if __name__ == "__main__":
    menu_inventario()