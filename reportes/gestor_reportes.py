class GestorReportes:
    def __init__(self, gestor_reservas, gestor_pagos, gestor_clientes, gestor_habitaciones):
        self.gestor_reservas = gestor_reservas
        self.gestor_pagos = gestor_pagos
        self.gestor_clientes = gestor_clientes
        self.gestor_habitaciones = gestor_habitaciones

    # 📌 RESERVAS
    def mostrar_reservas_activas(self):
        return [r for r in self.gestor_reservas.reservas if r.estado == "Confirmada"]

    def mostrar_reservas_canceladas(self):
        return [r for r in self.gestor_reservas.reservas if r.estado == "Cancelada"]

    def mostrar_reservas_pendientes(self):
        return [r for r in self.gestor_reservas.reservas if r.estado == "Pendiente"]

    def mostrar_reservas_por_cliente(self, documento):
        cliente = self.gestor_clientes.buscar_por_documento(documento)
        return cliente.reservas if cliente else []

    def mostrar_reservas_por_fecha(self, fecha):
        return [r for r in self.gestor_reservas.reservas if r.fecha_inicio <= fecha <= r.fecha_fin]

    # 💳 PAGOS
    def mostrar_historial_pagos(self):
        return [p for p in self.gestor_pagos.pagos if p.estado == "Pagado"]

    def mostrar_pagos_pendientes(self):
        return [p for p in self.gestor_pagos.pagos if p.estado == "Pendiente"]

    def mostrar_pagos_cancelados(self):
        return [p for p in self.gestor_pagos.pagos if p.estado == "Cancelado"]

    def mostrar_pagos_por_cliente(self, documento):
        cliente = self.gestor_clientes.buscar_por_documento(documento)
        return [p for p in self.gestor_pagos.pagos if p.reserva.cliente == cliente] if cliente else []

    def calcular_total_ingresos(self):
        return sum(p.monto for p in self.gestor_pagos.pagos if p.estado == "Pagado")

    # 🛏️ HABITACIONES
    def mostrar_ocupacion_habitaciones(self):
        ocupadas = [h for h in self.gestor_habitaciones.habitaciones if h.ocupaciones]
        disponibles = [h for h in self.gestor_habitaciones.habitaciones if not h.ocupaciones]
        return {
            "ocupadas": ocupadas,
            "disponibles": disponibles,
            "total": len(self.gestor_habitaciones.habitaciones)
    }

    def mostrar_habitaciones_por_tipo(self, tipo):
        return [h for h in self.gestor_habitaciones.habitaciones if h.tipo.lower() == tipo.lower()]

    # 👤 CLIENTES
    def mostrar_clientes_con_reservas(self):
        return [c for c in self.gestor_clientes.clientes if c.reservas]

    def mostrar_clientes_sin_reservas(self):
        return [c for c in self.gestor_clientes.clientes if not c.reservas]

    # 📊 RESUMEN GENERAL
    def resumen_general(self):
        return {
            "total_clientes": len(self.gestor_clientes.clientes),
            "total_reservas": len(self.gestor_reservas.reservas),
            "reservas_activas": len(self.mostrar_reservas_activas()),
            "reservas_canceladas": len(self.mostrar_reservas_canceladas()),
            "reservas_pendientes": len(self.mostrar_reservas_pendientes()),
            "total_pagos": len(self.gestor_pagos.pagos),
            "pagos_pendientes": len(self.mostrar_pagos_pendientes()),
            "pagos_cancelados": len(self.mostrar_pagos_cancelados()),
            "ingresos_totales": sum(p.monto for p in self.gestor_pagos.pagos if p.estado == "Pagado"),
            "habitaciones_ocupadas": len(self.mostrar_ocupacion_habitaciones()["ocupadas"]),
            "habitaciones_disponibles": len(self.mostrar_ocupacion_habitaciones()["disponibles"]),
        }
