from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from domain.models.base import Base

T = TypeVar("T", bound=Base)

class SQLAlchemyRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def list_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def create(self, entity: T) -> T:
        """Agrega y commitea. Lanza excepción si falla."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        """Actualiza usando merge para asegurar que esté en la sesión."""
        entity = self.session.merge(entity)
        self.session.commit()
        return entity

    def delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False