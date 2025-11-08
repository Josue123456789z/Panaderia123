import os
from productoRepository import menu as menu_productos
from categoriaRepository import menu_categorias
from inventario import menu_inventario
from clienteRepository import menu as menu_clientes
from ventasRepository import menu_ventas
from comprasRepository import menu_compras
from proveedoresRepository import menu_proveedores

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

def main():
    while True:
        limpiar_pantalla()
        print("="*33)
        print("| SISTEMA DE PANADERÍA |".center(33))
        print("="*33)
        print("1. Menú de Productos")
        print("2. Menú de Categorías")
        print("3. Menú de Inventario")
        print("4. Menú de Clientes")
        print("5. Menú de Ventas")
        print("6. Menú de Compras")
        print("7. Menú de Proveedores")
        print("8. Salir")
        print("="*33)
        opcion = input("Elige una opción (1-8): ").strip()

        if opcion == "1":
            menu_productos()
        elif opcion == "2":
            menu_categorias()
        elif opcion == "3":
            menu_inventario()
        elif opcion == "4":
            menu_clientes()
        elif opcion == "5":
            menu_ventas()
        elif opcion == "6":
            menu_compras()
        elif opcion == "7":
            menu_proveedores()
        elif opcion == "8":
            confirm = input("¿Seguro que deseas salir? (s/n): ").lower()
            if confirm == "s":
                limpiar_pantalla()
                print("Gracias por usar el sistema. ¡Hasta pronto!")
                break

print(main())

