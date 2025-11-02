class foto_x_modelo:
    def __init__ (self, modelo, color, foto_path,   anio_fabricacion):
        self.modelo = modelo
        self.color = color
        self.foto_path = foto_path
        self.anio_fabricacion = anio_fabricacion

    def __str__(self):
        return f"Modelo: {self.modelo}, Color: {self.color}, Foto Path: {self.foto_path}, Año de Fabricación: {self.anio_fabricacion}"
