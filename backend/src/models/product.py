from typing import Self

from pydantic import model_validator

from models.entity import Entity


class Product(Entity):
    name: str
    description: str
    quantity: int
    cod: str
    price: float

    @model_validator(mode="after")
    def validate_quantity(self) -> Self:
        if self.quantity < 0:
            raise ValueError(
                f"Product quantity can't be lower than 0 (receive {self.quantity})"
            )
        return self

    @model_validator(mode="after")
    def validate_price(self) -> Self:
        if self.price <= 0:
            raise ValueError(
                f"Product price can't be lower than or equal 0 (receive {self.price})"
            )
        return self
