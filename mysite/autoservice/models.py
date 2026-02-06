from django.db import models
from django.db.models.expressions import result
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField("VIN", max_length=17, unique=True, default="UNKNOWNVIN00000000")
    client_name = models.CharField()
    image = models.ImageField(upload_to="images", null=True, blank=True)

    def short_name(self):
        return f"{self.make} {self.model}"

    short_name.short_description = "Car"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name_plural = "Cars"
        verbose_name = "Car"


class Order(models.Model):
    car = models.ForeignKey("Car",
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name="orders")
    date = models.DateTimeField(auto_now_add=True)
    due_back = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(to=User, verbose_name="Owner",
                              on_delete=models.SET_NULL,
                              null=True, blank=True)

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]

    @property
    def status_color(self):
        return {
            "open": "secondary",
            "in_progress": "warning",
            "done": "success",
        }.get(self.status, "secondary")

    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car",
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name="orders")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    @property
    def total(self):
        return sum(line.line_sum for line in self.lines.all())

    def __str__(self):
        return f"Order #{self.id} - {self.total} €"

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
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_sum(self):
        if self.service is not None and self.service.unit_price is not None:
            return self.quantity * self.service.unit_price
        return Decimal("0.00")

    def __str__(self):
        return f"{self.service.name} - {self.quantity} ({self.service.unit_price} €)"

    class Meta:
        verbose_name_plural = "Order Lines"
        verbose_name = "Order Line"
