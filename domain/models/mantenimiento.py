class Mantenimiento:
    def __init__(self, vehiculo, costo, descripcion, estado, empleado, fecha_hora):
        self.vehiculo = vehiculo
        self.costo = costo
        self.descripcion = descripcion
        self.estado = estado
        self.empleado = empleado
        self.fecha_hora = fecha_hora

    def __str__(self):
        return f"Mantenimiento(vehiculo={self.vehiculo}, costo={self.costo}, descripcion={self.descripcion}, estado={self.estado}, empleado={self.empleado}, fecha_hora={self.fecha_hora})"

