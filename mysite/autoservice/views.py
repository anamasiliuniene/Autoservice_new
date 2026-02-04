from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Car, Service, Order
from django.views.generic import ListView, DetailView


# Create your views here.
def index(request):
    context = {
        "num_cars": Car.objects.count(),
        "num_services": Service.objects.count(),
        "num_order_done": Order.objects.filter(status='done').count(),
        "num_order_in_progress": Order.objects.filter(status='in_progress').count(),
        "num_order_open": Order.objects.filter(status='open').count(),
    }
    return render(request, 'autoservice/index.html', context=context)


def cars(request):
    context = {
        "cars": Car.objects.all
    }
    return render(request, 'autoservice/cars.html', context=context)


def car(request, car_pk):
    context = {
        "car": Car.objects.get(pk=car_pk),
    }
    return render(request, 'autoservice/car.html', context={"car": Car.objects.get(pk=car_pk)})


class OrderListView(ListView):
    model = Order
    template_name = 'autoservice/orders.html'
    context_object_name = 'orders'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'autoservice/order.html'
    context_object_name = 'order'
