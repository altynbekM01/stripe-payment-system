from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),
    path('buy/<int:item_id>/', views.buy_item, name='buy-item'),
]
