# Generated by Django 5.1.6 on 2025-03-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_currentitem_orderitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
