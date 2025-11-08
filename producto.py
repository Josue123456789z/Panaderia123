class Producto:
    def  __init__(self,id, nombre, precio,codigo,stock, categoria_id,descripcion):
        self.producto_id = id
        self.nombre = nombre
        self.precio = precio
        self.codigo = codigo
        self.stock = stock
        self.categoria_id = categoria_id
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.producto_id}. {self.nombre} {self.precio} {self.stock} {self.categoria_id}"
    
    def convertir(self):
        return {
            "producto_id" : self.producto_id,
            "nombre": self.nombre,
            "precio": self.precio,
            "codigo": self.codigo,
            "stock": self.stock,
            "categoria_id": self.categoria_id,
            "descripcion" : self.descripcion
        }