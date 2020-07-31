from django.urls import path
from .views import *
urlpatterns = [
    path('products_/', returnListProducts, name='all_products'),
    path('add-cart/<str:pk_>', addToCart, name='add_cart'),
    path('carts/', viewCart, name='the_cart'),
    path('delete-product/<str:pk_>', deleteItem, name='delete_item2'),
    path('pay/<str:pk_>', transactionProcess, name='pay'),
    path('my-cart/', currentCustomerOrders, name='my_cart')
]