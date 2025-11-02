class Contrato:
    def __init__(self, cliente, vehiculo, fecha_desde, fecha_hasta, metodo_de_pago, empleado, estado, tiene_seguro):
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.metodo_de_pago = metodo_de_pago
        self.empleado = empleado
        self.estado = estado
        self.tiene_seguro = tiene_seguro

    def __str__(self):
        return f"Contrato(cliente={self.cliente}, vehiculo={self.vehiculo}, fecha_desde={self.fecha_desde}, fecha_hasta={self.fecha_hasta}, metodo_de_pago={self.metodo_de_pago}, empleado={self.empleado}, estado={self.estado}, tiene_seguro={self.tiene_seguro})"
