# Generated by Django 3.2.4 on 2021-07-16 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210717_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
