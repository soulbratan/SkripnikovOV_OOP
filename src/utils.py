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