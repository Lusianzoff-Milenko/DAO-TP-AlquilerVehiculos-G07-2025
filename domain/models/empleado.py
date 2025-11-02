class Empleado:
    def __init__(self, tipo_puesto, persona, fecha_ingreso, fecha_egreso):
        self.tipo_puesto = tipo_puesto
        self.persona = persona
        self.fecha_ingreso = fecha_ingreso
        self.fecha_egreso = fecha_egreso

    def __str__(self):
        return f"Empleado(tipoPuesto={self.tipo_puesto}, id_persona={self.persona}, fecha_ingreso={self.fecha_ingreso}, fecha_egreso={self.fecha_egreso})"

