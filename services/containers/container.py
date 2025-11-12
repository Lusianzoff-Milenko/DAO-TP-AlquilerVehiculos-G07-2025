from dependency_injector import containers, providers

# Importa tus clases de repositorios, servicios, etc.
from data_access.repositories import (VehiculoRepository, ModeloRepository, ColorRepository,
                                      EstadoRepository, ContratoRepository, ClienteRepository,
                                      MetodoDePagoRepository, EmpleadoRepository, DetalleContratoRepository,
                                      MarcaRepository, TipoDocumentoRepository, TipoPuestoRepository,
                                      TipoInconvenienteRepository, InconvenienteRepository, MantenimientoRepository,
                                      PersonaRepository, FotoXModeloRepository, ModeloXColorRepository)
from services import (VehiculoService, ContratoService, EstadoService,
                      DetalleContratoService, MarcaService, ModeloService,
                      ClienteService, TipoPuestoService, EmpleadoService,
                      TipoInconvenienteService, InconvenienteService, MantenimientoService,
                      ColorService, MetodoDePagoService, TipoDocumentoService,
                      PersonaService, FotoXModeloService, ModeloXColorService)
from services.validation_mapper import ValidationMapper


class Container(containers.DeclarativeContainer):
    # Configuración (si tuvieras, ej: conexión a BD)
    config = providers.Configuration()

    # --- Definir Repositorios (como Singletons) ---
    # Singleton significa que solo se crea UNA instancia y se reutiliza
    modelo_repo = providers.Singleton(ModeloRepository)
    color_repo = providers.Singleton(ColorRepository)
    estado_repo = providers.Singleton(EstadoRepository)
    vehiculo_repo = providers.Singleton(VehiculoRepository)
    contrato_repo = providers.Singleton(ContratoRepository)
    cliente_repo = providers.Singleton(ClienteRepository)
    metodo_pago_repo = providers.Singleton(MetodoDePagoRepository)
    empleado_repo = providers.Singleton(EmpleadoRepository)
    detalle_contrato_repo = providers.Singleton(DetalleContratoRepository)
    marca_repo = providers.Singleton(MarcaRepository)
    tipo_documento_repo = providers.Singleton(TipoDocumentoRepository)
    tipo_puesto_repo = providers.Singleton(TipoPuestoRepository)
    tipo_inconveniente_repo = providers.Singleton(TipoInconvenienteRepository)
    inconveniente_repo = providers.Singleton(InconvenienteRepository)
    mantenimiento_repo = providers.Singleton(MantenimientoRepository)
    persona_repo = providers.Singleton(PersonaRepository)
    fotoxmodelo_repo = providers.Singleton(FotoXModeloRepository)
    modeloxcolor_repo = providers.Singleton(ModeloXColorRepository)

    # El contenedor puede inyectar dependencias en otros servicios

    # --- Tu Validación ---
    # Este es un buen candidato para un Factory,
    # ya que es una dependencia de tu servicio.

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
        # ¡CORRECCIÓN! Usamos el nombre 'repositories' que acepta el constructor
        repositories={
            'modelo': modelo_repo,
            'color': color_repo,
            'estado': estado_repo
        }
    )

    # 2. Mapper específico para ContratoService
    contrato_validation_mapper = providers.Factory(
        ValidationMapper,
        # ¡CORRECCIÓN! Usamos el nombre 'repositories'
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

    modeloxcolor_service = providers.Factory(
        ModeloXColorService,
        mxc_repo=modeloxcolor_repo,
        mapper=modeloxcolor_validation_mapper
    )

    persona_service = providers.Factory(
        PersonaService,
        persona_repo=persona_repo,
        mapper = inconveniente_validation_mapper
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
        metodo_pago_repo=metodo_pago_repo)

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
        estado_repo=estado_repo  # <-- ¡Añadido!
    )

    contrato_service = providers.Factory(
        ContratoService,
        contrato_repo=contrato_repo,
        estado_service=estado_service,
        validation_mapper=contrato_validation_mapper  # <-- Le pasamos el nuevo mapper
    )

    fotoxmodelo_service = providers.Factory(
        FotoXModeloService,
        foto_repo=fotoxmodelo_repo,
        modeloxcolor_repo=modeloxcolor_repo,
        mapper=fotoxmodelo_validation_mapper
    )


    vehiculo_service = providers.Factory(
        VehiculoService,
        vehiculo_repo=vehiculo_repo,
        contrato_service=contrato_service,
        mapper=vehiculo_validation_mapper  # <-- Este usa el mapper de vehículo
    )

    mantenimiento_service = providers.Factory(
        MantenimientoService,
        mantenimiento_repo=mantenimiento_repo,
        vehiculo_service=vehiculo_service,  # Inyección del servicio de vehículo
        mapper=mantenimiento_validation_mapper
    )

    detalle_contrato_service = providers.Factory(
        DetalleContratoService,
        detalle_repo=detalle_contrato_repo,
        contrato_repo=contrato_repo,
        vehiculo_repo=vehiculo_repo,  # <-- NECESARIO
        mapper=detalle_contrato_validation_mapper  # <-- NECESARIO (Asegúrate de que esté definido)
    )