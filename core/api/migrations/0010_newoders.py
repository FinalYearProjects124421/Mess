# Generated by Django 5.0.4 on 2024-04-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_leves'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewOders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
                ('data', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]