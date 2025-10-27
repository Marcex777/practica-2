import json
import random
from datetime import datetime
from pathlib import Path

def cargar_tasas(ruta):
    ruta = Path(ruta)
    with ruta.open("r", encoding="utf-8") as f:
        return json.load(f)

def convertir(precio_usd, moneda_destino, tasas):
    tasa = tasas.get("USD", {}).get(moneda_destino)
    if tasa is None:
        raise ValueError(f"Moneda no soportada: {moneda_destino}")
    return float(precio_usd) * float(tasa)

def registrar_transaccion(producto, precio_convertido, moneda, ruta_log):
    ruta_log = Path(ruta_log)
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with ruta_log.open("a", encoding="utf-8") as f:
        f.write(f"{fecha} | {producto}: {precio_convertido:.2f} {moneda}\n")

def actualizar_tasas(ruta, variacion=0.02):
    ruta = Path(ruta)
    with ruta.open("r+", encoding="utf-8") as f:
        tasas = json.load(f)
        for moneda, valor in list(tasas.get("USD", {}).items()):
            if moneda == "USD":
                continue
            if isinstance(valor, (int, float)):
                delta = (random.random() * 2 * variacion) - variacion
                tasas["USD"][moneda] = round(valor * (1 + delta), 6)
        tasas["actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.seek(0)
        json.dump(tasas, f, indent=2, ensure_ascii=False)
        f.truncate()

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    ruta_tasas = base / "data" / "tasas.json"
    ruta_log = base / "logs" / "historial.txt"
    actualizar_tasas(ruta_tasas)
    tasas = cargar_tasas(ruta_tasas)
    precio_usd = 100.0
    precio_eur = convertir(precio_usd, "EUR", tasas)
    registrar_transaccion("Laptop", precio_eur, "EUR", ruta_log)
    print(f"OK: 100 USD -> {precio_eur:.2f} EUR. Registro en {ruta_log}")
