from sqlalchemy.orm import Session
from data_access.repositories.base_repository import SQLAlchemyRepository
from data_access.vistas.views import (
    VistaClientesContacto, VistaContratosRentabilidad,
    VistaDisponibilidadFlota, VistaReporteFacturacion,
    VistaUtilizacionFlota, VistaVehiculosDetallados
)

class VistaClientesRepository(SQLAlchemyRepository[VistaClientesContacto]):
    def __init__(self, session: Session): super().__init__(session, VistaClientesContacto)

class VistaRentabilidadRepository(SQLAlchemyRepository[VistaContratosRentabilidad]):
    def __init__(self, session: Session): super().__init__(session, VistaContratosRentabilidad)

class VistaDisponibilidadRepository(SQLAlchemyRepository[VistaDisponibilidadFlota]):
    def __init__(self, session: Session): super().__init__(session, VistaDisponibilidadFlota)

class VistaFacturacionRepository(SQLAlchemyRepository[VistaReporteFacturacion]):
    def __init__(self, session: Session): super().__init__(session, VistaReporteFacturacion)

class VistaUtilizacionRepository(SQLAlchemyRepository[VistaUtilizacionFlota]):
    def __init__(self, session: Session): super().__init__(session, VistaUtilizacionFlota)

class VistaVehiculosRepository(SQLAlchemyRepository[VistaVehiculosDetallados]):
    def __init__(self, session: Session): super().__init__(session, VistaVehiculosDetallados)

class VistaEmpleadosRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        from data_access.vistas.views import VistaEmpleados
        super().__init__(session, VistaEmpleados)

class VistaHistorialMantenimientoRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        from data_access.vistas.views import VistaHistorialMantenimiento
        super().__init__(session, VistaHistorialMantenimiento)

class VistaDemandaPorModeloRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        from data_access.vistas.views import VistaDemandaPorModelo
        super().__init__(session, VistaDemandaPorModelo)

class VistaCantidadFlotaRepository(SQLAlchemyRepository):
    def __init__(self, session: Session):
        from data_access.vistas.views import VistaCantidadFlotaPorModelo
        super().__init__(session, VistaCantidadFlotaPorModelo)