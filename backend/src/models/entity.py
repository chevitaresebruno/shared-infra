from typing import Self

from pydantic import BaseModel, Field, model_validator


class Entity(BaseModel):
    id: int | None = Field(default=None, json_schema_extra={"readOnly": True})

    @model_validator(mode="after")
    def validate_id(self) -> Self:
        if self.id is not None and self.id <= 0:
            raise ValueError("Entity can`t have ID lower than or equal 0")
        return self
