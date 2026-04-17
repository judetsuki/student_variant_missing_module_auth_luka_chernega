from django.db import models
from django.conf import settings

# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=20,unique=True, verbose_name="Номер заказа")
    order_date = models.DateField(verbose_name="Дата заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='Клиент')
    pickup_point_id = models.ForeignKey('PickupPoint', on_delete=models.CASCADE,verbose_name='Адрес пункта доставки')
    status = models.ForeignKey('OrderStatus',on_delete=models.CASCADE, verbose_name="Статус заказа")


class OrderItem(models.Model):
    quantity = models.CharField(max_length=20,verbose_name="Количество")
    price = models.CharField(max_length=20,verbose_name="Цена")
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE,verbose_name='Заказ')
    product_id = models.ForeignKey('products.Product', on_delete=models.CASCADE,verbose_name='Товар')

class OrderStatus(models.Model):    
    STATUS_CHOICES = [
        ('Завершен', 'Завершен'),
        ('Новый', 'Новый')
    ]  
    status = models.CharField(choices=STATUS_CHOICES,max_length=30,verbose_name='Статус заказа')

class PickupPoint(models.Model):
    address = models.CharField(max_length=100,verbose_name='Адрес пункта выдачи')