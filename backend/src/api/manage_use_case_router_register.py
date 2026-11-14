from collections.abc import Iterable

from fastapi import APIRouter, HTTPException, status

from models.entity import Entity
from use_cases.use_case_types import IManageUseCase


def manage_use_case_router_register[E: Entity](
    e: type[E], router: APIRouter, use_case: IManageUseCase, tag: str | None = None
) -> None:
    tags = [] if tag is None else [tag]

    def list_entity() -> Iterable[e]:
        return use_case.list()

    def get_by_id(id: int) -> e:
        try:
            return use_case.get_by_id(id)
        except KeyError, LookupError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found",
            )

    def create(obj: e) -> e:
        use_case.create(obj)
        return obj

    def update(id: int, obj: e) -> None:
        obj.id = id
        use_case.update(obj)

    def delete(id: int) -> None:
        entity = use_case.get_by_id(id)
        use_case.delete(entity)

    router.add_api_route(
        "/",
        list_entity,
        methods=["GET"],
        response_model=list[e],
        tags=tags,
    )

    router.add_api_route(
        "/{id}",
        get_by_id,
        methods=["GET"],
        response_model=e,
        tags=tags,
    )

    router.add_api_route(
        "/",
        create,
        methods=["POST"],
        status_code=status.HTTP_201_CREATED,
        response_model=e,
        tags=tags,
    )

    router.add_api_route(
        "/",
        update,
        methods=["PUT"],
        status_code=status.HTTP_204_NO_CONTENT,
        tags=tags,
    )

    router.add_api_route(
        "/{id}",
        delete,
        methods=["DELETE"],
        status_code=status.HTTP_204_NO_CONTENT,
        tags=tags,
    )
