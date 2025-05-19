import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product
from src.utils import create_objects_from_json, read_json


def test_read_json_success() -> None:
    """Тест успешного чтения JSON файла"""
    test_data = {"key": "value"}
    json_str = json.dumps(test_data)

    with patch("builtins.open", mock_open(read_data=json_str)) as mock_file:
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = test_data
            result = read_json("test_path.json")

            # Проверяем, что файл открывался с правильными параметрами
            mock_file.assert_called_once_with(os.path.abspath("test_path.json"), "r", encoding="UTF-8")
            # Проверяем, что json.load был вызван
            mock_json_load.assert_called_once()
            # Проверяем результат
            assert result == test_data


def test_read_file_raises_file_not_found_error() -> None:
    non_existent_file = "non_existent_file.txt"
    # Проверяем, что при вызове read_file с несуществующим файлом
    # действительно выбрасывается FileNotFoundError
    with pytest.raises(FileNotFoundError):
        read_json(non_existent_file)


def test_read_json_invalid_json() -> None:
    """Тест обработки невалидного JSON (опционально)"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            with pytest.raises(json.JSONDecodeError):
                read_json("invalid.json")


def test_create_objects_from_json_structure(sample_data: list[dict]) -> None:
    """Тест правильности структуры возвращаемых данных"""
    result = create_objects_from_json(sample_data)

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(category, Category) for category in result)
    assert all(isinstance(product, Product) for category in result for product in category.products)


def test_create_objects_from_json_values(sample_data: list[dict]) -> None:
    """Тест корректности значений в созданных объектах"""
    result = create_objects_from_json(sample_data)

    # Проверка первой категории
    assert result[0].name == "Смартфоны"
    assert result[0].description == "Описание смартфонов"
    assert len(result[0].products) == 1
    assert result[0].products[0].name == "Samsung Galaxy"
    assert result[0].products[0].price == 180000.0

    # Проверка второй категории
    assert result[1].name == "Телевизоры"
    assert result[1].description == "Описание телевизоров"
    assert len(result[1].products) == 1
    assert result[1].products[0].name == "55 QLED 4K"
    assert result[1].products[0].price == 123000.0


def test_create_objects_from_json_empty_products() -> None:
    """Тест обработки категории без продуктов"""
    test_data = [{"name": "Пустая категория", "description": "Нет продуктов", "products": []}]
    result = create_objects_from_json(test_data)
    assert len(result) == 1
    assert result[0].name == "Пустая категория"
    assert len(result[0].products) == 0
