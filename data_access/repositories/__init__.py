from .base_repository import BaseRepository
from .cliente_repository import ClienteRepository
from .contrato_repository import ContratoRepository
from .detalle_contrato_repository import DetalleContratoRepository
from .estado_repository import EstadoRepository
from .empleado_repository import EmpleadoRepository
from .mantenimiento_repository import MantenimientoRepository
from .metododepago_repository import MetodoDePagoRepository
from .modelo_repository import ModeloRepository
from .vehiculo_repository import VehiculoRepository
from .color_repository import ColorRepository
from .inconveniente_repository import InconvenienteRepository
from .vehiculo_repository import VehiculoRepository
from .marca_repository import MarcaRepository
from .tipo_documento_repository import TipoDocumentoRepository
from .tipo_puesto_repository import TipoPuestoRepository
from .tipo_inconveniente_repository import TipoInconvenienteRepository
from .persona_repository import PersonaRepository
from .foto_x_modelo_repository import FotoXModeloRepository
from .modelo_x_color_repository import ModeloXColorRepository
__all__ = [
    "BaseRepository",
    "ClienteRepository",
    "ContratoRepository",
    "DetalleContratoRepository",
    "EstadoRepository",
    "EmpleadoRepository",
    "MantenimientoRepository",
    "MetodoDePagoRepository",
    "ModeloRepository",
    "VehiculoRepository",
    "ColorRepository",
    "InconvenienteRepository",
    "MarcaRepository",
    "TipoDocumentoRepository",
    "TipoPuestoRepository",
    "TipoInconvenienteRepository",
    "PersonaRepository",
    "FotoXModeloRepository",
    "ModeloXColorRepository",
]