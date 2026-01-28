from django.contrib import admin
from .models import Car, Order, Service, OrderLine


class CarAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'client_name', 'license_plate', 'vin_code']
    list_filter = ['client_name', 'make', 'model']
    search_fields = ['license_plate', 'vin_code']

    def short_name(self, obj):
        return f"{obj.make} {obj.model}"
    short_name.short_description = "Car"


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ("line_sum",)
    fields = ("service", "quantity", "line_sum")
    autocomplete_fields = ("service",)

    def line_sum(self, obj):
        return obj.quantity * obj.service.unit_price if obj.service else 0
    line_sum.short_description = "Total (€)"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_car', 'date', 'status']
    list_editable = ['status']
    list_filter = ['status', 'date']
    search_fields = ['car__license_plate', 'car__client_name']
    inlines = [OrderLineInline]

    def get_car(self, obj):
        return obj.car.short_name() if obj.car else None
    get_car.short_description = "Car"


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['get_order_car', 'get_order_status', 'service', 'quantity', 'line_sum']
    list_editable = ['quantity']
    readonly_fields = ['line_sum']
    list_filter = ['order__status']

    def get_order_car(self, obj):
        return obj.order.car.short_name() if obj.order and obj.order.car else None
    get_order_car.short_description = "Car"

    def get_order_status(self, obj):
        return obj.order.status if obj.order else None
    get_order_status.short_description = "Order Status"

    def line_sum(self, obj):
        return obj.quantity * obj.service.unit_price if obj.service else 0
    line_sum.short_description = "Total (€)"


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_price", "total_quantity", "total_revenue")
    search_fields = ("name",)  # <-- this is required for autocomplete

    def total_quantity(self, obj):
        return sum(ol.quantity for ol in obj.orderline_set.all())
    total_quantity.short_description = "Total Quantity"

    def total_revenue(self, obj):
        return sum(ol.quantity * ol.service.unit_price for ol in obj.orderline_set.all())
    total_revenue.short_description = "Revenue (€)"


admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Service, ServiceAdmin)