class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono


Diana = Cliente("Diana", 3124398432)

print(f"{Diana.nombre} {Diana.telefono}")