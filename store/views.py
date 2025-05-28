import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Currency, Order, Discount


def index(request):
    items = Item.objects.all()
    return render(request, 'store/index.html', {'items': items})


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


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    orders = request.user.orders.all()
    if orders.exists():
        currency = orders.first().currency
        _, public_key = get_stripe_keys(currency)
    else:
        public_key = ''

    return render(request, 'store/my_orders.html', {
        'orders': orders,
        'public_key': public_key,
    })

@login_required
def add_to_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    currency = item.currency

    order, created = Order.objects.get_or_create(
        user=request.user,
        paid=False,
        currency=currency,
    )

    order.items.add(item)
    return redirect('/')

@login_required
def buy_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.items.exists():
        return JsonResponse({'error': 'Заказ пуст'}, status=400)

    currency = order.currency
    stripe_secret_key, _ = get_stripe_keys(currency)
    stripe.api_key = stripe_secret_key

    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency.code,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': ['txr_1RT5PHPKlgc9fEydJsQsZN4x'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        discounts=[{'coupon': order.discount.stripe_coupon_id}] if order.discount else [],
        mode='payment',
        success_url=f'{settings.DOMAIN}/success',
        cancel_url=f'{settings.DOMAIN}/cancel',
        metadata={'order_id': order.id}
    )

    return JsonResponse({'id': session.id})


@csrf_exempt
def apply_coupon_view(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code')
            order = Order.objects.get(id=order_id)

            discount = Discount.objects.get(name=code)
            order.discount = discount
            order.save()
            total = order.total_amount()
            if discount.percent_off:
                new_total = total * (1 - discount.percent_off / 100)
            elif discount.amount_off:
                new_total = max(total - discount.amount_off, 0)
            else:
                new_total = total

            return JsonResponse({'success': True, 'new_total': float(round(new_total, 2))})
        except Discount.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Неверный промокод'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})