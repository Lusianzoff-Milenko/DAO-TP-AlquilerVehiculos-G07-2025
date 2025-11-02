class Vehiculo:
    def __init__(self, modelo, patente, nro_chasis, color, anio_fabricacion, precio_base, estado):
        self.modelo = modelo
        self.patente = patente
        self.nro_chasis = nro_chasis
        self.color = color
        self.anio_fabricacion = anio_fabricacion
        self.precio_base = precio_base
        self.estado = estado

    def __str__(self):
        return f"Vehiculo(modelo={self.modelo}, patente={self.patente}, nro_chasis={self.nro_chasis}, color={self.color}, anio_fabricacion={self.anio_fabricacion}, precio_base={self.precio_base}, estado={self.estado})"

