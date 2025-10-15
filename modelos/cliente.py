class Cliente:
    def __init__(self, id_cliente, nombre, documento, contacto):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.documento = documento
        self.contacto = contacto
        self.reservas = []

    def realizar_reserva(self, reserva):
        self.reservas.append(reserva)

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "documento": self.documento,
            "contacto": self.contacto
        }

    @staticmethod
    def from_dict(data):
        return Cliente(
            id_cliente=data["id_cliente"],
            nombre=data["nombre"],
            documento=data["documento"],
            contacto=data["contacto"]
        )

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

