from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),

    # Cars
    path('cars/', views.cars, name='cars'),
    path('car/<int:car_pk>/', views.car, name='car'),

    # Public orders
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.PublicOrderDetailView.as_view(), name='public_order_detail'),

    # Staff orders
    path('staff/orders/', views.StaffOrderListView.as_view(), name='order_list'),
    path('staff/orders/new/', views.OrderCreateView.as_view(), name='order_create'),
    path('staff/orders/<int:pk>/', views.StaffOrderDetailView.as_view(), name='order_detail'),
    path('staff/orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('staff/orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # Add service to order (minimal workflow)
    path('orders/<int:order_pk>/new_line/', views.OrderLineCreateView.as_view(), name='order_line_create'),

    # Services
    # path('services/', views.ServiceListView.as_view(), name='service_list'),
    # path('staff/services/', views.ServiceListView.as_view(), name='staff_service_list'),

    # My orders
    path('my_orders/', views.MyOrderListView.as_view(), name='my_orders'),

    # Other
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('search/', views.search, name='search'),
]