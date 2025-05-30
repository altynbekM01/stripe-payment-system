from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),


    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/add/<int:item_id>/', views.add_to_order, name='add_to_order'),

    path('orders/<int:order_id>/buy/', views.buy_order, name='buy_order'),
    path('orders/<int:order_id>/apply-coupon/', views.apply_coupon_view, name='apply-coupon'),
]
