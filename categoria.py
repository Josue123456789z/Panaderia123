class Categoria:
    def __init__(self, categoria_id, nombre):
        self.categoria_id = categoria_id
        self.nombre = nombre

    def __str__(self):
        return f"{self.categoria_id}. {self.nombre}"


