# Generated by Django 5.0.4 on 2024-04-16 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_newoders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=15)),
                ('data', models.CharField(max_length=200, null=True)),
                ('date', models.CharField(max_length=15)),
                ('time', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]