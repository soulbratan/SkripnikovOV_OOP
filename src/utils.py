import json
import os

from src.main import Product, Category

def read_json(path: str) -> dict:
    """
    Функция чтения данных из json-файла.
    Принимает путь до файла, возвращает словарь с данными
    """
    try:
        full_path = os.path.abspath(path)
        with open(full_path, "r", encoding="UTF-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = [{"name": "None",
                 "description": "None",
                 "products": [{"name": "None",
                               "description": "None",
                               "price": 0.0,
                               "quantity": 0
                               }
                              ]
                 }
                ]
    return data


def create_objects_from_json(data: dict) -> list:
    categories = []
    for category in data:
        products = []

        for product in category["products"]:
            products.append(Product(**product))

        category["products"] = products
        categories.append(Category(**category))
    return categories


if __name__ == "__main__": # pragma: no cover
    raw_data = read_json("../data/products.json")
    users_data = create_objects_from_json(raw_data)
    print(users_data[0].name)