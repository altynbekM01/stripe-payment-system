import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Item, Currency


def get_stripe_keys(currency):
    if currency.name.lower() == 'usd':
        return settings.STRIPE_SECRET_KEY_USD, settings.STRIPE_PUBLIC_KEY_USD
    elif currency.name.lower() == 'eur':
        return settings.STRIPE_SECRET_KEY_EUR, settings.STRIPE_PUBLIC_KEY_EUR
    else:
        return settings.STRIPE_SECRET_KEY_USD, settings.STRIPE_PUBLIC_KEY_USD

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    currencies = Currency.objects.all()
    _, stripe_public_key = get_stripe_keys(item.currency)
    return render(request, 'store/item.html', {
        'item': item,
        'currencies': currencies,
        'stripe_public_key': stripe_public_key,
    })

def buy_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    stripe_secret_key, _ = get_stripe_keys(item.currency)
    stripe.api_key = stripe_secret_key

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency.code,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{settings.DOMAIN}/success',
        cancel_url=f'{settings.DOMAIN}/cancel',
    )
    return JsonResponse({'id': session.id})

def success_view(request):
    return render(request, 'store/success.html')

def cancel_view(request):
    return render(request, 'store/cancel.html')

