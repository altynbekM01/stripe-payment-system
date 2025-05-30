import os
from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'defaultpassword')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0003_order_discount_order_tax'),  # проверь актуальную версию в твоём проекте
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
