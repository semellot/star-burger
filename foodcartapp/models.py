from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class OrderQuerySet(models.QuerySet):
    def calculation_cost(self):
        return self.annotate(cost=Sum(F('products__quantity') * F('products__product__price')))


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'Новый'),
        ('Gather', 'В сборке'),
        ('Courier', 'У курьера'),
        ('Done', 'Выполнен')
    ]
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=STATUS_CHOICES,
        default='New',
        db_index=True
    )
    PAYMENT_CHOICES = [
        ('CASH', 'Наличными'),
        ('CARD', 'Картой')
    ]
    payment = models.CharField(
        'Способ оплаты',
        max_length=4,
        choices=PAYMENT_CHOICES,
        blank=True,
        db_index=True
    )
    address = models.CharField(
        'Адрес',
        max_length=100,
    )
    firstname = models.CharField(
        'Имя',
        max_length=50
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        'Мобильный номер'
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )
    created_date = models.DateTimeField(
        'Дата создания',
        default=timezone.now,
        db_index=True
    )
    called_date = models.DateTimeField(
        'Дата звонка',
        null=True,
        blank=True,
        db_index=True
    )
    delivered_date = models.DateTimeField(
        'Дата доставки',
        null=True,
        blank=True,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='products',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='Товар',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'Количество'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f'{self.order} - {self.product.name} - {self.quantity}'
