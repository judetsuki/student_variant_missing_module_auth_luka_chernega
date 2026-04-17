from django.contrib import admin
from products.models import Category, Product, Manufacturer, Supplier, Unit
from orders.models import Order, OrderStatus ,PickupPoint


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    ...

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    ...

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    ...
