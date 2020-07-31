from django.urls import path, include
from .views import *
urlpatterns = [
    path('', AllObjectsOfOneItemsList.as_view(), name='items-list'),
    path('product/<slug:slug>/', getObjectChosen, name='product'),
    path('add-item/<slug:slug>', addToCart, name='add_to_cart'),
    # path('cart/', viewCart, name='cart')
    path('cart/', viewAllPurchasedItems.as_view(), name='cart'),
    path('remove-item/<slug:slug>', removeFromCart, name='remove-item')
    # here in this case we will need using get_absolute_url that we will take us to the object chosen by its slug
]