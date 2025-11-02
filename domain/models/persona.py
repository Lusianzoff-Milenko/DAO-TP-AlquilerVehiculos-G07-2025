class Persona:
    def __init__(self, nombre, apellido, telefono, mail, direccion, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f"{self.nombre} {self.apellido}, Tel: {self.telefono}, Email: {self.mail}, Dirección: {self.direccion}, Fecha de Nacimiento: {self.fecha_nacimiento}"

