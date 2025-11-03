# python
from typing import Any, Dict, Iterable, List, Optional

from data_access.repositories.base_repository import BaseRepository, T


class InMemoryRepository(BaseRepository[T]):
    def __init__(self, id_field: str = "id") -> None:
        self._store: Dict[Any, T] = {}
        self._id_field = id_field
        self._auto_id = 1

    def _get_id(self, entity: T) -> Any:
        if isinstance(entity, dict):
            return entity.get(self._id_field)
        return getattr(entity, self._id_field, None)

    def _set_id(self, entity: T, value: Any) -> None:
        if isinstance(entity, dict):
            entity[self._id_field] = value
        else:
            setattr(entity, self._id_field, value)

    def add(self, entity: T) -> T:
        eid = self._get_id(entity)
        if eid is None:
            eid = self._auto_id
            self._auto_id += 1
            self._set_id(entity, eid)
        self._store[eid] = entity
        return entity

    def add_all(self, entities: Iterable[T]) -> None:
        for e in entities:
            self.add(e)

    def get(self, id: Any) -> Optional[T]:
        return self._store.get(id)

    def list(self, filters: Optional[Dict[str, Any]] = None, offset: int = 0, limit: Optional[int] = None) -> List[T]:
        results = list(self._store.values())
        if filters:
            def matches(ent: T) -> bool:
                for k, v in filters.items():
                    if isinstance(ent, dict):
                        if ent.get(k) != v:
                            return False
                    else:
                        if getattr(ent, k, None) != v:
                            return False
                return True
            results = [r for r in results if matches(r)]
        if offset:
            results = results[offset:]
        if limit is not None:
            results = results[:limit]
        return results

    def update(self, entity: T, **kwargs) -> T:
        eid = self._get_id(entity)
        if eid is None:
            raise ValueError("Entity has no id; cannot update")
        for k, v in kwargs.items():
            if isinstance(entity, dict):
                entity[k] = v
            else:
                setattr(entity, k, v)
        self._store[eid] = entity
        return entity

    def delete(self, entity: T) -> None:
        eid = self._get_id(entity)
        if eid is not None:
            self._store.pop(eid, None)

    def delete_by_id(self, id: Any) -> None:
        self._store.pop(id, None)

    # commit/rollback remain no-ops for in-memory store
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
