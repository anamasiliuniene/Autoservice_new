from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.urls import reverse_lazy, reverse
from .models import Car, Service, Order, OrderLine
from .forms import InstanceCreateUpdateForm, OrderLineForm, CustomUserCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import InstanceCreateUpdateForm, OrderLineForm
from django.shortcuts import redirect
from django.forms import inlineformset_factory
from django.views.generic import UpdateView
from .models import Order, OrderLine, Service
from django.contrib.auth import get_user_model


# Home / stats
def index(request):
    context = {
        "num_cars": Car.objects.count(),
        "num_services": Service.objects.count(),
        "num_order_done": Order.objects.filter(status='done').count(),
        "num_order_in_progress": Order.objects.filter(status='in_progress').count(),
        "num_order_open": Order.objects.filter(status='open').count(),
    }
    return render(request, 'autoservice/index.html', context)


# Cars
def cars(request):
    return render(request, 'autoservice/cars.html', {"cars": Car.objects.all()})


def car(request, car_pk):
    return render(request, 'autoservice/car.html', {"car": get_object_or_404(Car, pk=car_pk)})


# Public Orders
class OrderListView(ListView):
    model = Order
    template_name = 'autoservice/orders.html'
    context_object_name = 'orders'
    ordering = ['-id']


class PublicOrderDetailView(DetailView):
    model = Order
    template_name = 'autoservice/order_detail_public.html'
    context_object_name = 'order'


class MyOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "autoservice/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(manager=self.request.user)


# Staff order list
class StaffOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "autoservice/order_list.html"
    context_object_name = "orders"
    paginate_by = 6
    ordering = ['-id']

    def test_func(self):
        return self.request.user.is_staff


# Staff order detail
class StaffOrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = "autoservice/order_list.html"
    context_object_name = "orders"
    paginate_by = 6
    ordering = ["-id"]

    def test_func(self):
        return self.request.user.is_staff


# -----------------------------
# CREATE ORDER
# -----------------------------
class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = InstanceCreateUpdateForm
    template_name = "autoservice/order_form.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


# -----------------------------
# UPDATE ORDER
# -----------------------------
# Inline formset for order lines
OrderLineFormSet = inlineformset_factory(
    Order,
    OrderLine,
    form=OrderLineForm,
    extra=1,
    can_delete=True
)


class OrderUpdateView(UpdateView):
    model = Order
    form_class = InstanceCreateUpdateForm
    template_name = "autoservice/order_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["lines"] = OrderLineFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context["lines"] = OrderLineFormSet(
                instance=self.object
            )

        context["all_services"] = Service.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save()

        lines = OrderLineFormSet(
            self.request.POST,
            instance=self.object
        )

        if lines.is_valid():
            lines.save()
            return redirect("order_list")

        return self.render_to_response(
            self.get_context_data(form=form)
        )


# -----------------------------
# DELETE ORDER
# -----------------------------
class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = "autoservice/order_delete.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('order_list')


# -----------------------------
# ADD SERVICE LINES
# -----------------------------
# Services
class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    template_name = "autoservice/order_line_form.html"
    fields = ['service', 'quantity']

    def get_success_url(self):
        return reverse('order_update', kwargs={"pk": self.kwargs['order_pk']})

    def test_func(self):
        order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        return self.request.user.is_staff or order.client == self.request.user

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        context['all_services'] = Service.objects.all()  # ← Add this line
        return context


class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = InstanceCreateUpdateForm
    template_name = "autoservice/order_line_form.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = self.object.orderline_set.all()  # existing lines
        context['all_services'] = Service.objects.all()  # needed for Add Service dropdown
        return context


# class ServiceListView(ListView):
#     model = Service
#     template_name = "autoservice/service_list.html"
#     context_object_name = "services"


# Signup / Profile
class SignUpView(View):
    template_name = "autoservice/signup.html"

    def get(self, request):
        form = CustomUserCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


User = get_user_model()


class ProfileUpdateView(UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']
    template_name = "autoservice/profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


def search(request):
    query = request.GET.get('query', '').strip()
    if query:
        cars = Car.objects.filter(
            Q(client_name__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(vin_code__icontains=query)
        )
    else:
        cars = Car.objects.none()

    return render(request, 'autoservice/search.html', {'cars': cars, 'query': query})
