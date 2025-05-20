from src.main import Category, Product


def test_product_1(first_product: Product, second_product: Product) -> None:
    """Тест проверяет корректность создания класса Продукт."""
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5

    assert second_product.name == "Iphone 15"
    assert second_product.description == "512GB, Gray space"
    assert second_product.price == 210000.0
    assert second_product.quantity == 8


def test_category_1(first_category: Category, third_product: Product, new_data_product: dict, new_data_product_n: dict) -> None:
    """Тест проверяет корректность создания класса Категория."""
    assert first_category.name == "Смартфоны"
    assert (
        first_category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт." in first_category.products
    assert "Iphone 15, 210000.0 руб. Остаток: 8 шт." in first_category.products
    assert "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт." not in first_category.products
    assert first_category.category_count == 1
    assert first_category.product_count == 2

    # Добавляем продукт в категорию
    first_category.add_product(third_product)
    assert first_category.category_count == 1
    assert first_category.product_count == 3
    assert "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт." in first_category.products

def test_new_product(new_data_product, new_data_product_n):
    """Тест метода new_product"""
    new_product = Product.new_product(new_data_product) # Создаём новый объект из словаря
    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.description == "256GB, Серый цвет, 200MP камера"
    assert new_product.price == 180000.0
    assert new_product.quantity == 5

    # Создаём новый объект из словаря и проверяем со списком, в котором находится предыдущий объект
    Product.new_product(new_data_product_n, [new_product])
    assert new_product.quantity == 8 # Проверка изменения количества на 3
    assert new_product.price == 190000.0 # Проверка изменения количества на 3



