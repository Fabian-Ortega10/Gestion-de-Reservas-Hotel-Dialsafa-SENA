from modelos.cliente import Cliente
from utilidades.persistencia import guardar_json, cargar_json

class GestorClientes:
    def __init__(self):
        self.clientes = []

    def buscar_por_id(self, id_cliente):
        return next((c for c in self.clientes if c.id_cliente == id_cliente), None)

    def registrar_cliente(self, cliente):
        if self.buscar_por_id(cliente.id_cliente):
            print("Cliente ya registrado.")
            return
        self.clientes.append(cliente)

    def buscar_por_documento(self, documento):
        return next((c for c in self.clientes if c.documento == documento), None)

    def eliminar_cliente(self, documento):
        cliente = self.buscar_por_documento(documento)
        if cliente:
            self.clientes.remove(cliente)

    def limpiar_clientes(self):
        self.clientes.clear()

    # ✅ NUEVO: Guardar clientes en archivo JSON
    def guardar_clientes(self, ruta="datos/clientes.json"):
        guardar_json(ruta, [c.to_dict() for c in self.clientes])

    # ✅ NUEVO: Cargar clientes desde archivo JSON
    def cargar_clientes(self, ruta="datos/clientes.json"):
        datos = cargar_json(ruta)
        self.clientes = [Cliente.from_dict(d) for d in datos]
