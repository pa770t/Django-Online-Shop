from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # shopping urls
    path('shop', views.shop, name='shop'),
    path('product/detail/<int:id>', views.shop_detail, name='detail'),

    # category urls
    path('category', views.category, name='category'),

    # cart urls
    path('cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('delete-cart/<int:product_id>', views.delete_cart, name='delete_cart'),
    
    # order urls
    path('add-order', views.add_order, name='add_order'),

    # by managers
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/products', views.product_manager_view, name='product_manager_view'),
    path('dashboard/products/delete_view/<int:product_id>', views.product_delete_manager_view, name='product_delete_manager_view'),
    path('dashboard/products/delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('dashboard/orders', views.order_manager_view, name='order_manager_view'),
    path('dashboard/customers', views.customer_manager_view, name='customer_manager_view'),
    path('dashboard/customers/<int:customer_id>', views.only_customer_manager_view, name='only_customer_manager_view'),
    path('dashboard/orders/<int:customer_id>', views.orders_by_customer_manager_view, name='orders_by_customer_manager_view'),
    # delete order by manager
    path('dashboard/orders/delete_view/<int:order_id>', views.order_delete_by_customer_manager_view, name='order_delete_by_customer_manager_view'),
    path('dashboard/orders/delete/<int:order_id>', views.delete_order_by_manager, name='delete_order_by_manager'),

    # user urls
    path('register', views.register_user, name='register_user'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('profile', views.profile_setting, name='profile'),

    # checkout
    path('checkout', views.checkout, name='checkout'),
]
