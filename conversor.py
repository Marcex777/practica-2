import json
from datetime import datetime
import random

def cargar_tasas(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def convertir(precio_usd, moneda_destino, tasas):
    tasa = tasas["USD"].get(moneda_destino)
    if tasa is None:
        raise ValueError("Moneda no soportada")
    return round(precio_usd * tasa, 2)


def registrar_transaccion(producto, precio_convertido, moneda, ruta_log):
    with open(ruta_log, "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"{fecha} | {producto}: {precio_convertido:.2f} {moneda}\n")

def actualizar_tasas(ruta):
    with open(ruta, "r+", encoding="utf-8") as archivo:
        tasas = json.load(archivo)
        for moneda in tasas["USD"]:
            tasas["USD"][moneda] *= 0.98 + (0.04 * random.random())
        tasas["actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.seek(0)
        json.dump(tasas, archivo, indent=2, ensure_ascii=False)
        archivo.truncate()

if __name__ == "__main__":
    actualizar_tasas("data/tasas.json")
    tasas = cargar_tasas("data/tasas.json")
    precio_usd = 100.00
    precio_eur = convertir(precio_usd, "EUR", tasas)
    registrar_transaccion("Laptop", precio_eur, "EUR", "logs/historial.txt")
