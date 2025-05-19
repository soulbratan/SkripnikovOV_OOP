import json
import os
from typing import Any
from src.main import Category, Product


def read_json(path: str) -> list[dict]:
    """
    Функция чтения данных из json-файла.
    Принимает путь до файла, возвращает словарь с данными
    """
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as f:
        data: list[dict] = json.load(f)
    return data


def create_objects_from_json(data: list[dict]) -> list:
    categories = []
    for category in data:
        products = []

        for product in category["products"]:
            products.append(Product(**product))

        category["products"] = products
        categories.append(Category(**category))
    return categories


if __name__ == "__main__":  # pragma: no cover
    raw_data = read_json("../data/products.json")
    users_data = create_objects_from_json(raw_data)
    print(users_data[0].name)
