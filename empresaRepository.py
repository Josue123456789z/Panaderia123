import json
import os
from empresa import Empresa

class EmpresaRepository:
    def __init__(self, archivo="empresa.json"):
        self.archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), archivo)
        self.empresa = None
        self.cargar_empresa()

    def cargar_empresa(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    empresa_data = data[0]
                    self.empresa = Empresa(
                        nombre=empresa_data.get("nombre", ""),
                        correo=empresa_data.get("correo", ""),
                        telefono=empresa_data.get("telefono", ""),
                        direccion=empresa_data.get("direccion", "")
                    )
                else:
                    self.empresa = None
        else:
            self.empresa = None

