from typing import Optional, List
from domain.models.vehiculo import Vehiculo
from data_access.repositories.vehiculo_repository import VehiculoRepository
from services import EstadoService
from services.contrato_service import ContratoService
from services.validation_mapper import ValidationMapper


class VehiculoService:
    def __init__(self,
                 vehiculo_repo: VehiculoRepository,
                 contrato_service: ContratoService,
                 mapper: ValidationMapper):

        self._repo = vehiculo_repo
        self._contrato_service = contrato_service
        self._mapper = mapper  # Asignación del mapper inyectado

    def create_vehiculo(self, vehiculo: Vehiculo, estado_service: EstadoService) -> Optional[int]:  # Adaptar a tu inyección de dependencias

        # 2. Obtener el ID del estado inicial ("Disponible")
        # Nota: Aquí usamos la clase de estado 'Disponible' y la clase del vehículo 'Vehiculo'
        estado_inicial_obj = estado_service.get_estado_by_name_and_ambito(
            name=vehiculo._state.__class__.__name__,
            ambito=Vehiculo.__name__
        )

        if estado_inicial_obj is None:
            # Esto indica que el estado inicial no existe en la DB, ¡revisa la carga inicial!
            print("Error: El estado inicial 'Disponible' no se encontró en la DB.")
            return None

        # 3. CRUCIAL: Asignar el id_estado al objeto Vehiculo.
        vehiculo.id_estado = estado_inicial_obj.id  # <--- 🎯 LA SOLUCIÓN

        # 4. Asignar el objeto State (patrón de diseño) si es necesario
        vehiculo.transition_to(vehiculo._state)  # Para que el objeto esté en el estado correcto

        # 5. Intentar persistir y validar

        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return None
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return None
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return None

        return self._repo.create(vehiculo)

    def get_vehiculo_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        return self._repo.get_by_id(vehiculo_id)

    def list_all_vehiculos(self) -> List[Vehiculo]:
        return self._repo.list_all()

    def update_vehiculo(self, vehiculo: Vehiculo) -> bool:
        if not vehiculo.id:
            print("ID de vehículo requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('modelo', vehiculo.id_modelo, 'id_modelo'): return False
        if not self._mapper.validate_fk_exists('color', vehiculo.id_color, 'id_color'): return False
        if not self._mapper.validate_fk_exists('estado', vehiculo.id_estado, 'id_estado'): return False

        return self._repo.update(vehiculo)

    def delete_vehiculo(self, vehiculo_id: int) -> bool | None:
        # Lógica de Negocio: Evitar eliminar si está en uso por Contratos/Mantenimientos/Inconvenientes
        active_contracts = self._contrato_service.get_active_contracts_by_entity('vehiculo', vehiculo_id)
        if active_contracts:
            print(f"No se puede eliminar el vehículo {vehiculo_id} porque tiene contratos activos.")
            return None

        return self._repo.delete(vehiculo_id)

    def get_all_vehiculos(self) -> List[Vehiculo]:
        return self._repo.list_all()