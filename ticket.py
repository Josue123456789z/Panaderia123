from datetime import datetime
import os

class Ticket:
    def __init__(self, numero_ticket, fecha, detalle, total):
        self.numero_ticket = numero_ticket
        self.fecha = fecha
        self.detalle = detalle 
        self.total = total

    def generar_ticket_txt(self, venta, empresa, cliente):
        carpeta = "tickets"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        nombre_archivo = os.path.join(os.getcwd(), carpeta, f"ticket_{self.numero_ticket}.txt")

        with open(nombre_archivo, "w", encoding="utf-8") as f:
            print("=" * 50, file=f)
            print(f"                {empresa.nombre}", file=f)
            print(f"{'Correo: ' + empresa.correo:<25}{'Tel: ' + empresa.telefono + ' | Dir: ' + empresa.direccion:>25}", file=f)
            print("                  FACTURA VENTA", file=f)
            print("=" * 50, file=f)
            print(f"ID de la venta: {self.numero_ticket}", file=f)
            print(f"Cliente: {cliente.nombre}", file=f)
            print(f"Responsable: {venta.responsable}", file=f)
            print(f"Fecha y hora: {self.fecha}", file=f)
            print("-" * 50, file=f)
            print(f"{'Producto':20} {'Cant.':>5} {'P.Unit.':>10} {'Subtotal':>10}", file=f)

            for item in self.detalle:
                print(f"{item['nombre']:20} {item['cantidad']:>5} "
                      f"${item['precio_unitario']:>9.2f} ${item['subtotal']:>9.2f}", file=f)

            print("-" * 50, file=f)
            print(f"{'TOTAL:':>40} ${self.total:>9.2f}", file=f)
            print("=" * 50, file=f)

        return nombre_archivo

    def mostrar_ticket(self, venta, empresa):
        print("\n----- TICKET DE VENTA -----")
        print(f"Número de Ticket: {self.numero_ticket}")
        print(f"Fecha: {self.fecha}")
        print("\nDetalles:")
        for item in self.detalle:
            print(f"- {item['nombre']} x {item['cantidad']} = ${item['subtotal']:.2f}")
        print(f"\nTotal a pagar: ${self.total:.2f}")
        print("---------------------------\n")

    def imprimir_ticket(self, venta, empresa, cliente):
        ruta_txt = self.generar_ticket_txt(venta, empresa, cliente)
        print(f"Generando ticket TXT: {ruta_txt}")

        if os.path.exists(ruta_txt):
            try:
                os.startfile(ruta_txt, "print")
                print("Ticket enviado a la impresora por defecto (etiquetera conectada).")
            except Exception as e:
                print(f"Error al imprimir: {e}.")
        else:
            print(f"Error: El archivo {ruta_txt} no existe. No se puede imprimir.")
