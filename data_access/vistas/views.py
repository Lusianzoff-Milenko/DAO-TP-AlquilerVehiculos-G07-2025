from sqlalchemy import Column, Integer, String, Float
from domain.models.base import Base

# Nota: SQLAlchemy no crea las vistas, asume que ya existen en la BD (creadas por tu script SQL).
# Usamos __tablename__ igual al nombre de la vista en BD.

class VistaClientesContacto(Base):
    __tablename__ = 'VistaClientesContacto'
    # Asumimos que la vista tiene una columna pseudo-pk o usamos la del cliente
    id_cliente = Column("Cliente_ID", Integer, primary_key=True)
    nombre = Column("Nombre", String)
    apellido = Column("Apellido", String)
    tipo_documento = Column("Tipo_Documento", String)
    documento = Column("Documento", String)
    fecha_nacimiento = Column("Fecha_Nacimiento", String)
    telefono = Column("Teléfono", String)
    mail = Column("Correo_Electrónico", String)
    direccion = Column("Dirección", String)

class VistaContratosRentabilidad(Base):
    __tablename__ = 'VistaContratosRentabilidad'
    id_contrato = Column("Contrato_ID", Integer, primary_key=True)
    patente = Column("Patente_Vehiculo", String)
    cliente = Column("Nombre_Cliente", String)
    empleado = Column("Empleado_Vendedor", String)
    fecha_desde = Column("Fecha_Desde", String)
    fecha_hasta = Column("Fecha_Hasta", String)
    fecha_entrega = Column("Fecha_Real_Entrega", String)
    metodo_pago = Column("Método_Pago", String)
    estado = Column("Estado_Contrato", String)
    monto = Column("Monto_Contrato", Float)
    tiene_seguro = Column("Tiene_Seguro", Integer)
    costo_inconvenientes = Column("Costo_Total_Inconvenientes", Float)

class VistaDisponibilidadFlota(Base):
    __tablename__ = 'VistaDisponibilidadFlota'
    id_vehiculo = Column("Vehiculo_ID", Integer, primary_key=True)
    patente = Column("Patente", String)
    marca = Column("Marca", String)
    modelo = Column("Modelo", String)
    precio_base = Column("Precio_Base", Float)
    estado_actual = Column("Estado_Actual", String)

class VistaReporteFacturacion(Base):
    __tablename__ = 'VistaReporteFacturacion'
    id_contrato = Column("Contrato_ID", Integer, primary_key=True)
    patente = Column("Patente", String)
    cliente = Column("Cliente", String)
    fecha_inicio = Column("Fecha_Inicio", String)
    fecha_fin = Column("Fecha_Fin_Esperada", String)
    fecha_entrega = Column("Fecha_Entrega_Real", String)
    dias_alquilados = Column("Dias_Alquilados", Float)
    monto_base = Column("Monto_Alquiler_Base", Float)
    costo_inconvenientes = Column("Costo_Total_Inconvenientes", Float)
    total_facturado = Column("Monto_Total_Facturado", Float)
    estado = Column("Estado_Contrato", String)

class VistaUtilizacionFlota(Base):
    __tablename__ = 'VistaUtilizacionFlota'
    id_vehiculo = Column("Vehiculo_ID", Integer, primary_key=True)
    patente = Column("Patente", String)
    marca = Column("Marca", String)
    modelo = Column("Modelo", String)
    anio = Column("Año", String)
    contratos_totales = Column("Contratos_Totales", Integer)
    dias_alquilados = Column("Total_Dias_Alquilados", Float)
    estado_actual = Column("Estado_Actual", String)

class VistaVehiculosDetallados(Base):
    __tablename__ = 'VistaVehiculosDetallados'
    modelo = Column("Modelo", String)
    marca = Column("Marca", String)
    color = Column("Color", String)
    patente = Column("Patente", String, primary_key=True)
    foto = Column("Foto", String)
    anio = Column("Año", String)
    puertas = Column("Cantidad_Puertas", Integer)
    pasajeros = Column("Cantidad_Pasajeros", Integer)
    precio = Column("Precio_Base", Float)
    estado = Column("Estado_Vehiculo", String)

class VistaEmpleados(Base):
    __tablename__ = 'VistaEmpleadosPuestos'
    id_empleado = Column("Empleado_ID", Integer, primary_key=True)
    nombre = Column("Nombre", String)
    apellido = Column("Apellido", String)
    puesto = Column("Puesto", String)
    fecha_contratacion = Column("Fecha_Ingreso", String)
    fecha_salida = Column("Fecha_Egreso", String)
    telefono = Column("Teléfono", String)
    mail = Column("Correo_Electrónico", String)