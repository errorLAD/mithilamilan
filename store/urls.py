from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
]
