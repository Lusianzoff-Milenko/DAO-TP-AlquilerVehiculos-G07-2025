from datetime import datetime, date
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
from services.containers.container import Container
from domain.enums import EstadosPoblador


def main():
    # IMPORTANTE: Usar una nueva sesión limpia
    container = Container()

    # Instanciar servicios
    servicios = {
        'vehiculo': container.vehiculo_service(),
        'estado': container.estado_service(),
        'marca': container.marca_service(),
        'modelo': container.modelo_service(),
        'color': container.color_service(),
        'tipo_doc': container.tipo_documento_service(),
        'tipo_inc': container.tipo_inconveniente_service(),
        'tipo_puesto': container.tipo_puesto_service(),
        'persona': container.persona_service(),
        'cliente': container.cliente_service(),
        'empleado': container.empleado_service(),
        'foto': container.fotoxmodelo_service(),
        'mxc': container.modeloxcolor_service(),
        'pago': container.metodo_pago_service(),
        'contrato': container.contrato_service(),
        'detalle': container.detalle_contrato_service(),
        'mantenimiento': container.mantenimiento_service()
    }

    print("🚀 Iniciando población de datos...")

    # 1. Estados
    estados = [Estado(nombre=name, ambito=ambito.value) for name, ambito in EstadosPoblador.__members__.items()]
    servicios['estado'].create_estados(estados)

    # 2. Marcas
    marcas = ["Toyota", "Ford", "Chevrolet", "Honda", "Nissan", "Volkswagen", "Hyundai", "Kia", "Mazda", "Subaru",
              "BMW", "Mercedes-Benz", "Audi", "Lexus", "Jeep"]
    for m in marcas:
        servicios['marca'].create_marca(Marca(nombre=m, descripcion="Marca reconocida"))

    # 3. Modelos
    modelos = [
        ("Corolla", 1, 5, 4, "1.8L I4", 1966),
        ("F-150", 2, 3, 2, "3.3L V6", 1948),
        ("Civic", 4, 5, 4, "2.0L I4", 1972),
        ("Mustang", 2, 4, 2, "5.0L V8", 1964),
        ("Camry", 1, 5, 4, "2.5L I4", 1982)
    ]
    for m in modelos:
        servicios['modelo'].create_modelo(Modelo(
            nombre=m[0], id_marca=m[1], cantidad_pasajeros=m[2],
            cantidad_puertas=m[3], motor=m[4], anio_lanzamiento=m[5]
        ))

    # 4. Colores
    colores = ["Rojo", "Azul", "Negro", "Blanco", "Gris", "Plata", "Verde", "Amarillo", "Naranja", "Marrón"]
    for c in colores:
        servicios['color'].create_color(Color(nombre=c))

    # 5. Tipos Documento
    for td in ["DNI", "Pasaporte", "Licencia de Conducir", "Cédula de Identidad"]:
        servicios['tipo_doc'].create_tipo_documento(TipoDocumento(nombre=td))

    # 6. Tipos Inconveniente
    tipos_inc = ["Mecánico", "Eléctrico", "Neumáticos", "Accesorios", "Otros"]
    for ti in tipos_inc:
        servicios['tipo_inc'].create_tipo_inconveniente(TipoInconveniente(nombre=ti, descripcion="Falla reportada"))

    # 7. Tipos Puesto
    tipos_puesto = ["Administrador", "Mecánico", "Atención al Cliente", "Ventas", "Logística"]
    for tp in tipos_puesto:
        servicios['tipo_puesto'].create_tipo_puesto(TipoPuesto(nombre=tp))

    # 8. Personas
    personas = [
        ("Juan", "Pérez", "12345678", "mailfalso@mail.com", "Calle Falsa 123", date(1990, 1, 1)),
        ("María", "Gómez", "87654321", "mailfalso1@mail.com", "Avenida Siempre Viva 742", date(1985, 6, 15)),
        ("Carlos", "López", "11223344", "mailfalso2@mail.com", "Boulevard Rotos 456", date(1978, 3, 22)),
        ("Ana", "Martínez", "44332211", "mailfalso3@mail.com", "Plaza Mayor 789", date(1995, 12, 5)),
        ("Luis", "Rodríguez", "55667788", "mailfalso4@mail.com", "Callejón del Beso 101", date(1988, 9, 30)),
        ("Laura", "Fernández", "99887766", "mailfalso5@mail.com", "Camino Real 202", date(1992, 11, 11))
    ]
    for p in personas:
        servicios['persona'].create_persona(Persona(
            nombre=p[0], apellido=p[1], telefono=p[2], mail=p[3],
            direccion=p[4], fecha_nacimiento=p[5]
        ))

    # 9. Clientes
    clientes = [("45404967", 1, 4), ("45404961", 1, 5), ("45404962", 1, 6)]
    for dni, tdni, pid in clientes:
        servicios['cliente'].create_cliente(Cliente(documento=dni, id_tipo_documento=tdni, id_persona=pid))

    # 10. Fotos y Colores por Modelo
    # ... (Simplificado: usamos las rutas que ya tenías)
    foto_modelos = [(1, 6, "sources/photos/toyota/corolla/Plata/img.png", 1996)]
    for id_modelo, id_color, ruta, anio in foto_modelos:
        servicios['foto'].create_foto_x_modelo(
            FotoXModelo(id_modelo=id_modelo, id_color=id_color, foto_path=ruta, anio_fabricacion=anio))

    modeloxcolores = [(1, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 1), (3, 3), (3, 4), (4, 2), (5, 3)]
    for id_m, id_c in modeloxcolores:
        servicios['mxc'].create_modelo_color(ModeloXColor(id_modelo=id_m, id_color=id_c))

    # 11. Métodos de Pago
    for mp in ["Efectivo", "Tarjeta de Crédito", "MercadoPago"]:
        servicios['pago'].create_metodo_pago(MetodoDePago(nombre=mp))

    # 12. Empleados
    # ID 1 (Juan) = Administrador, ID 2 (Maria) = Mecánico (Para asignar mantenimientos)
    empleados = [(1, 1, datetime(2020, 1, 15)), (2, 2, datetime(2019, 3, 22)), (3, 3, datetime(2021, 7, 30))]
    for id_tp, id_p, f_ing in empleados:
        servicios['empleado'].create_empleado(Empleado(id_tipo_puesto=id_tp, id_persona=id_p, fecha_ingreso=f_ing))

    # 13. Vehículos
    print("🚗 Creando flota de vehículos...")
    vehiculos = [
        Vehiculo(id_modelo=1, patente="AA111AA", nro_chasis="CH001", id_color=1, anio_fabricacion=datetime(2020, 5, 17),
                 precio_base=20000.0, id_estado=1),
        Vehiculo(id_modelo=2, patente="BB222BB", nro_chasis="CH002", id_color=2, anio_fabricacion=datetime(2019, 8, 25),
                 precio_base=30000.0, id_estado=1),
        Vehiculo(id_modelo=3, patente="CC333CC", nro_chasis="CH003", id_color=3, anio_fabricacion=datetime(2021, 3, 10),
                 precio_base=25000.0, id_estado=1),
    ]
    for v in vehiculos:
        servicios['vehiculo'].create_vehiculo(v)

    # 14. Contrato de Ejemplo
    print("📝 Creando contrato...")
    contrato_ej = Contrato(
        id_cliente=1, id_empleado=1, id_metodo_de_pago=1,
        fecha_desde=datetime(2025, 5, 1), fecha_hasta=datetime(2025, 5, 10),
        tiene_seguro=True, id_estado=9
    )
    detalles_ej = [
        DetalleContrato(id_vehiculo=1, monto=5000.0, fecha_retiro=datetime(2025, 5, 1),
                        fecha_entrega=datetime(2025, 5, 10)),
        DetalleContrato(id_vehiculo=2, monto=7500.0, fecha_retiro=datetime(2025, 5, 1),
                        fecha_entrega=datetime(2025, 5, 10))
    ]
    try:
        servicios['contrato'].crear_contrato_reserva(contrato_ej, detalles_ej)
        print("✅ Contrato creado con éxito.")
    except Exception as e:
        print(f"⚠️ Error creando contrato: {e}")

    # ==============================================================================
    # 15. CREAR VEHÍCULO Y MANDAR A MANTENIMIENTO (NUEVO)
    # ==============================================================================
    print("🔧 Simulando ingreso a taller...")

    # A. Crear un vehículo extra 'Disponible'
    vehiculo_taller = Vehiculo(
        id_modelo=3,  # Honda Civic
        patente="BROKEN1",
        nro_chasis="CH_BROKEN",
        id_color=3,  # Negro
        anio_fabricacion=datetime(2018, 6, 1),
        precio_base=22000.0,
        id_estado=1  # Disponible (ID 1)
    )

    # Guardarlo en BD
    v_id = servicios['vehiculo'].create_vehiculo(vehiculo_taller)

    if v_id:
        # B. Usar la lógica de negocio para enviarlo a mantenimiento
        # Esto actualiza el estado del Vehículo a 'EnMantenimiento' y crea el registro en la tabla Mantenimiento
        exito = servicios['vehiculo'].enviar_a_mantenimiento(
            vehiculo_id=v_id,
            costo=0.0,  # Costo inicial 0 (diagnóstico)
            descripcion="Ruido extraño en el motor al encender",
            id_empleado=2  # Empleado ID 2 (Mecánico María)
        )

        if exito:
            print(f"✅ Vehículo {vehiculo_taller.patente} enviado a mantenimiento exitosamente.")
            print("   -> Estado Vehículo: EnMantenimiento")
            print("   -> Estado Mantenimiento: EnDiagnostico")
        else:
            print("❌ Falló el envío a mantenimiento.")


if __name__ == '__main__':
    main()