from typing import Optional
from domain.models.mantenimiento import Mantenimiento
from data_access.repositories import MantenimientoRepository
from services.estado_service import EstadoService


class MantenimientoService:
    def __init__(self, mantenimiento_repo: MantenimientoRepository, estado_service: EstadoService):
        self._repo = mantenimiento_repo
        self._estado_service = estado_service

    def iniciar_nuevo_mantenimiento(self, id_vehiculo: int, costo: float, descripcion: str, id_empleado: int) -> \
    Optional[int]:
        # 1. Obtener estado inicial (EnDiagnostico)
        estado_inicial = self._estado_service.get_estado_by_name_and_ambito("EnDiagnostico", "Mantenimiento")
        if not estado_inicial:
            print("Error crítico: Estado 'EnDiagnostico' no configurado en BD.")
            return None

        # 2. Crear objeto
        nuevo_mantenimiento = Mantenimiento(
            id_vehiculo=id_vehiculo,
            costo=costo,
            descripcion=descripcion,
            id_empleado=id_empleado,
            id_estado=estado_inicial.id
        )

        # 3. Guardar (el repositorio maneja la sesión y commit)
        try:
            creado = self._repo.create(nuevo_mantenimiento)
            return creado.id
        except Exception as e:
            print(f"Error iniciando mantenimiento: {e}")
            self._repo.session.rollback()
            return None

    def get_last_finalized_mantenimiento(self, vehiculo_id: int) -> Optional[Mantenimiento]:
        """Retorna el último mantenimiento finalizado (Reparado o NoReparado)."""
        todos = self._repo.list_by_vehiculo(vehiculo_id)  # Ya viene ordenado por fecha DESC

        for m in todos:
            # SQLAlchemy carga el objeto Estado relacionado (lazy loading por defecto)
            if m.Estado and m.Estado.nombre in ["Reparado", "NoReparado"]:
                return m
        return None

    def get_mantenimiento_by_id(self, mantenimiento_id: int) -> Optional[Mantenimiento]:
        mantenimiento = self._repo.get_by_id(mantenimiento_id)
        if mantenimiento:
            from domain.states.mantenimiento.state import State
            # Inicializar estado
            if mantenimiento.Estado:
                mantenimiento._state = State.from_entity(mantenimiento.Estado)
            else:
                from domain.states.mantenimiento.en_diagnostico import EnDiagnostico
                mantenimiento._state = EnDiagnostico()

            mantenimiento._state.context = mantenimiento
        return mantenimiento