# Generated by Django 4.2.6 on 2023-12-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fooddelivery', '0006_alter_portion_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='extras',
            field=models.ManyToManyField(blank=True, related_name='carts', to='fooddelivery.extras'),
        ),
        migrations.AddField(
            model_name='cart',
            name='portions',
            field=models.ManyToManyField(blank=True, related_name='carts', to='fooddelivery.portion'),
        ),
    ]
