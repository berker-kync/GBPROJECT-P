# Generated by Django 4.2.5 on 2023-10-31 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('restaurant_name', models.CharField(max_length=150, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'RestaurantRegistration',
                'verbose_name_plural': 'RestaurantRegistrations',
                'db_table': 'restaurant_registration',
            },
        ),
    ]
