# Generated by Django 3.1 on 2020-10-01 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_newcustomer_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='name',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='user',
        ),
        migrations.AddField(
            model_name='seller',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='password',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]