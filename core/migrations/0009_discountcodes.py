# Generated by Django 4.0.3 on 2022-03-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_order_items_order_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=50)),
                ('discount_percentage', models.IntegerField(default=1)),
            ],
        ),
    ]
