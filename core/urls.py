from django.urls import path

from .views import *

urlpatterns = [
	path('', home, name = 'home'),

	path('item/<slug>', ItemDetailView.as_view(), name = 'item'),

	path('add_to_cart', add_to_cart, name = 'add_to_cart'),
	path('products', products, name = 'products'),
	path('checkout', checkout, name = 'checkout'),
	path('order', order, name = 'order'),

	path('remove_from_cart/<id>', remove_from_cart, name = 'remove_from_cart'),
	path('add_single_item/<id>', add_single_item, name = 'add_single_item'),
	path('remove_single_item/<id>', remove_single_item, name = 'remove_single_item'),
]