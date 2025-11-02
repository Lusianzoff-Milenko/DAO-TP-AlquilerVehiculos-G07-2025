class Modelo:
    def __init__(self,nombre, marca, cantidad_pasajeros, cantidad_puertas, motor, año_lanzamiento):
        self.nombre = nombre
        self.marca = marca
        self.cantidad_pasajeros = cantidad_pasajeros
        self.cantidad_puertas = cantidad_puertas
        self.motor = motor
        self.año_lanzamiento = año_lanzamiento

    def __str__(self):
        return f"Modelo: {self.nombre}, Marca: {self.marca}, Pasajeros: {self.cantidad_pasajeros}, Puertas: {self.cantidad_puertas}, Motor: {self.motor}, Año: {self.año_lanzamiento}"

