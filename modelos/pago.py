class Pago:
    def __init__(self, id_pago, reserva, monto, metodo_pago, fecha_pago, estado="Pendiente"):
        self.id_pago = id_pago
        self.reserva = reserva              # Referencia a objeto Reserva
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago
        self.estado = estado                # "Pendiente", "Pagado", "Cancelado"

    def procesar(self):
        self.estado = "Pagado"

    def cancelar(self):
        self.estado = "Cancelado"

    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "reserva_id": self.reserva.id_reserva,
            "monto": self.monto,
            "metodo_pago": self.metodo_pago,
            "fecha_pago": self.fecha_pago,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data, reservas):
        reserva = next((r for r in reservas if r.id_reserva == data["reserva_id"]), None)
        if not reserva:
            raise ValueError(f"Reserva con ID {data['reserva_id']} no encontrada para el pago.")
        return Pago(
            id_pago=data["id_pago"],
            reserva=reserva,
            monto=data["monto"],
            metodo_pago=data["metodo_pago"],
            fecha_pago=data["fecha_pago"],
            estado=data.get("estado", "Pendiente")
        )

    def __str__(self):
        return f"Pago {self.id_pago} - Reserva: {self.reserva.id_reserva} - Monto: ${self.monto} - Estado: {self.estado}"



