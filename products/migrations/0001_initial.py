# Generated by Django 3.2.4 on 2021-06-26 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.FloatField(default=0.0)),
                ('product_discount_price', models.FloatField(blank=True, null=True)),
                ('product_quantity_type', models.CharField(choices=[('250GM', '250 Grams'), ('500GM', '500 Grams'), ('750GM', '750 Grams'), ('1000GM', '1 Kg')], max_length=6)),
                ('product_type', models.CharField(choices=[('V', 'Vegetable'), ('F', 'Fruit')], max_length=1)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('product_quantity', models.IntegerField()),
            ],
        ),
    ]
