from django.db import models

# Create your models here.
class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    client_name = models.CharField()

    def __str__(self):
        return f"{self.license_plate} ({self.make})"