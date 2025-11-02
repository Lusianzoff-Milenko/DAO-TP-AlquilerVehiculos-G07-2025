class Cliente:
    def __init__(self, documento, tipo_documento, persona):
        self.documento = documento
        self.tipo_documento = tipo_documento
        self.persona = persona

    def __str__(self):
        return f"Cliente(documento={self.documento}, tipo_documento={self.tipo_documento}, persona={self.persona})"