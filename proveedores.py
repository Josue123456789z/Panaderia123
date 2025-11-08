class Proveedores:
    def __init__(self, proveedor_id, nombre, contacto, telefono, email):
        self.proveedor_id = proveedor_id
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.proveedor_id}. {self.nombre} | Contacto: {self.contacto} | Tel: {self.telefono} | Email: {self.email}"

    def convertir(self):
        return {
            "proveedor_id": self.proveedor_id,
            "nombre": self.nombre,
            "contacto": self.contacto,
            "telefono": self.telefono,
            "email": self.email
        }