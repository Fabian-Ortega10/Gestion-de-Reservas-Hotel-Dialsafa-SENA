from modelos.reserva import Reserva
from utilidades.persistencia import guardar_json, cargar_json

class GestorReservas:
    def __init__(self):
        self.reservas = []

    def crear_reserva(self, reserva):
        if self.buscar_por_id(reserva.id_reserva):
            print("Reserva ya registrada.")
            return
        if not reserva.habitacion.esta_disponible(reserva.fecha_inicio, reserva.fecha_fin):
            raise ValueError("La habitación no está disponible en ese rango de fechas.")
        reserva.confirmar()
        self.reservas.append(reserva)

    def cancelar_reserva(self, id_reserva):
        reserva = self.buscar_por_id(id_reserva)
        if reserva and reserva.estado != "Cancelada":
            reserva.cancelar_reserva()

    def modificar_reserva(self, id_reserva, nueva_entrada, nueva_salida):
        reserva = self.buscar_por_id(id_reserva)
        if reserva and reserva.estado == "Confirmada":
            reserva.modificar_fechas(nueva_entrada, nueva_salida)

    def buscar_por_id(self, id_reserva):
        return next((r for r in self.reservas if r.id_reserva == id_reserva), None)

    def limpiar_reservas(self):
        self.reservas.clear()

    # ✅ NUEVO: Guardar reservas en archivo JSON
    def guardar_reservas(self, ruta="datos/reservas.json"):
        guardar_json(ruta, [r.to_dict() for r in self.reservas])

    # ✅ NUEVO: Cargar reservas desde archivo JSON
    def cargar_reservas(self, clientes, habitaciones, ruta="datos/reservas.json"):
        datos = cargar_json(ruta)
        self.reservas = [Reserva.from_dict(d, clientes, habitaciones) for d in datos]

