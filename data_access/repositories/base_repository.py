# python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable, Optional, List, Dict, Any

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """Abstract repository interface (CRUD)."""

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def add_all(self, entities: Iterable[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: Optional[Dict[str, Any]] = None, offset: int = 0, limit: Optional[int] = None) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: Any) -> None:
        raise NotImplementedError

    # Optional transactional methods (no-op by default)
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
