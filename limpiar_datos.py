import json

archivos = [
    "datos/clientes.json",
    "datos/habitaciones.json",
    "datos/reservas.json",
    "datos/pagos.json"
]

for archivo in archivos:
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

print(" Archivos limpiados correctamente.")
