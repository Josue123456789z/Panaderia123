
from categoria import Categoria
from productoRepository import ProductoRepository
from producto import Producto  # Corregido: Debe ser 'producto.py' con clase Producto
from categoriaRepository import CategoriaRepository
from barcode import EAN13
from barcode.writer import ImageWriter
import os

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")


class GenerarCodigoBarra:
    def generar(self, producto_id, categoria_id):
        codigo_cat = str(categoria_id).zfill(2)
        codigo_pro = str(producto_id).zfill(10)
        codigo_base = codigo_cat + codigo_pro
        suma = 0
        for i in range(len(codigo_base)):
            digito = int(codigo_base[i])
            if i % 2 == 0:
                suma = suma + (digito * 3)
            else:
                suma = suma + digito
        digito_verificador = (10 - (suma % 10)) % 10
        result = codigo_base + str(digito_verificador)
        return result

class App:
    def __init__(self):
        self.repo_categoria = CategoriaRepository()
        self.repo_producto = ProductoRepository()
        self.generador = GenerarCodigoBarra()
        self.agregar_producto()

    def agregar_producto(self):
        print("Listado de Categorias")
        for item in self.repo_categoria.select_all():
            print(item)

        nombre = input("Nombre del producto: ").strip()
        precio = float(input("Escriba el precio: $ "))
        categoria_id = int(input("Escriba el id de la categoria: "))
        stock = int(input("Escriba el stock: "))
        descripcion = input("Escriba la descripcion del producto: ")

        categoria = self.repo_categoria.select_by_id(categoria_id)
        if categoria is None:
            print("La categoria no existe!")
            return

        id = self.repo_producto.get_id() + 1 
        codigo_barra = self.generador.generar(id, categoria_id)

        producto = Producto(id, nombre, precio, codigo_barra, stock, categoria_id, descripcion)
        self.repo_producto.add(producto)
        print("Producto Agregado con exito!")
        print("Codigo de barra: " + codigo_barra)

        # Generar la imagen del código de barras
        codigo_objeto = EAN13(codigo_barra, writer=ImageWriter())
        carpeta = "codebars"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        nombre_archivo = f"{carpeta}/{codigo_barra}"
        ruta_guardado = codigo_objeto.save(nombre_archivo)
        print(f"Imagen guardada como: {ruta_guardado}.png")

if __name__ == "__main__":
    limpiar_pantalla()
    app = App()

