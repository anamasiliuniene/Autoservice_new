from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import search

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('car/<int:car_pk>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name="order"),
    path('search/', views.search, name='search'),
    path("my_orders/", views.MyOrderListView.as_view(), name="my_orders"),
]
