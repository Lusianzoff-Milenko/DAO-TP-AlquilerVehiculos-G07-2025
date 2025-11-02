class ModeloXColor:
    def __init__(self, modelo, color):
        self.modelo = modelo
        self.color = color

    def __str__(self):
        return f"Modelo: {self.modelo}, Color: {self.color}"