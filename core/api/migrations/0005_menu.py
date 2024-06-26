# Generated by Django 5.0.4 on 2024-04-09 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_user_exp_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name_morning', models.CharField(max_length=15)),
                ('food_img_uri_morning', models.CharField(max_length=200, null=True)),
                ('food_name_evening', models.CharField(max_length=15)),
                ('food_img_uri_evening', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
