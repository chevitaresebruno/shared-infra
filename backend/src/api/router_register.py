from collections.abc import Callable

from fastapi import APIRouter

RouterRegister = Callable[[APIRouter], None]
