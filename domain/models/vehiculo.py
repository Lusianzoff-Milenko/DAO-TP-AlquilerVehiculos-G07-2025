from __future__ import annotations
from datetime import datetime
from typing import Any, List
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .mantenimiento import Mantenimiento
from ..states.vehiculo.state import State
from .estado import Estado
from .color import Color
from .modelo import Modelo


class Vehiculo(Base):
    __tablename__ = 'Vehiculo'
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo: int = Column(Integer, ForeignKey('Modelo.id'), nullable=False)
    patente: str = Column(String(20), nullable=False, unique=True)
    nro_chasis: str = Column(String(20), nullable=False, unique=True)
    id_color: int = Column("color", Integer, ForeignKey('Color.id'), nullable=False)

    anio_fabricacion: datetime = Column(DateTime, default=datetime.now(), name="año_fabricacion")
    precio_base: float = Column(Float, nullable=False)
    id_estado: int = Column(Integer, ForeignKey('Estado.id'), nullable=False)

    mantenimientos: List[Mantenimiento] = relationship("Mantenimiento", back_populates="Vehiculo")
    Estado = relationship(Estado)
    Modelo = relationship(Modelo)
    Color = relationship(Color)

    _state = None
    estados_disponibles: list[type[Estado]] = []

    def get_state(self) -> State:
        return self._state

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)

        # 1. Estado por defecto en BD (Si no se especifica, ID 1 = Disponible)
        if self.id_estado is None:
            self.id_estado = 1

        # 2. Inicializar el State Pattern en memoria
        # Importación local para evitar ciclos
        from domain.states.vehiculo.state import State

        # Si al crear el objeto le pasaste el objeto 'Estado' (entity), usamos la factory.
        # Si no (caso común: objeto nuevo), usamos 'Disponible' por defecto.
        if self.Estado:
            self._state = State.from_entity(self.Estado)
        else:
            from domain.states.vehiculo.disponible import Disponible
            self._state = Disponible()

        if self._state:
            self._state.context = self

    def transition_to(self, state: State):
        if self._state.__class__ != state.__class__:
            print(f"Vehiculo: Transicionando al estado {type(state).__name__}")
            self._state = state
            self._state.context = self

            nuevo_estado_nombre = type(state).__name__

            # Actualizamos el ID en la base de datos buscando en la lista inyectada
            if self.estados_disponibles:
                encontrado = False
                for estado_bd in self.estados_disponibles:
                    # Comparamos nombres (ignorando mayúsculas/minúsculas por seguridad)
                    if estado_bd.nombre.lower() == nuevo_estado_nombre.lower():
                        self.id_estado = estado_bd.id
                        self.Estado = estado_bd  # Actualizamos también la relación ORM
                        encontrado = True
                        break

                if not encontrado:
                    print(f"¡ADVERTENCIA! No se encontró ID para el estado '{nuevo_estado_nombre}' en la BD.")

    def agregar_mantenimiento(self, mantenimiento) -> None:
        self.mantenimientos.append(mantenimiento)
        mantenimiento.Vehiculo = self

    def __str__(self) -> str:
        # Cuidado aquí: self.Modelo y self.Color pueden ser None si no se cargaron (lazy loading)
        modelo_nombre = self.Modelo.nombre if self.Modelo else "Desconocido"
        color_nombre = self.Color.nombre if self.Color else "Desconocido"
        estado_nombre = self._state.__class__.__name__ if self._state else str(self.id_estado)

        return f"Vehiculo [id={self.id}, modelo={modelo_nombre}, patente={self.patente}, color={color_nombre}, estado={estado_nombre}]"

