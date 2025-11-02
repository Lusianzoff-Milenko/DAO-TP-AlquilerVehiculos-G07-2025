class Inconveniente:
    def __init__(self, nombre, descripcion, tipo_inconveniente, costo, contrato, estado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_inconveniente = tipo_inconveniente
        self.costo = costo
        self.contrato = contrato
        self.estado = estado

    def __str__(self):
        return f"Inconveniente(nombre={self.nombre}, descripcion={self.descripcion}, tipoInconveniente={self.tipo_inconveniente}, costo={self.costo}, contrato={self.contrato}, estado={self.estado})"
