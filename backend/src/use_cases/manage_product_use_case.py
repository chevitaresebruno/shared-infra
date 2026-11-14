from typing import Protocol

from models.product import Product
from use_cases.manage_use_case_imp import ICRUDRepository, ManageUseCaseImp


class IProductRepository(ICRUDRepository, Protocol):
    def get_by_cod(self, cod: str) -> Product: ...


class ManageProductUseCase(ManageUseCaseImp[Product, IProductRepository]):
    def get_by_cod(self, cod: str) -> Product:
        return self._repo.get_by_cod(cod)
