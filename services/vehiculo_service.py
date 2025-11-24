from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from domain.models.vehiculo import Vehiculo
from domain.models.contrato import Contrato
from data_access.repositories.vehiculo_repository import VehiculoRepository
from services import DetalleContratoService, EstadoService, MantenimientoService
from services.contrato_service import ContratoService


class VehiculoService:
    def __init__(self,
                 vehiculo_repo: VehiculoRepository,
                 contrato_service: ContratoService,
                 detalle_contrato_service: DetalleContratoService,
                 estado_service: EstadoService,
                 mantenimiento_service: MantenimientoService,
                 mapper=None):  # Mapper opcional ahora

        self._repo = vehiculo_repo
        self._contrato_service = contrato_service
        self._detalle_contrato_service = detalle_contrato_service
        self._estado_service = estado_service
        self._mantenimiento_service = mantenimiento_service

        # Carga perezosa o cacheada de estados si es necesario
        self._estados_vehiculo = self._estado_service.get_estado_by_ambito("Vehiculo")

    def create_vehiculo(self, vehiculo: Vehiculo) -> Optional[int]:
        try:
            # El repositorio base se encarga de la sesión y el commit
            nuevo_vehiculo = self._repo.create(vehiculo)
            return nuevo_vehiculo.id
        except IntegrityError as e:
            print(f"Error creando vehículo: {e}")
            self._repo.session.rollback()
            return None

    def update_vehiculo(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.id: return False
        try:
            self._repo.update(vehiculo)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def get_vehiculo_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        vehiculo = self._repo.get_by_id(vehiculo_id)
        # Inyectamos estados disponibles al recuperar el objeto para que funcione el State Pattern
        if vehiculo:
            vehiculo.estados_disponibles = self._estados_vehiculo
        return vehiculo

    # ... (resto de métodos de lectura simples list_all, get_all) ...

    def verificar_vencimiento_reserva(self, vehiculo_id: int) -> bool:
        vehiculo = self.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo or vehiculo.get_state().__class__.__name__ != 'Reservado':
            return False

        # Lógica de negocio... (idéntica a tu código anterior)
        # La diferencia es que al llamar a self._repo.update(vehiculo),
        # SQLAlchemy detecta el cambio de vehiculo.id_estado automáticamente.

        # ... (tu lógica de fechas) ...

        # Si cambia de estado:
        # vehiculo.get_state().reincorporar(...)
        # self._repo.update(vehiculo)
        return True

    def enviar_a_mantenimiento_desde_revision(self, vehiculo_id: int, costo: float, descripcion: str,
                                              id_empleado: int) -> Optional[int]:
        vehiculo = self.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo: return None

        # Transición de estado en memoria
        try:
            vehiculo.get_state().iniciar_mantenimiento()
        except Exception as e:
            print(f"Error transición: {e}")
            return None

        # Crear registro de mantenimiento
        # Nota: Podríamos hacer esto en una transacción atómica
        mant_id = self._mantenimiento_service.iniciar_nuevo_mantenimiento(
            id_vehiculo=vehiculo_id,
            costo=costo,
            descripcion=descripcion,
            id_empleado=id_empleado
        )

        if mant_id:
            # Persistir cambio de estado del vehículo
            # Necesitamos actualizar el ID del estado manualmente en el objeto si el State Pattern no lo hizo
            # (Tu implementación de State.transition_to SÍ actualiza self.id_estado, así que está bien)
            self._repo.update(vehiculo)
            return mant_id
        return None