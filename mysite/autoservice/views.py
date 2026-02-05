from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Car, Service, Order
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "num_cars": Car.objects.count(),
        "num_services": Service.objects.count(),
        "num_order_done": Order.objects.filter(status='done').count(),
        "num_order_in_progress": Order.objects.filter(status='in_progress').count(),
        "num_order_open": Order.objects.filter(status='open').count(),
        "num_visits": num_visits,

    }
    return render(request, 'autoservice/index.html', context=context)


def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        "cars": paged_cars,
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
    paginate_by = 3
    ordering = ['-id']  # newest first


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'autoservice/order.html'
    context_object_name = 'order'


def search(request):
    query = request.GET.get('query', '').strip()

    if query:
        cars = Car.objects.filter(
            Q(client_name__icontains=query) |  # savininkas
            Q(make__icontains=query) |  # markė
            Q(model__icontains=query) |  # modelis
            Q(license_plate__icontains=query) |  # valstybinis numeris
            Q(vin_code__icontains=query)  # VIN kodas
        )
    else:
        cars = Car.objects.none()

    return render(request, 'autoservice/search.html', {'cars': cars, 'query': query})