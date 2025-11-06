from data_access.repositories.tipo_documento_repository import TipoDocumentoRepository
from domain.models.tipoDocumento import TipoDocumento
from services.tipodocumento_service import TipoDocumentoService


def main():
    tipoDocumento_service = TipoDocumentoService(tipo_documento_repo=TipoDocumentoRepository())
    tipoDocumento = TipoDocumento(
        nombre="DNI")
    tipoDocumento_service.create_tipo_documento(tipoDocumento)

if __name__ == '__main__':
    main()