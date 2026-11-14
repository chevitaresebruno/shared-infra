from fastapi import APIRouter, HTTPException, status

from api.manage_use_case_router_register import manage_use_case_router_register
from models.product import Product
from use_cases.manage_product_use_case import ManageProductUseCase


def product_register(router: APIRouter, use_case: ManageProductUseCase) -> None:
    manage_use_case_router_register(Product, router, use_case, "product")

    def get_by_code(cod: str) -> Product:
        try:
            return use_case.get_by_cod(cod)
        except KeyError, LookupError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found",
            )

    router.add_api_route(
        "/get_by_code/{cod}",
        get_by_code,
        methods=["GET"],
        response_model=Product,
        tags=["product"],
    )
