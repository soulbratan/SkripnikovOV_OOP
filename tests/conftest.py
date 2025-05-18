import pytest

from src.main import Category, Product


@pytest.fixture
def first_product() -> Product:
    return Product(
        name="Samsung Galaxy S23 Ultra", description="256GB, Серый цвет, 200MP камера", price=180000.0, quantity=5
    )


@pytest.fixture
def second_product() -> Product:
    return Product(name="Iphone 15", description="512GB, Gray space", price=210000.0, quantity=8)


@pytest.fixture
def first_category(first_product: Product, second_product: Product) -> Category:
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни",
        products=[first_product, second_product],
    )


@pytest.fixture
def sample_data() -> list[dict]:
    """Фикстура с тестовыми данными"""
    return [
        {
            "name": "Смартфоны",
            "description": "Описание смартфонов",
            "products": [{"name": "Samsung Galaxy", "description": "256GB, Серый", "price": 180000.0, "quantity": 5}],
        },
        {
            "name": "Телевизоры",
            "description": "Описание телевизоров",
            "products": [{"name": "55 QLED 4K", "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}],
        },
    ]
