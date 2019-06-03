from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Transaction(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    truck_number = models.CharField(max_length=20)
    purchased_date = models.DateField()
    base_price = models.FloatField(default=0.0)
    plus_fees = models.FloatField(default=0.0)
    net_price = models.FloatField(default=0.0)
    pump_price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    gallons_pumped = models.FloatField(default=0.0)
    gross_amount = models.FloatField(default=0.0)
    net_amount = models.FloatField(default=0.0)
    discount_on_fuel = models.FloatField(default=0.0)

    def __str__(self):
        return self.customer.username + ' (' + str(self.purchased_date) + ')'
