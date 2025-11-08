class Compra:
    def __init__(self, compra_id, proveedor_id, responsable, productos, fecha):
        self.compra_id = compra_id
        self.proveedor_id = proveedor_id
        self.responsable = responsable
        self.productos = productos
        self.fecha = fecha
        self.total = sum(p["subtotal"] for p in productos)

    def convertir(self):
        return {
            "compra_id": self.compra_id,
            "proveedor_id": self.proveedor_id,
            "responsable": self.responsable,
            "fecha": self.fecha,
            "productos": self.productos,
            "total": self.total
        }

    def __str__(self):
        return f"Compra {self.compra_id} | Proveedor ID: {self.proveedor_id} | Responsable: {self.responsable} | Total: ${self.total:.2f}"
