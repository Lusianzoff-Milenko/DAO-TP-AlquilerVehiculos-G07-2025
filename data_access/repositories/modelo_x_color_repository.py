from typing import Optional
from sqlalchemy.orm import Session
from domain.models.modeloXColor import ModeloXColor
from data_access.repositories.base_repository import SQLAlchemyRepository


class ModeloXColorRepository(SQLAlchemyRepository[ModeloXColor]):
    def __init__(self, session: Session):
        super().__init__(session, ModeloXColor)

    # Método específico para obtener por clave compuesta
    def get_by_ids(self, id_modelo: int, id_color: int) -> Optional[ModeloXColor]:
        return self.session.query(ModeloXColor).filter_by(
            id_modelo=id_modelo,
            id_color=id_color
        ).first()

    # Override de delete porque el genérico usa .id y aquí no existe
    def delete_composite(self, id_modelo: int, id_color: int) -> bool:
        obj = self.get_by_ids(id_modelo, id_color)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False