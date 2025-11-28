from dependency_injector import containers, providers

# 1. Configuración de DB (SQLAlchemy)
from config.database_sqlalchemy import SessionLocal

# 2. Repositorios de Entidades
from data_access.repositories import (
    VehiculoRepository, ModeloRepository, ColorRepository,
    EstadoRepository, ContratoRepository, ClienteRepository,
    MetodoDePagoRepository, EmpleadoRepository, DetalleContratoRepository,
    MarcaRepository, TipoDocumentoRepository, TipoPuestoRepository,
    TipoInconvenienteRepository, InconvenienteRepository, MantenimientoRepository,
    PersonaRepository, FotoXModeloRepository, ModeloXColorRepository, VistaEmpleadosRepository, VistaHistorialMantenimientoRepository, VistaDemandaPorModeloRepository
)

# 3. Repositorios de Vistas (Reportes)
from data_access.repositories.view_repositories import (
    VistaClientesRepository, VistaRentabilidadRepository,
    VistaDisponibilidadRepository, VistaFacturacionRepository,
    VistaUtilizacionRepository, VistaVehiculosRepository
)

# 4. Servicios
from services import (
    VehiculoService, ContratoService, EstadoService,
    DetalleContratoService, MarcaService, ModeloService,
    ClienteService, TipoPuestoService, EmpleadoService,
    TipoInconvenienteService, InconvenienteService, MantenimientoService,
    ColorService, MetodoDePagoService, TipoDocumentoService,
    PersonaService, FotoXModeloService, ModeloXColorService
)
from services.reporte_service import ReporteService

from controlladores.controller_vehiculo import VehiculoController
from controlladores.controller_cliente import ClienteController
from controlladores.controlle_empleado import EmpleadoController
from controlladores.controller_contrato import ContratoController
from controlladores.controller_mantenimiento import MantenimientoController
from controlladores.controller_reportes import ReporteController

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # --- Recurso de Sesión (Thread-Safe) ---
    db_session = providers.Resource(SessionLocal)

    # --- Repositorios (Factories con inyección de sesión) ---

    # Entidades
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

    # Vistas
    vista_clientes_repo = providers.Factory(VistaClientesRepository, session=db_session)
    vista_rentabilidad_repo = providers.Factory(VistaRentabilidadRepository, session=db_session)
    vista_disponibilidad_repo = providers.Factory(VistaDisponibilidadRepository, session=db_session)
    vista_facturacion_repo = providers.Factory(VistaFacturacionRepository, session=db_session)
    vista_utilizacion_repo = providers.Factory(VistaUtilizacionRepository, session=db_session)
    vista_vehiculos_repo = providers.Factory(VistaVehiculosRepository, session=db_session)
    vista_empleados_repo = providers.Factory(VistaEmpleadosRepository, session=db_session)
    vista_historial_mantenimiento_repo = providers.Factory(VistaHistorialMantenimientoRepository, session=db_session)
    vista_demanda_por_modelo_repo = providers.Factory(VistaDemandaPorModeloRepository, session=db_session)

    # --- Servicios (Factories con inyección de repositorios y otros servicios) ---

    # Servicios Básicos / Catálogos
    estado_service = providers.Factory(EstadoService, estado_repo=estado_repo)
    marca_service = providers.Factory(MarcaService, marca_repo=marca_repo)
    color_service = providers.Factory(ColorService, color_repo=color_repo)
    modelo_service = providers.Factory(ModeloService, modelo_repo=modelo_repo)
    tipo_documento_service = providers.Factory(TipoDocumentoService, tipo_documento_repo=tipo_documento_repo)
    tipo_puesto_service = providers.Factory(TipoPuestoService, tipo_puesto_repo=tipo_puesto_repo)
    tipo_inconveniente_service = providers.Factory(TipoInconvenienteService, tipo_inconveniente_repo=tipo_inconveniente_repo)
    metodo_pago_service = providers.Factory(MetodoDePagoService, metodo_pago_repo=metodo_pago_repo)

    # Servicios Intermedios
    persona_service = providers.Factory(PersonaService, persona_repo=persona_repo)
    modeloxcolor_service = providers.Factory(ModeloXColorService, mxc_repo=modeloxcolor_repo)
    fotoxmodelo_service = providers.Factory(FotoXModeloService, foto_repo=fotoxmodelo_repo)

    # Servicios Core (Con dependencias cruzadas)
    empleado_service = providers.Factory(EmpleadoService, empleado_repo=empleado_repo)
    cliente_service = providers.Factory(ClienteService, cliente_repo=cliente_repo)

    inconveniente_service = providers.Factory(InconvenienteService, inconveniente_repo=inconveniente_repo)

    mantenimiento_service = providers.Factory(
        MantenimientoService,
        mantenimiento_repo=mantenimiento_repo,
        estado_service=estado_service
    )

    detalle_contrato_service = providers.Factory(
        DetalleContratoService,
        detalle_repo=detalle_contrato_repo
    )

    contrato_service = providers.Factory(
        ContratoService,
        contrato_repo=contrato_repo,
        estado_service=estado_service
    )


    vehiculo_service = providers.Factory(
        VehiculoService,
        vehiculo_repo=vehiculo_repo,
        estado_service=estado_service,
        mantenimiento_service=mantenimiento_service
    )

    # Servicio de Reportes (Agregador)
    reporte_service = providers.Factory(
        ReporteService,
        vista_clientes_repo=vista_clientes_repo,
        vista_rentabilidad_repo=vista_rentabilidad_repo,
        vista_disponibilidad_repo=vista_disponibilidad_repo,
        vista_facturacion_repo=vista_facturacion_repo,
        vista_utilizacion_repo=vista_utilizacion_repo,
        vista_vehiculos_repo=vista_vehiculos_repo,
        vista_empleados_repo=vista_empleados_repo,
        vista_historial_mantenimiento_repo=vista_historial_mantenimiento_repo,
        vista_demanda_por_modelo_repo=vista_demanda_por_modelo_repo,

        contrato_repo = contrato_repo,    #nuevo
        detalle_contrato_repo = detalle_contrato_repo   #nuevo
    )

    vehiculo_controller = providers.Factory(
        VehiculoController,
        vehiculo_service=vehiculo_service,
        modelo_service=modelo_service,
        color_service=color_service,
        estado_service=estado_service,
        marca_service=marca_service
    )

    cliente_controller = providers.Factory(
        ClienteController,
        cliente_service=cliente_service,
        persona_service=persona_service,
        tipo_doc_service=tipo_documento_service
    )

    empleado_controller = providers.Factory(
        EmpleadoController,
        empleado_service=empleado_service,
        persona_service=persona_service,
        tipo_puesto_service=tipo_puesto_service
    )

    contrato_controller = providers.Factory(
        ContratoController,
        contrato_service=contrato_service,
        vehiculo_service=vehiculo_service,
        cliente_service=cliente_service,
        empleado_service=empleado_service,
        pago_service=metodo_pago_service
    )

    mantenimiento_controller = providers.Factory(
        MantenimientoController,
        mantenimiento_service=mantenimiento_service,
        vehiculo_service=vehiculo_service,
        empleado_service=empleado_service
    )

    reporte_controller = providers.Factory(
        ReporteController,
        reporte_service=reporte_service
    )