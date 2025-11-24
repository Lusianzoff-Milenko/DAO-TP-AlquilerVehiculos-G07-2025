from dependency_injector import containers, providers

# 1. Importamos la configuración de BD refactorizada
# Asegúrate de haber creado config/database_sqlalchemy.py como se indicó
from config.database_sqlalchemy import SessionLocal

# 2. Importamos Repositorios
from data_access.repositories import (
    VehiculoRepository, ModeloRepository, ColorRepository,
    EstadoRepository, ContratoRepository, ClienteRepository,
    MetodoDePagoRepository, EmpleadoRepository, DetalleContratoRepository,
    MarcaRepository, TipoDocumentoRepository, TipoPuestoRepository,
    TipoInconvenienteRepository, InconvenienteRepository, MantenimientoRepository,
    PersonaRepository, FotoXModeloRepository, ModeloXColorRepository
)

# 3. Importamos Servicios
from services import (
    VehiculoService, ContratoService, EstadoService,
    DetalleContratoService, MarcaService, ModeloService,
    ClienteService, TipoPuestoService, EmpleadoService,
    TipoInconvenienteService, InconvenienteService, MantenimientoService,
    ColorService, MetodoDePagoService, TipoDocumentoService,
    PersonaService, FotoXModeloService, ModeloXColorService
)

from services.validation_mapper import ValidationMapper


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # --- Gestión de Sesión de Base de Datos ---
    # Proveedor de recurso para la Sesión de SQLAlchemy.
    # Esto asegura que la sesión se cree y se cierre correctamente.
    db_session = providers.Resource(SessionLocal)

    # --- Repositorios (Inyectando la sesión) ---
    # Cambiamos a Factory para que reciban la sesión actual del contexto.

    modelo_repo = providers.Factory(ModeloRepository, session=db_session)
    color_repo = providers.Factory(ColorRepository, session=db_session)
    estado_repo = providers.Factory(EstadoRepository, session=db_session)
    vehiculo_repo = providers.Factory(VehiculoRepository, session=db_session)
    contrato_repo = providers.Factory(ContratoRepository, session=db_session)
    cliente_repo = providers.Factory(ClienteRepository, session=db_session)
    metodo_pago_repo = providers.Factory(MetodoDePagoRepository, session=db_session)
    empleado_repo = providers.Factory(EmpleadoRepository, session=db_session)
    detalle_contrato_repo = providers.Factory(DetalleContratoRepository, session=db_session)
    marca_repo = providers.Factory(MarcaRepository, session=db_session)
    tipo_documento_repo = providers.Factory(TipoDocumentoRepository, session=db_session)
    tipo_puesto_repo = providers.Factory(TipoPuestoRepository, session=db_session)
    tipo_inconveniente_repo = providers.Factory(TipoInconvenienteRepository, session=db_session)
    inconveniente_repo = providers.Factory(InconvenienteRepository, session=db_session)
    mantenimiento_repo = providers.Factory(MantenimientoRepository, session=db_session)
    persona_repo = providers.Factory(PersonaRepository, session=db_session)
    fotoxmodelo_repo = providers.Factory(FotoXModeloRepository, session=db_session)
    modeloxcolor_repo = providers.Factory(ModeloXColorRepository, session=db_session)

    # --- Mappers de Validación ---
    # ValidationMapper utiliza los repositorios para verificar la existencia de claves foráneas.

    detalle_contrato_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'contrato': contrato_repo,
            'vehiculo': vehiculo_repo,
        }
    )

    empleado_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'tipo_documento': tipo_documento_repo,
            'tipo_puesto': tipo_puesto_repo,
            'persona': persona_repo,
        }
    )

    vehiculo_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'modelo': modelo_repo,
            'color': color_repo,
            'estado': estado_repo
        }
    )

    contrato_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'cliente': cliente_repo,
            'vehiculo': vehiculo_repo,
            'metodo_pago': metodo_pago_repo,
            'empleado': empleado_repo,
            'estado': estado_repo
        }
    )

    modelo_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'marca': marca_repo,
        }
    )

    cliente_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'tipo_documento': tipo_documento_repo,
            'persona': persona_repo,
        }
    )

    inconveniente_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'vehiculo': vehiculo_repo,
            'tipo_inconveniente': tipo_inconveniente_repo,
        }
    )

    mantenimiento_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'vehiculo': vehiculo_repo,
        }
    )

    fotoxmodelo_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            "modeloxcolor": modeloxcolor_repo,
            "modelo": modelo_repo,
            "color": color_repo,
        }
    )

    modeloxcolor_validation_mapper = providers.Factory(
        ValidationMapper,
        repositories={
            'modelo': modelo_repo,
            'color': color_repo,
        }
    )

    # --- Servicios ---
    # Los servicios reciben los repositorios (que ya tienen la sesión inyectada).

    modeloxcolor_service = providers.Factory(
        ModeloXColorService,
        mxc_repo=modeloxcolor_repo,
        mapper=modeloxcolor_validation_mapper
    )

    persona_service = providers.Factory(
        PersonaService,
        persona_repo=persona_repo,
        # Se mantiene el mapper original aunque PersonaService tiene pocas validaciones FK
        mapper=inconveniente_validation_mapper
    )

    marca_service = providers.Factory(
        MarcaService,
        marca_repo=marca_repo
    )

    color_service = providers.Factory(
        ColorService,
        color_repo=color_repo
    )

    tipo_documento_service = providers.Factory(
        TipoDocumentoService,
        tipo_documento_repo=tipo_documento_repo
    )

    tipo_puesto_service = providers.Factory(
        TipoPuestoService,
        tipo_puesto_repo=tipo_puesto_repo
    )

    tipo_inconveniente_service = providers.Factory(
        TipoInconvenienteService,
        tipo_inconveniente_repo=tipo_inconveniente_repo
    )

    metodo_pago_service = providers.Factory(
        MetodoDePagoService,
        metodo_pago_repo=metodo_pago_repo
    )

    inconveniente_service = providers.Factory(
        InconvenienteService,
        inconveniente_repo=inconveniente_repo,
        mapper=inconveniente_validation_mapper
    )

    empleado_service = providers.Factory(
        EmpleadoService,
        empleado_repo=empleado_repo,
        mapper=empleado_validation_mapper
    )

    cliente_service = providers.Factory(
        ClienteService,
        cliente_repo=cliente_repo,
        mapper=cliente_validation_mapper
    )

    modelo_service = providers.Factory(
        ModeloService,
        modelo_repo=modelo_repo,
        mapper=modelo_validation_mapper
    )

    estado_service = providers.Factory(
        EstadoService,
        estado_repo=estado_repo
    )

    contrato_service = providers.Factory(
        ContratoService,
        contrato_repo=contrato_repo,
        estado_service=estado_service,
        validation_mapper=contrato_validation_mapper
    )

    fotoxmodelo_service = providers.Factory(
        FotoXModeloService,
        foto_repo=fotoxmodelo_repo,
        modeloxcolor_repo=modeloxcolor_repo,
        mapper=fotoxmodelo_validation_mapper
    )

    detalle_contrato_service = providers.Factory(
        DetalleContratoService,
        detalle_repo=detalle_contrato_repo,
        contrato_repo=contrato_repo,
        vehiculo_repo=vehiculo_repo,
        mapper=detalle_contrato_validation_mapper
    )

    mantenimiento_service = providers.Factory(
        MantenimientoService,
        mantenimiento_repo=mantenimiento_repo,
        mapper=mantenimiento_validation_mapper,
        estado_service=estado_service
    )

    vehiculo_service = providers.Factory(
        VehiculoService,
        vehiculo_repo=vehiculo_repo,
        contrato_service=contrato_service,
        mapper=vehiculo_validation_mapper,
        detalle_contrato_service=detalle_contrato_service,
        estado_service=estado_service,
        mantenimiento_service=mantenimiento_service
    )