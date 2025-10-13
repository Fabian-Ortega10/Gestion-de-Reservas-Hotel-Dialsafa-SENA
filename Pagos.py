class Pago:
    def __init__(self, id_pago, reserva, monto, metodo_pago):
        self.id_pago = id_pago
        self.reserva = reserva  
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.estado = "Pendiente"

    def Procesar(self):
        if self.estado == "Pendiente":
            self.estado = "Pagado"
            print(f"Pago {self.id_pago} procesado correctamente")
        else:
            print("Este pago ya fue procesado o cancelado")

    def Cancelar(self):
        if self.estado == "Pendiente":
            self.estado = "Cancelado"
            print(f"Pago {self.id_pago} cancelado.")
        else:
            print("No se puede cancelar este pago.")

    def Mostrar(self):
        return (f"ID Pago: {self.id_pago}\n"
                f"Reserva: {self.reserva}\n"
                f"Monto: ${self.monto}\n"
                f"Método: {self.metodo_pago}\n"
                f"Estado: {self.estado}")
    
if __name__ == "__main__":
    pago1 = Pago(1, "Reserva001", 250000, "Tarjeta")
    print(pago1.Mostrar())
    pago1.Procesar()
    print(pago1.Mostrar())
