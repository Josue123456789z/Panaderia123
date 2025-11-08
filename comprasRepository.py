import json
import os
from datetime import datetime
from compras import Compra 
from productoRepository import ProductoRepository
from proveedoresRepository import ProveedoresRepository
from lectorCodigoBarra import LectorCodigoBarra 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def limpiar_pantalla():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

class CompraRepository:
    def __init__(self, archivo="compras.json"):
        self.archivo = archivo
        self.compras = []
        self.producto_repo = ProductoRepository()
        self.proveedor_repo = ProveedoresRepository()
        self.cargar_compras()

    def cargar_compras(self):
        if not os.path.exists(self.archivo):
            self.guardar_compras()
            return
        try:
            with open(self.archivo, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.compras = [
                Compra(
                    compra_id=c["compra_id"],
                    proveedor_id=c["proveedor_id"],
                    responsable=c["responsable"],
                    productos=c["productos"],
                    fecha=c["fecha"]
                ) for c in data
            ]
        except (json.JSONDecodeError, KeyError, Exception):
            self.compras = []

    def guardar_compras(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as file:
                json.dump([c.convertir() for c in self.compras], file, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def get_id(self):
        return max((c.compra_id for c in self.compras), default=0)

    def registrar_compra(self):
        limpiar_pantalla()
        print("\n--- REGISTRAR COMPRA ---")

        try:
            proveedor_id = int(input("ID del proveedor: "))
            if not self.proveedor_repo.buscar_por_id(proveedor_id):
                print("Proveedor no existe.")
                input("Enter...")
                return
        except ValueError:
            print("ID debe ser número.")
            input("Enter...")
            return

        responsable = input("Responsable: ").strip()
        if not responsable:
            print("Responsable requerido.")
            input("Enter...")
            return

        productos_comprados = []

        while True:
            limpiar_pantalla()
            print("Productos disponibles:")
            for prod in self.producto_repo.productos:
                print(f"ID: {prod.producto_id} | Nombre: {prod.nombre} | Stock: {prod.stock} | Precio: ${prod.precio:.2f}")

            try:
                prod_id = int(input("\nIngrese el ID del producto a comprar (0 para terminar): "))
            except ValueError:
                print("ID inválido.")
                input("Enter...")
                continue

            if prod_id == 0:
                break

            producto = self.producto_repo.select_by_id(prod_id)
            if not producto:
                print("Producto no encontrado.")
                input("Enter...")
                continue

            try:
                cantidad = int(input(f"Ingrese cantidad a comprar para '{producto.nombre}': "))
                if cantidad <= 0:
                    print("Cantidad inválida.")
                    input("Enter...")
                    continue
            except ValueError:
                print("Cantidad inválida.")
                input("Enter...")
                continue

            subtotal = cantidad * producto.precio
            producto.stock += cantidad
            self.producto_repo.save()

            productos_comprados.append({
                "producto_id": producto.producto_id,
                "nombre": producto.nombre,
                "cantidad": cantidad,
                "precio_unitario": producto.precio,
                "subtotal": subtotal
            })

        if not productos_comprados:
            print("No se agregó ningún producto.")
            input("Enter...")
            return

        nuevo_id = self.get_id() + 1
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_compra = Compra(nuevo_id, proveedor_id, responsable, productos_comprados, fecha_actual)
        self.compras.append(nueva_compra)
        self.guardar_compras()

        print("\n----- Panadería San Deli -----")
        print(f"ID de la compra: {nuevo_id}")
        print(f"Responsable: {responsable}")
        print(f"Fecha y hora: {fecha_actual}")
        print("Productos:")
        for p in nueva_compra.productos:
            print(f"- {p['nombre']}")
            print(f"  Precio Unitario: ${p['precio_unitario']:.2f}")
            print(f"  Cantidad: {p['cantidad']}")
        print(f"Total a pagar: ${nueva_compra.total:.2f}")
        print("-------------------------------")

        if input("\n¿Generar PDF? (s/n): ").lower() == "s":
            self.generar_factura_pdf(nueva_compra)

        input("\nEnter para continuar...")


    def generar_factura_pdf(self, compra):
        carpeta = "facturas_compras"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        nombre = os.path.join(carpeta, f"factura_compra_{compra.compra_id}.pdf")
        doc = SimpleDocTemplate(nombre, pagesize=letter)
        styles = getSampleStyleSheet()
        contenido = []

        contenido.append(Paragraph("<b>FACTURA DE COMPRA</b>", styles["Title"]))
        contenido.append(Spacer(1, 12))
        contenido.append(Paragraph(f"<b>ID Compra:</b> {compra.compra_id}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Proveedor ID:</b> {compra.proveedor_id}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Responsable:</b> {compra.responsable}", styles["Normal"]))
        contenido.append(Paragraph(f"<b>Fecha:</b> {compra.fecha}", styles["Normal"]))
        contenido.append(Spacer(1, 12))

        data = [["Producto", "Cant.", "P.Unit.", "Subtotal"]]
        for p in compra.productos:
            data.append([
                p["nombre"],
                str(p["cantidad"]),
                f"${p['precio_unitario']:.2f}",
                f"${p['subtotal']:.2f}"
            ])
        data.append(["", "", "TOTAL:", f"${compra.total:.2f}"])

        tabla = Table(data, hAlign='CENTER')
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),
            ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
        ]))

        contenido.append(tabla)
        contenido.append(Spacer(1, 12))
        doc.build(contenido)
        print(f"PDF generado correctamente: {nombre}")

    def listar_compras(self):
        limpiar_pantalla()
        if not self.compras:
            print("No hay compras registradas.")
        else:
            print("COMPRAS REGISTRADAS".center(70, "="))
            for c in self.compras:
                print(c)
            print("=" * 70)
        input("Enter...")

def menu_compras():
    repo = CompraRepository()
    while True:
        limpiar_pantalla()
        print("\n===== MENÚ DE COMPRAS =====")
        print("1. Registrar nueva compra")
        print("2. Listar compras")
        print("3. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            repo.registrar_compra()
        elif op == "2":
            repo.listar_compras()
        elif op == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
            input("Enter...")

if __name__ == "__main__":
    menu_compras()