from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.tipoDocumento import TipoDocumento
from data_access.repositories.tipo_documento_repository import TipoDocumentoRepository

class TipoDocumentoService:
    def __init__(self, tipo_documento_repo: TipoDocumentoRepository):
        self._repo = tipo_documento_repo

    def create_tipo_documento(self, tipo_documento: TipoDocumento) -> Optional[int]:
        try:
            nuevo = self._repo.create(tipo_documento)
            return nuevo.id
        except IntegrityError:
            self._repo.session.rollback()
            return None

    def get_tipo_documento_by_id(self, tipo_documento_id: int) -> Optional[TipoDocumento]:
        return self._repo.get_by_id(tipo_documento_id)

    def list_all_tipos_documento(self) -> List[TipoDocumento]:
        return self._repo.list_all()

    def update_tipo_documento(self, tipo_documento: TipoDocumento) -> bool:
        if not tipo_documento.id: return False
        try:
            self._repo.update(tipo_documento)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_tipo_documento(self, tipo_documento_id: int) -> bool:
        try:
            return self._repo.delete(tipo_documento_id)
        except IntegrityError:
            self._repo.session.rollback()
            return False