from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.main import Category, Product, CategoryIterator


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


def test_category_1(
    first_category: Category, third_product: Product, new_data_product: dict, new_data_product_n: dict
) -> None:
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


def test_new_product(new_data_product: dict, new_data_product_n: dict, capsys: Any) -> None:
    """Тест метода new_product"""
    new_product = Product.new_product(new_data_product)  # Создаём новый объект из словаря
    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.description == "256GB, Серый цвет, 200MP камера"
    assert new_product.price == 180000.0
    assert new_product.quantity == 5

    # Создаём новый объект из словаря и проверяем со списком, в котором находится предыдущий объект
    Product.new_product(new_data_product_n, [new_product])
    assert new_product.quantity == 8  # Проверка изменения количества на 3
    assert new_product.price == 190000.0  # Проверка изменения количества на 3


def test_new_price_to_product(new_data_product: dict, capsys: Any) -> None:
    new_product = Product.new_product(new_data_product)  # Создаём новый объект из словаря
    assert new_product.price == 180000.0
    new_product.price = -1000.0
    captured = capsys.readouterr()
    assert captured.out == "Цена не должна быть нулевая или отрицательная\n"


@patch("builtins.input", return_value="y")
def test_new_price_confirm_to_product(mock_input: MagicMock, new_data_product: dict, capsys: Any) -> None:
    """Проверка понижения цены с подтверждением (пользователь согласен)"""
    new_product = Product.new_product(new_data_product)  # Создаём новый объект из словаря
    assert new_product.price == 180000.0
    new_product.price = 1000.0
    captured = capsys.readouterr()
    assert captured.out == "Цена успешно обновлена\n"
    mock_input.assert_called_once()


@patch("builtins.input", return_value="n")
def test_new_price_cancel_to_product(mock_input: MagicMock, new_data_product: dict, capsys: Any) -> None:
    """Проверка понижения цены с отказом (пользователь отказался)"""
    new_product = Product.new_product(new_data_product)  # Создаём новый объект из словаря
    assert new_product.price == 180000.0
    new_product.price = 1000.0
    captured = capsys.readouterr()
    assert captured.out == "Изменение цены отменено\n"
    mock_input.assert_called_once()


def test_str_methods(
    first_category: Category, first_product: Product, second_product: Product, third_product: Product
) -> None:
    """Тестирование метода __str__ для классов Product и Category"""
    assert str(first_category) == "Смартфоны, количество продуктов: 13 шт."
    assert str(first_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert str(second_product) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."
    assert str(third_product) == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт."


def test_add_products(first_product: Product, second_product: Product, third_product: Product) -> None:
    """Тестирование переопределённого метода __add__ для класса Product"""
    assert (first_product + second_product) == 2580000.0
    assert (first_product + third_product) == 1334000.0
    assert (second_product + third_product) == 2114000.0


def test_products_list_getter(first_category: Category, first_product: Product, second_product: Product) -> None:
    """Тест геттера products_list"""
    assert len(first_category.products_list) == 2
    assert first_category.products_list[0] == first_product
    assert first_category.products_list[1] == second_product


def test_category_iterator(category_iterator: CategoryIterator) -> None:
    """Тестирование итератора CategoryIterator"""
    iter(category_iterator)
    assert category_iterator.index == 0
    assert next(category_iterator).name == "Samsung Galaxy S23 Ultra"
    assert next(category_iterator).name == "Iphone 15"

    with pytest.raises(StopIteration):
        next(category_iterator)
