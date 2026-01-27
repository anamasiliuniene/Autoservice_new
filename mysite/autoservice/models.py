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
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="open")

    def __str__(self):
        return f"Order #{self.id} – {self.car}"