from django.db import models
from django.db.models.expressions import result


# Create your models here.
class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField("VIN", max_length=17, unique=True, default="UNKNOWNVIN00000000")
    client_name = models.CharField()

    def short_name(self):
        return f"{self.make} {self.model}"
    short_name.short_description = "Car"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name_plural = "Cars"
        verbose_name = "Car"

class Order(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]

    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to = "Car", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )
    def total_cost(self):
        result = 0
        for line in self.order_lines.all():
            result += line.service.unit_price * line.quantity
        return result

    def __str__(self):
        return f" {self.car} - ({self.date:%Y-%m-%d}) - {self.status} - {self.total_cost()}"

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

class Service(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.unit_price} €)"

    class Meta:
        verbose_name_plural = "Services"
        verbose_name = "Service"

class OrderLine(models.Model):
    order = models.ForeignKey(to = "Order", on_delete=models.CASCADE, related_name="order_lines")
    service = models.ForeignKey(to = "Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.service.name} - {self.quantity} ({self.service.unit_price} €)"

    class Meta:
        verbose_name_plural = "Order Lines"
        verbose_name = "Order Line"

    @property
    def line_sum(self):
        if self.service:
            return self.quantity * self.service.unit_price
        return 0