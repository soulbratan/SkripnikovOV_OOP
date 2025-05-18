import json
import os

from src.main import Product, Category

def read_json(path: str) -> dict:
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def create_objects_from_json(data):
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
    print(users_data[1].name)