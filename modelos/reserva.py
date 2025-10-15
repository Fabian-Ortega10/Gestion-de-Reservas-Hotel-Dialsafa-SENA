class Reserva:
    def __init__(self, id_reserva, cliente, habitacion, fecha_inicio, fecha_fin, estado="Pendiente"):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def confirmar_reserva(self):
        if self.habitacion.esta_disponible(self.fecha_inicio, self.fecha_fin):
            self.habitacion.reservar_rango(self.fecha_inicio, self.fecha_fin)
            self.estado = "Confirmada"
        else:
            raise Exception("La habitación no está disponible en ese rango de fechas.")

    def confirmar(self):
        # Alias para compatibilidad con gestor_reservas
        self.confirmar_reserva()

    def cancelar_reserva(self):
        if self.estado == "Confirmada":
            self.habitacion.liberar_rango(self.fecha_inicio, self.fecha_fin)
        self.estado = "Cancelada"

    def modificar_fechas(self, nueva_entrada, nueva_salida):
        if self.estado == "Confirmada":
            self.habitacion.liberar_rango(self.fecha_inicio, self.fecha_fin)
        self.fecha_inicio = nueva_entrada
        self.fecha_fin = nueva_salida
        self.confirmar_reserva()

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "cliente_id": self.cliente.id_cliente,
            "habitacion_numero": self.habitacion.numero,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(data, clientes, habitaciones):
        cliente = next(c for c in clientes if c.id_cliente == data["cliente_id"])
        habitacion = next(h for h in habitaciones if h.numero == data["habitacion_numero"])
        return Reserva(
            id_reserva=data["id_reserva"],
            cliente=cliente,
            habitacion=habitacion,
            fecha_inicio=data["fecha_inicio"],
            fecha_fin=data["fecha_fin"],
            estado=data["estado"]
        )

    def __str__(self):
        return f"Reserva {self.id_reserva} - Cliente: {self.cliente.nombre} - Habitación: {self.habitacion.numero} - Estado: {self.estado}"



