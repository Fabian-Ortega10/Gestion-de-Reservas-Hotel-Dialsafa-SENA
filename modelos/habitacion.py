from datetime import datetime, timedelta

class Habitacion:
    def __init__(self, numero, tipo, precio, capacidad=2, cantidad_disponible=1):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.capacidad = capacidad
        self.cantidad_disponible = cantidad_disponible
        self.ocupaciones = set()  # Fechas ocupadas como strings "YYYY-MM-DD"

    def esta_disponible(self, fecha_inicio, fecha_fin):
        fechas = self._rango_fechas(fecha_inicio, fecha_fin)
        return all(fecha not in self.ocupaciones for fecha in fechas)

    def reservar_rango(self, fecha_inicio, fecha_fin):
        fechas = self._rango_fechas(fecha_inicio, fecha_fin)
        self.ocupaciones.update(fechas)

    def liberar_rango(self, fecha_inicio, fecha_fin):
        fechas = self._rango_fechas(fecha_inicio, fecha_fin)
        self.ocupaciones.difference_update(fechas)

    def _rango_fechas(self, inicio, fin):
        inicio_dt = datetime.strptime(inicio, "%Y-%m-%d")
        fin_dt = datetime.strptime(fin, "%Y-%m-%d")
        return [(inicio_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((fin_dt - inicio_dt).days)]

    def to_dict(self):
        return {
            "numero": self.numero,
            "tipo": self.tipo,
            "precio": self.precio,
            "capacidad": self.capacidad,
            "cantidad_disponible": self.cantidad_disponible,
            "ocupaciones": list(self.ocupaciones)
        }

    @staticmethod
    def from_dict(data):
        habitacion = Habitacion(
            numero=data["numero"],
            tipo=data["tipo"],
            precio=data["precio"],
            capacidad=data["capacidad"],
            cantidad_disponible=data["cantidad_disponible"]
        )
        habitacion.ocupaciones = set(data.get("ocupaciones", []))
        return habitacion

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo} - ${self.precio}"

