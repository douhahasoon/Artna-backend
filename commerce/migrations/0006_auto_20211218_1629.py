# Generated by Django 3.2.8 on 2021-12-18 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_auto_20211217_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='product',
        ),
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='merchant',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Merchant',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
    ]