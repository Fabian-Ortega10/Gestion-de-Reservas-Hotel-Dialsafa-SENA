from datetime import datetime
from modelos.cliente import Cliente
from modelos.habitacion import Habitacion
from modelos.reserva import Reserva
from modelos.pago import Pago

from gestores.gestor_clientes import GestorClientes
from gestores.gestor_habitaciones import GestorHabitaciones
from gestores.gestor_reservas import GestorReservas
from gestores.gestor_pagos import GestorPagos

from reportes.gestor_reportes import GestorReportes

# Inicializar gestores
gestor_clientes = GestorClientes()
gestor_habitaciones = GestorHabitaciones()
gestor_reservas = GestorReservas()
gestor_pagos = GestorPagos()

# Cargar datos
gestor_clientes.limpiar_clientes()
gestor_habitaciones.limpiar_habitaciones()
gestor_reservas.limpiar_reservas()
gestor_pagos.limpiar_pagos()

gestor_clientes.cargar_clientes()
gestor_habitaciones.cargar_habitaciones()
gestor_reservas.cargar_reservas(gestor_clientes.clientes, gestor_habitaciones.habitaciones)
gestor_pagos.cargar_pagos(gestor_reservas.reservas)

gestor_reportes = GestorReportes(
    gestor_reservas,
    gestor_pagos,
    gestor_clientes,
    gestor_habitaciones
)

# Validación de fechas
def validar_fechas(fecha_inicio, fecha_fin):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        if inicio >= fin:
            print("La fecha de entrada debe ser anterior a la fecha de salida.")
            return False
        return True
    except ValueError:
        print("Formato de fecha inválido. Usa YYYY-MM-DD.")
        return False

# Funciones del menú
def registrar_cliente():
    nombre = input("Nombre del cliente: ")
    documento = input("Número de documento: ")
    contacto = input("Correo de contacto: ")
    cliente = Cliente(id_cliente=documento, nombre=nombre, documento=documento, contacto=contacto)
    gestor_clientes.registrar_cliente(cliente)
    gestor_clientes.guardar_clientes()
    print("Cliente registrado.")

def registrar_habitacion():
    numero = input("Número de habitación: ")
    tipo = input("Tipo de habitación (Ej: Sencilla, Doble, Suite): ")
    precio = float(input("Precio por noche: "))
    capacidad = int(input("Capacidad máxima: "))
    cantidad_disponible = int(input("Cantidad disponible: "))
    habitacion = Habitacion(numero, tipo, precio, capacidad, cantidad_disponible)
    gestor_habitaciones.registrar_habitacion(habitacion)
    gestor_habitaciones.guardar_habitaciones()
    print("Habitación registrada.")

def ver_disponibilidad():
    numero = input("Número de habitación: ")
    fecha_inicio = input("Fecha de entrada (YYYY-MM-DD): ")
    fecha_fin = input("Fecha de salida (YYYY-MM-DD): ")
    if not validar_fechas(fecha_inicio, fecha_fin):
        return
    habitacion = gestor_habitaciones.buscar_por_numero(numero)
    if habitacion:
        if habitacion.esta_disponible(fecha_inicio, fecha_fin):
            print(f"La habitación {numero} está disponible.")
        else:
            print(f"La habitación {numero} NO está disponible.")
    else:
        print("Habitación no encontrada.")

def crear_reserva():
    id_reserva = input("ID de la reserva: ")
    if gestor_reservas.buscar_por_id(id_reserva):
        print("Ya existe una reserva con ese ID.")
        return
    documento = input("Documento del cliente: ")
    numero = input("Número de habitación: ")
    fecha_inicio = input("Fecha de entrada (YYYY-MM-DD): ")
    fecha_fin = input("Fecha de salida (YYYY-MM-DD): ")
    if not validar_fechas(fecha_inicio, fecha_fin):
        return

    cliente = gestor_clientes.buscar_por_id(documento)
    habitacion = gestor_habitaciones.buscar_por_numero(numero)

    if not cliente:
        print("Cliente no encontrado.")
        return
    if not habitacion:
        print("Habitación no encontrada.")
        return

    reserva = Reserva(id_reserva, cliente, habitacion, fecha_inicio, fecha_fin)
    try:
        gestor_reservas.crear_reserva(reserva)
        gestor_reservas.guardar_reservas()
        print("Reserva creada y confirmada.")
    except Exception as e:
        print(f"Error al crear la reserva: {e}")

def cancelar_reserva():
    id_reserva = input("ID de la reserva a cancelar: ")
    reserva = gestor_reservas.buscar_por_id(id_reserva)
    if reserva:
        reserva.cancelar_reserva()
        gestor_reservas.guardar_reservas()
        print("✅ Reserva cancelada.")
    else:
        print("Reserva no encontrada.")

def procesar_pago():
    id_pago = input("ID del pago: ")
    if gestor_pagos.buscar_por_id(id_pago):
        print("Ya existe un pago con ese ID.")
        return
    id_reserva = input("ID de la reserva asociada: ")
    metodo = input("Método de pago (Ej: Tarjeta, Efectivo): ")
    monto = float(input("Monto a pagar: "))
    fecha = input("Fecha del pago (YYYY-MM-DD): ")

    reserva = gestor_reservas.buscar_por_id(id_reserva)
    if not reserva:
        print("Reserva no encontrada.")
        return
    if reserva.estado != "Confirmada":
        print("La reserva no está confirmada. No se puede procesar el pago.")
        return

    # Validar monto según noches y precio
    inicio = datetime.strptime(reserva.fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(reserva.fecha_fin, "%Y-%m-%d")
    noches = (fin - inicio).days
    monto_esperado = noches * reserva.habitacion.precio

    if monto != monto_esperado:
        print(f"El monto ingresado no coincide con el precio total esperado (${monto_esperado}).")
        return

    pago = Pago(id_pago, reserva, monto, metodo, fecha, estado="Pendiente")
    try:
        gestor_pagos.procesar_pago(pago)
        gestor_pagos.guardar_pagos()
        print("Pago procesado.")
    except Exception as e:
        print(f"Error al procesar el pago: {e}")

def ver_reportes():
    print("\n Reporte de reservas activas:")
    for r in gestor_reportes.mostrar_reservas_activas():
        print(r)

    print("\n Historial de pagos:")
    for p in gestor_reportes.mostrar_historial_pagos():
        print(p)

    print("\n Ocupación de habitaciones:")
    ocupacion = gestor_reportes.mostrar_ocupacion_habitaciones()
    print(f"Total: {ocupacion['total']}, Ocupadas: {len(ocupacion['ocupadas'])}, Disponibles: {len(ocupacion['disponibles'])}")

    print("\n Resumen general:")
    resumen = gestor_reportes.resumen_general()
    for clave, valor in resumen.items():
        print(f"{clave}: {valor}")

# Menú principal
def mostrar_menu():
    print("\n MENÚ PRINCIPAL")
    print("1. Registrar cliente")
    print("2. Registrar habitación")
    print("3. Ver disponibilidad de habitación")
    print("4. Crear reserva")
    print("5. Cancelar reserva")
    print("6. Procesar pago")
    print("7. Ver reportes")
    print("8. Salir")

# Bucle principal
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción (1-8): ")

    if opcion == "1":
        registrar_cliente()
    elif opcion == "2":
        registrar_habitacion()
    elif opcion == "3":
        ver_disponibilidad()
    elif opcion == "4":
        crear_reserva()
    elif opcion == "5":
        cancelar_reserva()
    elif opcion == "6":
        procesar_pago()
    elif opcion == "7":
        ver_reportes()
    elif opcion == "8":
        print(" Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print(" Opción no válida. Intenta de nuevo.")

#  Guardar datos al salir
gestor_clientes.guardar_clientes()
gestor_habitaciones.guardar_habitaciones()
gestor_reservas.guardar_reservas()







