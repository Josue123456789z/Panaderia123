class Cliente:
    def __init__(self, id, nombre, telefono, correo):
        self.cliente_id = id
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"{self.cliente_id}. {self.nombre} | {self.telefono} | {self.correo}"

    def convertir(self):
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo
        }