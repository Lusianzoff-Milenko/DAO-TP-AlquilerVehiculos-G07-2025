import datetime
from data_access.database_connector import Database
from typing import Dict, Any

from data_access.repositories.detalle_contrato_repository import DetalleContratoRepository
from data_access.repositories.inconveniente_repository import InconvenienteRepository
# --- Repositorios (Necesarios solo para la inyección) ---
from data_access.repositories.persona_repository import PersonaRepository
from data_access.repositories.cliente_repository import ClienteRepository
from data_access.repositories.empleado_repository import EmpleadoRepository
from data_access.repositories.vehiculo_repository import VehiculoRepository
from data_access.repositories.contrato_repository import ContratoRepository
from data_access.repositories.mantenimiento_repository import MantenimientoRepository
from data_access.repositories.tipo_documento_repository import TipoDocumentoRepository
from data_access.repositories.tipo_puesto_repository import TipoPuestoRepository
from data_access.repositories.metododepago_repository import MetodoDePagoRepository
from data_access.repositories.marca_repository import MarcaRepository
from data_access.repositories.color_repository import ColorRepository
from data_access.repositories.modelo_repository import ModeloRepository
from data_access.repositories.tipo_inconveniente_repository import TipoInconvenienteRepository
from data_access.repositories.estado_repository import EstadoRepository
from data_access.repositories.modelo_x_color_repository import ModeloXColorRepository
from data_access.repositories.foto_x_modelo_repository import FotoXModeloRepository
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from domain.models.inconveniente import Inconveniente
from domain.models.mantenimiento import Mantenimiento
from services.detalle_contrato_service import DetalleContratoService
from services.inconveniente_service import InconvenienteService

# --- Servicios (Capa de Interacción) ---
from services.persona_service import PersonaService  # Asumido
from services.cliente_service import ClienteService
from services.empleado_service import EmpleadoService
from services.vehiculo_service import VehiculoService
from services.contrato_service import ContratoService
from services.mantenimiento_service import MantenimientoService
from services.estado_service import EstadoService
from services.tipodocumento_service import TipoDocumentoService
from services.tipopuesto_service import TipoPuestoService
from services.metododepago_service import MetodoDePagoService
from services.marca_service import MarcaService
from services.color_service import ColorService
from services.modelo_service import ModeloService
from services.tipoinconveniente_service import TipoInconvenienteService
from services.fotoxmodelo_service import FotoXModeloService
from services.modeloxcolor_service import ModeloXColorService

# --- Modelos de Dominio ---
from domain.models.persona import Persona
from domain.models.cliente import Cliente
from domain.models.empleado import Empleado
from domain.models.vehiculo import Vehiculo
from domain.models.tipoDocumento import TipoDocumento
from domain.models.tipoPuesto import TipoPuesto
from domain.models.metodoDePago import MetodoDePago
from domain.models.marca import Marca
from domain.models.color import Color
from domain.models.modelo import Modelo
from domain.models.tipoInconveniente import TipoInconveniente
from domain.models.fotoXModelo import FotoXModelo
DATABASE_FILE = "./alquiler_vehiculos_data_base.db"

# --- IDs CLAVE (Necesarios para la población) ---
ID_VEHICULO_DISPONIBLE = 5
ID_VEHICULO_ALQUILADO = 7
ID_VEHICULO_EN_MANTENIMIENTO = 10


# ------------------------------------------------


def setup_architecture(db_instance: Database) -> Dict[str, Any]:
    """Inicializa toda la arquitectura de Repositorios y Servicios."""

    # 1. INICIALIZACIÓN DE REPOSITORIOS
    repos = {
        'persona': PersonaRepository(db_instance), 'cliente': ClienteRepository(db_instance),
        'empleado': EmpleadoRepository(db_instance), 'vehiculo': VehiculoRepository(db_instance),
        'contrato': ContratoRepository(db_instance), 'mantenimiento': MantenimientoRepository(db_instance),
        'tipo_documento': TipoDocumentoRepository(db_instance), 'tipo_puesto': TipoPuestoRepository(db_instance),
        'metodo_pago': MetodoDePagoRepository(db_instance), 'marca': MarcaRepository(db_instance),
        'color': ColorRepository(db_instance), 'modelo': ModeloRepository(db_instance),
        'tipo_inconveniente': TipoInconvenienteRepository(db_instance), 'estado': EstadoRepository(db_instance),
        'mxc': ModeloXColorRepository(db_instance), 'fotoxm': FotoXModeloRepository(db_instance),
        'detalle_contrato': DetalleContratoRepository(db_instance),
        'inconveniente': InconvenienteRepository(db_instance)
    }

    # 2. INICIALIZACIÓN DE SERVICIOS (Con Inyección de Dependencias)
    services = {}
    services['estado'] = EstadoService(repos['estado'])
    services['tipo_documento'] = TipoDocumentoService(repos['tipo_documento'])
    services['tipo_puesto'] = TipoPuestoService(repos['tipo_puesto'])
    services['metodo_pago'] = MetodoDePagoService(repos['metodo_pago'])
    services['marca'] = MarcaService(repos['marca'])
    services['color'] = ColorService(repos['color'])
    services['tipo_inconveniente'] = TipoInconvenienteService(repos['tipo_inconveniente'])
    services['persona'] = PersonaService(repos['persona'])
    services['detalle_contrato'] = DetalleContratoService(repos['detalle_contrato'], repos['contrato'])

    # Manejar dependencias para Servicios Complejos
    services['modelo'] = ModeloService(repos['modelo'], repos['marca'])
    services['mantenimiento'] = MantenimientoService(repos['mantenimiento'], repos['vehiculo'], repos['estado'],
                                                     repos['empleado'])
    services['fotoxm'] = FotoXModeloService(repos['fotoxm'], repos['modelo'], repos['color'])
    services['mxc'] = ModeloXColorService(repos['mxc'], repos['modelo'], repos['color'])

    # ContratoService y Servicios dependientes
    # Nota: ContratoService se necesita para inyectar en Cliente/Empleado/Vehiculo
    services['contrato'] = ContratoService(
        contrato_repo=repos['contrato'], cliente_repo=repos['cliente'], vehiculo_repo=repos['vehiculo'],
        metodo_pago_repo=repos['metodo_pago'], empleado_repo=repos['empleado'], estado_repo=repos['estado'],
        estado_service=services['estado'], detalle_contrato_service=services['detalle_contrato']  # Se inyectará después
    )
    services['vehiculo'] = VehiculoService(repos['vehiculo'], repos['modelo'], repos['color'], repos['estado'],
                                           services['contrato'])

    services['cliente'] = ClienteService(repos['cliente'], repos['persona'], repos['tipo_documento'],
                                         services['contrato'])

    services['empleado'] = EmpleadoService(repos['empleado'], repos['persona'], repos['tipo_puesto'],
                                           services['contrato'])

    services['inconveniente'] = InconvenienteService(repos['inconveniente'], repos['tipo_inconveniente'],
                                                     repos['contrato'], repos['estado'])

    return services


def populate_system_base(services: Dict[str, Any]):
    print("Iniciando la población de datos base (Orden Topológico) a través de SERVICIOS...")
    today = datetime.datetime.now()

    # ----------------------------------------------------
    # 1. CATÁLOGO BASE Y ESTADOS (Nivel 0: Sin dependencias)
    # ----------------------------------------------------
    print("\n1. Insertando Catálogo Base y Estados...")

    # A. ESTADOS (Crítico, debe ir primero)
    # B. CATÁLOGO BASE
    services['tipo_documento'].create_tipo_documento(TipoDocumento(nombre="DNI"))  # ID 1
    services['tipo_puesto'].create_tipo_puesto(TipoPuesto(nombre="Vendedor"))  # ID 1 (Asumido)
    services['tipo_puesto'].create_tipo_puesto(TipoPuesto(nombre="Gerente"))  # ID 2 (Asumido)
    services['metodo_pago'].create_metodo_pago(MetodoDePago(nombre="Tarjeta"))  # ID 1
    services['color'].create_color(Color(nombre="Rojo"))  # ID 1
    services['marca'].create_marca(Marca(nombre="Toyota", descripcion="Marca Japonesa confiable"))  # ID 1
    services['tipo_inconveniente'].create_tipo_inconveniente(
        TipoInconveniente(nombre="Choque", descripcion="Daño por colisión"))  # ID 1

    # ----------------------------------------------------
    # 2. PERSONAS (Entidad Base)
    # ----------------------------------------------------
    print("2. Insertando Personas...")

    # P1: Cliente Ana (id_persona=1)
    p1_id = services['persona'].create_persona(
        Persona(nombre="Ana", apellido="Gomez", telefono="1122334455", mail="ana@ejemplo.com",
                direccion="Calle Falsa 123", fecha_nacimiento=today - datetime.timedelta(days=365 * 30)))

    # P2: Cliente Luis (id_persona=2)
    p2_id = services['persona'].create_persona(
        Persona(nombre="Luis", apellido="Perez", telefono="9988776655", mail="luis@ejemplo.com",
                direccion="Av. Central 456", fecha_nacimiento=today - datetime.timedelta(days=365 * 25)))

    # P3: Empleado Carlos (id_persona=3)
    p3_id = services['persona'].create_persona(
        Persona(nombre="Carlos", apellido="Diaz", telefono="5544332211", mail="carlos@ejemplo.com",
                direccion="Ruta Sur 789", fecha_nacimiento=today - datetime.timedelta(days=365 * 40)))

    # ----------------------------------------------------
    # 3. ENTIDADES DE NIVEL 1 (Dependen de Personas/Catálogo)
    # ----------------------------------------------------
    print("3. Insertando Clientes, Empleados y Modelos...")

    # Clientes (Depende de Persona y TipoDocumento)
    services['cliente'].create_cliente(Cliente(documento="12345678", id_tipo_documento=1, id_persona=p1_id))
    services['cliente'].create_cliente(Cliente(documento="87654321", id_tipo_documento=1, id_persona=p2_id))

    # Empleados (Depende de Persona y TipoPuesto)
    # Asumo que TipoPuesto ID 2 es 'Gerente' o un puesto válido
    services['empleado'].create_empleado(
        Empleado(id_tipo_puesto=2, id_persona=p3_id, fecha_ingreso=today - datetime.timedelta(days=365 * 2)))

    # Modelos (Depende de Marca)
    m1_id = services['modelo'].create_modelo(
        Modelo(nombre="Corolla", id_marca=1, cantidad_pasajeros=5, cantidad_puertas=4, motor="1.8L",
               anio_lanzamiento="2020"))
    m2_id = services['modelo'].create_modelo(
        Modelo(nombre="Hilux", id_marca=1, cantidad_pasajeros=5, cantidad_puertas=4, motor="2.8D",
               anio_lanzamiento="2022"))

    # ----------------------------------------------------
    # 4. ENTIDADES DE NIVEL 2 (Dependen de Modelo/Color/Estado)
    # ----------------------------------------------------
    print("4. Insertando Vehículos y Relaciones Modelo...")

    # Vehículos (Dependen de Modelo, Color, Estado)
    v1_id = services['vehiculo'].create_vehiculo(
        Vehiculo(id_modelo=m1_id, patente="AA123BB", nro_chasis="CHASIS001", id_color=1,
                 anio_fabricacion=datetime.datetime(2020, 1, 1), precio_base=500.00, id_estado=ID_VEHICULO_DISPONIBLE))
    v2_id = services['vehiculo'].create_vehiculo(
        Vehiculo(id_modelo=m2_id, patente="CC456DD", nro_chasis="CHASIS002", id_color=1,
                 anio_fabricacion=datetime.datetime(2022, 1, 1), precio_base=800.00, id_estado=ID_VEHICULO_ALQUILADO))
    v3_id = services['vehiculo'].create_vehiculo(
        Vehiculo(id_modelo=m1_id, patente="EE789FF", nro_chasis="CHASIS003", id_color=1,
                 anio_fabricacion=datetime.datetime(2019, 1, 1), precio_base=400.00,
                 id_estado=ID_VEHICULO_EN_MANTENIMIENTO))

    # Relación M:N Modelo X Color (Depende de Modelo y Color)
    services['mxc'].add_modelo_color(id_modelo=m1_id, id_color=1)

    # Foto X Modelo (Depende de Modelo y Color)
    services['fotoxm'].create_foto_x_modelo(
        FotoXModelo(id_modelo=m1_id, id_color=1, foto_path="/path/to/corolla_rojo.jpg", anio_fabricacion=2020))

    print("\n✅ Base de datos base poblada exitosamente a través de Servicios. Las entidades base están listas.")

    print("4. Insertando Vehículos y Relaciones Modelo...")

    # --- Asumimos que los IDs de la Sección 4 fueron capturados localmente ---
    # Para la Sección 5, recuperamos los IDs de Modelo que serán usados para Inconvenientes

    today = datetime.datetime.now()

    # python
    # file: `populate_db_final.py` (Sección 5 Corregida)

    # NOTA: Asegúrese de que la clave 'inconveniente' exista en el diccionario 'services'.

    # --- Constantes Usadas ---
    ID_CLIENTE_ANA = 1
    ID_CLIENTE_LUIS = 2
    ID_EMPLEADO_CARLOS = 1
    ID_VEHICULO_V1 = v1_id  # Disponible (Para C1)
    ID_VEHICULO_V2 = v2_id  # Alquilado (Para C2)
    ID_VEHICULO_V3 = v3_id  # En Mantenimiento (Para M2)
    ID_TIPO_INCONVENIENTE_CHOQUE = 1
    ID_CONTRATO_EN_CURSO = 2
    ID_CONTRATO_CANCELADO = 3
    ID_MANTENIMIENTO_REPARADO = 14
    ID_MANTENIMIENTO_EN_DIAGNOSTICO = 12
    ID_INCONVENIENTE_EN_CURSO = 2  # Usamos el mismo ID que Contrato EN_CURSO para el estado del incidente, como se infiere del ejemplo.

    print("\n5. Insertando Contratos, Detalles, Mantenimientos e Inconvenientes...")

    contrato1 = Contrato(
        id_cliente=ID_CLIENTE_ANA, id_vehiculo=ID_VEHICULO_V1,
        fecha_desde=today - datetime.timedelta(days=10), fecha_hasta=today - datetime.timedelta(days=5),
        id_metodo_de_pago=1, id_empleado=ID_EMPLEADO_CARLOS,
        id_estado=ID_CONTRATO_CANCELADO, tiene_seguro=True
    )
    detalles1 = [
        DetalleContrato(monto=500.00, fecha_entrega=today - datetime.timedelta(days=5),
                        fecha_retiro=today - datetime.timedelta(days=10))
    ]
    c1_id = services['contrato'].create_contrato(contrato1, detalles1)

    # C2: Contrato ACTIVO/En Curso - Cliente Luis
    contrato2 = Contrato(
        id_cliente=ID_CLIENTE_LUIS, id_vehiculo=ID_VEHICULO_V2,
        fecha_desde=today - datetime.timedelta(days=2), fecha_hasta=today + datetime.timedelta(days=5),
        id_metodo_de_pago=1, id_empleado=ID_EMPLEADO_CARLOS,
        id_estado=ID_CONTRATO_EN_CURSO, tiene_seguro=True
    )
    detalles2 = [
        DetalleContrato(monto=1600.00, fecha_entrega=today + datetime.timedelta(days=5),
                        fecha_retiro=today - datetime.timedelta(days=2))
    ]
    c2_id = services['contrato'].create_contrato(contrato2, detalles2)

    # B. MANTENIMIENTO

    # M1: Histórico/Reparado (Vehículo V1)
    services['mantenimiento'].create_mantenimiento(Mantenimiento(
        id_vehiculo=ID_VEHICULO_V1, costo=150.00, descripcion="Cambio de aceite y filtros",
        id_estado=ID_MANTENIMIENTO_REPARADO, id_empleado=ID_EMPLEADO_CARLOS,
        fecha_hora=today - datetime.timedelta(days=20))
    )

    # M2: Activo/En Diagnóstico (Vehículo V3)
    # [CORRECCIÓN] Cambiado id_vehiculo=2 a id_vehiculo=ID_VEHICULO_V3 (3)
    services['mantenimiento'].create_mantenimiento(Mantenimiento(
        id_vehiculo=ID_VEHICULO_V3, costo=0.00, descripcion="Diagnóstico de fallas en motor",
        id_estado=ID_MANTENIMIENTO_EN_DIAGNOSTICO, id_empleado=ID_EMPLEADO_CARLOS,
        fecha_hora=today - datetime.timedelta(hours=2))
    )

    # C. REGISTRO INCONVENIENTES

    # I1: Inconveniente registrado en Contrato ACTIVO (C2)
    # [CORRECCIÓN] Cambiado id_contrato=2 a id_contrato=c2_id (usando el ID recién creado)
    services['inconveniente'].create_inconveniente(Inconveniente(
        nombre="Rayón en puerta", descripcion="Rayón leve en puerta trasera",
        id_tipo_inconveniente=ID_TIPO_INCONVENIENTE_CHOQUE, costo=300.00,
        id_contrato=c2_id, id_estado=ID_INCONVENIENTE_EN_CURSO)
    )

    print("\n✅ Población FINALIZADA. Entidades transaccionales creadas con éxito.")


if __name__ == "__main__":
    try:
        db_instance = Database(db_path=DATABASE_FILE)
        services = setup_architecture(db_instance)
        populate_system_base(services)

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO AL POBLAR EL SISTEMA: {e}")

    finally:
        if 'db_instance' in locals():
            db_instance.close()