from typing import Any, Optional
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Базовый класс для продуктов"""
    @abstractmethod
    def __add__(self, other: "Product") -> float:
        pass


class PrintMixin:
    """Миксин класс для печати информации о том, от какого класса и с какими параметрами создан объект"""
    def __init__(self) -> None:
        print(repr(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(BaseProduct, PrintMixin):
    """Класс продукта для интернет-магазина"""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Конструктор класса Product для создания экземпляра объекта"""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity
        super().__init__()

    def __str__(self) -> str:
        """Строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Магический метод сложения сумм всех товаров в наличии"""
        if type(other) is Product:
            return self.quantity * self.__price + other.quantity * other.price
        else:
            raise TypeError

    @property
    def price(self) -> float:
        """Геттер для получения цены продукта"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
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
            answer = input(f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): ").lower()
            if answer != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price
        print("Цена успешно обновлена")

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[list["Product"]] = None) -> "Product":
        """
        Класс-метод для создания нового товара из словаря с параметрами.
        Если товар с таким именем уже существует, объединяет количество и выбирает максимальную цену.

        :param product_data: Словарь с данными товара (name, description, price, quantity)
        :param existing_products: Список существующих товаров для проверки дубликатов
        :return: Объект класса Product (новый или обновленный)
        """
        if existing_products is None:
            existing_products = []

        name = product_data.get("name", "")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

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

    def __init__(self, name: str, description: str, products: Optional[list] = None) -> None:
        """Конструктор класса Category для создания экземпляра объекта"""
        self.name = name
        self.description = description
        self.__products = products if products else []  # Приватный атрибут
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Метод для добавления товара в приватный список товаров категории"""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError

    @property
    def products(self) -> str:
        """Геттер для получения списка товаров в заданном формате"""
        products_info = ""
        for product in self.__products:
            products_info += f"{str(product)}\n"
        return products_info

    @property
    def products_list(self) -> list:
        """Геттер для списка продуктов (чтобы итерировать)"""
        return self.__products


class CategoryIterator:
    """Вспомогательный класс для итерации по товарам категории"""

    def __init__(self, category: "Category") -> None:
        """Инициализация итератора с указанной категорией"""
        self.category = category
        self.products: list = category.products_list  # Доступ к приватному атрибуту товаров
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        """Возвращает сам объект итератора"""
        self.index = 0
        return self

    def __next__(self) -> Any:
        """Возвращает следующий товар в категории"""
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            self.index = 0
            raise StopIteration


class Smartphone(Product):
    """Дочерний класс от Product для описания товара Смартфон"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other: "Product") -> float:
        """Магический метод сложения сумм всех товаров в наличии"""
        if type(other) is Smartphone:
            return self.quantity * self.price + other.quantity * other.price
        else:
            raise TypeError


class LawnGrass(Product):
    """Дочерний класс от Product для описания товара Трава газонная"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other: "Product") -> float:
        """Магический метод сложения сумм всех товаров одного продукта в наличии"""
        if type(other) is LawnGrass:
            return self.quantity * self.price + other.quantity * other.price
        else:
            raise TypeError


if __name__ == '__main__':  # pragma: no cover
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)
