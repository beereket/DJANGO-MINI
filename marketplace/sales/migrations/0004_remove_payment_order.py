# Generated by Django 4.2 on 2025-02-23 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
    ]
