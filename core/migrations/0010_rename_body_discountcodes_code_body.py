# Generated by Django 4.0.3 on 2022-03-12 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_discountcodes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountcodes',
            old_name='body',
            new_name='code_body',
        ),
    ]
