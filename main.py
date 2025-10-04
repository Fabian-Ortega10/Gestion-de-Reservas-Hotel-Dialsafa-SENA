print("hola mundo")

class Hotel:
        def __init__(self, nombre, direccion):
            self.nombre = nombre
            self.direccion = direccion

la_estrella = Hotel("La estrella", "Calle 15 #3-98")

print(f"{la_estrella.nombre} {la_estrella.direccion}")
