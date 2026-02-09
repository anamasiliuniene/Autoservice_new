from django.shortcuts import render, reverse
from django.views import generic
from .models import Car, Service, Order
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import OrderReviewForm
from django.views.generic.edit import FormMixin


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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'autoservice/order.html'
    context_object_name = 'order'
    form_class = OrderReviewForm

# nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

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


class MyOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(manager=self.request.user)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'autoservice/signup.html'
    success_url = reverse_lazy('login')
