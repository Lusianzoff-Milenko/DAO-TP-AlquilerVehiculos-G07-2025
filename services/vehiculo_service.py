from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from domain.models.vehiculo import Vehiculo
from domain.states.vehiculo.state import State
from data_access.repositories import VehiculoRepository
from services.estado_service import EstadoService
from services.mantenimiento_service import MantenimientoService


class VehiculoService:
    def __init__(self,
                 vehiculo_repo: VehiculoRepository,
                 estado_service: EstadoService,
                 mantenimiento_service: MantenimientoService):
        self._repo = vehiculo_repo
        self._estado_service = estado_service
        self._mantenimiento_service = mantenimiento_service

    def _init_vehiculo_state(self, vehiculo: Vehiculo):
        """Inicializa el State Pattern usando el objeto Estado relacionado."""
        if vehiculo:
            # Inyectamos estados disponibles para transiciones
            vehiculo.estados_disponibles = self._estado_service.get_estado_by_ambito("Vehiculo")

            # AQUI EL CAMBIO: Usamos el objeto Estado completo, no el ID
            # SQLAlchemy cargará vehiculo.Estado automáticamente al accederlo
            if vehiculo.Estado:
                state_instance = State.from_entity(vehiculo.Estado)
            else:
                # Si por alguna razón no cargó la relación, intentamos buscarlo o default
                # (Opcional: buscar por ID si vehicle.Estado es None)
                from domain.states.vehiculo.disponible import Disponible
                state_instance = Disponible()

            state_instance.context = vehiculo
            vehiculo._state = state_instance

    # --- CRUD ---
    def create_vehiculo(self, vehiculo: Vehiculo) -> Optional[int]:
        try:
            # Asignar estado inicial 'Disponible' si viene sin estado
            if not vehiculo.id_estado:
                est = self._estado_service.get_estado_by_name_and_ambito("Disponible", "Vehiculo")
                if est: vehiculo.id_estado = est.id

            created = self._repo.create(vehiculo)
            return created.id
        except IntegrityError as e:
            print(f"Error creando vehículo (Patente/Chasis duplicado o Modelo inválido): {e}")
            self._repo.session.rollback()
            return None

    def get_vehiculo_by_id(self, id: int) -> Optional[Vehiculo]:
        vehiculo = self._repo.get_by_id(id)
        self._init_vehiculo_state(vehiculo)
        return vehiculo

    def list_all_vehiculos(self) -> List[Vehiculo]:
        vehiculos = self._repo.list_all()
        for v in vehiculos:
            self._init_vehiculo_state(v)
        return vehiculos

    def update_vehiculo(self, vehiculo: Vehiculo) -> bool:
        try:
            self._repo.update(vehiculo)
            return True
        except IntegrityError:
            self._repo.session.rollback()
            return False

    def delete_vehiculo(self, vehiculo_id: int) -> bool:
        try:
            return self._repo.delete(vehiculo_id)
        except IntegrityError:
            print("No se puede eliminar el vehículo: tiene historial asociado.")
            self._repo.session.rollback()
            return False

    # --- Lógica de Negocio Avanzada ---

    def enviar_a_mantenimiento(self, vehiculo_id: int, costo: float, descripcion: str, id_empleado: int) -> bool:
        """Intenta pasar el vehículo a mantenimiento y crea el registro correspondiente."""
        vehiculo = self.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo: return False

        # 1. Intentar transición de estado (En memoria)
        # Si el vehículo no está en un estado válido (ej. Alquilado), el State imprimirá error y no cambiará
        estado_anterior = vehiculo.id_estado

        # Dependiendo de donde venga, usamos el método adecuado.
        # Si asumimos que viene de "EnRevision" o "Disponible":
        vehiculo.get_state().iniciar_mantenimiento()

        if vehiculo.id_estado == estado_anterior:
            print("No se pudo transicionar el vehículo a Mantenimiento.")
            return False

        # 2. Crear el registro de Mantenimiento
        mant_id = self._mantenimiento_service.iniciar_nuevo_mantenimiento(
            id_vehiculo=vehiculo.id,
            costo=costo,
            descripcion=descripcion,
            id_empleado=id_empleado
        )

        if mant_id:
            # 3. Persistir el cambio de estado del vehículo
            self._repo.update(vehiculo)
            return True
        else:
            # Si falló crear el mantenimiento, no guardamos el cambio de vehículo (rollback lógico)
            print("Falló el registro de mantenimiento.")
            return False

    def finalizar_mantenimiento(self, vehiculo_id: int) -> bool:
        """
        Consulta el último mantenimiento. Si está 'Reparado', habilita el vehículo.
        Si está 'NoReparado', lo marca fuera de servicio.
        """
        vehiculo = self.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo: return False

        # Solo procesar si el vehículo está físicamente en mantenimiento
        if vehiculo.get_state().__class__.__name__ != 'EnMantenimiento':
            print("El vehículo no está en estado 'EnMantenimiento'.")
            return False

        ultimo_mant = self._mantenimiento_service.get_last_finalized_mantenimiento(vehiculo_id)

        if not ultimo_mant:
            print("No se encontró un dictamen final (Reparado/NoReparado) para este vehículo.")
            return False

        estado_mant = ultimo_mant.Estado.nombre

        if estado_mant == "Reparado":
            vehiculo.get_state().reincorporar("Mantenimiento finalizado con éxito")
            self._repo.update(vehiculo)
            return True
        elif estado_mant == "NoReparado":
            vehiculo.get_state().marcar_fuera_de_servicio()
            self._repo.update(vehiculo)
            return True

        return False