# Generated by Django 5.2.1 on 2025-05-26 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stripe_coupon_id', models.CharField(max_length=255)),
                ('percent_off', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('amount_off', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stripe_tax_rate_id', models.CharField(max_length=255)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
