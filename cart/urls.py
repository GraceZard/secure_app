from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:item_id>/', views.cart_add, name='add'),
    path('remove/<int:item_id>/', views.cart_remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-created/<int:order_id>/', views.order_created, name='order_created'),
    path('orders/', views.order_history, name='order_history'),
]