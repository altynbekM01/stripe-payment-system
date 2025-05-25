from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from django.db import models

from stripe_cart import settings


class CustomUser(AbstractUser):
    def __str__(self):
        return f"{self.id} — {self.username} ({self.email})"

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

class Discount(models.Model):
    name = models.CharField(max_length=255)
    stripe_coupon_id = models.CharField(max_length=255)  # Coupon созданный в Stripe
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount_off = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean(self):
        if self.percent_off and self.amount_off:
            raise ValidationError("Укажите только одно: либо процентную, либо фиксированную скидку.")
        if not self.percent_off and not self.amount_off:
            raise ValidationError("Нужно указать хотя бы один тип скидки — процентную или фиксированную.")

class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_tax_rate_id = models.CharField(max_length=255)  # ID из Stripe
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    items = models.ManyToManyField(Item)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def total_amount(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} ({self.currency})"