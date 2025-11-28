from typing import Any

from sqlalchemy.orm import Session, joinedload

from domain.models.cliente import Cliente
from domain.models.contrato import Contrato
from data_access.repositories.base_repository import SQLAlchemyRepository
from domain.models.detalle_contrato import DetalleContrato
from domain.models.vehiculo import Vehiculo


class ContratoRepository(SQLAlchemyRepository[Contrato]):
    def __init__(self, session: Session):
        super().__init__(session, Contrato)

    def list_all(self) -> list[type[Contrato]]:
        """
        Sobreescribe el listado para incluir relaciones clave (Eager Loading).
        Esto es vital para los reportes que filtran por Estado o muestran Cliente/Vehículos
        sin causar errores de carga diferida o datos vacíos.
        """
        return self.session.query(Contrato).options(
            # Cargar Estado para poder filtrar por "YaEntregado"
            joinedload(Contrato.Estado),
            # Cargar Cliente y su Persona para mostrar el nombre
            joinedload(Contrato.Cliente).joinedload(Cliente.persona),
            # Cargar Detalles y sus Vehículos/Modelos para el desglose
            joinedload(Contrato.detalles_contrato).joinedload(DetalleContrato.Vehiculo).joinedload(Vehiculo.Modelo)
        ).all()