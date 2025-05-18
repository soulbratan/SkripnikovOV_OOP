class Product:
    """Класс продукта для интернет-магазина"""
    name: str
    description: str
    price: float
    quantity: int


    def __init__(self, name, description, price, quantity):
        """Конструктор класса Product для создания экземпляра объекта"""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс категории товара для интернет-магазина"""
    name: str
    description: str
    products: list
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.products = products if products else []
        Category.category_count += 1
        Category.product_count += len(products) if products else 0