from sqlalchemy import MetaData, Table, create_engine
from uvicorn import run

from api.build_api import build_api
from api.product_register import product_register
from models.product import Product
from repositories.product_repository import ProductRepositorySQLAlchemyImp
from settings import load_settings_from_env
from use_cases.manage_product_use_case import ManageProductUseCase


def main() -> None:
    settings = load_settings_from_env()

    engine = create_engine(settings.database_connection_url)

    metadata = MetaData()

    table = Table(
        "product",
        metadata,
        autoload_with=engine,
    )

    app = build_api(
        root_path=settings.app_sub_path,
        title=settings.app_title,
        description=settings.app_description,
        debug=settings.is_debug,
        use_cases=(
            (
                "/product",
                lambda x: product_register(
                    x,
                    ManageProductUseCase(
                        ProductRepositorySQLAlchemyImp(
                            engine=engine, table=table, model_type=Product
                        )
                    ),
                ),
            ),
        ),
    )

    run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        forwarded_allow_ips=settings.app_allow_ips,
    )


if __name__ == "__main__":
    main()
