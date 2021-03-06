from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=255, null=True, verbose_name="Имя")
    email = models.CharField(max_length=255, null=True, verbose_name="Почта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    image = models.ImageField(verbose_name="Изображение", upload_to='images/%Y/%m/%d/', null=True)
    # description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    digital = models.BooleanField(default=False, null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError:
            url = ''
        return url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Покупатель")
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    complete = models.BooleanField(default=False, null=True, blank=True, verbose_name="Завершен")
    transaction_id = models.CharField(max_length=255, verbose_name="Транзакция")

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if not orderitem.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Продукт")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Заказ")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Покупатель")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Заказ")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    city = models.CharField(max_length=255, verbose_name="Город")
    state = models.CharField(max_length=255, verbose_name="Страна")
    zipcode = models.CharField(max_length=255, verbose_name="Индекс")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Информация о заказе"
        verbose_name_plural = "Информации о заказе"
