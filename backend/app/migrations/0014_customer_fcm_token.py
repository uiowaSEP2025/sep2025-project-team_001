# Generated by Django 5.2 on 2025-04-14 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_orderitem_unwanted_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='fcm_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
