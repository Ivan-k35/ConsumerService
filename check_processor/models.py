from django.db import models


class Place(models.Model):
    place_id = models.CharField(max_length=100, unique=True, verbose_name='Идентификатор места')
    place_name = models.CharField(max_length=255, verbose_name='Название места')

    def __str__(self):
        return self.place_name


class Purchase(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name='Идентификатор транзакции')
    timestamp = models.DateTimeField(verbose_name='Дата и время')
    place_id = models.CharField(null=True, blank=True, max_length=255, verbose_name='Идентификатор места')
    place_name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Название места')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма НДС')
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      verbose_name='Сумма чаевых')
    payment_method = models.CharField(null=True, blank=True, max_length=100, verbose_name='Метод оплаты')


class Item(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE, verbose_name='Покупка')
    product_id = models.CharField(max_length=255, verbose_name='Идентификатор продукта')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return f'{self.quantity} x {self.product_id}'


class CategoryAnalytics(models.Model):
    place = models.ForeignKey(Place, related_name='category_analytics', on_delete=models.CASCADE, verbose_name='Место')
    category = models.CharField(max_length=100, verbose_name='Категория')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Средний чек')

    def __str__(self):
        return f'Аналитика для {self.place} - {self.category}'


class TotalAnalytics(models.Model):
    place = models.OneToOneField(Place, related_name='total_analytics', on_delete=models.CASCADE, verbose_name='Место')
    total_purchases = models.IntegerField(default=0, verbose_name='Общее количество покупок')
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Средний чек')
    total_nds = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма НДС')
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма чаевых')
    category_analytics = models.ForeignKey(CategoryAnalytics, related_name='total_analytics', on_delete=models.CASCADE,
                                           null=True, blank=True, verbose_name='Аналитика по категориям')

    def __str__(self):
        return f'Общая аналитика для {self.place}'
