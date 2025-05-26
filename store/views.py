import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .forms import PromoCodeForm
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


def create_order(request):
    # Пример: создаём заказ с валютой, переданной через GET ?currency=USD
    currency_code = request.GET.get('currency', 'usd')
    currency = get_object_or_404(Currency, code=currency_code)

    order = Order.objects.create(currency=currency)
    return redirect('order_detail', order_id=order.id)

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


def apply_coupon_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    message = ""

    if request.method == "POST":
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                discount = Discount.objects.get(name=code)
                order.discount = discount
                order.save()
                message = f"Скидка '{discount.name}' успешно применена!"
            except Discount.DoesNotExist:
                message = "Промокод не найден."
    else:
        form = PromoCodeForm()

    return render(request, 'store/apply_coupon.html', {
        'order': order,
        'form': form,
        'message': message,
    })