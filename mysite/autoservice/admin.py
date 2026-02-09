from django.contrib import admin
from .models import Car, Order, Service, OrderLine, OrderReview


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

    def total_display(self, obj):
        return obj.total

    total_display.short_description = "Total (€)"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_car', 'manager', 'date', 'status', 'due_back', 'total_display']
    list_editable = ['status', 'due_back']
    list_filter = ['status', 'due_back', 'manager']
    search_fields = ['car__license_plate', 'manager__username']  # use managers__username if manager is FK to User
    inlines = [OrderLineInline]

    # Corrected fieldsets: remove 'license_plate', use only real fields on Order
    fieldsets = [
        ('General', {'fields': ('car', 'status', 'manager')}),
        ('Due Back', {'fields': ('due_back',)}),
    ]

    def total_display(self, obj):
        return obj.total  # make sure Order has a 'total' property or method

    total_display.short_description = "Total (€)"

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


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'date_created', 'reviewer', 'content']

admin.site.register(OrderReview, OrderReviewAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_price", "total_quantity", "total_revenue")
    search_fields = ("name",)

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
