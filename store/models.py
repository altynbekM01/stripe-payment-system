from django.db import models

from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency.name.upper()}"

