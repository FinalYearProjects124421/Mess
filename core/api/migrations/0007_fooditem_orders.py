# Generated by Django 5.0.4 on 2024-04-09 22:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_poll'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('food_type', models.CharField(max_length=20)),
                ('cost', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Not Completed'), (1, 'Completed')], default=0)),
                ('tableno', models.IntegerField(max_length=100)),
                ('session_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_list', models.CharField(default=' ', max_length=800)),
            ],
        ),
    ]