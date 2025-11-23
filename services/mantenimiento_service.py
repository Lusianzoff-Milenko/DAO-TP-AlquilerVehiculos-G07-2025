from typing import Optional, List
from domain.models.mantenimiento import Mantenimiento
from services import EstadoService
from services.validation_mapper import ValidationMapper


class MantenimientoService:
    def __init__(self, mantenimiento_repo, vehiculo_service, mapper: ValidationMapper, estado_service: EstadoService):
        self._repo = mantenimiento_repo
        self._vehiculo_service = vehiculo_service # Inyección de servicio
        self._mapper = mapper
        self._estado_service = estado_service  # Será inyectado externamente

    def create_mantenimiento(self, mantenimiento: Mantenimiento) -> Optional[int]:
        if not self._mapper.validate_fk_exists('vehiculo', mantenimiento.id_vehiculo, 'id_vehiculo'): return None
        if not self._mapper.validate_fk_exists('estado', mantenimiento.id_estado, 'id_estado'): return None
        if not self._mapper.validate_fk_exists('empleado', mantenimiento.id_empleado, 'id_empleado'): return None

        return self._repo.create(mantenimiento)

    def get_mantenimiento_by_id(self, mantenimiento_id: int) -> Optional[Mantenimiento]:
        return self._repo.get_by_id(mantenimiento_id)

    def list_all_mantenimientos(self) -> List[Mantenimiento]:
        return self._repo.list_all()

    def update_mantenimiento(self, mantenimiento: Mantenimiento) -> bool:
        if not mantenimiento.id:
            print("ID de mantenimiento requerido para actualizar.")
            return False
        if not self._mapper.validate_fk_exists('vehiculo', mantenimiento.id_vehiculo, 'id_vehiculo'): return False
        if not self._mapper.validate_fk_exists('estado', mantenimiento.id_estado, 'id_estado'): return False
        if not self._mapper.validate_fk_exists('empleado', mantenimiento.id_empleado, 'id_empleado'): return False

        return self._repo.update(mantenimiento)

    def delete_mantenimiento(self, mantenimiento_id: int) -> bool:
        return self._repo.delete(mantenimiento_id)

    def iniciar_nuevo_mantenimiento(self, id_vehiculo: int, costo: float, descripcion: str, id_empleado: int) -> \
    Optional[int]:

        mantenimiento = Mantenimiento(
            id_vehiculo=id_vehiculo,
            costo=costo,
            descripcion=descripcion,
            id_empleado=id_empleado,
        )

        return self.create_mantenimiento(mantenimiento)

    # Tarea: Añadir a services/mantenimiento_service.py

    def get_last_finalized_mantenimiento_by_vehiculo_id(self, vehiculo_id: int) -> Optional[Mantenimiento]:
        """
        Busca el último registro de Mantenimiento para un vehículo dado que se encuentre
        en un estado final ('Reparado' o 'NoReparado').
        """
        # 1. Obtener los IDs de los estados finales de Mantenimiento

        # Estos IDs deben buscarse por nombre y ámbito 'Mantenimiento'
        estado_reparado = self._estado_service.get_estado_by_name_and_ambito('Reparado', 'Mantenimiento')
        estado_no_reparado = self._estado_service.get_estado_by_name_and_ambito('NoReparado', 'Mantenimiento')

        final_state_ids = []
        if estado_reparado:
            final_state_ids.append(estado_reparado.id)
        if estado_no_reparado:
            final_state_ids.append(estado_no_reparado.id)

        if not final_state_ids:
            print("Error: No se encontraron los IDs de los estados finales 'Reparado' o 'NoReparado'.")
            return None

        # 2. Obtener todos los mantenimientos del vehículo (Asumiendo un método en el Repositorio)
        # Nota: La forma más eficiente sería que el Repositorio haga esta consulta,
        # pero para el Service, asumimos un método de listado filtrado.

        # 🚨 Asumimos la existencia de un método en el Repositorio
        # mantenimientos_vehiculo = self._repo.list_by_vehiculo(vehiculo_id)

        # --- Implementación usando list_all() y filtrado en memoria (menos eficiente, pero posible) ---
        mantenimientos_vehiculo = [
            m for m in self._repo.list_all()  # <-- Asumimos que list_all() retorna Mantenimiento objects
            if m.id_vehiculo == vehiculo_id
        ]

        # 3. Filtrar y encontrar el más reciente
        ultimo_finalizado: Optional[Mantenimiento] = None

        for m in mantenimientos_vehiculo:
            if m.id_estado in final_state_ids:
                if (ultimo_finalizado is None or
                        m.fecha_hora > ultimo_finalizado.fecha_hora):  # <-- Asumimos que fecha_hora es datetime

                    ultimo_finalizado = m

        return ultimo_finalizado