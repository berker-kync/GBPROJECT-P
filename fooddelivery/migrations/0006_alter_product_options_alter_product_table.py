# Generated by Django 4.2.5 on 2023-09-19 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fooddelivery', '0005_alter_product_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
    ]
