from typing import Optional, List
from domain.models.tipoDocumento import TipoDocumento
from data_access.repositories.tipo_documento_repository import TipoDocumentoRepository

class TipoDocumentoService:
    def __init__(self, tipo_documento_repo: TipoDocumentoRepository):
        self._repo = tipo_documento_repo

    def create_tipo_documento(self, tipo_documento: TipoDocumento) -> Optional[int]:
        """Crea un nuevo tipo de documento si no existe."""
        return self._repo.create(tipo_documento)

    def get_tipo_documento_by_id(self, tipo_documento_id: int) -> Optional[TipoDocumento]:
        return self._repo.get_by_id(tipo_documento_id)

    def list_all_tipos_documento(self) -> List[TipoDocumento]:
        return self._repo.list_all()

    def update_tipo_documento(self, tipo_documento: TipoDocumento) -> bool:
        """Actualiza un tipo de documento existente."""
        if not tipo_documento.id:
            print("ID de tipo de documento requerido para actualizar.")
            return False
        return self._repo.update(tipo_documento)

    def delete_tipo_documento(self, tipo_documento_id: int) -> bool:
        """Elimina un tipo de documento. Se recomienda chequear antes si está en uso por Clientes."""
        return self._repo.delete(tipo_documento_id)