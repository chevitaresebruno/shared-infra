from sqlalchemy import Column, select

from models.product import Product
from repositories.crud_repository_sqlachemy_imp import CRUDRepositorySQLAlchemyImp
from use_cases.manage_product_use_case import IProductRepository


class ProductRepositorySQLAlchemyImp(
    IProductRepository, CRUDRepositorySQLAlchemyImp[Product]
):
    def get_by_cod(self, cod: str) -> Product:
        query = select(self._table).where(Column("cod") == cod)

        with self._engine.connect() as connection:
            result = connection.execute(query).mappings().first()

        if result is None:
            raise LookupError(f"Product with code {cod} not found.")

        return self._to_model(dict(result))
