from barcode import EAN13
from barcode.writer import ImageWriter

class GenerarCodigoBarra:
    def generar(self, producto_id, categoria_id):
        codigo_cat = str(categoria_id).zfill(2)
        codigo_pro = str(producto_id).zfill(10)
        codigo_base = codigo_cat + codigo_pro
        suma = 0
        for i in range(len(codigo_base)):
            digito = int(codigo_base[i])
            if i % 2 == 0:
                suma = suma + (digito * 3)
            else:
                suma = suma + digito
        digito_verificador = (10 - (suma % 10)) % 10
        result = codigo_base + str(digito_verificador)
        return result

