from django.contrib import admin
from orders.models import Order, OrderStatus ,PickupPoint
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    ...

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    ...