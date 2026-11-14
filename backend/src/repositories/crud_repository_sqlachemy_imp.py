from collections.abc import Iterable
from typing import Any

from sqlalchemy import Engine, Table, delete, insert, select, update

from models.entity import Entity
from use_cases.manage_use_case_imp import ICRUDRepository


class CRUDRepositorySQLAlchemyImp[T: Entity](ICRUDRepository[T]):
    def __init__(self, engine: Engine, table: Table, model_type: type[T]) -> None:
        self._engine = engine
        self._table = table
        self._model_type = model_type

        primary_keys = list(table.primary_key.columns)

        if len(primary_keys) != 1:
            raise ValueError("The repository requires exactly one primary key.")

        self.__primary_key = primary_keys[0]

    def _to_model(self, data: dict[str, Any]) -> T:
        return self._model_type.model_validate(data)

    def _to_dict(self, obj: T) -> dict[str, Any]:
        data = obj.model_dump(
            mode="python",
            by_alias=True,
        )

        return {key: value for key, value in data.items() if key in self._table.c}

    def list(self) -> Iterable[T]:
        query = select(self._table)

        with self._engine.connect() as connection:
            result = connection.execute(query).mappings().all()

        return [self._to_model(dict(row)) for row in result]

    def get_by_id(self, id: int) -> T:
        query = select(self._table).where(self.__primary_key == id)

        with self._engine.connect() as connection:
            result = connection.execute(query).mappings().first()

        if result is None:
            raise LookupError(f"{self._model_type.__name__} with id {id} not found.")

        return self._to_model(dict(result))

    def create(self, obj: T) -> int:
        data = self._to_dict(obj)

        if data.get(self.__primary_key.name) is None:
            data.pop(self.__primary_key.name, None)

        query = insert(self._table).values(**data).returning(self.__primary_key)

        with self._engine.begin() as connection:
            result = connection.execute(query)
            inserted_id = result.scalar_one()

        return int(inserted_id)

    def update(self, obj: T) -> None:
        data = self._to_dict(obj)
        entity_id = data.pop(self.__primary_key.name)

        query = (
            update(self._table).where(self.__primary_key == entity_id).values(**data)
        )

        with self._engine.begin() as connection:
            result = connection.execute(query)

            if result.rowcount == 0:
                raise LookupError(
                    f"{self._model_type.__name__} with id {entity_id} not found."
                )

    def delete(self, obj: T) -> None:
        entity_id = obj.id

        query = delete(self._table).where(self.__primary_key == entity_id)

        with self._engine.begin() as connection:
            result = connection.execute(query)

            if result.rowcount == 0:
                raise LookupError(
                    f"{self._model_type.__name__} with id {entity_id} not found."
                )
