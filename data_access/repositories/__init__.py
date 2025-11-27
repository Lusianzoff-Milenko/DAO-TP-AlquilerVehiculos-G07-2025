from .base_repository import SQLAlchemyRepository
from .cliente_repository import ClienteRepository
from .contrato_repository import ContratoRepository
from .detalle_contrato_repository import DetalleContratoRepository
from .empleado_repository import EmpleadoRepository
from .estado_repository import EstadoRepository
from .mantenimiento_repository import MantenimientoRepository
from .vehiculo_repository import VehiculoRepository
from .modelo_repository import ModeloRepository
from .marca_repository import MarcaRepository
from .color_repository import ColorRepository
from .metododepago_repository import MetodoDePagoRepository
from .tipo_documento_repository import TipoDocumentoRepository
from .tipo_puesto_repository import TipoPuestoRepository
from .tipo_inconveniente_repository import TipoInconvenienteRepository
from .inconveniente_repository import InconvenienteRepository
from .persona_repository import PersonaRepository
from .foto_x_modelo_repository import FotoXModeloRepository
from .modelo_x_color_repository import ModeloXColorRepository
from .view_repositories import (
    VistaClientesRepository,
    VistaRentabilidadRepository,
    VistaDisponibilidadRepository,
    VistaFacturacionRepository,
    VistaUtilizacionRepository,
    VistaVehiculosRepository,
    VistaEmpleadosRepository,
    VistaHistorialMantenimientoRepository,
    VistaDemandaPorModeloRepository)

__all__ = [
    "SQLAlchemyRepository",
    "ClienteRepository",
    "ContratoRepository",
    "DetalleContratoRepository",
    "EmpleadoRepository",
    "EstadoRepository",
    "MantenimientoRepository",
    "VehiculoRepository",
    "ModeloRepository",
    "MarcaRepository",
    "ColorRepository",
    "MetodoDePagoRepository",
    "TipoDocumentoRepository",
    "TipoPuestoRepository",
    "TipoInconvenienteRepository",
    "InconvenienteRepository",
    "PersonaRepository",
    "FotoXModeloRepository",
    "ModeloXColorRepository",
    "VistaClientesRepository",
    "VistaRentabilidadRepository",
    "VistaDisponibilidadRepository",
    "VistaFacturacionRepository",
    "VistaUtilizacionRepository",
    "VistaVehiculosRepository",
    "VistaEmpleadosRepository",
    "VistaHistorialMantenimientoRepository",
    "VistaDemandaPorModeloRepository"
]