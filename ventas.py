class Ventas:
    def __init__(self, venta_id, cliente_id, productos, fecha):
        self.venta_id = venta_id
        self.cliente_id = cliente_id
        self.productos = productos
        self.fecha = fecha
        self.total = sum(p["subtotal"] for p in productos)

    def convertir(self):
        return {
            "venta_id": self.venta_id,
            "cliente_id": self.cliente_id,
            "productos": self.productos,
            "fecha": self.fecha,
            "total": self.total
        }

    def __str__(self):
        return f"Venta {self.venta_id} | Cliente ID: {self.cliente_id} | Total: ${self.total:.2f}"
