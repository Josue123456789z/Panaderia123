class Compra:
    def __init__(self, compra_id, proveedor_id, productos, fecha):
        self.compra_id = compra_id
        self.proveedor_id = proveedor_id
        self.productos = productos
        self.fecha = fecha
        self.total = sum(p["subtotal"] for p in productos)

    def convertir(self):
        return {
            "compra_id": self.compra_id,
            "proveedor_id": self.proveedor_id,
            "productos": self.productos,
            "fecha": self.fecha,
            "total": self.total
        }

    def __str__(self):
        return f"Compra {self.compra_id} | Proveedor ID: {self.proveedor_id} | Total: ${self.total:.2f}"

