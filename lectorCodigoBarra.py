from productoRepository import ProductoRepository

class LectorCodigoBarra:
    def __init__(self):
        self.repo = ProductoRepository()

    def escanear(self):
        codigo = input("\nEscanea o ingresa el código de barras (igual al código del producto): ").strip()
        
        if len(codigo) == 13:
            codigo_base = codigo[:-1]
        else:
            codigo_base = codigo
        
        producto = self.buscar_por_codigo(codigo_base)
        if producto:
            print("\nProducto encontrado:")
            print(f"  ID: {producto.producto_id}")
            print(f"  Nombre: {producto.nombre}")
            print(f"  Precio: ${producto.precio:.2f}")
            print(f"  Stock: {producto.stock}")
            print(f"  Código: {producto.codigo}")
            print(f"  Categoría: {producto.categoria_id}")
            print(f"  Descripción: {producto.descripcion}")
            return producto
        else:
            print(f"No se encontró producto con código: {codigo}")
            return None

    def buscar_por_codigo(self, codigo):
        for p in self.repo.productos:
            if p.codigo == codigo:
                return p
        return None

if __name__ == "__main__":
    lector = LectorCodigoBarra()
    lector.escanear()
