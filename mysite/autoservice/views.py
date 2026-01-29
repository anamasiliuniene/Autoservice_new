from django.shortcuts import render
from .models import Car, Order, Service, OrderLine


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
