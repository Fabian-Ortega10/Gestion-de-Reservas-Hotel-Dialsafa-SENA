from modelos.pago import Pago
from utilidades.persistencia import guardar_json, cargar_json

class GestorPagos:
    def __init__(self):
        self.pagos = []

    def procesar_pago(self, pago):
        # Verifica si el pago ya está registrado
        pago_existente = self.buscar_por_id(pago.id_pago)
        
        if pago_existente:
            print("El pago ya fue procesado o cancelado.")
            return

        # Procesa el pago si está pendiente
        if pago.estado == "Pendiente":
            pago.procesar()
            self.pagos.append(pago)
        else:
            print("El pago no está en estado pendiente.")

    def cancelar_pago(self, id_pago):
        pago = self.buscar_por_id(id_pago)
        if pago and pago.estado == "Pendiente":
            pago.cancelar()

    def buscar_por_id(self, id_pago):
        return next((p for p in self.pagos if p.id_pago == id_pago), None)

    def limpiar_pagos(self):
        self.pagos.clear()

    # ✅ Guardar pagos en archivo JSON
    def guardar_pagos(self, ruta="datos/pagos.json"):
        guardar_json(ruta, [p.to_dict() for p in self.pagos])

    # ✅ Cargar pagos desde archivo JSON
    def cargar_pagos(self, reservas, ruta="datos/pagos.json"):
        datos = cargar_json(ruta)
        self.pagos = [Pago.from_dict(d, reservas) for d in datos]


