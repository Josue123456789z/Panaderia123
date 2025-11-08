import json
import os
from datetime import datetime
from ventas import Ventas
from cliente import Cliente
from empresa import Empresa
from productoRepository import ProductoRepository
from clienteRepository import ClienteRepository
from empresaRepository import EmpresaRepository
from lectorCodigoBarra import LectorCodigoBarra 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from ticket import Ticket


def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")
    

class VentasRepository:
    def __init__(self, archivo="ventas.json"):
        self.archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), archivo)
        self.ventas = []
        self.producto_repo = ProductoRepository()
        self.cliente_repo = ClienteRepository()
        self.empresa_repo = EmpresaRepository()
        self.cargar_ventas()

    def cargar_ventas(self):
        if not os.path.exists(self.archivo):
            self.guardar_ventas()
            return
        try:
            with open(self.archivo, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.ventas = [
                Ventas(
                    venta_id=v["venta_id"],
                    cliente_id=v["cliente_id"],
                    responsable=v["responsable"],
                    productos=v["productos"],
                    fecha=v["fecha"]
                ) for v in data
            ]
        except Exception:
            self.ventas = []

    def guardar_ventas(self):
        with open(self.archivo, "w", encoding="utf-8") as file:
            json.dump([v.convertir() for v in self.ventas], file, indent=4, ensure_ascii=False)

    def get_id(self):
        return max((v.venta_id for v in self.ventas), default=0)

    def registrar_venta(self):
        limpiar_pantalla()
        print("\n--- REGISTRAR VENTA ---")

        nombre_cliente = input("Nombre del cliente: ").strip()
        clientes_encontrados = self.cliente_repo.buscar_por_nombre(nombre_cliente)

        cliente = None
        if clientes_encontrados:
            if len(clientes_encontrados) == 1:
                cliente = clientes_encontrados[0]
            else:
                print("\nClientes encontrados con ese nombre:")
                for c in clientes_encontrados:
                    print(c)
                try:
                    cliente_id_sel = int(input("Ingrese ID del cliente correcto: "))
                    cliente = self.cliente_repo.buscar_por_id(cliente_id_sel)
                    if cliente is None:
                        print("ID inválido. Cancelando venta.")
                        input("Enter...")
                        return
                except ValueError:
                    print("Entrada inválida. Cancelando venta.")
                    input("Enter...")
                    return
        else:
            print("Cliente no encontrado. Ingrese los datos para agregarlo.")
            nombre = nombre_cliente
            telefono = input("Teléfono: ").strip()
            correo = input("Correo: ").strip()
            nuevo_id = self.cliente_repo.get_id() + 1
            cliente = Cliente(nuevo_id, nombre, telefono, correo)
            self.cliente_repo.add(cliente)
            print(f"Cliente {nombre} agregado exitosamente.")
            input("Enter para continuar...")

        responsable = input("Responsable de la venta: ").strip()
        if not responsable:
            print("Responsable requerido.")
            input("Enter...")
            return

        lector = LectorCodigoBarra() 
        productos_vendidos = []

        while True:
            limpiar_pantalla()
            opcion_ingreso = input("¿Deseas ingresar código escaneado/manual? (s/n): ").strip().lower()
            if opcion_ingreso in ("s", "n"):
                break
            print("Opción inválida. Por favor ingresa 's' o 'n'.")

        if opcion_ingreso == "s":

            while True:
                limpiar_pantalla()
                print("=== ESCANEA PRODUCTOS PARA LA VENTA ===")
                print("Ingresa '0' para finalizar.\n")

                entrada = input("Escanea o ingresa código (0 para terminar): ").strip()
                if entrada == "0":
                    break

                producto = lector.buscar_por_codigo(entrada)
                if not producto:
                    print("Producto no encontrado.")
                    input("Enter...")
                    continue

                try:
                    cantidad = int(input(f"Cantidad de '{producto.nombre}': "))
                    if cantidad <= 0:
                        print("Cantidad inválida.")
                        input("Enter...")
                        continue
                    if cantidad > producto.stock:
                        print(f"Stock insuficiente. Disponible: {producto.stock}")
                        input("Enter...")
                        continue

                    subtotal = cantidad * producto.precio
                    producto.stock -= cantidad
                    self.producto_repo.save()

                    productos_vendidos.append({
                        "producto_id": producto.producto_id,
                        "nombre": producto.nombre,
                        "cantidad": cantidad,
                        "precio_unitario": producto.precio,
                        "subtotal": subtotal
                    })
                    print(f"Agregado: {cantidad} x {producto.nombre}")
                    input("Enter para continuar...")
                except ValueError:
                    print("Cantidad inválida.")
                    input("Enter...")
        else:
            while True:
                limpiar_pantalla()
                print("=== LISTA DE PRODUCTOS ===")
                for p in self.producto_repo.productos:
                    print(f"{p.producto_id}: {p.nombre} (Stock: {p.stock}, Precio: ${p.precio:.2f})")
                print("0: Finalizar selección")

                try:
                    opcion = int(input("Ingresa el ID del producto a agregar (0 para terminar): "))
                except ValueError:
                    print("Entrada inválida.")
                    input("Enter para continuar...")
                    continue

                if opcion == 0:
                    break

                producto = None
                for p in self.producto_repo.productos:
                    if p.producto_id == opcion:
                        producto = p
                        break

                if not producto:
                    print("Producto no encontrado.")
                    input("Enter para continuar...")
                    continue

                try:
                    cantidad = int(input(f"Cantidad de '{producto.nombre}': "))
                    if cantidad <= 0:
                        print("Cantidad inválida.")
                        input("Enter para continuar...")
                        continue
                    if cantidad > producto.stock:
                        print(f"Stock insuficiente. Disponible: {producto.stock}")
                        input("Enter para continuar...")
                        continue

                    subtotal = cantidad * producto.precio
                    producto.stock -= cantidad
                    self.producto_repo.save()

                    productos_vendidos.append({
                        "producto_id": producto.producto_id,
                        "nombre": producto.nombre,
                        "cantidad": cantidad,
                        "precio_unitario": producto.precio,
                        "subtotal": subtotal
                    })
                    print(f"Agregado: {cantidad} x {producto.nombre}")
                    input("Enter para continuar...")
                except ValueError:
                    print("Cantidad inválida.")
                    input("Enter para continuar...")

        if not productos_vendidos:
            print("No se agregó ningún producto a la venta.")
            input("Enter...")
            return

        nuevo_id = self.get_id() + 1
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_venta = Ventas(nuevo_id, cliente.cliente_id, responsable, productos_vendidos, fecha_actual)
        self.ventas.append(nueva_venta)
        self.guardar_ventas()

        empresa = self.empresa_repo.empresa

        print("\n" + "="*50)
        if empresa:
            print(empresa.nombre.center(50))
            print(f"Correo: {empresa.correo}".ljust(25) + f"Tel: {empresa.telefono} | Dir: {empresa.direccion}".rjust(25))
        print("FACTURA VENTA".center(50))
        print("="*50)
        print(f"ID de la venta: {nuevo_id}")
        print(f"Cliente: {cliente.nombre}")
        print(f"Responsable: {responsable}")
        print(f"Fecha y hora: {fecha_actual}")
        print("-" * 50)
        print(f"{'Producto':20} {'Cant.':>5} {'P.Unit.':>10} {'Subtotal':>10}")
        for p in nueva_venta.productos:
            print(f"{p['nombre']:20} {p['cantidad']:>5} ${p['precio_unitario']:>9.2f} ${p['subtotal']:>9.2f}")
        print("-" * 50)
        print(f"{'TOTAL:':>40} ${nueva_venta.total:>9.2f}")
        print("="*50)

        if input("\n¿Generar PDF? (s/n): ").lower() == "s":
            self.generar_factura_pdf(nueva_venta, cliente, empresa)

        # Aquí pasamos venta y empresa a mostrar_ticket e imprimir_ticket
        ticket = Ticket(nuevo_id, fecha_actual, productos_vendidos, nueva_venta.total)
        ticket.mostrar_ticket(nueva_venta, empresa)  # si quieres pasar cliente aquí, cambia también

        imprimir = input("\n¿Deseas imprimir el ticket? (s/n): ").lower()
        if imprimir == "s":
            try:
                ticket.imprimir_ticket(nueva_venta, empresa, cliente)
            except Exception as e:
                print(f"No se pudo imprimir el ticket: {e}")


        input("\nEnter para continuar...")

    def generar_factura_pdf(self, venta, cliente, empresa=None):
        carpeta = "facturas_ventas"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        nombre = os.path.join(carpeta, f"factura_venta_{venta.venta_id}.pdf")
        doc = SimpleDocTemplate(nombre, pagesize=letter)
        styles = getSampleStyleSheet()
        contenido = []

        if empresa:
            estilo_nombre = ParagraphStyle('nombreEmpresa', parent=styles['Title'], alignment=TA_CENTER)
            contenido.append(Paragraph(getattr(empresa, 'nombre', 'NOMBRE EMPRESA NO DISPONIBLE'), estilo_nombre))

            estilo_peq_izq = ParagraphStyle('peqIzq', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)
            correo = getattr(empresa, 'correo', 'correo@desconocido.com')
            contenido.append(Paragraph(f"Correo: {correo}", estilo_peq_izq))

            telefono = getattr(empresa, 'telefono', '0000-0000')
            direccion = getattr(empresa, 'direccion', 'DIRECCIÓN NO DISPONIBLE')
            data = [[f"Tel: {telefono}", f"Dirección: {direccion}"]]
            tabla = Table(data, colWidths=[270, 270])
            estilo_tabla = TableStyle([
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('TOPPADDING', (0,0), (-1,-1), 2),
            ])
            tabla.setStyle(estilo_tabla)
            contenido.append(tabla)

            estilo_titulo = ParagraphStyle('tituloFactura', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)
            contenido.append(Paragraph("FACTURA VENTA", estilo_titulo))
        else:
            contenido.append(Paragraph("FACTURA VENTA", styles["Title"]))

        contenido.append(Spacer(1, 12))
        contenido.append(Paragraph(f"<b>ID Venta:</b> {venta.venta_id}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Cliente:</b> {cliente.nombre}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Responsable:</b> {venta.responsable}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Fecha:</b> {venta.fecha}", styles["Normal"]))
        contenido.append(Spacer(1, 12))

        data = [["Producto", "Cant.", "P.Unit.", "Subtotal"]]
        for p in venta.productos:
            data.append([
                p["nombre"],
                str(p["cantidad"]),
                f"${p['precio_unitario']:.2f}",
                f"${p['subtotal']:.2f}"
            ])
        data.append(["", "", "TOTAL:", f"${venta.total:.2f}"])

        tabla = Table(data, hAlign='CENTER')
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (-2,-1), (-1,-1), 'Helvetica-Bold'),
            ('ALIGN', (-1,-1), (-1,-1), 'RIGHT'),
            ('BACKGROUND', (-2,-1), (-1,-1), colors.lightgrey),
        ]))
        contenido.append(tabla)
        contenido.append(Spacer(1, 12))

        doc.build(contenido)
        print(f"PDF generado correctamente: {nombre}")

    def listar_ventas(self):
        limpiar_pantalla()
        if not self.ventas:
            print("No hay ventas registradas.")
        else:
            print("VENTAS REGISTRADAS".center(70, "="))
            for v in self.ventas:
                print(v)
            print("="*70)
        input("Enter...")


def menu_ventas():
    repo = VentasRepository()
    while True:
        limpiar_pantalla()
        print("\n===== MENÚ DE VENTAS =====")
        print("1. Registrar nueva venta")
        print("2. Listar ventas")
        print("3. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            repo.registrar_venta()
        elif opcion == "2":
            repo.listar_ventas()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")
            input("Enter para continuar...")


if __name__ == "__main__":
    menu_ventas()
