# Generated by Django 5.2 on 2025-04-07 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_customer_stripe_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='managers',
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=4)),
                ('role', models.CharField(choices=[('manager', 'Manager'), ('bartender', 'Bartender')], max_length=10)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='app.restaurant')),
            ],
        ),
        migrations.DeleteModel(
            name='Manager',
        ),
    ]
