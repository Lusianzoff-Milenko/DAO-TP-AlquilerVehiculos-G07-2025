class Marca:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"Marca(nombre={self.nombre}, descripcion={self.descripcion})"

