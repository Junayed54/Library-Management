# Generated by Django 5.0.6 on 2024-07-16 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='fine_amount',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='fine_paid',
        ),
    ]
