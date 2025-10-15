from modelos.habitacion import Habitacion
from utilidades.persistencia import guardar_json, cargar_json

class GestorHabitaciones:
    def __init__(self):
        self.habitaciones = []

    def registrar_habitacion(self, habitacion):
        if self.buscar_por_numero(habitacion.numero):
            print("Habitación ya registrada.")
            return
        self.habitaciones.append(habitacion)

    def buscar_por_numero(self, numero):
        return next((h for h in self.habitaciones if h.numero == numero), None)

    def obtener_disponibles(self):
        # Si usas lógica de fechas, reemplaza esto por:
        return [h for h in self.habitaciones if not h.ocupaciones]

    def actualizar_disponibilidad(self, numero, disponible):
        habitacion = self.buscar_por_numero(numero)
        if habitacion and hasattr(habitacion, "actualizar_disponibilidad"):
            habitacion.actualizar_disponibilidad(disponible)

    def limpiar_habitaciones(self):
        self.habitaciones.clear()

    # ✅ NUEVO: Guardar habitaciones en archivo JSON
    def guardar_habitaciones(self, ruta="datos/habitaciones.json"):
        guardar_json(ruta, [h.to_dict() for h in self.habitaciones])

    # ✅ NUEVO: Cargar habitaciones desde archivo JSON
    def cargar_habitaciones(self, ruta="datos/habitaciones.json"):
        datos = cargar_json(ruta)
        self.habitaciones = [Habitacion.from_dict(d) for d in datos]

