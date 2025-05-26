from django.core.management.base import BaseCommand
from store.stripe_utils import get_or_create_coupon_and_save


class Command(BaseCommand):
    help = 'Создаёт купон в Stripe и сохраняет в базу'

    def handle(self, *args, **options):
        name = "20% OFF coupon"
        percent_off = 20

        discount = get_or_create_coupon_and_save(name, percent_off)

        self.stdout.write(self.style.SUCCESS(
            f'Купон "{discount.name}" с id {discount.stripe_coupon_id} обработан.'
        ))
