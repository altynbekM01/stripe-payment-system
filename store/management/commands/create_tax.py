from django.core.management.base import BaseCommand
from store.stripe_utils import get_or_create_tax_and_save

class Command(BaseCommand):
    help = 'Создаёт налог в Stripe и сохраняет в базу'

    def handle(self, *args, **options):
        name = "Standard Tax"
        percentage = 10.0

        tax = get_or_create_tax_and_save(name, percentage)

        self.stdout.write(self.style.SUCCESS(
            f'Налог "{tax.name}" с id {tax.stripe_tax_rate_id} обработан.'
        ))
