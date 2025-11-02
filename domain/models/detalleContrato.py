class DetalleContrato:
    def __init__(self, contrato, monto, fecha_entrega, fecha_retiro):
        self.contrato = contrato
        self.monto = monto
        self.fecha_entrega = fecha_entrega
        self.fecha_retiro = fecha_retiro

    def __str__(self):
        return (f"DetalleContrato(contrato={self.contrato}, monto={self.monto}, "
                f"fecha_entrega={self.fecha_entrega}, fecha_retiro={self.fecha_retiro})")