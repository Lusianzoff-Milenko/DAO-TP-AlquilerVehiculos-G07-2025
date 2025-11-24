from typing import Optional, List
from sqlalchemy.exc import IntegrityError

from data_access.repositories import ContratoRepository
from domain.models.contrato import Contrato
from domain.models.detalle_contrato import DetalleContrato
from services.detalle_contrato_service import DetalleContratoService
from services.estado_service import EstadoService


class ContratoService:
    def __init__(
            self,
            contrato_repo: ContratoRepository,
            estado_service: EstadoService
    ):
        self._repo = contrato_repo
        self._estado_service = estado_service
        self._estados_contrato = self._estado_service.get_estado_by_ambito('Contrato')

    def create_contrato(self, contrato: Contrato) -> Optional[int]:
        try:
            nuevo = self._repo.create(contrato)
            return nuevo.id
        except IntegrityError as e:
            print(f"Error creando contrato: {e}")
            self._repo.session.rollback()
            return None

    def crear_contrato_con_detalles(
            self,
            contrato: Contrato,
            detalles: List[DetalleContrato],
            detalles_service: DetalleContratoService
    ) -> Optional[int]:
        """
        Crea Contrato y Detalles en una sola transacción atómica.
        """
        session = self._repo.session
        try:
            # 1. Agregar contrato a la sesión (aún no commit)
            session.add(contrato)
            session.flush()  # Esto genera el ID del contrato sin cerrar la transacción

            contrato_id = contrato.id
            print(f"Contrato pre-generado con ID: {contrato_id}")

            # 2. Asociar y agregar detalles
            for detalle in detalles:
                detalle.id_contrato = contrato_id
                session.add(detalle)  # Agregamos a la misma sesión

            # 3. Commit de TODO junto
            session.commit()
            return contrato_id

        except IntegrityError as e:
            print(f"Error de integridad en transacción compleja: {e}")
            session.rollback()  # Deshace contrato Y detalles
            return None
        except Exception as e:
            print(f"Error desconocido: {e}")
            session.rollback()
            return None

    def get_contrato_by_id(self, contrato_id: int) -> Optional[Contrato]:
        contrato = self._repo.get_by_id(contrato_id)
        if contrato:
            contrato.estados_disponibles = self._estados_contrato
        return contrato

    # ... (update y otros métodos similares usando try/except IntegrityError) ...

    def confirmar_pago_reserva(self, contrato: Contrato, monto: float, vehiculo_service, detalle_service) -> bool:
        # Asegurarse de tener el objeto persistente conectado a la sesión
        contrato = self._repo.update(contrato)  # Re-attach si es necesario

        contrato.estados_disponibles = self._estados_contrato

        if contrato.get_state().__class__.__name__ != 'EnReservado':
            return False

        exito = contrato.get_state().tomar_pago(monto)
        if not exito: return False

        # Actualizar vehículos
        # Nota: Al usar ORM, si navegas por contrato.detalles_contrato (relationship),
        # puedes acceder a los vehículos directamente sin el detalle_service si las relaciones están bien definidas.
        # Si no, usa el servicio como antes.

        try:
            # Guardar cambios del contrato (nuevo estado)
            self._repo.update(contrato)
            return True
        except Exception as e:
            print(f"Error confirmando pago: {e}")
            self._repo.session.rollback()
            return False