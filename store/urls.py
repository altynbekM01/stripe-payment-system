from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),


    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),

    path('orders/create/', views.create_order, name='create_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/add/<int:item_id>/', views.add_to_order, name='add_to_order'),

    path('orders/<int:order_id>/buy/', views.buy_order, name='buy_order')
]
