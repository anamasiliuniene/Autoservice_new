from django.db import models

# Create your models here.
class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    client_name = models.CharField()

    def __str__(self):
        return f"{self.license_plate} ({self.make})"

class Order(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]

    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )
    def __str__(self):
        return f" {self.car} - ({self.date:%Y-%m-%d}) - {self.status}"