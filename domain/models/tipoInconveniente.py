class TipoInconveniente:
    def __init__(self, nombre, descipcion):
        self.nombre = nombre
        self.descipcion = descipcion

    def __str__(self):
        return f"TipoInconveniente(nombre={self.nombre}, descripcion={self.descipcion})"