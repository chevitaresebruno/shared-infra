from collections.abc import Iterable
from typing import Protocol

from models.entity import Entity
from use_cases.use_case_types import IManageUseCase


class ICRUDRepository[T: Entity](Protocol):
    def list(self) -> Iterable[T]: ...

    def get_by_id(self, id: int) -> T: ...

    def create(self, obj: T) -> int: ...

    def update(self, obj: T) -> None: ...

    def delete(self, obj: T) -> None: ...


class ManageUseCaseImp[E: Entity, R: ICRUDRepository](IManageUseCase):
    def __init__(self, repo: R) -> None:
        self._repo = repo

    def list(self) -> Iterable[E]:
        return self._repo.list()

    def get_by_id(self, id: int) -> E:
        return self._repo.get_by_id(id)

    def create(self, obj: E) -> None:
        created_id = self._repo.create(obj)
        obj.id = created_id

    def update(self, obj: E) -> None:
        self._repo.update(obj)

    def delete(self, obj: E) -> None:
        self._repo.delete(obj)
