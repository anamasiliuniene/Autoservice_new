from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser

# ----------------------------
# Custom User
# ----------------------------
class CustomUser(AbstractUser):
    photo = models.ImageField(
        upload_to="profile_pics",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

# ----------------------------
# Car
# ----------------------------
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    vin_code = models.CharField("VIN", max_length=17, unique=True, default="UNKNOWNVIN00000000")
    client_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    description = HTMLField(verbose_name="Description", max_length=3000, default="")

    def short_name(self):
        return f"{self.make} {self.model}"

    short_name.short_description = "Car"

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

# ----------------------------
# Service
# ----------------------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.unit_price} €)"

# ----------------------------
# Order
# ----------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]

    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    manager = models.ForeignKey(to="autoservice.CustomUser", verbose_name="Manager", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    due_back = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    @property
    def status_color(self):
        return {
            "open": "secondary",
            "in_progress": "warning",
            "done": "success",
        }.get(self.status, "secondary")

    @property
    def is_overdue(self):
        return bool(self.due_back and timezone.now() > self.due_back)

    @property
    def total(self):
        return sum(line.line_sum for line in self.lines.all())

    def __str__(self):
        return f"Order #{self.id} - {self.total} €"

# ----------------------------
# OrderLine
# ----------------------------
class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_sum(self):
        if self.service and self.service.unit_price:
            return self.quantity * self.service.unit_price
        return Decimal("0.00")

    def __str__(self):
        return f"{self.service.name if self.service else 'Service'} - {self.quantity}"

# ----------------------------
# OrderReview
# ----------------------------
class OrderReview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to="autoservice.CustomUser", verbose_name="Reviewer", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=2000)

    class Meta:
        ordering = ["-date_created"]