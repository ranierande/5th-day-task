# Generated by Django 3.1 on 2020-09-28 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_product_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category'),
        ),
    ]