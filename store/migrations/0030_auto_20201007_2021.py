# Generated by Django 3.1 on 2020-10-07 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20201006_2241'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order1',
            new_name='PreviousOrder',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
    ]
