# Generated by Django 3.1 on 2020-08-10 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200810_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='Customer',
            new_name='customer',
        ),
    ]
