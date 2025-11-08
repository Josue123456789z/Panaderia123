import json
import os
from cliente import Cliente

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

class ClienteRepository:
    def __init__(self, archivo="clientes.json"):
        self.archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), archivo)
        print(f"Usando archivo: {self.archivo}")
        self.clientes = []
        self.read()  

    def read(self):
        if not os.path.exists(self.archivo):
            print(f"Archivo no encontrado. Creando: {self.archivo}")
            self.save()
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as file:
                data = json.load(file)
            print(f"Cargados {len(data)} clientes.")
            self.clientes = [
                Cliente(c["cliente_id"], c["nombre"], c["telefono"], c["correo"])
                for c in data
            ]
        except KeyError as e:
            print(f"Error en JSON: clave faltante '{e}'")
            self.clientes = []
        except Exception as e:
            print(f"Error al leer: {e}")
            self.clientes = []

    def save(self):
        datos = [c.convertir() for c in self.clientes]
        try:
            with open(self.archivo, "w", encoding="utf-8") as file:
                json.dump(datos, file, indent=4, ensure_ascii=False)
            print("Guardado exitoso.")
        except Exception as e:
            print(f"Error al guardar: {e}")

    def get_id(self):
        return max((c.cliente_id for c in self.clientes), default=0)

    def add(self, cliente):
        self.clientes.append(cliente)
        self.save()

    def eliminar_por_id(self, id):
        self.clientes = [c for c in self.clientes if c.cliente_id != id]
        self.save()

    def buscar_por_id(self, id):
        return next((c for c in self.clientes if c.cliente_id == id), None)

    def buscar_por_nombre(self, nombre):
        return [c for c in self.clientes if nombre.lower() in c.nombre.lower()]

    def agregar_cliente(self):
        limpiar_pantalla()
        print("\n--- AGREGAR CLIENTE ---")
        try:
            nuevo_id = self.get_id() + 1
            nombre = input("Nombre: ").strip()
            telefono = input("Teléfono: ").strip()
            correo = input("Correo: ").strip()
            if not nombre or not telefono:
                print("Nombre y teléfono obligatorios.")
                input("Enter...")
                return
            self.add(Cliente(nuevo_id, nombre, telefono, correo))
            print(f"Cliente agregado (ID: {nuevo_id})")
        except Exception as e:
            print(f"Error: {e}")
        input("Enter...")

    def mostrar_clientes(self):
        limpiar_pantalla()
        if not self.clientes:
            print("No hay clientes registrados.")
        else:
            print("\nLISTA DE CLIENTES:")
            print("-" * 80)
            for c in self.clientes:
                print(c)
            print("-" * 80)
        input("Enter...")

    def eliminar_cliente(self):
        limpiar_pantalla()
        try:
            id = int(input("ID a eliminar: "))
            if self.buscar_por_id(id):
                self.eliminar_por_id(id)
                print("Eliminado.")
            else:
                print("No encontrado.")
        except:
            print("ID inválido.")
        input("Enter...")

    def buscar_cliente(self):
        limpiar_pantalla()
        op = input("1. Por ID | 2. Por nombre: ")
        if op == "1":
            try:
                id = int(input("ID: "))
                c = self.buscar_por_id(id)
                print(c or "No encontrado.")
            except:
                print("ID inválido.")
        elif op == "2":
            nombre = input("Nombre: ").lower()
            res = self.buscar_por_nombre(nombre)
            if res:
                for c in res: print(f"  {c}")
            else:
                print("No encontrado.")
        input("Enter...")

def menu():
    repo = ClienteRepository()
    while True:
        limpiar_pantalla()
        print("\n====== GESTIÓN DE CLIENTES ======")
        print("1. Agregar")
        print("2. Mostrar todos")
        print("3. Eliminar")
        print("4. Buscar")
        print("5. Salir")
        op = input("Opción: ").strip()
        if op == "1": repo.agregar_cliente()
        elif op == "2": repo.mostrar_clientes()
        elif op == "3": repo.eliminar_cliente()
        elif op == "4": repo.buscar_cliente()
        elif op == "5": break
        else: print("Opción inválida."); input("Enter...")

if __name__ == "__main__":
    menu()