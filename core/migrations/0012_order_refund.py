# Generated by Django 4.0.3 on 2022-03-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_discountcodes_uses'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refund',
            field=models.BooleanField(default=False),
        ),
    ]
