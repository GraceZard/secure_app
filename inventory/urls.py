from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('<int:pk>/stock/in/', views.stock_in, name='stock_in'),
    path('<int:pk>/stock/out/', views.stock_out, name='stock_out'),
]