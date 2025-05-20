class Product:
    """Класс продукта для интернет-магазина"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Конструктор класса Product для создания экземпляра объекта"""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для получения цены продукта"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """
        Сеттер для установки цены продукта с проверками:
        1. Цена должна быть положительной
        2. При понижении цены требует подтверждения пользователя
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            # Если цена понижается, запрашиваем подтверждение
            answer = input(
                f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): ").lower()
            if answer != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price
        print("Цена успешно обновлена")

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None):
        """
        Класс-метод для создания нового товара из словаря с параметрами.
        Если товар с таким именем уже существует, объединяет количество и выбирает максимальную цену.

        :param product_data: Словарь с данными товара (name, description, price, quantity)
        :param existing_products: Список существующих товаров для проверки дубликатов
        :return: Объект класса Product (новый или обновленный)
        """
        if existing_products is None:
            existing_products = []

        name = product_data.get('name')
        description = product_data.get('description')
        price = product_data.get('price')
        quantity = product_data.get('quantity')

        # Поиск товара с таким же именем
        for product in existing_products:
            if product.name.lower() == name.lower():
                # Объединение количества и выбор максимальной цены
                product.quantity += quantity
                product.price = max(product.price, price)  # Используем сеттер price
                return product

        # Если дубликат не найден, создаем новый товар
        return cls(name, description, price, quantity)


class Category:
    """Класс категории товара для интернет-магазина"""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product] | None = None):
        """Конструктор класса Category для создания экземпляра объекта"""
        self.name = name
        self.description = description
        self.__products = products if products else []  # Приватный атрибут
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product):
        """Метод для добавления товара в приватный список товаров категории"""
        # Проверяем, нет ли уже такого товара в категории
        existing_product = None
        for p in self.__products:
            if p.name.lower() == product.name.lower():
                existing_product = p
                break

        if existing_product:
            # Если товар найден, обновляем количество и цену
            existing_product.quantity += product.quantity
            existing_product.price = max(existing_product.price, product.price)
        else:
            # Если товар не найден, добавляем новый
            self.__products.append(product)
            Category.product_count += 1

    @property
    def products(self):
        """Геттер для получения списка товаров в заданном формате"""
        products_info = ""
        for product in self.__products:
            products_info += (f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n")
        return products_info


if __name__ == "__main__":  # pragma: no cover
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5})
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
