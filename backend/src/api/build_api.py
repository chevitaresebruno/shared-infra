from collections.abc import Iterable

from fastapi import APIRouter, FastAPI

from api.router_register import RouterRegister


async def health():
    return {"stats": "ok"}


def build_api(
    root_path: str,
    title: str,
    description: str,
    debug: bool,
    use_cases: Iterable[tuple[str, RouterRegister]],
) -> FastAPI:
    app = FastAPI(
        title=title,
        debug=debug,
        description=description,
    )

    main_router = APIRouter(prefix=root_path)
    app.include_router(main_router)

    main_router.add_api_route(path="/health/", endpoint=health, methods=["GET"])

    for use_case_name, use_case_register in use_cases:
        router = APIRouter(prefix=use_case_name)
        use_case_register(router)
        main_router.include_router(router)

    return app
