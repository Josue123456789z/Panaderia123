from barcode import EAN13
from barcode.writer import ImageWriter
import os

class GenerarCodigoBarra:
    def generar_imagen(self, codigo_producto, nombre_archivo="codigo_barra"):
        """
        Genera y guarda la imagen del código de barras en la carpeta 'codigos_barras/'.
        El código_producto debe ser un string numérico de 13 dígitos para EAN13 (incluye dígito verificador).
        """
        codigo = str(codigo_producto)

        if len(codigo) != 12:
            raise ValueError("El código debe tener exactamente 13 dígitos para EAN-13.")

        carpeta = "codigos_barras"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ean = EAN13(codigo, writer=ImageWriter())
        ruta = os.path.join(carpeta, nombre_archivo)
        ean.save(ruta)
        print(f"Imagen guardada: {ruta}.png")
        return f"{ruta}.png"


if __name__ == "__main__":
    generador = GenerarCodigoBarra()

    while True:
        codigo = input("Ingresa el código del producto para generar el código de barras (13 dígitos numéricos): ").strip()
        if not (codigo.isdigit() and len(codigo) == 12):
            print("Código inválido, debe contener exactamente 13 números.")
            continue

        nombre_archivo = input("Nombre del archivo para guardar (ENTER = código): ").strip()
        if not nombre_archivo:
            nombre_archivo = f"prod_{codigo}"

        try:
            ruta = generador.generar_imagen(codigo, nombre_archivo)
            print(f"Código de barras generado y guardado en: {ruta}")
        except Exception as e:
            print(f"Error al generar código de barras: {e}")

        otro = input("¿Generar otro código? (s/n): ").lower()
        if otro != "s":
            break

