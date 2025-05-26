import stripe
import os
from dotenv import load_dotenv
from store.models import Discount, Tax
from stripe_cart import settings

stripe.api_key = settings.STRIPE_SECRET_KEY_USD

def get_or_create_tax_and_save(name, percentage, inclusive=False):
    tax_rates = stripe.TaxRate.list(limit=100)
    for rate in tax_rates.data:
        if rate.display_name == name and float(rate.percentage) == float(percentage):
            tax_rate_id = rate.id
            break
    else:
        tax_rate = stripe.TaxRate.create(
            display_name=name,
            percentage=percentage,
            inclusive=inclusive,
            country="US",  # укажи нужное
            jurisdiction="US",
            description=f"{percentage}% Tax"
        )
        tax_rate_id = tax_rate.id

    tax, created = Tax.objects.get_or_create(
        stripe_tax_rate_id=tax_rate_id,
        defaults={
            'name': name,
            'percentage': percentage,
        }
    )
    return tax


def get_or_create_coupon_and_save(name, percent_off):
    coupons = stripe.Coupon.list(limit=100)
    for c in coupons.data:
        if c.name == name:
            coupon_id = c.id
            break
    else:
        coupon = stripe.Coupon.create(percent_off=percent_off, duration="once", name=name)
        coupon_id = coupon.id

    discount, created = Discount.objects.get_or_create(
        stripe_coupon_id=coupon_id,
        defaults={
            'name': name,
            'percent_off': percent_off,
        }
    )
    return discount
