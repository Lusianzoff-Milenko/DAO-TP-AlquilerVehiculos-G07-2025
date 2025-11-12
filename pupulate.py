from datetime import datetime
from typing import List

from domain.models.cliente import Cliente
from domain.models.color import Color
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from domain.models.empleado import Empleado
from domain.models.estado import Estado
from domain.models.fotoXModelo import FotoXModelo
from domain.models.marca import Marca
from domain.models.metodoDePago import MetodoDePago
from domain.models.modelo import Modelo
from domain.models.modeloXColor import ModeloXColor
from domain.models.persona import Persona
from domain.models.tipoDocumento import TipoDocumento
from domain.models.tipoInconveniente import TipoInconveniente
from domain.models.tipoPuesto import TipoPuesto
from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.disponible import Disponible
from services.containers.container import Container
from domain.enums import EstadosPoblador

def main():
    container: Container = Container()
    vehiculo_service = container.vehiculo_service()
    estado_service = container.estado_service()
    marca_service = container.marca_service()
    modelo_service = container.modelo_service()
    color_service = container.color_service()
    tipo_documento_service = container.tipo_documento_service()
    tipo_inconveniente_service = container.tipo_inconveniente_service()
    tipo_puesto_service = container.tipo_puesto_service()
    persona_service = container.persona_service()
    cliente_service = container.cliente_service()
    empleado_service = container.empleado_service()
    fotoxmodelo_service = container.fotoxmodelo_service()
    modeloxcolor_service = container.modeloxcolor_service()
    metodoDeMedopago_service = container.metodo_pago_service()
    contrato_service = container.contrato_service()

    # Crar estados
    estados = [Estado(nombre=name, ambito=ambito.value) for name, ambito in EstadosPoblador.__members__.items()]
    for e in estados:
        print(f"Creando estado: {e.nombre} - {e.ambito}")
    estado_service.create_estados(estados)

    #Crear marcas
    marcas = ["Toyota", "Ford", "Chevrolet", "Honda", "Nissan", "Volkswagen", "Hyundai", "Kia", "Mazda", "Subaru", "BMW", "Mercedes-Benz", "Audi", "Lexus", "Jeep"]
    marca_descripciones = ["Marca japonesa reconocida por su fiabilidad y eficiencia.",
                         "Marca estadounidense famosa por sus camionetas y vehículos robustos.",
                         "Marca estadounidense con una amplia gama de vehículos, desde autos compactos hasta camionetas.",
                         "Marca japonesa conocida por sus autos deportivos y motocicletas.",
                         "Marca japonesa con una fuerte presencia en el mercado de autos compactos y sedanes.",
                         "Marca alemana reconocida por su ingeniería y diseño innovador.",
                         "Marca surcoreana que ha ganado popularidad por sus vehículos asequibles y bien equipados.",
                         "Marca surcoreana que ofrece una combinación de estilo, rendimiento y valor.",
                         "Marca japonesa conocida por sus autos deportivos y tecnología avanzada.",
                         "Marca japonesa famosa por sus vehículos todo terreno y rendimiento en condiciones adversas.",
                         "Marca alemana de lujo conocida por su rendimiento y tecnología avanzada.",
                         "Marca alemana de lujo reconocida por su calidad, rendimiento y diseño elegante.",
                         "Marca alemana de lujo famosa por su ingeniería de precisión y tecnología avanzada.",
                         "Marca japonesa de lujo conocida por su comodidad, rendimiento y fiabilidad.",
                         "Marca estadounidense famosa por sus vehículos todoterreno y SUVs."]
    for marca, descripcion in zip(marcas, marca_descripciones):
        print(f"Creando marca: {marca} - {descripcion}")
        marca = Marca(nombre=marca, descripcion=descripcion)
        marca_service.create_marca(marca)

    #Crear modelos
    modelos = [("Corolla", 1, 5, 4, "1.8L I4", datetime(1966, 10, 20).year),
               ("F-150", 2, 3, 2, "3.3L V6", datetime(1948, 1, 1).year),
               ("Civic", 4, 5, 4, "2.0L I4", datetime(1972, 7, 11).year),
               ("Mustang", 2, 4, 2, "5.0L V8", datetime(1964, 4, 17).year),
               ("Camry", 1, 5, 4, "2.5L I4", datetime(1982, 3, 22).year)]
    for nombre, id_marca, pasajeros, puertas, motor, anio in modelos:
        print(f"Creando modelo: {nombre} - Marca ID: {id_marca} - año: {anio}")
        modelo = Modelo(nombre=nombre, id_marca=id_marca, cantidad_puertas=puertas, cantidad_pasajeros=pasajeros, motor=motor, anio_lanzamiento=anio)
        modelo_service.create_modelo(modelo)

    #Crear colores
    colores = ["Rojo", "Azul", "Negro", "Blanco", "Gris", "Plata", "Verde", "Amarillo", "Naranja", "Marrón"]
    for c in colores:
        print(f"Creando color: {c}")
        color = Color(nombre=c)
        color_service.create_color(color)

    #Crear tipos de documento
    tipos_documento = ["DNI", "Pasaporte", "Licencia de Conducir", "Cédula de Identidad"]
    for td in tipos_documento:
        print(f"Creando tipo de documento: {td}")
        tipo_documento = TipoDocumento(nombre=td)
        tipo_documento_service.create_tipo_documento(tipo_documento)


    #Crear tipos de inconveniente
    tipos_inconveniente = ["Mecánico", "Eléctrico", "Neumáticos", "Accesorios", "Otros"]
    tipos_inconveniente_descripciones = ["Problemas relacionados con el motor, transmisión, frenos, suspensión, etc.",
                                        "Problemas relacionados con el sistema eléctrico, batería, luces, etc.",
                                        "Problemas relacionados con los neumáticos, como pinchazos, desgaste irregular, etc.",
                                        "Problemas relacionados con accesorios del vehículo, como sistema de audio, aire acondicionado, etc.",
                                        "Otros tipos de inconvenientes no categorizados anteriormente."]
    for ti, descripcion in zip(tipos_inconveniente, tipos_inconveniente_descripciones):
        print(f"Creando tipo de inconveniente: {ti}")
        tipo_inconveniente = TipoInconveniente(nombre=ti, descripcion=descripcion)
        tipo_inconveniente_service.create_tipo_inconveniente(tipo_inconveniente)


    #Crear tipos de puesto
    tipos_puesto = ["Administrador", "Mecánico", "Atención al Cliente", "Ventas", "Logística"]
    for tp in tipos_puesto:
        print(f"Creando tipo de puesto: {tp}")
        tipo_puesto = TipoPuesto(nombre=tp)
        tipo_puesto_service.create_tipo_puesto(tipo_puesto)

    #Crear Persona
    personas = [("Juan", "Pérez", "12345678", "mailfalso@mail.com", "Calle Falsa 123", datetime(1990, 1, 1)),
                ("María", "Gómez", "87654321", "mailfalso1@mail.com", "Avenida Siempre Viva 742", datetime(1985, 6, 15)),
                ("Carlos", "López", "11223344", "mailfalso2@mail.com", "Boulevard de los Sueños Rotos 456", datetime(1978, 3, 22)),
                ("Ana", "Martínez", "44332211", "mailfalso3@mail.com", "Plaza Mayor 789", datetime(1995, 12, 5)),
                ("Luis", "Rodríguez", "55667788", "mailfalso4@mail.com", "Callejón del Beso 101", datetime(1988, 9, 30)),
                ("Laura", "Fernández", "99887766", "mailfalso5@mail.com", "Camino Real 202", datetime(1992, 11, 11))]
    for nombre, apellido, telefono, mail, direccion, fecha_nacimiento in personas:
        print(f"Creando persona: {nombre} {apellido} - Tel: {telefono}")
        persona = Persona(nombre=nombre, apellido=apellido, telefono=telefono, mail=mail, direccion=direccion, fecha_nacimiento=fecha_nacimiento)
        persona_service.create_persona(persona)


    #Create clientes
    clientes=[("45404967", 1, 4),
              ("45404961", 1, 5),
              ("45404962", 1, 6),]
    for dni, tdni, pid in clientes:
        print(f"Creando cliente para persona ID: {dni}")
        cliente = Cliente(documento=dni, id_tipo_documento=tdni, id_persona=pid)
        cliente_service.create_cliente(cliente)

    #Crear FotoXModelo
    foto_modelos=[
        (1, 6,"sources/photos/toyota/corolla/Plata/img.png", datetime(1996, 1, 1).year),
        (1, 6,"sources/photos/toyota/corolla/Plata/img_1.png", datetime(1996, 1, 1).year),
        (1, 6,"sources/photos/toyota/corolla/Plata/img_2.png", datetime(1996, 1, 1).year),
        (1, 6,"sources/photos/toyota/corolla/Plata/img_3.png", datetime(1996, 1, 1).year),
        (1, 6, "sources/photos/toyota/corolla/Plata/img_4.png", datetime(1996, 1, 1).year),
        (1, 6, "sources/photos/toyota/corolla/Plata/img_5.png", datetime(1996, 1, 1).year),
        (1, 6, "sources/photos/toyota/corolla/Plata/img_6.png", datetime(1996, 1, 1).year),]
    for id_modelo, id_color, ruta, anio in foto_modelos:
        print(f"Creando foto para modelo ID: {id_modelo} - Marca ID: {id_color}")
        modeloxfoto = FotoXModelo(id_modelo=id_modelo, id_color=id_color, foto_path=ruta, anio_fabricacion=anio)
        fotoxmodelo_service.create_foto_x_modelo(modeloxfoto)


    #Create ModeloXColor
    modeloxcolores = [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 4),
        (2, 5),
        (3, 1),
        (3, 4),
        (4, 2),
        (4, 5),
        (5, 3),
        (5, 4),
    ]
    for id_modelo, id_color in modeloxcolores:
        print(f"Asignando color ID: {id_color} al modelo ID: {id_modelo}")
        mxc = ModeloXColor(id_modelo=id_modelo, id_color=id_color)
        modeloxcolor_service.create_modelo_color(mxc)

    #Crear Metodos de pago
    metodos_pago = ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia Bancaria", "MercadoPago"]
    for mp in metodos_pago:
        print(f"Creando método de pago: {mp}")
        metodo_pago = MetodoDePago(nombre=mp)
        metodoDeMedopago_service.create_metodo_pago(metodo_pago)

    #Create empleados
    empleados=[(1, 1, datetime(2020, 1, 15), None)
               ,(2, 2, datetime(2019, 3, 22), None)
               ,(3, 3, datetime(2021, 7, 30), None)]
    for id_tipo_puesto, id_persona, fecha_ingreso, fecha_egreso in empleados:
        print(f"Creando empleado para persona ID: {id_persona}")
        empleado = Empleado(id_tipo_puesto=id_tipo_puesto, id_persona=id_persona, fecha_ingreso=fecha_ingreso, fecha_egreso=fecha_egreso)
        empleado_service.create_empleado(empleado)

    # Crear vehiculos
    vehiculos = [Vehiculo(state=Disponible(), id_modelo=1, patente="ABC123", nro_chasis="CHASIS001", id_color=1, anio_fabricacion=datetime(2020, 5, 17), precio_base=20000.0),
                 Vehiculo(state=Disponible(), id_modelo=2, patente="DEF456", nro_chasis="CHASIS002", id_color=2, anio_fabricacion=datetime(2019, 8, 25), precio_base=30000.0),
                 Vehiculo(state=Disponible(), id_modelo=3, patente="GHI789", nro_chasis="CHASIS003", id_color=3, anio_fabricacion=datetime(2021, 3, 10), precio_base=25000.0),
                 Vehiculo(state=Disponible(), id_modelo=4, patente="JKL012", nro_chasis="CHASIS004", id_color=4, anio_fabricacion=datetime(2018, 11, 5), precio_base=35000.0),
                 Vehiculo(state=Disponible(), id_modelo=5, patente="MNO345", nro_chasis="CHASIS005", id_color=5, anio_fabricacion=datetime(2022, 1, 15), precio_base=22000.0)]
    for v in vehiculos:
        print(f"Creando vehiculo: {v.patente} - Modelo ID: {v.id_modelo} - Color ID: {v.id_color}")
        vehiculo_service.create_vehiculo(v, estado_service)


    contrato_ejemplo = Contrato(
        id_cliente=1,
        fecha_desde=datetime(2025, 5, 1),
        fecha_hasta=datetime(2025, 5, 10),
        id_metodo_de_pago=1,
        id_empleado=1,
        # Asumiendo que el ID 9 es un estado 'Activo' o 'En Curso'
        id_estado=9,
        tiene_seguro=True
    )

    # 2. Definir la lista de Detalles del Contrato (los vehículos alquilados)
    # NOTA: NO asignamos el id_contrato. El servicio lo hace automáticamente.
    detalles_ejemplo: List[DetalleContrato] = [
        DetalleContrato(
            # id_contrato= El servicio lo asignará (debe ser None al inicio)
            id_vehiculo=1,  # Alquila el Vehículo con ID 1
            monto=5000.0,
            fecha_retiro=datetime(2025, 5, 1),
            fecha_entrega=datetime(2025, 5, 10),
        ),
        DetalleContrato(
            # id_contrato= El servicio lo asignará
            id_vehiculo=2,  # Alquila el Vehículo con ID 2
            monto=7500.0,
            fecha_retiro=datetime(2025, 5, 1),
            fecha_entrega=datetime(2025, 5, 10),
        )
    ]

    # 3. Llamar al nuevo método del servicio
    nuevo_contrato_id = contrato_service.crear_contrato_con_detalles(
        contrato=contrato_ejemplo,
        detalles=detalles_ejemplo,
        detalles_service=container.detalle_contrato_service()
    )

    if nuevo_contrato_id:
        print(f"✅ Nuevo Contrato con detalles creado exitosamente. ID: {nuevo_contrato_id}")
    else:
        print("❌ Falló la creación del Contrato o sus detalles.")

if __name__ == '__main__':
    main()