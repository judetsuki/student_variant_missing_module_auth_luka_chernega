from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    path('orders/', views.order_list, name='order_list'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/update/', views.order_update, name='order_update'),
    path('orders/create/', views.order_create, name='order_create')
]