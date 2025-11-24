from typing import Optional, List
from sqlalchemy.orm import Session
from domain.models.fotoXModelo import FotoXModelo
from data_access.repositories.base_repository import SQLAlchemyRepository


class FotoXModeloRepository(SQLAlchemyRepository[FotoXModelo]):
    def __init__(self, session: Session):
        super().__init__(session, FotoXModelo)

    def get_by_path(self, path: str) -> Optional[FotoXModelo]:
        return self.session.query(FotoXModelo).filter(FotoXModelo.foto_path == path).first()

    def list_by_modelo(self, id_modelo: int) -> List[FotoXModelo]:
        return self.session.query(FotoXModelo).filter(FotoXModelo.id_modelo == id_modelo).all()